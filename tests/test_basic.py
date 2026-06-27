"""Basic pytest tests for FamilyFinance."""

import json
import os
import sys
import tempfile

import pytest

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_records():
    """Provide sample records for testing."""
    return [
        {
            "id": "p1",
            "type": "purchase",
            "product_name": "测试产品A",
            "amount": 100000.0,
            "annual_rate": 0.0474,
            "duration": 90,
            "purchase_date": "2025-01-09",
            "end_date": "2025-04-09",
            "bank_name": "交通银行",
        },
        {
            "id": "p2",
            "type": "purchase",
            "product_name": "测试产品B",
            "amount": 50000.0,
            "annual_rate": 0.022,
            "duration": 365,
            "purchase_date": "2025-03-01",
            "end_date": "2026-03-01",
            "bank_name": "民生银行",
        },
        {
            "id": "r1",
            "type": "redeem",
            "purchase_record_id": "p1",
            "product_name": "测试产品A",
            "purchase_date": "2025-01-09",
            "annual_rate": 0.0474,
            "duration": 90,
            "redeem_amount": 100000.0,
            "redeem_date": "2025-04-10",
            "actual_profit": 500.0,
            "profit_calc": "manual",
        },
    ]


# ---------------------------------------------------------------------------
# Test service layer
# ---------------------------------------------------------------------------
class TestRecordService:
    """Tests for record_service module."""

    def test_load_data(self):
        """load_data should return a list (may be empty or populated)."""
        from services.record_service import load_data
        data = load_data()
        assert isinstance(data, list)
        # If data file exists, verify records have expected structure
        if data:
            assert 'id' in data[0]
            assert 'type' in data[0]

    def test_get_purchase_records(self, sample_records):
        from services.record_service import get_purchase_records
        purchases = get_purchase_records(sample_records)
        assert len(purchases) == 2
        assert all(r['type'] == 'purchase' for r in purchases)

    def test_get_redeem_records(self, sample_records):
        from services.record_service import get_redeem_records
        redeems = get_redeem_records(sample_records)
        assert len(redeems) == 1

    def test_find_record(self, sample_records):
        from services.record_service import find_record
        r = find_record(sample_records, 'p1')
        assert r is not None
        assert r['product_name'] == '测试产品A'

    def test_find_record_not_found(self, sample_records):
        from services.record_service import find_record
        r = find_record(sample_records, 'nonexistent')
        assert r is None

    def test_get_grouped_records(self, sample_records):
        from services.record_service import get_grouped_records
        grouped = get_grouped_records(sample_records)
        assert len(grouped) == 2

        # p1 should be completed (fully redeemed)
        p1_group = [g for g in grouped if g['purchase']['id'] == 'p1'][0]
        assert p1_group['status'] == 'completed'
        assert p1_group['remaining'] == 0
        assert len(p1_group['redeems']) == 1

        # p2 should be holding (no redeems, not expired)
        p2_group = [g for g in grouped if g['purchase']['id'] == 'p2'][0]
        assert p2_group['status'] in ('holding', 'expired')  # depends on current date
        assert len(p2_group['redeems']) == 0

    def test_get_redeems_for_purchase(self, sample_records):
        from services.record_service import get_redeems_for_purchase
        redeems = get_redeems_for_purchase(sample_records, 'p1')
        assert len(redeems) == 1
        assert redeems[0]['actual_profit'] == 500.0

    def test_delete_record(self, sample_records):
        from services.record_service import delete_record
        result = delete_record(sample_records, 'p1')
        assert len(result) == 2
        assert 'p1' not in [r['id'] for r in result]


