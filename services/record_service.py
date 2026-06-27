"""Record service for CRUD operations and purchase-redeem grouping."""

import json
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from config import DATA_FILE
from utils.helpers import calculate_end_date, calculate_real_rate, days_between


def load_data() -> List[Dict[str, Any]]:
    """Load records from JSON data file."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_data(records: List[Dict[str, Any]]) -> None:
    """Save records to JSON data file."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=4, ensure_ascii=False)


def get_purchase_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter purchase records."""
    return [r for r in records if r.get('type') == 'purchase']


def get_redeem_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter redeem records."""
    return [r for r in records if r.get('type') == 'redeem']


def create_purchase(data: dict) -> dict:
    """Create a new purchase record."""
    record = {
        'id': str(uuid.uuid4()),
        'type': 'purchase',
        'product_name': data['product_name'].strip(),
        'amount': float(data['amount']),
        'annual_rate': float(data['annual_rate']),
        'duration': int(data['duration']),
        'purchase_date': data['purchase_date'],
        'end_date': calculate_end_date(data['purchase_date'], int(data['duration'])),
        'bank_name': data.get('bank_name', '未知银行').strip(),
    }
    return record


def create_redeem(data: dict, purchase: dict) -> dict:
    """Create a new redeem record linked to a purchase."""
    purchase_date = purchase['purchase_date']
    redeem_date = data['redeem_date']
    duration_days = days_between(purchase_date, redeem_date)
    annual_rate = purchase['annual_rate']
    redeem_amount = float(data['redeem_amount'])

    if data.get('profit_calc') == 'manual':
        actual_profit = float(data['actual_profit'])
    else:
        from utils.helpers import calculate_auto_profit
        actual_profit = calculate_auto_profit(redeem_amount, annual_rate, duration_days)

    record = {
        'id': str(uuid.uuid4()),
        'type': 'redeem',
        'purchase_record_id': purchase['id'],
        'product_name': purchase['product_name'],
        'purchase_date': purchase_date,
        'annual_rate': annual_rate,
        'duration': purchase['duration'],
        'redeem_amount': redeem_amount,
        'redeem_date': redeem_date,
        'actual_profit': round(actual_profit, 2),
        'profit_calc': data.get('profit_calc', 'auto'),
    }
    return record


def get_grouped_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Group records by purchase, with nested redeem records."""
    purchases = get_purchase_records(records)
    redeems = get_redeem_records(records)

    # Build redeem lookup by purchase_record_id
    redeems_by_purchase = defaultdict(list)
    for r in redeems:
        redeems_by_purchase[r['purchase_record_id']].append(r)

    # Get status for each purchase
    result = []
    for p in purchases:
        purchase_redeems = redeems_by_purchase.get(p['id'], [])
        total_redeemed = sum(r['redeem_amount'] for r in purchase_redeems)
        remaining = p['amount'] - total_redeemed

        # Determine status
        if remaining <= 0:
            status = 'completed'
        elif total_redeemed > 0:
            status = 'partial'
        else:
            end = datetime.strptime(p['end_date'], '%Y-%m-%d')
            status = 'expired' if end < datetime.now() else 'holding'

        result.append({
            'purchase': p,
            'redeems': sorted(purchase_redeems, key=lambda x: x['redeem_date']),
            'status': status,
            'remaining': round(remaining, 2),
            'total_redeemed': round(total_redeemed, 2),
        })

    return result


def find_record(records: List[Dict[str, Any]], record_id: str) -> Optional[Dict[str, Any]]:
    """Find a record by ID."""
    return next((r for r in records if r['id'] == str(record_id)), None)


def delete_record(records: List[Dict[str, Any]], record_id: str) -> List[Dict[str, Any]]:
    """Delete a record by ID."""
    return [r for r in records if r['id'] != str(record_id)]


def get_redeems_for_purchase(records: List[Dict[str, Any]], purchase_id: str) -> List[Dict[str, Any]]:
    """Get all redeem records for a purchase."""
    return [r for r in get_redeem_records(records) if r.get('purchase_record_id') == purchase_id]
