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
| **仪表盘** | 总投入/持有中/累计收益/平均年化 | P0 | 四大核心指标 |
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

> 注意：赎回记录反规范化冗余存储购入时的产品名、年化等信息，避免每次展示都做 JOIN 查询。

```json
{
  "id": "uuid",
  "type": "redeem",
  "purchase_record_id": "关联ID",
  "product_name": "交银理财灵动慧利6号90天",
  "purchase_date": "2025-01-09",
  "annual_rate": 0.0474,
  "duration": 90,
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
│  │ 总投入   │  │ 持有中   │  │ 累计收益 │  │ 平均年化 │           │
│  │ 500,000 │  │ 300,000 │  │ 3,250   │  │ 3.85%  │           │
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
├── app.py                  # Flask 应用入口（需同步修改 DATA_FILE 路径指向 data/）
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
│   │   └── edit.html      # 编辑记录（需添加 bank_name 字段）
│   └── statistics/
│       └── index.html     # 统计分析
│
├── data/                   # 数据目录
│   └── finance_data.json
│
└── tests/                  # 测试（使用 pytest）
    ├── test_services.py
    └── test_routes.py
```

### 4.2 路由清理

当前代码存在**两条冲突的赎回路径**，必须统一：

| 路径 | 当前行为 | 处理方式 |
|------|----------|----------|
| `/add` type=redeem | 创建独立赎回记录 ✅ | 保留并增强 |
| `/redeem` | 原地修改 purchase.amount ❌ | **删除此路由及对应模板** |

统一策略：所有赎回操作通过 `POST /add` 提交创建独立的 redeem 记录。删除 `/redeem` 路由和 `templates/redeem.html`。

### 4.3 依赖清单
```
flask>=3.0.0
openpyxl>=3.1.0
pytest>=7.0.0          # 测试框架
```

⚠️ **注意**：当前 `requirements.txt` 错误地列出了 `uuid` 和 `datetime`——这俩是 Python 标准库，pip 安装同名包会装错。需清理为以上条目。

### 4.4 核心代码示例

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
        
        # 持有中本金 = 总投入 - 已赎回本金
        holding_principal = total_invested - total_redeemed
        
        # 总资产 = 持有中本金 + 累计已到账收益
        total_assets = holding_principal + total_profit if holding_principal > 0 else total_profit
        
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
            'holding_principal': holding_principal,   # 持有中本金
            'total_assets': round(total_assets, 2),   # 总资产
            'total_profit': round(total_profit, 2),
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
        """按产品统计收益（从购买记录反查产品名，避免依赖冗余字段）"""
        product_profits = defaultdict(float)
        product_info = {}
        
        for r in self.redeems:
            # 从关联的购买记录获取产品名，而非依赖 r.get('product_name')
            purchase = self._find_purchase(r['purchase_record_id'])
            if not purchase:
                continue
            product_name = purchase['product_name']
            product_profits[product_name] += r.get('actual_profit', 0)
            
            if product_name not in product_info:
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
                'days': info['days'],
                'sort_by_rate': round(info['rate'], 2)  # 支持按年化收益率排序
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

> 当前代码功能约 80% 已完成，主要工作是前端重构 + 统计增强 + 路由清理 + 测试。

### 5.1 阶段划分

| 阶段 | 时间 | 内容 | 交付物 |
|------|------|------|--------|
| 阶段一 | 2天 | 基础架构+路由清理 | 目录结构、删除 `/redeem` 路由、数据迁移 |
| 阶段二 | 3天 | 核心功能重构 | 买卖关联卡片式展示、表单优化（补 bank_name） |
| 阶段三 | 3天 | 仪表盘 | 四大指标卡片、到期提醒、持有列表、最近赎回 |
| 阶段四 | 2天 | 统计分析增强 | 月度趋势图、收益/银行分布图、排行榜、摘要 |
| 阶段五 | 1天 | 导出+测试 | Excel导出、pytest 基础测试 |
| **总计** | **11天（约2-3周）** | | |

### 5.2 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| M1 | 第2天 | 基础架构完成，路由清理完毕 |
| M2 | 第5天 | 核心功能可用，买卖关联展示上线 |
| M3 | 第8天 | 仪表盘完成 |
| M4 | 第10天 | 统计分析完成 |
| M5 | 第11天 | 全部完成，可上线 |

---

## 六、其他说明

### 6.1 CLI 入口处理

当前项目有 `main.py`（CLI 菜单界面）和 `finance_manager.py`（CLI 业务逻辑），使用整型 ID 而非 UUID。建议：

- **保留不变**：与 Web 端数据文件共用 `finance_data.json`，但各自独立操作
- **不主动重构 CLI**：家庭用户通常只用 Web 端，CLI 作为备用入口保持最小可维护状态
- 如需删除 CLI，需确认用户是否依赖 `main.py`

### 6.2 数据迁移脚本要点

迁移脚本 `migrate_data.py` 需处理：

1. **数据目录迁移**：将根目录的 `finance_data.json` 复制到 `data/finance_data.json`
2. **补全 bank_name**：旧数据可能缺 `bank_name`，设为 `"未知银行"` 兜底
3. **清理错误依赖**：删除 `requirements.txt` 中的 `uuid` 和 `datetime`
4. **兼容性**：不改动现有数据结构，只增字段

### 6.3 编辑页面缺失字段

当前 `templates/edit.html` 只编辑实际收益，产品名称/金额为 `disabled`。在添加 `bank_name` 字段后，编辑页需要：

- 将 `bank_name` 加入可编辑字段（select 下拉框）
- 添加 `{{ record.get('bank_name', '未知银行') }}` 回显

### 6.4 快速开始

```bash
# 1. 修复 requirements.txt（删除 uuid/datetime，保留 flask+openpyxl+pytest）
# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据迁移（路径迁移 + 字段补全）
python migrate_data.py

# 4. 修改 app.py 中 DATA_FILE = 'data/finance_data.json'
# 5. 运行应用
python app.py

# 6. 访问
# http://localhost:5000
```

---

*家庭增强版方案 - 专注核心功能，增强仪表盘和统计分析*