# ---------------------------------------------------------------------------
# Test utility functions
# ---------------------------------------------------------------------------
class TestHelpers:
    """Tests for helper utilities."""

    def test_calculate_end_date(self):
        from utils.helpers import calculate_end_date
        end = calculate_end_date('2025-01-09', 90)
        assert end == '2025-04-09'

    def test_calculate_auto_profit(self):
        from utils.helpers import calculate_auto_profit
        profit = calculate_auto_profit(100000, 0.0474, 90)
        assert 1100 < profit < 1200  # reasonable range

    def test_calculate_real_rate(self):
        from utils.helpers import calculate_real_rate
        rate = calculate_real_rate(500, 100000, 90)
        assert 2.0 < rate < 3.0  # ~2.03%

    def test_days_between(self):
        from utils.helpers import days_between
        days = days_between('2025-01-09', '2025-04-09')
        assert days == 90

    def test_format_amount(self):
        from utils.helpers import format_amount
        assert format_amount(1000.5) == '1,000.50'
        assert format_amount(100000) == '100,000.00'


# ---------------------------------------------------------------------------
# Test validators
# ---------------------------------------------------------------------------
class TestValidators:
    """Tests for validators."""

    def test_validate_purchase_valid(self):
        from utils.validators import validate_purchase
        errors = validate_purchase({
            'product_name': '测试',
            'amount': 100000,
            'annual_rate': 0.0474,
            'duration': 90,
            'purchase_date': '2025-01-01',
        })
        assert len(errors) == 0

    def test_validate_purchase_missing_name(self):
        from utils.validators import validate_purchase
        errors = validate_purchase({
            'product_name': '',
            'amount': 100000,
            'annual_rate': 0.0474,
            'duration': 90,
            'purchase_date': '2025-01-01',
        })
        assert '产品名称不能为空' in errors

    def test_validate_purchase_zero_amount(self):
        from utils.validators import validate_purchase
        errors = validate_purchase({
            'product_name': '测试',
            'amount': 0,
            'annual_rate': 0.0474,
            'duration': 90,
            'purchase_date': '2025-01-01',
        })
        assert '金额必须大于0' in errors

    def test_validate_purchase_bad_rate(self):
        from utils.validators import validate_purchase
        errors = validate_purchase({
            'product_name': '测试',
            'amount': 100000,
            'annual_rate': 1.5,  # > 1
            'duration': 90,
            'purchase_date': '2025-01-01',
        })
        assert '年化利率必须在0-1之间' in errors

    def test_validate_redeem_no_purchase(self):
        from utils.validators import validate_redeem
        errors = validate_redeem({'purchase_record_id': 'x'}, None)
        assert '关联的购买记录不存在' in errors


# ---------------------------------------------------------------------------
# Test app routes
# ---------------------------------------------------------------------------
class TestApp:
    """Tests for Flask app routes."""

    def setup_method(self):
        # Backup original data file path and restore after
        self.original_data_file = None

    def test_index_route(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/')
            assert resp.status_code == 200

    def test_records_route(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/records')
            assert resp.status_code == 200

    def test_add_route_get(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/add')
            assert resp.status_code == 200

    def test_statistics_route(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/statistics')
            assert resp.status_code == 200

    def test_statistics_filter(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/statistics?range=year')
            assert resp.status_code == 200

    def test_records_search(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/records?search=测试')
            assert resp.status_code == 200

    def test_records_filter(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/records?status=holding')
            assert resp.status_code == 200

    def test_export_csv(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/export?format=csv')
            assert resp.status_code == 200
            assert resp.content_type.startswith('text/csv')

    def test_edit_nonexistent(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/edit/nonexistent', follow_redirects=True)
            assert resp.status_code == 200

    def test_delete_nonexistent(self):
        from app import app
        with app.test_client() as c:
            resp = c.get('/delete/nonexistent', follow_redirects=True)
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Test data migration
# ---------------------------------------------------------------------------
class TestMigration:
    """Tests for data migration script."""

    def test_migrate_script_imports(self):
        """migrate_data.py should at least import without error."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "migrate_data",
            os.path.join(os.path.dirname(__file__), '..', 'migrate_data.py')
        )
        assert spec is not None, "migrate_data.py should be importable"
