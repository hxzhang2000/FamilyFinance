"""Simple validators for purchase and redeem records (replaces Marshmallow)."""

from datetime import datetime


def validate_purchase(data: dict) -> list:
    """Validate purchase record data, returns list of error messages."""
    errors = []

    if not data.get('product_name', '').strip():
        errors.append('产品名称不能为空')

    amount = data.get('amount', 0)
    if not isinstance(amount, (int, float)) or amount <= 0:
        errors.append('金额必须大于0')

    rate = data.get('annual_rate', 0)
    if not isinstance(rate, (int, float)) or not (0 < rate < 1):
        errors.append('年化利率必须在0-1之间')

    duration = data.get('duration', 0)
    if not isinstance(duration, int) or duration <= 0:
        errors.append('期限必须大于0天')

    if not data.get('purchase_date'):
        errors.append('购买日期不能为空')

    return errors


def validate_redeem(data: dict, purchase: dict = None) -> list:
    """Validate redeem record data, returns list of error messages."""
    errors = []

    if not data.get('purchase_record_id'):
        errors.append('请选择关联的购买记录')

    if purchase is None:
        errors.append('关联的购买记录不存在')
        return errors

    redeem_amount = data.get('redeem_amount', 0)
    if not isinstance(redeem_amount, (int, float)) or redeem_amount <= 0:
        errors.append('赎回金额必须大于0')
    elif redeem_amount > purchase['amount']:
        errors.append('赎回金额不能超过原始金额')

    if not data.get('redeem_date'):
        errors.append('赎回日期不能为空')

    profit_calc = data.get('profit_calc', 'auto')
    if profit_calc == 'manual':
        actual_profit = data.get('actual_profit', 0)
        if not isinstance(actual_profit, (int, float)):
            errors.append('实际收益必须是数字')

    return errors
