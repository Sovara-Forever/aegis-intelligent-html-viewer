#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  ShadowForge Bridge — JSON → Canonical CSV Converter             ║
║  Converts any JSON inventory format to ShadowForge v2 schema     ║
║  Compatible with shadowforge_v2.py CANONICAL_FIELDS (26 fields)  ║
║                                                                  ║
║  Usage:                                                          ║
║    python shadowforge_bridge.py --input inventory.json           ║
║                                 --output csv_inputs/out.csv      ║
║                                 --dealer "RC Auto Group"         ║
║                                 --format auto                    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import csv
import argparse
import re
import os
import sys
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"

# ─── Canonical 26-field schema (matches shadowforge_v2.py) ───────────────────
CANONICAL_FIELDS = [
    'Year', 'Make', 'Model', 'Trim', 'VIN', 'Stock', 'Status',
    'MSRP', 'Sale_Price', 'Discount', 'Monthly_Payment',
    'Image_URL', 'Detail_URL', 'Dealer', 'Dealer_Phone',
    'Exterior_Color', 'Interior_Color', 'Engine', 'Transmission',
    'Drivetrain', 'Mileage', 'Body_Style', 'Features',
    'Market_Comp', 'Lead_Score', 'Urgency_Flag', 'SEO_Notes',
    'Enrichment_TS', 'Source_Format', 'Source_File'
]

# ─── Price cleaner (mirrors shadowforge_v2.py) ────────────────────────────────
def clean_price(val):
    if val is None or val == '': return 0.0
    s = str(val).strip().replace('$', '').replace(',', '').replace(' ', '')
    s = s.replace('−', '-').replace('–', '-').replace('—', '-')
    match = re.search(r'-?[\d]+\.?\d*', s)
    if match: return abs(float(match.group()))
    return 0.0

def safe_str(val):
    if val is None: return ''
    return str(val).strip()

# ─── Year/Make/Model/Trim extractor ──────────────────────────────────────────
def extract_ymmt(name_str):
    s = safe_str(name_str)
    if not s: return '', '', '', ''
    s = re.sub(r'^(New|Pre-Owned|Used|Certified|CPO)\s+', '', s, flags=re.IGNORECASE).strip()
    year_match = re.match(r'(\d{4})\s+(.+)', s)
    if not year_match: return '', '', '', s
    year = year_match.group(1)
    rest = year_match.group(2).strip()

    MAKES = [
        'Alfa Romeo', 'Aston Martin', 'Land Rover', 'Mercedes-Benz',
        'Rolls-Royce', 'Acura', 'Audi', 'BMW', 'Buick', 'Cadillac',
        'Chevrolet', 'Chrysler', 'Dodge', 'Ferrari', 'Ford', 'Genesis',
        'GMC', 'Honda', 'Hyundai', 'Infiniti', 'Jaguar', 'Jeep', 'Kia',
        'Lexus', 'Lincoln', 'Mazda', 'Mini', 'Mitsubishi', 'Nissan',
        'Porsche', 'Ram', 'RAM', 'Rivian', 'Subaru', 'Tesla', 'Toyota',
        'Volkswagen', 'Volvo', 'Wagoneer'
    ]
    make = ''
    model_trim = rest
    for m in sorted(MAKES, key=len, reverse=True):
        if rest.lower().startswith(m.lower()):
            make = m
            model_trim = rest[len(m):].strip()
            break

    if not make:
        parts = rest.split(None, 1)
        make = parts[0]
        model_trim = parts[1] if len(parts) > 1 else ''

    mt_parts = model_trim.split()
    if not mt_parts: return year, make, '', ''
    if len(mt_parts) == 1: return year, make, mt_parts[0], ''
    if len(mt_parts) == 2: return year, make, mt_parts[0], mt_parts[1]
    model = mt_parts[0]
    trim = ' '.join(mt_parts[1:])
    return year, make, model, trim

