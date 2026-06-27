from flask import Flask, render_template, request, redirect, flash, url_for
import json
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILE = 'finance_data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(records):
    with open(DATA_FILE, 'w') as f:
        json.dump(records, f, indent=4)

def calculate_end_date(purchase_date, duration_days):
    purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
    end_date = purchase_date + timedelta(days=duration_days)
    return end_date.strftime('%Y-%m-%d')

def calculate_profit(record):
    if record.get('type') == 'purchase':
        principal = record['amount']
        rate = record['annual_rate']
        duration_days = record['duration']
        # 将年利率转换为日利率
        daily_rate = (1 + rate) ** (1/365) - 1
        return principal * (1 + daily_rate) ** duration_days - principal
    return 0

def calculate_monthly_profits(records):
    monthly_profits = defaultdict(float)
    monthly_labels = []
    
    for record in records:
        if record.get('type') == 'redeem' and 'actual_profit' in record:
            redeem_date = datetime.strptime(record['redeem_date'], '%Y-%m-%d')
            month_key = redeem_date.strftime('%Y-%m')
            
            if month_key not in monthly_labels:
                monthly_labels.append(month_key)
                    
            monthly_profits[month_key] += record['actual_profit']
    
    # Sort by date
    monthly_labels.sort()
    sorted_profits = [monthly_profits[month] for month in monthly_labels]
    
    return monthly_labels, sorted_profits

def calculate_real_rate(record):
    """计算真实收益率"""
    if record.get('type') == 'redeem' and 'actual_profit' in record:
        purchase_date = datetime.strptime(record['purchase_date'], '%Y-%m-%d')
        redeem_date = datetime.strptime(record['redeem_date'], '%Y-%m-%d')
        days_held = (redeem_date - purchase_date).days
        if days_held > 0:
            return (record['actual_profit'] / record['redeem_amount']) * (365 / days_held) * 100
    return 0

def calculate_product_distribution(records):
    product_amounts = defaultdict(float)
    product_names = []
    
    for record in records:
        product_name = record['product_name']
        if product_name not in product_amounts:
            product_names.append(product_name)
            
        if record['type'] == 'purchase':
            product_amounts[product_name] += record['amount']
        elif record['type'] == 'redeem':
            product_amounts[product_name] += record['redeem_amount']
    
    return product_names, [product_amounts[name] for name in product_names]

def calculate_yearly_profits(records):
    yearly_profits = defaultdict(float)
    yearly_labels = []
    
    for record in records:
        if record.get('type') == 'redeem' and 'actual_profit' in record:
            redeem_date = datetime.strptime(record['redeem_date'], '%Y-%m-%d')
            year_key = redeem_date.strftime('%Y')
            
            if year_key not in yearly_labels:
                yearly_labels.append(year_key)
                
            yearly_profits[year_key] += record['actual_profit']
    
    # Sort by year
    yearly_labels.sort()
    sorted_profits = [yearly_profits[year] for year in yearly_labels]
    
    return yearly_labels, sorted_profits

@app.route('/statistics')
def statistics():
    records = load_data()
    monthly_labels, monthly_profits = calculate_monthly_profits(records)
    yearly_labels, yearly_profits = calculate_yearly_profits(records)
    product_names, product_amounts = calculate_product_distribution(records)
    
    return render_template('statistics.html',
                         monthly_labels=monthly_labels,
                         monthly_profits=monthly_profits,
                         yearly_labels=yearly_labels,
                         yearly_profits=yearly_profits,
                         product_names=product_names,
                         product_amounts=product_amounts)

