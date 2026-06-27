import json
from datetime import datetime

class FinanceManager:
    def __init__(self, data_file='finance_data.json'):
        self.data_file = data_file
        self.records = self.load_data()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.records, f, indent=4)

    def add_record(self, product_name, amount, purchase_date, annual_rate, duration):
        record = {
            'id': len(self.records) + 1,
            'product_name': product_name,
            'amount': float(amount),
            'purchase_date': purchase_date,
            'annual_rate': float(annual_rate),
            'duration': int(duration),
            'status': '持有中'
        }
        self.records.append(record)
        self.save_data()
        return record

    def calculate_profit(self, record_id):
        record = next((r for r in self.records if r['id'] == record_id), None)
        if not record:
            return None
            
        purchase_date = datetime.strptime(record['purchase_date'], '%Y-%m-%d')
        current_date = datetime.now()
        days_held = (current_date - purchase_date).days
        
        if days_held < 0:
            return 0
            
        annual_rate = record['annual_rate'] / 100
        amount = record['amount']
        
        # 简单利息计算
        profit = amount * annual_rate * (days_held / 365)
        return round(profit, 2)

    def get_total_profit(self):
        total = 0
        for record in self.records:
            if record['status'] == '持有中':
                profit = self.calculate_profit(record['id'])
                if profit:
                    total += profit
        return round(total, 2)

    def calculate_real_rate(self, principal, profit, days):
        if days == 0 or principal == 0:
            return 0
        return (profit / principal) * (365 / days) * 100

    def redeem_record(self, record_id, redeem_amount, manual_profit=None):
        record = next((r for r in self.records if r['id'] == record_id), None)
        if record:
            purchase_date = datetime.strptime(record['purchase_date'], '%Y-%m-%d')
            current_date = datetime.now()
            days_held = (current_date - purchase_date).days
            
            if manual_profit is not None:
                profit = float(manual_profit)
                real_rate = self.calculate_real_rate(float(redeem_amount), profit, days_held)
            else:
                profit = self.calculate_profit(record_id)
                real_rate = record['annual_rate']
            
            record.update({
                'status': '已赎回',
                'purchase_date': record['purchase_date'],
                'redeem_date': current_date.strftime('%Y-%m-%d'),
                'redeem_amount': float(redeem_amount),
                'profit': profit,
                'real_rate': real_rate
            })
            self.save_data()
            return True
        return False

    def get_all_records(self):
        return self.records