def detect_status(name='', url='', mileage=0):
    s = (safe_str(name) + ' ' + safe_str(url)).lower()
    if 'certified' in s or 'cpo' in s: return 'CPO'
    if 'pre-owned' in s or 'used' in s or '/used/' in s: return 'Used'
    if 'new' in s or '/new/' in s: return 'New'
    if mileage and float(mileage) > 500: return 'Used'
    return 'New'

def detect_body(name='', trim=''):
    s = (safe_str(name) + ' ' + safe_str(trim)).lower()
    if any(x in s for x in ['suv', 'sport utility', 'crossover']): return 'SUV'
    if any(x in s for x in ['sedan', 'saloon']): return 'Sedan'
    if any(x in s for x in ['truck', 'pickup', 'crew cab']): return 'Truck'
    if 'coupe' in s: return 'Coupe'
    if 'convertible' in s: return 'Convertible'
    if any(x in s for x in ['van', 'minivan']): return 'Van'
    return ''

# ─── Format Detectors ─────────────────────────────────────────────────────────
def detect_json_format(data):
    """
    IF/ELSE detection tree for JSON formats
    Returns format string matching ShadowForge conventions
    """
    if isinstance(data, list) and len(data) > 0:
        sample = data[0]
        keys = set(str(k).lower() for k in sample.keys())

        # Typesense response
        if 'hits' in keys:
            return 'TYPESENSE_RESPONSE'

        # Algolia response
        if 'nbhits' in keys or 'nb_hits' in keys:
            return 'ALGOLIA_RESPONSE'

        # ShadowForge canonical (already processed)
        if 'lead_score' in keys and 'urgency_flag' in keys:
            return 'SHADOWFORGE_CANONICAL'

        # PixelMotion pmVlpData style
        if 'detailurl' in keys or 'stocknum' in keys:
            return 'PIXELMOTION_JSON'

        # Standard vehicle record with year/make/model
        if all(k in keys for k in ['year', 'make', 'model']):
            return 'STANDARD_VEHICLE'

        # ATC / third-party feed with name field
        if 'vehiclename' in keys or 'vehicle_name' in keys or 'title' in keys:
            return 'GENERIC_NAMED'

        # VDP structured data / JSON-LD
        if '@type' in keys or '@context' in keys:
            return 'JSONLD_SCHEMA'

    elif isinstance(data, dict):
        keys = set(str(k).lower() for k in data.keys())

        # Typesense query result
        if 'hits' in keys and 'found' in keys:
            return 'TYPESENSE_RESPONSE'

        # PixelMotion pmVlpData top-level
        if 'vehicles' in keys and 'pagination' in keys:
            return 'PIXELMOTION_VLP'

        # WordPress REST API inventory
        if 'id' in keys and 'slug' in keys and 'acf' in keys:
            return 'WORDPRESS_ACF'

        # Generic inventory wrapper
        if 'inventory' in keys or 'vehicles' in keys or 'results' in keys:
            inner = data.get('inventory') or data.get('vehicles') or data.get('results') or []
            if inner and isinstance(inner, list) and len(inner) > 0:
                return detect_json_format(inner)

    return 'UNKNOWN_JSON'


# ─── Format Parsers ───────────────────────────────────────────────────────────

