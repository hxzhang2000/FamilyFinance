from finance_manager import FinanceManager
from datetime import datetime

def display_menu():
    print("\n家庭理财管理系统")
    print("1. 添加理财记录")
    print("2. 查看所有记录")
    print("3. 计算单笔收益")
    print("4. 计算总收益")
    print("5. 赎回理财产品")
    print("6. 退出")

def get_valid_input(prompt, input_type):
    while True:
        try:
            value = input_type(input(prompt))
            return value
        except ValueError:
            print("输入无效，请重新输入")

def main():
    manager = FinanceManager()
    
    while True:
        display_menu()
        choice = input("请选择操作（1-6）：")
        
        if choice == '1':
            print("\n添加新理财记录")
            product_name = input("产品名称：")
            amount = get_valid_input("投资金额：", float)
            purchase_date = input("购买日期（YYYY-MM-DD）：")
            annual_rate = get_valid_input("年化收益率（%）：", float)
            duration = get_valid_input("投资期限（天）：", int)
            
            record = manager.add_record(product_name, amount, purchase_date, annual_rate, duration)
            print(f"\n成功添加记录：{record}")
            
        elif choice == '2':
            print("\n所有理财记录：")
            for record in manager.get_all_records():
                print(f"{record['id']}. {record['product_name']} - {record['amount']}元 - {record['purchase_date']} - {record['status']}")
                
        elif choice == '3':
            record_id = get_valid_input("请输入要计算收益的记录ID：", int)
            profit = manager.calculate_profit(record_id)
            if profit is not None:
                print(f"\n当前收益：{profit}元")
            else:
                print("未找到该记录")
                
        elif choice == '4':
            total_profit = manager.get_total_profit()
            print(f"\n当前总收益：{total_profit}元")
            
        elif choice == '5':
            record_id = get_valid_input("请输入要赎回的记录ID：", int)
            if manager.redeem_record(record_id):
                print("成功赎回")
            else:
                print("赎回失败，请检查ID是否正确")
                
        elif choice == '6':
            print("退出系统")
            break
            
        else:
            print("无效选择，请输入1-6之间的数字")

if __name__ == "__main__":
    main()
