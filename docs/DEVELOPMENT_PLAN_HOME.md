# FamilyFinance 家庭增强版开发方案

> **版本：v1.0-home** | 更新日期：2026-06-27
>
> 专注家庭使用场景，保留核心功能，增强仪表盘和统计分析

---

## 一、功能规划

### 1.1 功能清单

| 模块 | 功能 | 优先级 | 说明 |
|------|------|--------|------|
| **核心** | 买卖关联展示 | P0 | 分组视图，展示投资生命周期 |
| **核心** | 添加/编辑/删除记录 | P0 | 基础CRUD操作 |
| **核心** | 收益计算 | P0 | 自动计算+手动输入 |
| **仪表盘** | 总投入/总资产/总收益/年化收益 | P0 | 四大核心指标 |
| **仪表盘** | 即将到期产品列表 | P0 | 未来30天到期提醒 |
| **仪表盘** | 持有中产品列表 | P0 | 快速查看当前投资 |
| **仪表盘** | 最近赎回记录 | P1 | 查看最近收益 |
| **统计** | 月度收益趋势图 | P0 | 柱状图展示 |
| **统计** | 收益来源分布图 | P1 | 饼图展示 |
| **统计** | 银行分布图 | P1 | 饼图展示 |
| **统计** | 产品收益排行榜 | P1 | 按收益排序 |
| **统计** | 投资统计摘要 | P1 | 关键统计数据 |
| **统计** | 时间范围筛选 | P1 | 本年/本月/自定义 |
| **导出** | Excel导出 | P1 | 导出记录数据 |

### 1.2 不做的功能

| 功能 | 原因 |
|------|------|
| 投资组合分析 | 家庭用不到 |
| 现金流预测 | 过于复杂 |
| 税务计算 | 国内理财通常免税 |
| 复投管理 | 手动管理即可 |
| 多用户支持 | 家庭共用 |
| 产品推荐 | 需要外部数据 |
| 风险评估 | 过于专业 |
| 银行数据导入 | 手动录入更可靠 |
| 批量操作 | 逐条操作即可 |
| 标签/分类系统 | 用银行名区分即可 |

---

## 二、数据模型

### 2.1 购买记录
```json
{
  "id": "uuid",
  "type": "purchase",
  "product_name": "产品名称",
  "amount": 100000.0,
  "annual_rate": 0.0474,
  "duration": 90,
  "purchase_date": "2025-01-09",
  "end_date": "2025-04-09",
  "bank_name": "交通银行"
}
```

### 2.2 赎回记录
```json
{
  "id": "uuid",
  "type": "redeem",
  "purchase_record_id": "关联ID",
  "redeem_amount": 100000.0,
  "redeem_date": "2025-04-17",
  "actual_profit": 511.0,
  "profit_calc": "manual"
}
```

---

## 三、界面设计

### 3.1 仪表盘

```
┌─────────────────────────────────────────────────────────────────┐
│                        投资仪表盘                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ 总投入   │  │ 总资产   │  │ 总收益   │  │ 年化收益 │           │
│  │ 500,000 │  │ 503,250 │  │ 3,250   │  │ 3.85%  │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
├─────────────────────────────────────────────────────────────────┤
│  即将到期产品（未来30天）                      [查看全部]        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 交银理财90天  │ 到期: 2026-07-01 │ 100,000元 │ 3天后到期  │   │
│  │ 民生安心存    │ 到期: 2026-07-15 │ 100,000元 │ 17天后到期 │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  持有中产品                                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ▼ 民生安心存                                              │   │
│  │   金额: 100,000元 │ 年化: 2.20% │ 期限: 1095天            │   │
│  │   购买: 2024-09-23 │ 到期: 2027-09-23                    │   │
│  │   预计收益: 6,600元 │ [赎回] [编辑]                       │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ ▼ 民生贵竹增利月月盈18号                                  │   │
│  │   金额: 100,000元 │ 年化: 4.78% │ 期限: 30天              │   │
│  │   购买: 2025-01-09 │ 到期: 2025-02-08                    │   │
│  │   预计收益: 393元 │ [赎回] [编辑]                         │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  最近赎回                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 交银理财90天 │ 赎回: 2025-04-17 │ 收益: 511元 │ 年化: 5.04% │   │
│  │ 民生贵竹30天 │ 赎回: 2025-02-12 │ 收益: 175元 │ 年化: 6.39% │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 统计分析

```
┌─────────────────────────────────────────────────────────────────┐
│                        统计分析                                  │
├─────────────────────────────────────────────────────────────────┤
│  时间范围: [全部] [本年] [本月] [自定义]                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    月度收益趋势                           │   │
│  │    ▲                                                      │   │
│  │    │      ██                                              │   │
│  │    │   ██ ██ ██                                           │   │
│  │    │██ ██ ██ ██ ██                                        │   │
│  │    └─────────────────────────────────────────────▶        │   │
│  │      1月 2月 3月 4月 5月 6月                               │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │    收益来源分布      │  │    银行分布          │              │
│  │                     │  │                     │              │
│  │    ██████ 交银      │  │    █████████ 民生   │              │
│  │    ████ 民生        │  │    ██████ 交银      │              │
│  │                     │  │                     │              │
│  └─────────────────────┘  └─────────────────────┘              │
├─────────────────────────────────────────────────────────────────┤
│  产品收益排行榜                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 排名 │ 产品名称          │ 收益   │ 年化   │ 持有天数      │   │
│  │  1   │ 交银理财90天      │ 511元  │ 5.04%  │ 90天         │   │
│  │  2   │ 民生贵竹30天      │ 175元  │ 6.39%  │ 30天         │   │
│  │  3   │ 民生固收91天      │ 598元  │ 2.41%  │ 91天         │   │
│  └─────────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  投资统计摘要                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 总投资笔数: 12笔    │  平均持有天数: 85天                  │   │
│  │ 平均年化收益: 3.85% │  最高年化收益: 6.39%                │   │
│  │ 单笔最高收益: 681元 │  单笔最低收益: 125元                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 四、技术实现