def parse_typesense_response(data, dealer, source_file):
    """Parse Typesense API response format"""
    vehicles = []
    hits = data if isinstance(data, list) else data.get('hits', [])

    for hit in hits:
        doc = hit.get('document', hit)  # Typesense wraps in 'document'

        name = safe_str(doc.get('name', doc.get('vehicleName', doc.get('title', ''))))
        year_raw = safe_str(doc.get('year', ''))
        make_raw = safe_str(doc.get('make', ''))
        model_raw = safe_str(doc.get('model', ''))
        trim_raw = safe_str(doc.get('trim', ''))

        if year_raw and make_raw and model_raw:
            year, make, model, trim = year_raw, make_raw, model_raw, trim_raw
        else:
            year, make, model, trim = extract_ymmt(name)

        msrp = clean_price(doc.get('msrp', doc.get('MSRP', doc.get('price', 0))))
        sale = clean_price(doc.get('salePrice', doc.get('sale_price', doc.get('internetPrice', msrp))))
        discount = round(msrp - sale, 2) if msrp > sale > 0 else 0

        vehicles.append(build_record(
            year=year, make=make, model=model, trim=trim,
            vin=safe_str(doc.get('vin', doc.get('VIN', ''))),
            stock=safe_str(doc.get('stock', doc.get('stockNumber', ''))),
            status=detect_status(name, safe_str(doc.get('url', ''))),
            msrp=msrp, sale=sale, discount=discount,
            img=safe_str(doc.get('imageUrl', doc.get('image', ''))),
            url=safe_str(doc.get('url', doc.get('detailUrl', ''))),
            dealer=dealer, phone=safe_str(doc.get('phone', '')),
            ext_color=safe_str(doc.get('exteriorColor', '')),
            int_color=safe_str(doc.get('interiorColor', '')),
            engine=safe_str(doc.get('engine', '')),
            transmission=safe_str(doc.get('transmission', '')),
            drivetrain=safe_str(doc.get('drivetrain', '')),
            mileage=safe_str(doc.get('mileage', '0')),
            body=detect_body(name, trim_raw),
            features=safe_str(doc.get('features', '')),
            source_format='TYPESENSE_RESPONSE',
            source_file=source_file
        ))
    return vehicles


def parse_pixelmotion_vlp(data, dealer, source_file):
    """Parse PixelMotion pmVlpData top-level object"""
    vehicles_raw = data.get('vehicles', [])
    vehicles = []

    for v in vehicles_raw:
        name = safe_str(v.get('condition', v.get('name', '')))
        year, make, model, trim = extract_ymmt(name)

        msrp = clean_price(v.get('msrp', v.get('MSRP', 0)))
        sale = clean_price(v.get('salePrice', v.get('sale_price', v.get('internetPrice', msrp))))
        discount = clean_price(v.get('discount', 0)) or round(msrp - sale, 2) if msrp > sale > 0 else 0

        vehicles.append(build_record(
            year=year, make=make, model=model, trim=trim,
            vin=safe_str(v.get('vin', v.get('VIN', ''))),
            stock=safe_str(v.get('stockNum', v.get('stock', ''))),
            status=detect_status(name, safe_str(v.get('detailUrl', v.get('url', '')))),
            msrp=msrp, sale=sale, discount=discount,
            img=safe_str(v.get('imageUrl', v.get('image', ''))),
            url=safe_str(v.get('detailUrl', v.get('url', ''))),
            dealer=dealer, phone='',
            ext_color=safe_str(v.get('exteriorColor', '')),
            int_color=safe_str(v.get('interiorColor', '')),
            engine=safe_str(v.get('engine', '')),
            transmission=safe_str(v.get('transmission', '')),
            drivetrain=safe_str(v.get('drivetrain', '')),
            mileage=safe_str(v.get('mileage', '0')),
            body=detect_body(name, trim),
            features=safe_str(v.get('comments', v.get('features', ''))),
            source_format='PIXELMOTION_JSON',
            source_file=source_file
        ))
    return vehicles


