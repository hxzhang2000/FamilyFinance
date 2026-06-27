"""Helper utilities for date formatting, amount formatting, and profit calculations."""

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

DATE_FORMAT = '%Y-%m-%d'


def calculate_end_date(purchase_date: str, duration_days: int) -> str:
    """Calculate end date from purchase date and duration."""
    d = datetime.strptime(purchase_date, DATE_FORMAT)
    end = d + timedelta(days=duration_days)
    return end.strftime(DATE_FORMAT)


def calculate_auto_profit(amount: float, annual_rate: float, days_held: int) -> float:
    """Calculate profit using compound interest formula.

    daily_rate = (1 + annual_rate)^(1/365) - 1
    profit = amount * (1 + daily_rate)^days_held - amount
    """
    daily_rate = (1 + annual_rate) ** (1 / 365) - 1
    return amount * (1 + daily_rate) ** days_held - amount


def calculate_real_rate(actual_profit: float, redeem_amount: float, days_held: int) -> float:
    """Calculate real annualized rate of return."""
    if days_held <= 0 or redeem_amount <= 0:
        return 0.0
    return (actual_profit / redeem_amount) * (365 / days_held) * 100


def days_between(date1_str: str, date2_str: str) -> int:
    """Calculate days between two dates."""
    d1 = datetime.strptime(date1_str, DATE_FORMAT)
    d2 = datetime.strptime(date2_str, DATE_FORMAT)
    return (d2 - d1).days


def format_amount(amount: float) -> str:
    """Format amount with thousands separator."""
    d = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f'{d:,.2f}'