@app.route('/')
def index():
    records = load_data()
    total_profit = 0
    total_actual_profit = 0
    total_real_rate = 0
    redeem_count = 0
    
    for record in records:
        if record.get('type') == 'purchase':
            record['profit'] = calculate_profit(record)
            total_profit += record['profit']
        elif record.get('type') == 'redeem' and 'actual_profit' in record:
            # 计算真实收益率
            purchase_date = datetime.strptime(record['purchase_date'], '%Y-%m-%d')
            redeem_date = datetime.strptime(record['redeem_date'], '%Y-%m-%d')
            days_held = (redeem_date - purchase_date).days
            if days_held > 0:
                record['real_rate'] = (record['actual_profit'] / record['redeem_amount']) * (365 / days_held) * 100
                total_real_rate += record['real_rate']
                redeem_count += 1
            total_actual_profit += record['actual_profit']
    
    # 计算平均真实收益率
    avg_real_rate = total_real_rate / redeem_count if redeem_count > 0 else 0
    
    monthly_labels, monthly_profits = calculate_monthly_profits(records)
    
    return render_template('index.html', 
                         records=records, 
                         total_profit=total_profit,
                         total_actual_profit=total_actual_profit,
                         avg_real_rate=avg_real_rate,
                         monthly_labels=monthly_labels,
                         monthly_profits=monthly_profits)

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    records = load_data()
    if request.method == 'POST':
        try:
            record_type = request.form['record_type']
            
            if record_type == 'purchase':
                record = {
                    'id': str(uuid.uuid4()),
                    'type': 'purchase',
                    'product_name': request.form['product_name'],
                    'amount': float(request.form['amount']),
                    'annual_rate': float(request.form['annual_rate']),
                    'duration': int(request.form['duration']),
                    'purchase_date': request.form['purchase_date'],
                    'end_date': calculate_end_date(request.form['purchase_date'], int(request.form['duration']))
                }
            else:
                purchase_record_id = request.form['purchase_record_id']
                purchase_record = next((r for r in records if r['id'] == purchase_record_id), None)
                
                if not purchase_record:
                    flash('买入记录未找到', 'error')
                    return redirect('/add')
                    
                redeem_amount = float(request.form['redeem_amount'])
                if redeem_amount > purchase_record['amount']:
                    flash('赎回金额不能超过原始金额', 'error')
                    return redirect('/add')
                    
                # 计算实际收益
                purchase_date = datetime.strptime(purchase_record['purchase_date'], '%Y-%m-%d')
                redeem_date = datetime.strptime(request.form['redeem_date'], '%Y-%m-%d')
                duration_days = (redeem_date - purchase_date).days
                
                # 根据收益计算方式处理
                profit_calc = request.form.get('profit_calc', 'auto')
                if profit_calc == 'manual':
                    actual_profit = float(request.form['actual_profit'])
                else:
                    # 将年利率转换为日利率
                    daily_rate = (1 + purchase_record['annual_rate']) ** (1/365) - 1
                    actual_profit = redeem_amount * (1 + daily_rate) ** duration_days - redeem_amount
                
                record = {
                    'id': str(uuid.uuid4()),
                    'type': 'redeem',
                    'purchase_record_id': purchase_record_id,
                    'redeem_amount': redeem_amount,
                    'redeem_date': request.form['redeem_date'],
                    'purchase_date': purchase_record['purchase_date'],
                    'product_name': purchase_record['product_name'],
                    'annual_rate': purchase_record['annual_rate'],
                    'duration': purchase_record['duration'],
                    'actual_profit': actual_profit,
                    'profit_calc': profit_calc
                }
            
            # 确保数据文件存在
            if not records:
                with open(DATA_FILE, 'w') as f:
                    json.dump([], f)
            records.append(record)
            save_data(records)
            
            flash('理财记录添加成功！', 'success')
            return redirect('/')
            
        except Exception as e:
            flash(f'添加记录失败: {str(e)}', 'error')
            return redirect('/add')
    
    # 获取所有买入记录用于赎回选择
    purchase_records = [r for r in records if r.get('type') == 'purchase']
    return render_template('add.html', purchase_records=purchase_records)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_record(id):
    records = load_data()
    record = next((r for r in records if r['id'] == str(id)), None)
    if not record:
        flash('记录未找到', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        try:
            record['product_name'] = request.form['product_name']
            record['amount'] = float(request.form['amount'])
            record['annual_rate'] = float(request.form['annual_rate'])
            record['duration'] = int(request.form['duration'])
            record['purchase_date'] = request.form['purchase_date']
            record['end_date'] = calculate_end_date(request.form['purchase_date'], int(request.form['duration']))
            
            save_data(records)
            flash('记录更新成功！', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'更新记录失败: {str(e)}', 'error')
            return redirect(url_for('edit_record', id=id))
        
    return render_template('edit.html', record=record)

@app.route('/delete/<id>')
def delete_record(id):
    records = load_data()
    records = [r for r in records if r['id'] != str(id)]
    save_data(records)
    flash('记录删除成功！', 'success')
    return redirect(url_for('index'))

@app.route('/redeem', methods=['GET', 'POST'])
def redeem_record():
    records = load_data()
    if request.method == 'POST':
        try:
            record_id = request.form['record_id']
            redeem_date_str = request.form['redeem_date']
            if not redeem_date_str:
                flash('请填写赎回日期', 'error')
                return redirect(url_for('redeem_record'))
                
            try:
                redeem_date = datetime.strptime(redeem_date_str, '%Y-%m-%d')
            except ValueError:
                flash('日期格式不正确，请使用YYYY-MM-DD格式', 'error')
                return redirect(url_for('redeem_record'))
                
            redeem_amount = float(request.form['redeem_amount'])
            
            record = next((r for r in records if r['id'] == record_id), None)
            if not record:
                flash('理财记录未找到', 'error')
                return redirect(url_for('redeem_record'))
                
            # 检查是否已赎回
            if record.get('type') == 'redeem':
                flash('该记录已经是赎回记录，不能再次赎回', 'error')
                return redirect(url_for('redeem_record'))
                
            if record.get('redeemed', False):
                flash('该理财记录已赎回', 'error')
                return redirect(url_for('redeem_record'))
                
            # 检查剩余金额
            remaining_amount = record['amount'] - sum(
                r['redeem_amount'] for r in records 
                if r.get('purchase_record_id') == record_id
            )
            if redeem_amount > remaining_amount:
                flash(f'赎回金额不能超过剩余金额（当前剩余：{remaining_amount:.2f}）', 'error')
                return redirect(url_for('redeem_record'))
                
            # 计算实际收益
            profit_calc = request.form.get('profit_calc', 'auto')
            purchase_date = datetime.strptime(record['purchase_date'], '%Y-%m-%d')
            redeem_date = datetime.strptime(redeem_date, '%Y-%m-%d')
            days_held = (redeem_date - purchase_date).days
            
            if profit_calc == 'auto':
                # 将年利率转换为日利率
                daily_rate = (1 + record['annual_rate']) ** (1/365) - 1
                actual_profit = record['amount'] * (1 + daily_rate) ** days_held - record['amount']
                real_rate = record['annual_rate']
            else:
                actual_profit = float(request.form.get('actual_profit', 0))
                if actual_profit < 0:
                    flash('请输入有效的收益金额', 'error')
                    return redirect(url_for('redeem_record'))
                # 计算真实收益率
                real_rate = (actual_profit / redeem_amount) * (365 / days_held) * 100
                # 更新实际收益
                record['actual_profit'] = actual_profit
            
            # 更新记录
            record['redeemed'] = True
            record['redeem_date'] = redeem_date
            record['redeem_amount'] = redeem_amount
            record['actual_profit'] = actual_profit
            record['real_rate'] = real_rate
            record['amount'] = record['amount'] - redeem_amount  # 更新剩余金额
            
            # 标记原始买入记录为已赎回
            purchase_record = next((r for r in records if r['id'] == record_id), None)
            if purchase_record:
                purchase_record['redeemed'] = True
            
            save_data(records)
            flash('赎回成功！', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'赎回失败: {str(e)}', 'error')
            return redirect(url_for('redeem_record'))
    
    # 只显示未赎回的记录
    active_records = [r for r in records if not r.get('redeemed', False)]
    return render_template('redeem.html', records=active_records)

if __name__ == "__main__":
    from werkzeug.serving import is_running_from_reloader
    import signal
    import sys
    
    def shutdown_handler(signum, frame):
        print("\nServer is shutting down...")
        sys.exit(0)
        
    if not is_running_from_reloader():
        signal.signal(signal.SIGINT, shutdown_handler)
        signal.signal(signal.SIGTERM, shutdown_handler)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        print("Server stopped")