def parse_standard_vehicle(data, dealer, source_file):
    """Parse standard year/make/model/trim flat JSON array"""
    vehicles = []
    records = data if isinstance(data, list) else []

    for v in records:
        year = safe_str(v.get('year', v.get('Year', '')))
        make = safe_str(v.get('make', v.get('Make', '')))
        model = safe_str(v.get('model', v.get('Model', '')))
        trim = safe_str(v.get('trim', v.get('Trim', '')))

        msrp = clean_price(v.get('msrp', v.get('MSRP', v.get('price', 0))))
        sale = clean_price(v.get('salePrice', v.get('sale_price', v.get('Sale_Price', v.get('internetPrice', msrp)))))
        discount = clean_price(v.get('discount', v.get('Discount', 0))) or (round(msrp - sale, 2) if msrp > sale > 0 else 0)
        url = safe_str(v.get('url', v.get('detailUrl', v.get('Detail_URL', v.get('vehicleUrl', '')))))

        vehicles.append(build_record(
            year=year, make=make, model=model, trim=trim,
            vin=safe_str(v.get('vin', v.get('VIN', ''))),
            stock=safe_str(v.get('stock', v.get('Stock', v.get('stockNumber', '')))),
            status=detect_status(f"{year} {make} {model}", url, clean_price(v.get('mileage', 0))),
            msrp=msrp, sale=sale if sale > 0 else msrp, discount=discount,
            img=safe_str(v.get('imageUrl', v.get('Image_URL', v.get('image', '')))),
            url=url,
            dealer=safe_str(v.get('dealer', v.get('Dealer', dealer))),
            phone=safe_str(v.get('phone', v.get('Dealer_Phone', ''))),
            ext_color=safe_str(v.get('exteriorColor', v.get('Exterior_Color', ''))),
            int_color=safe_str(v.get('interiorColor', v.get('Interior_Color', ''))),
            engine=safe_str(v.get('engine', v.get('Engine', ''))),
            transmission=safe_str(v.get('transmission', v.get('Transmission', ''))),
            drivetrain=safe_str(v.get('drivetrain', v.get('Drivetrain', ''))),
            mileage=safe_str(v.get('mileage', v.get('Mileage', '0'))),
            body=detect_body(f"{make} {model}", trim),
            features=safe_str(v.get('features', v.get('Features', ''))),
            source_format='STANDARD_VEHICLE',
            source_file=source_file
        ))
    return vehicles


def parse_jsonld_schema(data, dealer, source_file):
    """Parse JSON-LD @type Vehicle schema records"""
    vehicles = []
    records = data if isinstance(data, list) else [data]

    for v in records:
        graph = v.get('@graph', [v])
        for item in graph:
            if item.get('@type') not in ['Vehicle', 'Car', 'Product']:
                continue

            name = safe_str(item.get('name', ''))
            year, make, model, trim = extract_ymmt(name)

            offer = item.get('offers', {})
            if isinstance(offer, list): offer = offer[0] if offer else {}

            msrp = clean_price(item.get('msrpValue', offer.get('price', 0)))
            sale = clean_price(offer.get('price', msrp))
            discount = round(msrp - sale, 2) if msrp > sale > 0 else 0

            vehicles.append(build_record(
                year=safe_str(item.get('modelDate', year)),
                make=safe_str(item.get('brand', {}).get('name', make)),
                model=safe_str(item.get('model', model)),
                trim=safe_str(item.get('vehicleModelDate', trim)),
                vin=safe_str(item.get('vehicleIdentificationNumber', '')),
                stock='',
                status=detect_status(name, safe_str(offer.get('url', ''))),
                msrp=msrp, sale=sale if sale > 0 else msrp, discount=discount,
                img=safe_str(item.get('image', '')),
                url=safe_str(offer.get('url', item.get('url', ''))),
                dealer=dealer, phone='',
                ext_color=safe_str(item.get('color', '')),
                int_color='',
                engine=safe_str(item.get('vehicleEngine', {}).get('engineType', '') if isinstance(item.get('vehicleEngine'), dict) else ''),
                transmission=safe_str(item.get('vehicleTransmission', '')),
                drivetrain=safe_str(item.get('driveWheelConfiguration', '')),
                mileage=safe_str(item.get('mileageFromOdometer', {}).get('value', '0') if isinstance(item.get('mileageFromOdometer'), dict) else '0'),
                body=safe_str(item.get('bodyType', detect_body(name, trim))),
                features='',
                source_format='JSONLD_SCHEMA',
                source_file=source_file
            ))
    return vehicles


