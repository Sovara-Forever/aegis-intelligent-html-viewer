// Page Review kit. Static, no server. Loads ./meta.json, ./page.html, ./notes.md and ../../cms-rules/<cms>.json.
(async function(){
  const $=id=>document.getElementById(id), base='../../';
  const meta=await (await fetch('meta.json',{cache:'no-store'})).json();
  const buf=await (await fetch('page.html',{cache:'no-store'})).arrayBuffer();
  const raw=new TextDecoder().decode(buf);
  const hex=[...new Uint8Array(await crypto.subtle.digest('SHA-256',buf))].map(b=>b.toString(16).padStart(2,'0')).join('');
  const match=hex===meta.sha256.toLowerCase();
  $('title').textContent=meta.title; $('store').textContent=meta.store_label+' · '+meta.cms+' · post '+meta.post_id;
  const s=$('sha'); s.textContent=(match?'SHA-256 match ':'SHA-256 MISMATCH ')+hex.slice(0,8)+'…'+hex.slice(-6); s.className='pill '+(match?'ok':'bad'); s.title=hex;
  const cms=await (await fetch(base+'cms-rules/'+meta.cms_rules+'.json',{cache:'no-store'})).json();
  const rules=Object.assign({},cms.render_rules||{},((cms.stores||{})[meta.store]||{}).render_rules||{});
  function stripCss(h,list){ if(!list||!list.length) return h;
    return h.replace(/style\s*=\s*"([^"]*)"/gi,(m,css)=>{const k=css.split(';').filter(d=>{const p=d.split(':')[0].trim().toLowerCase();return p&&!list.includes(p)});return 'style="'+k.join(';')+(k.length?';':'')+'"';});}
  function autop(h){ const blk='(?:table|thead|tbody|tr|td|th|div|ul|ol|li|h[1-6]|p|section|figure|blockquote|pre|script|style|hr|details|summary)';
    const re=new RegExp('^\\s*</?'+blk+'\\b','i');
    return h.split(/\n\s*\n/).map(c=>{const t=c.trim(); if(!t) return ''; if(re.test(t)) return t.replace(/>\s*\n\s*(?=[^<\s])/g,'>\n'); return '<p>'+t.replace(/\n/g,'<br />\n')+'</p>';}).join('\n');}
  function texturize(h,list){ (list||[]).forEach(r=>{ const re=new RegExp(r.pattern,'g'); h=h.replace(/>([^<]+)</g,(m,t)=>'>'+t.replace(re,r.replace)+'<'); }); return h;}
  function cmsSave(h){ if(rules.strip_json_ld) h=h.replace(/<script[^>]*application\/ld\+json[^>]*>[\s\S]*?<\/script>/gi,'');
    h=stripCss(h,rules.strip_css); if(rules.wpautop) h=autop(h); return texturize(h,rules.wptexturize);}
  const saved=cmsSave(raw);
  const flags=(rules.flag_tags||[]).filter(t=>new RegExp('<'+t+'\\b','i').test(raw));
  $('rules').textContent='Rules: '+cms.label+(meta.store?' / '+meta.store:'')+(rules.strip_css&&rules.strip_css.length?' · strips '+rules.strip_css.join(', '):'')+(rules.strip_json_ld?' · strips JSON-LD':'')+(flags.length?' · FLAG: '+flags.join(','):'');
  const wrap=b=>'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><base target="_blank"><style>body{margin:0;padding:12px;font-family:Arial,sans-serif;color:#111}img{max-width:100%;height:auto}</style></head><body>'+b+'</body></html>';
  let mode='saved'; const render=()=>{const d=wrap(mode==='saved'?saved:raw); $('desk').srcdoc=d; $('phone').srcdoc=d; $('mode').textContent='Showing: '+(mode==='saved'?'CMS-saved (approx.)':'Raw paste')+' · switch';};
  $('mode').onclick=()=>{mode=mode==='saved'?'raw':'saved';render();};
  const fit=()=>{const w=$('desk-wrap').clientWidth; document.documentElement.style.setProperty('--s',Math.min(1,w/1280));}; addEventListener('resize',fit); fit(); render();
  const md=await (await fetch('notes.md',{cache:'no-store'})).text(); $('notes').innerHTML=mdToHtml(md);
  const body='Review: '+meta.slug+'\nSHA-256: '+meta.sha256+'\nURL: '+location.href+'\n\n## Works\n- \n\n## Needs / changes\n- \n\n## Decision\n- [ ] Approved as is\n- [ ] Needs changes\n';
  $('notes-link').href='https://github.com/'+meta.repo+'/issues/new?labels=page-review&title='+encodeURIComponent('Review: '+meta.slug)+'&body='+encodeURIComponent(body);
  document.body.dataset.sha=match?'match':'mismatch'; document.body.dataset.ready='1';
  function esc(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
  function inl(t){return esc(t).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');}
  function mdToHtml(src){const out=[];let list=false,tbl=false,code=false;
    for(const line of src.split('\n')){
      if(/^```/.test(line)){code=!code;out.push(code?'<pre>':'</pre>');continue;} if(code){out.push(esc(line));continue;}
      if(/^\s*\|/.test(line)){ if(/^\s*\|[\s:|-]+\|\s*$/.test(line)) continue; if(!tbl){out.push('<table>');tbl=true;} out.push('<tr>'+line.trim().replace(/^\||\|$/g,'').split('|').map(c=>'<td>'+inl(c.trim())+'</td>').join('')+'</tr>'); continue;} else if(tbl){out.push('</table>');tbl=false;}
      const li=line.match(/^\s*[-*]\s+(.*)/); if(li){ if(!list){out.push('<ul>');list=true;} out.push('<li>'+inl(li[1])+'</li>'); continue;} else if(list){out.push('</ul>');list=false;}
      const h=line.match(/^(#{1,4})\s+(.*)/); if(h){out.push('<h'+(h[1].length+1)+'>'+inl(h[2])+'</h'+(h[1].length+1)+'>');continue;}
      if(/^---+\s*$/.test(line)){out.push('<hr>');continue;} if(line.trim()) out.push('<p>'+inl(line)+'</p>');}
    if(list)out.push('</ul>'); if(tbl)out.push('</table>'); return out.join('\n');}
})().catch(e=>{document.getElementById('rules').textContent='Review kit error: '+e;});