### 4.1 目录结构
```
FamilyFinance/
├── app.py                  # Flask 应用入口
├── config.py               # 配置文件
├── requirements.txt        # 依赖管理
│
├── models/                 # 数据模型
│   ├── __init__.py
│   └── record.py          # 记录模型
│
├── services/               # 业务逻辑
│   ├── __init__.py
│   ├── record_service.py  # 记录服务
│   └── statistics_service.py # 统计服务
│
├── utils/                  # 工具函数
│   ├── __init__.py
│   └── helpers.py         # 辅助函数
│
├── static/                 # 静态资源
│   ├── css/style.css
│   └── js/app.js
│
├── templates/              # 模板
│   ├── base.html
│   ├── index.html         # 仪表盘
│   ├── records/
│   │   ├── list.html      # 记录列表
│   │   ├── add.html       # 添加记录
│   │   └── edit.html      # 编辑记录
│   └── statistics/
│       └── index.html     # 统计分析
│
├── data/                   # 数据目录
│   └── finance_data.json
│
└── tests/                  # 测试
    ├── test_services.py
    └── test_routes.py
```

### 4.2 依赖清单
```
flask>=3.0.0
openpyxl>=3.1.0
```

### 4.3 核心代码示例

**services/statistics_service.py**
```python
"""统计分析服务"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any

DATE_FORMAT = '%Y-%m-%d'


class StatisticsService:
    """统计服务类"""
    
    def __init__(self, records: List[Dict[str, Any]]):
        self.records = records
        self.purchases = [r for r in records if r['type'] == 'purchase']
        self.redeems = [r for r in records if r['type'] == 'redeem']
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """获取仪表盘汇总数据"""
        total_invested = sum(r['amount'] for r in self.purchases)
        total_redeemed = sum(r['redeem_amount'] for r in self.redeems)
        total_profit = sum(r.get('actual_profit', 0) for r in self.redeems)
        
        # 计算平均年化收益率
        avg_rate = 0
        if self.redeems:
            rates = []
            for r in self.redeems:
                purchase = self._find_purchase(r['purchase_record_id'])
                if purchase:
                    days = self._days_between(purchase['purchase_date'], r['redeem_date'])
                    if days > 0:
                        rate = (r['actual_profit'] / r['redeem_amount']) * (365 / days) * 100
                        rates.append(rate)
            avg_rate = sum(rates) / len(rates) if rates else 0
        
        return {
            'total_invested': total_invested,
            'total_assets': total_invested,  # 简化：不计算已赎回
            'total_profit': total_profit,
            'avg_rate': round(avg_rate, 2)
        }
    
    def get_upcoming_maturities(self, days: int = 30) -> List[Dict[str, Any]]:
        """获取即将到期的产品"""
        today = datetime.now()
        upcoming = []
        
        for p in self.purchases:
            end_date = datetime.strptime(p['end_date'], DATE_FORMAT)
            days_remaining = (end_date - today).days
            
            if 0 < days_remaining <= days:
                # 检查是否已全部赎回
                remaining = self._get_remaining_amount(p['id'])
                if remaining > 0:
                    upcoming.append({
                        'product_name': p['product_name'],
                        'end_date': p['end_date'],
                        'amount': remaining,
                        'days_remaining': days_remaining
                    })
        
        return sorted(upcoming, key=lambda x: x['days_remaining'])
    
    def get_monthly_profits(self, year: int = None) -> Dict[str, float]:
        """获取月度收益"""
        if year is None:
            year = datetime.now().year
        
        monthly = defaultdict(float)
        for r in self.redeems:
            redeem_date = datetime.strptime(r['redeem_date'], DATE_FORMAT)
            if redeem_date.year == year:
                month_key = redeem_date.strftime('%Y-%m')
                monthly[month_key] += r.get('actual_profit', 0)
        
        return dict(sorted(monthly.items()))
    
    def get_profit_by_product(self) -> List[Dict[str, Any]]:
        """按产品统计收益"""
        product_profits = defaultdict(float)
        product_info = {}
        
        for r in self.redeems:
            product_name = r.get('product_name', '未知产品')
            product_profits[product_name] += r.get('actual_profit', 0)
            
            if product_name not in product_info:
                purchase = self._find_purchase(r['purchase_record_id'])
                if purchase:
                    days = self._days_between(purchase['purchase_date'], r['redeem_date'])
                    rate = (r['actual_profit'] / r['redeem_amount']) * (365 / days) * 100 if days > 0 else 0
                    product_info[product_name] = {
                        'days': days,
                        'rate': round(rate, 2)
                    }
        
        result = []
        for name, profit in sorted(product_profits.items(), key=lambda x: x[1], reverse=True):
            info = product_info.get(name, {'days': 0, 'rate': 0})
            result.append({
                'product_name': name,
                'profit': profit,
                'rate': info['rate'],
                'days': info['days']
            })
        
        return result
    
    def get_profit_by_bank(self) -> Dict[str, float]:
        """按银行统计收益"""
        bank_profits = defaultdict(float)
        
        for r in self.redeems:
            purchase = self._find_purchase(r['purchase_record_id'])
            bank = purchase.get('bank_name', '未知银行') if purchase else '未知银行'
            bank_profits[bank] += r.get('actual_profit', 0)
        
        return dict(sorted(bank_profits.items(), key=lambda x: x[1], reverse=True))
    
    def get_statistics_summary(self) -> Dict[str, Any]:
        """获取统计摘要"""
        if not self.redeems:
            return {
                'total_count': 0,
                'avg_days': 0,
                'avg_rate': 0,
                'max_rate': 0,
                'max_profit': 0,
                'min_profit': 0
            }
        
        profits = [r.get('actual_profit', 0) for r in self.redeems]
        rates = []
        days_list = []
        
        for r in self.redeems:
            purchase = self._find_purchase(r['purchase_record_id'])
            if purchase:
                days = self._days_between(purchase['purchase_date'], r['redeem_date'])
                if days > 0:
                    rate = (r['actual_profit'] / r['redeem_amount']) * (365 / days) * 100
                    rates.append(rate)
                    days_list.append(days)
        
        return {
            'total_count': len(self.redeems),
            'avg_days': round(sum(days_list) / len(days_list)) if days_list else 0,
            'avg_rate': round(sum(rates) / len(rates), 2) if rates else 0,
            'max_rate': round(max(rates), 2) if rates else 0,
            'max_profit': max(profits),
            'min_profit': min(profits)
        }
    
    def _find_purchase(self, purchase_id: str) -> Dict[str, Any]:
        """查找购买记录"""
        return next((p for p in self.purchases if p['id'] == purchase_id), None)
    
    def _get_remaining_amount(self, purchase_id: str) -> float:
        """获取剩余金额"""
        purchase = self._find_purchase(purchase_id)
        if not purchase:
            return 0
        
        redeemed = sum(
            r['redeem_amount'] for r in self.redeems
            if r['purchase_record_id'] == purchase_id
        )
        return purchase['amount'] - redeemed
    
    def _days_between(self, date1_str: str, date2_str: str) -> int:
        """计算日期天数差"""
        date1 = datetime.strptime(date1_str, DATE_FORMAT)
        date2 = datetime.strptime(date2_str, DATE_FORMAT)
        return (date2 - date1).days
```

---

## 五、开发计划

### 5.1 阶段划分

| 阶段 | 时间 | 内容 | 交付物 |
|------|------|------|--------|
| 阶段一 | 1周 | 基础架构 | 目录结构、数据模型、迁移脚本 |
| 阶段二 | 1.5周 | 核心功能 | 买卖关联展示、CRUD操作 |
| 阶段三 | 1.5周 | 仪表盘 | 指标卡片、到期提醒、持有列表 |
| 阶段四 | 1.5周 | 统计分析 | 图表、排行榜、摘要 |
| 阶段五 | 0.5周 | 导出+测试 | Excel导出、基础测试 |
| **总计** | **6周** | | |

### 5.2 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| M1 | 第1周末 | 基础架构完成 |
| M2 | 第2.5周末 | 核心功能可用 |
| M3 | 第4周末 | 仪表盘完成 |
| M4 | 第5.5周末 | 统计分析完成 |
| M5 | 第6周末 | 全部完成，可上线 |

---

## 六、快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 数据迁移
python migrate_data.py

# 运行应用
python app.py

# 访问
# http://localhost:5000
```

---

*家庭增强版方案 - 专注核心功能，增强仪表盘和统计分析*