def parse_generic_named(data, dealer, source_file):
    """Parse generic JSON with name/title fields"""
    vehicles = []
    records = data if isinstance(data, list) else []

    for v in records:
        name = safe_str(v.get('vehicleName', v.get('vehicle_name', v.get('title', v.get('name', '')))))
        year, make, model, trim = extract_ymmt(name)

        price_fields = ['price', 'salePrice', 'sale_price', 'internetPrice', 'internet_price', 'finalPrice']
        msrp_fields = ['msrp', 'MSRP', 'listPrice', 'list_price']

        msrp = 0
        for f in msrp_fields:
            val = clean_price(v.get(f, 0))
            if val > 0: msrp = val; break

        sale = 0
        for f in price_fields:
            val = clean_price(v.get(f, 0))
            if val > 0: sale = val; break

        if sale == 0: sale = msrp
        discount = round(msrp - sale, 2) if msrp > sale > 0 else 0

        url = safe_str(v.get('url', v.get('link', v.get('detailUrl', v.get('vehicleUrl', '')))))

        vehicles.append(build_record(
            year=year, make=make, model=model, trim=trim,
            vin=safe_str(v.get('vin', v.get('VIN', ''))),
            stock=safe_str(v.get('stock', v.get('stockNum', v.get('stockNumber', '')))),
            status=detect_status(name, url),
            msrp=msrp, sale=sale, discount=discount,
            img=safe_str(v.get('imageUrl', v.get('image', v.get('photo', '')))),
            url=url, dealer=dealer, phone='',
            ext_color=safe_str(v.get('exteriorColor', v.get('extColor', ''))),
            int_color=safe_str(v.get('interiorColor', v.get('intColor', ''))),
            engine=safe_str(v.get('engine', '')),
            transmission=safe_str(v.get('transmission', '')),
            drivetrain=safe_str(v.get('drivetrain', v.get('driveType', ''))),
            mileage=safe_str(v.get('mileage', '0')),
            body=detect_body(name, trim),
            features=safe_str(v.get('features', v.get('description', ''))),
            source_format='GENERIC_NAMED',
            source_file=source_file
        ))
    return vehicles


# ─── Record Builder ───────────────────────────────────────────────────────────
def build_record(**kwargs):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msrp = kwargs.get('msrp', 0)
    sale = kwargs.get('sale', 0)
    discount = kwargs.get('discount', 0)

    # Lead Score
    score = 50
    if msrp > 0 and discount > 0:
        pct = (discount / msrp) * 100
        if pct >= 20: score += 25
        elif pct >= 10: score += 15
        elif pct >= 5: score += 10

    # Urgency Flag
    if msrp > 0 and discount > 0:
        pct = (discount / msrp) * 100
        if pct >= 20: urgency = '🔥 DEEP DISCOUNT'
        elif pct >= 15: urgency = '🔥 HOT DEAL'
        elif pct >= 10: urgency = '⚡ STRONG DEAL'
        elif pct >= 5: urgency = '✅ GOOD DEAL'
        else: urgency = '⏰ MARKET PRICE'
    else:
        urgency = '⏰ STANDARD'

    year = kwargs.get('year', '')
    make = kwargs.get('make', '')
    model = kwargs.get('model', '')
    dealer = kwargs.get('dealer', '')

    seo_parts = []
    if year and make and model: seo_parts.append(f"{year} {make} {model}")
    if dealer: seo_parts.append(f"at {dealer}")
    if sale > 0: seo_parts.append(f"${sale:,.0f}")
    if discount > 0: seo_parts.append(f"Save ${discount:,.0f}")

    return {
        'Year': year,
        'Make': make,
        'Model': model,
        'Trim': kwargs.get('trim', ''),
        'VIN': kwargs.get('vin', ''),
        'Stock': kwargs.get('stock', ''),
        'Status': kwargs.get('status', 'New'),
        'MSRP': msrp,
        'Sale_Price': sale,
        'Discount': discount,
        'Monthly_Payment': kwargs.get('monthly', 0),
        'Image_URL': kwargs.get('img', ''),
        'Detail_URL': kwargs.get('url', ''),
        'Dealer': dealer,
        'Dealer_Phone': kwargs.get('phone', ''),
        'Exterior_Color': kwargs.get('ext_color', ''),
        'Interior_Color': kwargs.get('int_color', ''),
        'Engine': kwargs.get('engine', ''),
        'Transmission': kwargs.get('transmission', ''),
        'Drivetrain': kwargs.get('drivetrain', ''),
        'Mileage': kwargs.get('mileage', ''),
        'Body_Style': kwargs.get('body', ''),
        'Features': kwargs.get('features', ''),
        'Market_Comp': '',
        'Lead_Score': score,
        'Urgency_Flag': urgency,
        'SEO_Notes': ' | '.join(seo_parts),
        'Enrichment_TS': now,
        'Source_Format': kwargs.get('source_format', 'BRIDGE_CONVERTED'),
        'Source_File': kwargs.get('source_file', '')
    }


# ─── Main Router ─────────────────────────────────────────────────────────────
FORMAT_PARSERS = {
    'TYPESENSE_RESPONSE': parse_typesense_response,
    'ALGOLIA_RESPONSE': parse_typesense_response,  # same structure
    'PIXELMOTION_VLP': parse_pixelmotion_vlp,
    'PIXELMOTION_JSON': parse_standard_vehicle,
    'STANDARD_VEHICLE': parse_standard_vehicle,
    'GENERIC_NAMED': parse_generic_named,
    'JSONLD_SCHEMA': parse_jsonld_schema,
    'WORDPRESS_ACF': parse_standard_vehicle,
}


def convert_json_to_csv(input_path, output_path, dealer_name, force_format=None):
    print(f"\n{'═'*60}")
    print(f"  ShadowForge Bridge v{VERSION}")
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Dealer: {dealer_name}")
    print(f"{'═'*60}")

    # Load JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Unwrap common wrappers
    if isinstance(data, dict):
        for key in ['inventory', 'vehicles', 'results', 'hits', 'data', 'items']:
            if key in data:
                inner = data[key]
                if isinstance(inner, list) and len(inner) > 0:
                    print(f"  Unwrapped JSON key: '{key}'")
                    data = inner
                    break

    fmt = force_format or detect_json_format(data)
    print(f"  Detected format: {fmt}")

    if fmt == 'SHADOWFORGE_CANONICAL':
        print("  ⏭️  Already in ShadowForge canonical format — no conversion needed")
        return

    parser = FORMAT_PARSERS.get(fmt, parse_generic_named)
    source_file = os.path.basename(input_path)

    vehicles = parser(data if not isinstance(data, dict) else data, dealer_name, source_file)
    print(f"  ✅ Parsed {len(vehicles)} vehicles")

    if not vehicles:
        print("  ❌ No vehicles extracted — check input format")
        return

    # Write CSV
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_FIELDS, extrasaction='ignore')
        writer.writeheader()
        for v in vehicles:
            # Ensure all canonical fields present
            for field in CANONICAL_FIELDS:
                if field not in v:
                    v[field] = ''
            writer.writerow(v)

    print(f"  💾 Saved: {output_path}")
    print(f"\n  Next step: Run shadowforge_v2.py on the output CSV:")
    print(f"    python shadowforge_v2.py -i {os.path.dirname(output_path) or '.'} -o ./shadowforge_output --force")
    print(f"\n{'═'*60}")


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f'ShadowForge Bridge v{VERSION} — JSON → Canonical CSV Converter'
    )
    parser.add_argument('-i', '--input', required=True, help='Input JSON file path')
    parser.add_argument('-o', '--output', default='csv_inputs/bridge_output.csv', help='Output CSV file path')
    parser.add_argument('-d', '--dealer', default='Unknown Dealer', help='Dealer name')
    parser.add_argument('-f', '--format', default=None, help='Force format (TYPESENSE_RESPONSE, STANDARD_VEHICLE, etc.)')
    args = parser.parse_args()

    convert_json_to_csv(args.input, args.output, args.dealer, args.format)


if __name__ == '__main__':
    main()