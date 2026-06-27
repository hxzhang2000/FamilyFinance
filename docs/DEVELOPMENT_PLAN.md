# FamilyFinance 完整开发方案

> **版本：v1.1** | 更新日期：2026-06-27
>
> ⚠️ **注意**：本方案包含企业级安全配置。如需精简版，见 [DEVELOPMENT_PLAN_LITE.md](DEVELOPMENT_PLAN_LITE.md)
>
> **可延后内容**：CSRF防护、Marshmallow验证、Docker安全配置、Nginx配置、环境变量管理

## 一、项目概述

### 1.1 项目背景
FamilyFinance 是一个家庭理财管理系统，用于记录和管理理财产品的购买与赎回。当前系统存在界面简陋、操作不便、买卖关联展示缺失等问题。

### 1.2 项目目标
1. **核心目标**：实现买卖记录的关联展示，体现投资生命周期
2. **体验目标**：现代化UI设计，提升操作便捷性
3. **功能目标**：增加智能分析、提醒、导出等实用功能
4. **技术目标**：代码重构，提升可维护性和扩展性

### 1.3 成功标准
- [ ] 买卖记录能按投资分组展示完整生命周期
- [ ] 界面响应式设计，移动端可用
- [ ] 支持数据导出（CSV/Excel）
- [ ] 到期提醒功能正常工作
- [ ] 所有现有数据平滑迁移

---

## 二、技术架构设计

### 2.1 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (Browser)                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  仪表盘  │  │ 记录管理 │  │ 统计分析 │  │  设置   │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask 后端 (app.py)                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  路由层  │  │ 业务层  │  │ 数据层  │  │ 工具层  │       │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据存储 (JSON File)                       │
│  ┌─────────────────┐  ┌─────────────────┐                   │
│  │ finance_data.json│  │ user_settings.json│                 │
│  └─────────────────┘  └─────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 目录结构（重构后）
```
FamilyFinance/
├── app.py                    # Flask 应用入口
├── config.py                 # 配置文件
├── constants.py              # 常量定义
├── requirements.txt          # 依赖管理
├── .env.example              # 环境变量模板
│
├── models/                   # 数据模型
│   ├── __init__.py
│   ├── record.py            # 记录模型（Purchase, Redeem）
│   ├── schemas.py           # Marshmallow 数据验证
│   └── settings.py          # 设置模型
│
├── services/                 # 业务逻辑层
│   ├── __init__.py
│   ├── record_service.py    # 记录业务逻辑
│   ├── statistics_service.py # 统计分析
│   ├── export_service.py    # 导出功能
│   └── reminder_service.py  # 提醒功能
│
├── utils/                    # 工具函数
│   ├── __init__.py
│   ├── validators.py        # 数据验证
│   ├── error_handlers.py    # 统一错误处理
│   ├── formatters.py        # 格式化工具
│   └── helpers.py           # 辅助函数
│
├── static/                   # 静态资源
│   ├── css/
│   │   ├── style.css        # 主样式
│   │   └── dashboard.css    # 仪表盘样式
│   ├── js/
│   │   ├── app.js           # 主脚本
│   │   ├── dashboard.js     # 仪表盘脚本
│   │   └── charts.js        # 图表脚本
│   └── images/              # 图片资源
│
├── templates/                # Jinja2 模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页/仪表盘
│   ├── records/
│   │   ├── list.html        # 记录列表
│   │   ├── add.html         # 添加记录
│   │   ├── edit.html        # 编辑记录
│   │   └── detail.html      # 记录详情
│   ├── statistics/
│   │   └── index.html       # 统计页面
│   ├── export/
│   │   └── index.html       # 导出页面
│   └── settings/
│       └── index.html       # 设置页面
│
├── data/                     # 数据目录
│   ├── finance_data.json    # 理财数据
│   ├── user_settings.json   # 用户设置
│   └── backups/             # 备份目录
│
├── tests/                    # 测试文件
│   ├── conftest.py          # 测试配置和 Fixtures
│   ├── factories.py         # 测试数据工厂
│   ├── test_models.py
│   ├── test_services.py
│   └── test_routes.py
│
└── docs/                     # 文档
    ├── API.md               # API 文档
    └── CHANGELOG.md         # 更新日志
```

### 2.3 技术栈选择

#### 前端
| 技术 | 用途 | 版本 |
|------|------|------|
| Bootstrap 5 | UI框架 | 5.3.x |
| Chart.js | 图表库 | 4.x |
| Flatpickr | 日期选择 | 4.6.x |
| DataTables | 表格增强 | 1.13.x |

#### 后端
| 技术 | 用途 | 版本 |
|------|------|------|
| Flask | Web框架 | 3.x |
| Flask-WTF | 表单验证 | 1.2.x |
| Marshmallow | 数据序列化 | 3.x |
| APScheduler | 任务调度 | 3.10.x |

---

## 三、数据结构设计

### 3.1 核心数据模型

#### 3.1.1 购买记录 (Purchase Record)
```json
{
  "id": "uuid-string",
  "type": "purchase",
  
  // 基本信息
  "product_name": "产品名称",
  "amount": 100000.0,
  "annual_rate": 0.0474,
  "duration": 90,
  "purchase_date": "2025-01-09",
  "end_date": "2025-04-09",
  
  // 扩展信息（新增）
  "bank_name": "交通银行",
  "product_code": "2174567890",
  "risk_level": "medium",
  "category": "固定收益",
  "tags": ["稳健", "短期"],
  "notes": "首次购买",
  
  // 系统字段
  "created_at": "2025-01-09T10:30:00",
  "updated_at": "2025-01-09T10:30:00",
  "deleted": false,
  "deleted_at": null
}
```

#### 3.1.2 赎回记录 (Redeem Record)
```json
{
  "id": "uuid-string",
  "type": "redeem",
  "purchase_record_id": "关联的购买记录ID",
  
  // 赎回信息
  "redeem_amount": 100000.0,
  "redeem_date": "2025-04-17",
  "actual_profit": 511.0,
  "profit_calc": "manual",
  
  // 扩展信息（新增）
  "redeem_type": "maturity",
  "redeem_reason": "到期自动赎回",
  "fees": 0.0,
  "tax": 0.0,
  "net_profit": 511.0,
  "settlement_date": "2025-04-18",
  "transaction_id": "TXN20250417001",
  
  // 系统字段
  "created_at": "2025-04-17T09:00:00",
  "updated_at": "2025-04-17T09:00:00",
  "deleted": false,
  "deleted_at": null
}
```

#### 3.1.3 用户设置 (User Settings)
```json
{
  "display": {
    "default_view": "grouped",
    "items_per_page": 20,
    "date_format": "YYYY-MM-DD",
    "currency_symbol": "元"
  },
  "notifications": {
    "enabled": true,
    "maturity_reminder_days": 3,
    "browser_notifications": true
  },
  "export": {
    "default_format": "xlsx",
    "include_headers": true
  },
  "auto_reinvest": {
    "enabled": false,
    "default_action": "ask"
  }
}
```

### 3.2 数据关系图
```
┌──────────────────┐       ┌──────────────────┐
│  Purchase Record │       │  Redeem Record   │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │◄──────│ purchase_record_id│
│ product_name     │       │ id (PK)          │
│ amount           │       │ redeem_amount    │
│ annual_rate      │       │ redeem_date      │
│ duration         │       │ actual_profit    │
│ purchase_date    │       │ profit_calc      │
│ end_date         │       │ redeem_type      │
│ bank_name        │       │ fees             │
│ risk_level       │       │ tax              │
│ deleted          │       │ deleted          │
│ ...              │       │ ...              │
└──────────────────┘       └──────────────────┘
        │
        │ 1:N
        ▼
┌──────────────────┐
│ Investment Group │ (逻辑分组)
├──────────────────┤
│ purchase         │
│ redeems[]        │
│ summary          │
└──────────────────┘
```

### 3.3 常量定义

**constants.py**
```python
"""项目常量定义"""

# 日期格式
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

# 记录类型
RECORD_TYPE_PURCHASE = 'purchase'
RECORD_TYPE_REDEEM = 'redeem'

# 投资状态
STATUS_HOLDING = 'holding'
STATUS_PARTIAL = 'partial'
STATUS_COMPLETED = 'completed'
STATUS_EXPIRED = 'expired'

# 风险等级
RISK_LOW = 'low'
RISK_MEDIUM = 'medium'
RISK_HIGH = 'high'

# 赎回类型
REDEEM_MATURITY = 'maturity'
REDEEM_EARLY = 'early'
REDEEM_PARTIAL = 'partial'

# 收益计算方式
PROFIT_CALC_AUTO = 'auto'
PROFIT_CALC_MANUAL = 'manual'

# 默认设置
DEFAULT_ITEMS_PER_PAGE = 20
DEFAULT_MATURITY_REMINDER_DAYS = 3

# 提醒相关
MATURITY_CHECK_DAYS = 30  # 检查未来30天到期的产品
```

### 3.4 数据验证层

**models/schemas.py**
```python
"""Marshmallow 数据验证 Schema"""
from marshmallow import Schema, fields, validate, post_load
from datetime import datetime
from typing import Dict, Any

from constants import (
    DATE_FORMAT, RECORD_TYPE_PURCHASE, RECORD_TYPE_REDEEM,
    RISK_LOW, RISK_MEDIUM, RISK_HIGH,
    REDEEM_MATURITY, REDEEM_EARLY, REDEEM_PARTIAL,
    PROFIT_CALC_AUTO, PROFIT_CALC_MANUAL
)


class PurchaseSchema(Schema):
    """购买记录验证 Schema"""
    id = fields.Str(load_default=None)
    type = fields.Str(validate=validate.Equal(RECORD_TYPE_PURCHASE))
    product_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    annual_rate = fields.Float(required=True, validate=validate.Range(min=0, max=1))
    duration = fields.Int(required=True, validate=validate.Range(min=1, max=36500))
    purchase_date = fields.Date(required=True, format=DATE_FORMAT)
    end_date = fields.Date(required=True, format=DATE_FORMAT)
    bank_name = fields.Str(load_default=None, validate=validate.Length(max=50))
    product_code = fields.Str(load_default=None, validate=validate.Length(max=50))
    risk_level = fields.Str(
        load_default=RISK_MEDIUM,
        validate=validate.OneOf([RISK_LOW, RISK_MEDIUM, RISK_HIGH])
    )
    category = fields.Str(load_default='固定收益', validate=validate.Length(max=50))
    tags = fields.List(fields.Str(), load_default=list)
    notes = fields.Str(load_default='', validate=validate.Length(max=500))
    created_at = fields.DateTime(load_default=None)
    updated_at = fields.DateTime(load_default=None)
    deleted = fields.Bool(load_default=False)
    deleted_at = fields.DateTime(load_default=None)


class RedeemSchema(Schema):
    """赎回记录验证 Schema"""
    id = fields.Str(load_default=None)
    type = fields.Str(validate=validate.Equal(RECORD_TYPE_REDEEM))
    purchase_record_id = fields.Str(required=True)
    redeem_amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    redeem_date = fields.Date(required=True, format=DATE_FORMAT)
    actual_profit = fields.Float(required=True)
    profit_calc = fields.Str(
        load_default=PROFIT_CALC_AUTO,
        validate=validate.OneOf([PROFIT_CALC_AUTO, PROFIT_CALC_MANUAL])
    )
    redeem_type = fields.Str(
        load_default=REDEEM_MATURITY,
        validate=validate.OneOf([REDEEM_MATURITY, REDEEM_EARLY, REDEEM_PARTIAL])
    )
    redeem_reason = fields.Str(load_default='', validate=validate.Length(max=200))
    fees = fields.Float(load_default=0.0, validate=validate.Range(min=0))
    tax = fields.Float(load_default=0.0, validate=validate.Range(min=0))
    net_profit = fields.Float(load_default=0.0)
    settlement_date = fields.Date(load_default=None, format=DATE_FORMAT)
    transaction_id = fields.Str(load_default=None, validate=validate.Length(max=50))
    created_at = fields.DateTime(load_default=None)
    updated_at = fields.DateTime(load_default=None)
    deleted = fields.Bool(load_default=False)
    deleted_at = fields.DateTime(load_default=None)


# Schema 实例
purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
redeem_schema = RedeemSchema()
redeems_schema = RedeemSchema(many=True)
```

### 3.5 统一错误处理

**utils/error_handlers.py**
```python
"""统一错误处理模块"""
from flask import jsonify
from typing import Tuple, Dict, Any


class AppError(Exception):
    """应用自定义异常基类"""
    def __init__(self, message: str, code: int = 400, details: Any = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppError):
    """资源未找到"""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f'{resource} 未找到: {resource_id}',
            code=404
        )


class ValidationError(AppError):
    """数据验证错误"""
    def __init__(self, message: str, details: Any = None):
        super().__init__(message=message, code=400, details=details)


class BusinessError(AppError):
    """业务逻辑错误"""
    def __init__(self, message: str, code: int = 400):
        super().__init__(message=message, code=code)


def register_error_handlers(app):
    """注册全局错误处理器"""
    
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError) -> Tuple[Dict, int]:
        response = {
            'success': False,
            'error': {
                'message': error.message,
                'code': error.code
            }
        }
        if error.details:
            response['error']['details'] = error.details
        return jsonify(response), error.code
    
    @app.errorhandler(404)
    def not_found(error) -> Tuple[Dict, int]:
        return jsonify({
            'success': False,
            'error': {
                'message': '资源未找到',
                'code': 404
            }
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error) -> Tuple[Dict, int]:
        return jsonify({
            'success': False,
            'error': {
                'message': '请求方法不允许',
                'code': 405
            }
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error) -> Tuple[Dict, int]:
        return jsonify({
            'success': False,
            'error': {
                'message': '服务器内部错误',
                'code': 500
            }
        }), 500
```

---

## 四、功能模块设计

### 4.1 模块一：仪表盘（Dashboard）

#### 4.1.1 功能描述
首页展示投资概览，包括关键指标、资产分布、即将到期提醒等。

#### 4.1.2 界面布局
```
┌─────────────────────────────────────────────────────────────────┐
│                        仪表盘                                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ 总资产   │  │ 持有中   │  │ 已赎回   │  │ 总收益   │           │
│  │ 500,000 │  │ 300,000 │  │ 200,000 │  │ 3,250  │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌─────────────────────────┐      │
│  │                         │  │                         │      │
│  │    收益趋势折线图        │  │    资产配置饼图          │      │
│  │                         │  │                         │      │
│  └─────────────────────────┘  └─────────────────────────┘      │
├─────────────────────────────────────────────────────────────────┤
│  即将到期产品                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 交银理财90天  │ 2026-07-01 │ 100,000元 │ 预计收益 1,185元│   │
│  │ 民生安心存    │ 2026-07-15 │ 100,000元 │ 预计收益 2,200元│   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.1.3 后端接口
```python
@app.route('/api/dashboard')
def get_dashboard_data():
    """获取仪表盘数据"""
    return {
        "summary": {
            "total_assets": 500000,
            "holding": 300000,
            "redeemed": 200000,
            "total_profit": 3250,
            "avg_rate": 3.85
        },
        "upcoming_maturities": [...],
        "asset_allocation": {...},
        "profit_trend": {...}
    }
```

### 4.2 模块二：记录管理（Records）

#### 4.2.1 功能描述
管理理财产品的购买和赎回记录，支持分组视图和平铺视图。

#### 4.2.2 分组视图设计
```
┌─────────────────────────────────────────────────────────────────┐
│  筛选: [全部] [持有中] [已完结] [部分赎回]    搜索: [________]   │
├─────────────────────────────────────────────────────────────────┤
│  ▼ 交银理财灵动慧利6号90天                                       │
│    金额: 100,000元 │ 年化: 4.74% │ 期限: 90天 │ 状态: ● 已完结   │
│    ┌───────────────────────────────────────────────────────────┐│
│    │ 买入 │ 2025-01-09 │ 100,000元 │ 到期日: 2025-04-09       ││
│    │ 赎回 │ 2025-04-17 │ 100,000元 │ 收益: 511元 │ 收益率: 5.04%││
│    └───────────────────────────────────────────────────────────┘│
│    汇总: 总收益 511元 │ 真实年化 5.04%                           │
├─────────────────────────────────────────────────────────────────┤
│  ▼ 民生安心存                                                     │
│    金额: 100,000元 │ 年化: 2.20% │ 期限: 1095天 │ 状态: ● 持有中 │
│    ┌───────────────────────────────────────────────────────────┐│
│    │ 买入 │ 2024-09-23 │ 100,000元 │ 到期日: 2027-09-23       ││
│    └───────────────────────────────────────────────────────────┘│
│    [赎回] [编辑] [删除]                                          │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.2.3 后端接口
```python
@app.route('/api/records')
def get_records():
    """获取记录列表（支持分组）"""
    view_type = request.args.get('view', 'grouped')
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('q', '')
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 20)
    
    # 返回分组或平铺数据
    if view_type == 'grouped':
        return get_grouped_records(status_filter, search_query, page, per_page)
    else:
        return get_flat_records(status_filter, search_query, page, per_page)

@app.route('/api/records/<record_id>')
def get_record_detail(record_id):
    """获取单条记录详情（包含关联记录）"""
    # 返回购买记录及其所有赎回记录
    return get_record_with_redeems(record_id)
```

### 4.3 模块三：添加/编辑记录

#### 4.3.1 购买记录表单
```
┌─────────────────────────────────────────────────────────────────┐
│                        添加购买记录                              │
├─────────────────────────────────────────────────────────────────┤
│  基本信息                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 产品名称: [交银理财灵动慧利6号90天          ]               │   │
│  │ 银行/机构: [交通银行                        ]               │   │
│  │ 产品代码: [2174567890                      ]               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  投资信息                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 投资金额: [100,000    ] 元                               │   │
│  │ 年化利率: [4.74       ] %                                │   │
│  │ 投资期限: [90         ] 天                               │   │
│  │ 购买日期: [2025-01-09 ]                                  │   │
│  │ 到期日期: [2025-04-09 ] (自动计算)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  分类信息                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 风险等级: ○低风险  ●中风险  ○高风险                        │   │
│  │ 产品分类: [固定收益    ▼]                                 │   │
│  │ 标签:     [稳健] [短期] [+ 添加]                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  备注: [首次购买该产品                                    ]      │
│                                                                 │
│  [取消]  [保存并继续添加]  [保存]                                │
└─────────────────────────────────────────────────────────────────┘
```

#### 4.3.2 赎回记录表单
```
┌─────────────────────────────────────────────────────────────────┐
│                        添加赎回记录                              │
├─────────────────────────────────────────────────────────────────┤
│  选择购买记录:                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ▼ 交银理财灵动慧利6号90天                                 │   │
│  │   金额: 100,000元 │ 购买日: 2025-01-09 │ 剩余: 100,000元 │   │
│  │ ○ 民生安心存                                              │   │
│  │   金额: 100,000元 │ 购买日: 2024-09-23 │ 剩余: 100,000元 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  赎回信息                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 赎回金额:   [100,000    ] 元 (最大: 100,000元)            │   │
│  │ 赎回日期:   [2025-04-17 ]                                │   │
│  │ 赎回类型:   ○到期赎回  ○提前赎回  ○部分赎回                │   │
│  │ 赎回原因:   [到期自动赎回                        ]        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  收益计算                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 计算方式: ●自动计算  ○手动输入                             │   │
│  │                                                         │   │
│  │ 预计收益: 1,185.00 元 (自动计算)                          │   │
│  │ 手续费:   [0        ] 元                                 │   │
│  │ 税费:     [0        ] 元                                 │   │
│  │ 净收益:   1,185.00 元                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [取消]  [保存]                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 模块四：统计分析

#### 4.4.1 功能描述
提供多维度的投资数据分析和可视化图表。

#### 4.4.2 图表类型
1. **收益趋势图**：折线图展示月度/年度收益变化
2. **资产配置图**：饼图展示按银行/产品类型的分布
3. **收益率分布图**：柱状图展示不同收益率区间的投资数量
4. **持有期分析图**：散点图分析持有期与收益率的关系
5. **实际vs预期对比图**：柱状图对比预期收益和实际收益

#### 4.4.3 后端接口
```python
@app.route('/api/statistics')
def get_statistics():
    """获取统计数据"""
    return {
        "monthly_profits": [...],
        "yearly_profits": [...],
        "asset_allocation": {...},
        "rate_distribution": {...],
        "holding_period_analysis": {...}
    }
```

### 4.5 模块五：数据导出

#### 4.5.1 功能描述
支持将数据导出为 CSV、Excel、PDF 等格式。

#### 4.5.2 导出选项
```
┌─────────────────────────────────────────────────────────────────┐
│                        数据导出                                  │
├─────────────────────────────────────────────────────────────────┤
│  导出格式:                                                       │
│  ● Excel (.xlsx)  ○ CSV  ○ PDF  ○ JSON                          │
│                                                                 │
│  导出范围:                                                       │
│  ● 全部记录  ○仅持有中  ○仅已完结  ○自定义日期范围                 │
│                                                                 │
│  日期范围: [2025-01-01] 至 [2025-12-31]                          │
│                                                                 │
│  包含字段:                                                       │
│  ☑ 产品名称  ☑ 金额  ☑ 收益率  ☑ 日期                           │
│  ☑ 银行  ☑ 风险等级  ☑ 备注                                     │
│                                                                 │
│  [取消]  [导出]                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.6 模块六：到期提醒

#### 4.6.1 功能描述
提前提醒即将到期的理财产品，支持浏览器通知。

#### 4.6.2 提醒逻辑
```python
class ReminderService:
    def check_maturities(self):
        """检查即将到期的产品"""
        settings = load_settings()
        reminder_days = settings['notifications']['maturity_reminder_days']
        
        upcoming = []
        for record in get_holding_records():
            days_until_maturity = (record['end_date'] - today).days
            if 0 < days_until_maturity <= reminder_days:
                upcoming.append({
                    'record': record,
                    'days_remaining': days_until_maturity
                })
        
        return upcoming
```

#### 4.6.3 前端通知
```javascript
// 浏览器通知
function sendNotification(record) {
    if (Notification.permission === 'granted') {
        new Notification('理财到期提醒', {
            body: `${record.product_name} 将于 ${record.end_date} 到期`,
            icon: '/static/images/icon.png'
        });
    }
}
```

### 4.7 模块七：设置管理

#### 4.7.1 功能描述
管理用户偏好设置，包括显示、通知、导出等配置。

#### 4.7.2 设置界面
```
┌─────────────────────────────────────────────────────────────────┐
│                        设置                                      │
├─────────────────────────────────────────────────────────────────┤
│  显示设置                                                        │
│  ├─ 默认视图:      [分组视图 ▼]                                  │
│  ├─ 每页显示:      [20 ▼] 条                                     │
│  ├─ 日期格式:      [YYYY-MM-DD ▼]                                │
│  └─ 货币符号:      [元]                                          │
│                                                                 │
│  通知设置                                                        │
│  ├─ 启用通知:      [✓]                                           │
│  ├─ 提前提醒:      [3 ▼] 天                                      │
│  └─ 浏览器通知:    [✓]                                           │
│                                                                 │
│  导出设置                                                        │
│  ├─ 默认格式:      [Excel ▼]                                     │
│  └─ 包含表头:      [✓]                                           │
│                                                                 │
│  [重置默认]  [保存]                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、开发阶段

### 5.1 阶段划分

#### 阶段一：基础架构（第1-2周）
**目标**：搭建项目骨架，完成核心数据结构

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 1.1 | 项目目录重构 | 1天 |
| 1.2 | 数据模型设计与实现 | 2天 |
| 1.3 | 基础路由框架 | 1天 |
| 1.4 | 模板继承结构 | 1天 |
| 1.5 | Bootstrap 集成 | 1天 |
| 1.6 | 数据迁移脚本 | 2天 |
| 1.7 | 单元测试框架 | 1天 |

**交付物**：
- [x] 重构后的项目目录
- [x] 数据模型代码
- [x] 基础路由和模板
- [x] 数据迁移脚本

#### 阶段二：核心功能（第3-4周）
**目标**：实现买卖关联展示和基础CRUD

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 2.1 | 记录分组逻辑 | 2天 |
| 2.2 | 分组视图模板 | 2天 |
| 2.3 | 添加购买记录表单 | 1天 |
| 2.4 | 添加赎回记录表单 | 1天 |
| 2.5 | 编辑记录功能 | 1天 |
| 2.6 | 删除记录功能（含保护） | 1天 |
| 2.7 | 搜索筛选功能 | 2天 |

**交付物**：
- [x] 分组视图页面
- [x] 完整的CRUD功能
- [x] 搜索筛选功能

#### 阶段三：仪表盘（第5周）
**目标**：实现首页仪表盘

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 3.1 | 仪表盘数据接口 | 1天 |
| 3.2 | 指标卡片组件 | 0.5天 |
| 3.3 | 收益趋势图表 | 1天 |
| 3.4 | 资产配置图表 | 1天 |
| 3.5 | 即将到期提醒 | 0.5天 |

**交付物**：
- [x] 仪表盘页面
- [x] 图表可视化

#### 阶段四：统计分析（第6周）
**目标**：实现统计分析功能

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 4.1 | 统计数据接口 | 1天 |
| 4.2 | 月度/年度收益图表 | 1天 |
| 4.3 | 收益率分布图 | 1天 |
| 4.4 | 产品对比分析 | 1天 |
| 4.5 | 持有期分析 | 1天 |

**交付物**：
- [x] 统计分析页面
- [x] 多维度图表

#### 阶段五：数据导出（第7周）
**目标**：实现数据导出功能

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 5.1 | CSV导出 | 1天 |
| 5.2 | Excel导出 | 1天 |
| 5.3 | PDF导出 | 2天 |
| 5.4 | 导出设置页面 | 1天 |

**交付物**：
- [x] 数据导出功能
- [x] 导出设置页面

#### 阶段六：到期提醒（第8周）
**目标**：实现到期提醒功能

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 6.1 | 提醒服务逻辑 | 1天 |
| 6.2 | 浏览器通知 | 1天 |
| 6.3 | 提醒设置页面 | 1天 |
| 6.4 | 提醒列表页面 | 1天 |
| 6.5 | 定时任务配置 | 1天 |

**交付物**：
- [x] 到期提醒功能
- [x] 提醒设置页面

#### 阶段七：设置与优化（第9周）
**目标**：实现设置功能，优化用户体验

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 7.1 | 设置页面开发 | 1天 |
| 7.2 | 设置数据持久化 | 0.5天 |
| 7.3 | 响应式适配优化 | 1天 |
| 7.4 | 表单验证优化 | 1天 |
| 7.5 | 错误处理优化 | 0.5天 |

**交付物**：
- [x] 设置管理功能
- [x] 响应式设计
- [x] 表单验证

#### 阶段八：测试与部署（第10周）
**目标**：完成测试，准备部署

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| 8.1 | 单元测试 | 2天 |
| 8.2 | 集成测试 | 1天 |
| 8.3 | 用户验收测试 | 1天 |
| 8.4 | 文档编写 | 1天 |
| 8.5 | 部署准备 | 1天 |

**交付物**：
- [x] 完整的测试用例
- [x] 用户文档
- [x] 部署文档

### 5.2 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| M1 | 第2周末 | 基础架构完成，可运行 |
| M2 | 第4周末 | 核心功能完成，可使用 |
| M3 | 第6周末 | 分析功能完成 |
| M4 | 第8周末 | 全部功能完成 |
| M5 | 第10周末 | 测试完成，可部署 |

---

## 六、详细开发任务

### 6.1 阶段一：基础架构

#### 任务1.1：项目目录重构
```
创建新的目录结构：
├── models/
├── services/
├── utils/
├── static/css/
├── static/js/
├── templates/records/
├── templates/statistics/
├── templates/export/
├── templates/settings/
├── data/
├── tests/
└── docs/
```

#### 任务1.2：数据模型设计与实现

**models/record.py**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class PurchaseRecord:
    id: str
    product_name: str
    amount: float
    annual_rate: float
    duration: int
    purchase_date: str
    end_date: str
    bank_name: Optional[str] = None
    product_code: Optional[str] = None
    risk_level: str = "medium"
    category: str = "固定收益"
    tags: List[str] = None
    notes: str = ""
    created_at: str = None
    updated_at: str = None

@dataclass
class RedeemRecord:
    id: str
    purchase_record_id: str
    redeem_amount: float
    redeem_date: str
    actual_profit: float
    profit_calc: str = "auto"
    redeem_type: str = "maturity"
    redeem_reason: str = ""
    fees: float = 0.0
    tax: float = 0.0
    net_profit: float = 0.0
    settlement_date: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: str = None
    updated_at: str = None

@dataclass
class InvestmentGroup:
    purchase: PurchaseRecord
    redeems: List[RedeemRecord]
    total_redeemed: float
    remaining: float
    total_profit: float
    real_rate: float
    status: str  # holding, partial, completed, expired
```

#### 任务1.3：基础路由框架

**app.py**
```python
import os
from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

from models.record import PurchaseRecord, RedeemRecord
from services.record_service import RecordService
from utils.error_handlers import register_error_handlers

# 加载环境变量
load_dotenv()

# 创建 Flask 应用
app = Flask(__name__)

# 安全配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # CSRF token 有效期1小时

# 初始化 CSRF 保护
csrf = CSRFProtect(app)

# 注册错误处理器
register_error_handlers(app)

# 初始化服务
record_service = RecordService()


@app.route('/')
def index():
    """首页/仪表盘"""
    return render_template('index.html')


@app.route('/records')
def records_list():
    """记录列表"""
    return render_template('records/list.html')


@app.route('/records/add', methods=['GET', 'POST'])
def add_record():
    """添加记录"""
    return render_template('records/add.html')


@app.route('/statistics')
def statistics():
    """统计分析"""
    return render_template('statistics/index.html')


@app.route('/export')
def export():
    """数据导出"""
    return render_template('export/index.html')


@app.route('/settings')
def settings():
    """设置"""
    return render_template('settings/index.html')


# API 路由需要排除 CSRF 检验（使用 token 认证）
@csrf.exempt
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(path):
    """API 路由代理"""
    # API 路由的具体实现
    pass


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
```

**.env.example**
```bash
# Flask 配置
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_DEBUG=False
PORT=5000

# 数据目录
DATA_DIR=data

# 日志级别
LOG_LEVEL=INFO
```

#### 任务1.4：模板继承结构

**templates/base.html**
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>家庭理财管理系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">家庭理财管理系统</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/"><i class="bi bi-speedometer2"></i> 仪表盘</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/records"><i class="bi bi-list-ul"></i> 记录管理</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/statistics"><i class="bi bi-graph-up"></i> 统计分析</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/export"><i class="bi bi-download"></i> 数据导出</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/settings"><i class="bi bi-gear"></i> 设置</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer class="mt-5 py-3 bg-light">
        <div class="container text-center text-muted">
            家庭理财管理系统 © 2026
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### 任务1.6：数据迁移脚本

**migrate_data.py**
```python
import json
from datetime import datetime

def migrate_v1_to_v2(input_file, output_file):
    """迁移v1数据到v2格式"""
    with open(input_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    new_data = []
    for record in old_data:
        new_record = record.copy()
        
        # 添加新字段
        new_record['bank_name'] = None
        new_record['product_code'] = None
        new_record['risk_level'] = 'medium'
        new_record['category'] = '固定收益'
        new_record['tags'] = []
        new_record['notes'] = ''
        new_record['created_at'] = datetime.now().isoformat()
        new_record['updated_at'] = datetime.now().isoformat()
        
        # 赎回记录额外字段
        if record['type'] == 'redeem':
            new_record['redeem_type'] = 'maturity'
            new_record['redeem_reason'] = ''
            new_record['fees'] = 0.0
            new_record['tax'] = 0.0
            new_record['net_profit'] = record.get('actual_profit', 0)
            new_record['settlement_date'] = None
            new_record['transaction_id'] = None
        
        new_data.append(new_record)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    print(f"迁移完成: {len(new_data)} 条记录")

if __name__ == '__main__':
    migrate_v1_to_v2('finance_data.json', 'data/finance_data.json')
```

### 6.2 阶段二：核心功能

#### 任务2.1：记录分组逻辑

**services/record_service.py**
```python
"""记录业务逻辑服务"""
import json
from datetime import datetime
from typing import List, Dict, Optional, Any

from constants import (
    DATE_FORMAT, DATETIME_FORMAT,
    RECORD_TYPE_PURCHASE, RECORD_TYPE_REDEEM,
    STATUS_HOLDING, STATUS_PARTIAL, STATUS_COMPLETED, STATUS_EXPIRED,
    DEFAULT_ITEMS_PER_PAGE
)
from utils.error_handlers import NotFoundError, ValidationError, BusinessError


class RecordService:
    """记录服务类"""
    
    def __init__(self, data_file: str = 'data/finance_data.json'):
        self.data_file = data_file
        self.records: List[Dict[str, Any]] = self._load_data()
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 过滤已删除的记录
                return [r for r in data if not r.get('deleted', False)]
        except FileNotFoundError:
            return []
    
    def _save_data(self) -> None:
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, indent=2, ensure_ascii=False)
    
    def get_grouped_records(
        self,
        status_filter: Optional[str] = None,
        search_query: Optional[str] = None,
        page: int = 1,
        per_page: int = DEFAULT_ITEMS_PER_PAGE
    ) -> Dict[str, Any]:
        """获取分组记录"""
        purchases = [r for r in self.records if r['type'] == RECORD_TYPE_PURCHASE]
        redeems = [r for r in self.records if r['type'] == RECORD_TYPE_REDEEM]
        
        groups = []
        for purchase in purchases:
            # 获取关联的赎回记录
            related_redeems = [
                r for r in redeems 
                if r['purchase_record_id'] == purchase['id']
            ]
            
            # 计算汇总信息
            total_redeemed = sum(r['redeem_amount'] for r in related_redeems)
            total_profit = sum(r.get('actual_profit', 0) for r in related_redeems)
            remaining = purchase['amount'] - total_redeemed
            
            # 计算真实年化收益率
            real_rate = self._calculate_real_rate(purchase, related_redeems)
            
            # 确定状态
            status = self._determine_status(purchase, remaining)
            
            # 应用筛选
            if status_filter and status != status_filter:
                continue
            
            # 应用搜索
            if search_query:
                search_lower = search_query.lower()
                if (search_lower not in purchase['product_name'].lower() and
                    search_lower not in (purchase.get('bank_name') or '').lower()):
                    continue
            
            groups.append({
                'purchase': purchase,
                'redeems': related_redeems,
                'summary': {
                    'total_redeemed': total_redeemed,
                    'remaining': remaining,
                    'total_profit': total_profit,
                    'real_rate': real_rate,
                    'status': status
                }
            })
        
        # 分页
        total = len(groups)
        total_pages = (total + per_page - 1) // per_page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_groups = groups[start:end]
        
        return {
            'groups': paginated_groups,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }
    
    def delete_record(self, record_id: str, soft_delete: bool = True) -> bool:
        """删除记录（支持软删除）"""
        record = next((r for r in self.records if r['id'] == record_id), None)
        if not record:
            raise NotFoundError('记录', record_id)
        
        if soft_delete:
            # 软删除
            record['deleted'] = True
            record['deleted_at'] = datetime.now().strftime(DATETIME_FORMAT)
            self._save_data()
        else:
            # 硬删除
            self.records = [r for r in self.records if r['id'] != record_id]
            # 同时删除关联的赎回记录
            if record['type'] == RECORD_TYPE_PURCHASE:
                self.records = [
                    r for r in self.records 
                    if r.get('purchase_record_id') != record_id
                ]
            self._save_data()
        
        return True
    
    def restore_record(self, record_id: str) -> bool:
        """恢复已软删除的记录"""
        # 从完整数据中查找（包括已删除的）
        all_records = self._load_all_data()
        record = next((r for r in all_records if r['id'] == record_id), None)
        
        if not record:
            raise NotFoundError('记录', record_id)
        
        if not record.get('deleted', False):
            raise BusinessError('记录未被删除，无需恢复')
        
        record['deleted'] = False
        record['deleted_at'] = None
        
        # 保存完整数据
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(all_records, f, indent=2, ensure_ascii=False)
        
        # 重新加载
        self.records = [r for r in all_records if not r.get('deleted', False)]
        return True
    
    def _load_all_data(self) -> List[Dict[str, Any]]:
        """加载所有数据（包括已删除的）"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _calculate_real_rate(
        self,
        purchase: Dict[str, Any],
        redeems: List[Dict[str, Any]]
    ) -> float:
        """计算真实年化收益率"""
        if not redeems:
            return 0.0
        
        total_profit = sum(r.get('actual_profit', 0) for r in redeems)
        total_amount = sum(r['redeem_amount'] for r in redeems)
        
        if total_amount <= 0:
            return 0.0
        
        # 加权平均持有天数
        total_days = sum(
            r['redeem_amount'] * self._days_between(
                purchase['purchase_date'], 
                r['redeem_date']
            )
            for r in redeems
        )
        avg_days = total_days / total_amount if total_amount > 0 else 0
        
        if avg_days <= 0:
            return 0.0
        
        return (total_profit / total_amount) * (365 / avg_days) * 100
    
    def _determine_status(
        self,
        purchase: Dict[str, Any],
        remaining: float
    ) -> str:
        """确定投资状态"""
        if remaining <= 0:
            return STATUS_COMPLETED
        elif remaining < purchase['amount']:
            return STATUS_PARTIAL
        elif datetime.strptime(purchase['end_date'], DATE_FORMAT) < datetime.now():
            return STATUS_EXPIRED
        else:
            return STATUS_HOLDING
    
    def _days_between(self, date1_str: str, date2_str: str) -> int:
        """计算两个日期之间的天数"""
        date1 = datetime.strptime(date1_str, DATE_FORMAT)
        date2 = datetime.strptime(date2_str, DATE_FORMAT)
        return (date2 - date1).days
```

#### 任务2.2：分组视图模板

**templates/records/list.html**
```html
{% extends "base.html" %}

{% block content %}
<div class="row mb-4">
    <div class="col-md-6">
        <h2>记录管理</h2>
    </div>
    <div class="col-md-6 text-end">
        <a href="/records/add" class="btn btn-primary">
            <i class="bi bi-plus-circle"></i> 添加记录
        </a>
    </div>
</div>

<!-- 筛选栏 -->
<div class="card mb-4">
    <div class="card-body">
        <form class="row g-3" id="filterForm">
            <div class="col-md-3">
                <select class="form-select" name="status" id="statusFilter">
                    <option value="all">全部状态</option>
                    <option value="holding">持有中</option>
                    <option value="partial">部分赎回</option>
                    <option value="completed">已完结</option>
                    <option value="expired">已到期</option>
                </select>
            </div>
            <div class="col-md-6">
                <input type="text" class="form-control" name="q" id="searchInput" 
                       placeholder="搜索产品名称、银行...">
            </div>
            <div class="col-md-3">
                <button type="submit" class="btn btn-outline-primary w-100">
                    <i class="bi bi-search"></i> 搜索
                </button>
            </div>
        </form>
    </div>
</div>

<!-- 记录列表 -->
<div id="recordsList">
    {% for group in groups %}
    <div class="card mb-3 record-group" data-status="{{ group.summary.status }}">
        <div class="card-header d-flex justify-content-between align-items-center"
             data-bs-toggle="collapse" href="#group{{ loop.index }}" role="button">
            <div>
                <h5 class="mb-0">
                    <i class="bi bi-box"></i> {{ group.purchase.product_name }}
                </h5>
                <small class="text-muted">
                    {{ group.purchase.bank_name or '未知银行' }} | 
                    金额: {{ "%.2f"|format(group.purchase.amount) }}元 | 
                    年化: {{ "%.2f"|format(group.purchase.annual_rate * 100) }}% | 
                    期限: {{ group.purchase.duration }}天
                </small>
            </div>
            <div class="text-end">
                <span class="badge bg-{{ 'success' if group.summary.status == 'completed' else 
                                          'warning' if group.summary.status == 'partial' else
                                          'info' if group.summary.status == 'holding' else 'secondary' }}">
                    {{ '已完结' if group.summary.status == 'completed' else
                       '部分赎回' if group.summary.status == 'partial' else
                       '持有中' if group.summary.status == 'holding' else '已到期' }}
                </span>
            </div>
        </div>
        
        <div class="collapse show" id="group{{ loop.index }}">
            <div class="card-body">
                <!-- 买入记录 -->
                <div class="mb-3">
                    <div class="d-flex align-items-center mb-2">
                        <span class="badge bg-primary me-2">买入</span>
                        <span>{{ group.purchase.purchase_date }}</span>
                    </div>
                    <div class="row">
                        <div class="col-md-4">
                            <small class="text-muted">金额</small>
                            <div>{{ "%.2f"|format(group.purchase.amount) }}元</div>
                        </div>
                        <div class="col-md-4">
                            <small class="text-muted">到期日</small>
                            <div>{{ group.purchase.end_date }}</div>
                        </div>
                        <div class="col-md-4">
                            <small class="text-muted">预计收益</small>
                            <div>{{ "%.2f"|format(group.purchase.amount * group.purchase.annual_rate * group.purchase.duration / 365) }}元</div>
                        </div>
                    </div>
                </div>
                
                <!-- 赎回记录 -->
                {% for redeem in group.redeems %}
                <div class="mb-3 {% if not loop.last %}border-bottom pb-3{% endif %}">
                    <div class="d-flex align-items-center mb-2">
                        <span class="badge bg-warning me-2">赎回</span>
                        <span>{{ redeem.redeem_date }}</span>
                    </div>
                    <div class="row">
                        <div class="col-md-3">
                            <small class="text-muted">赎回金额</small>
                            <div>{{ "%.2f"|format(redeem.redeem_amount) }}元</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">实际收益</small>
                            <div>{{ "%.2f"|format(redeem.actual_profit) }}元</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">收益率</small>
                            <div>{{ "%.2f"|format(redeem.actual_profit / redeem.redeem_amount * 365 / group.purchase.duration * 100) }}%</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">类型</small>
                            <div>{{ '到期赎回' if redeem.redeem_type == 'maturity' else '提前赎回' if redeem.redeem_type == 'early' else '部分赎回' }}</div>
                        </div>
                    </div>
                </div>
                {% endfor %}
                
                <!-- 汇总信息 -->
                <div class="alert alert-light mb-0">
                    <div class="row">
                        <div class="col-md-3">
                            <small class="text-muted">已赎回</small>
                            <div>{{ "%.2f"|format(group.summary.total_redeemed) }}元</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">剩余金额</small>
                            <div>{{ "%.2f"|format(group.summary.remaining) }}元</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">总收益</small>
                            <div>{{ "%.2f"|format(group.summary.total_profit) }}元</div>
                        </div>
                        <div class="col-md-3">
                            <small class="text-muted">真实年化</small>
                            <div>{{ "%.2f"|format(group.summary.real_rate) }}%</div>
                        </div>
                    </div>
                </div>
                
                <!-- 操作按钮 -->
                {% if group.summary.status == 'holding' or group.summary.status == 'partial' %}
                <div class="mt-3">
                    <a href="/records/add?purchase_id={{ group.purchase.id }}&type=redeem" 
                       class="btn btn-sm btn-warning">
                        <i class="bi bi-cash-stack"></i> 赎回
                    </a>
                    <a href="/records/edit/{{ group.purchase.id }}" 
                       class="btn btn-sm btn-outline-primary">
                        <i class="bi bi-pencil"></i> 编辑
                    </a>
                    <button class="btn btn-sm btn-outline-danger" 
                            onclick="deleteRecord('{{ group.purchase.id }}')">
                        <i class="bi bi-trash"></i> 删除
                    </button>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    {% endfor %}
</div>

<!-- 分页 -->
{% if total_pages > 1 %}
<nav>
    <ul class="pagination justify-content-center">
        {% for p in range(1, total_pages + 1) %}
        <li class="page-item {% if p == current_page %}active{% endif %}">
            <a class="page-link" href="?page={{ p }}">{{ p }}</a>
        </li>
        {% endfor %}
    </ul>
</nav>
{% endif %}
{% endblock %}

{% block extra_js %}
<script>
// 筛选表单提交
document.getElementById('filterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const status = document.getElementById('statusFilter').value;
    const query = document.getElementById('searchInput').value;
    window.location.href = `/records?status=${status}&q=${encodeURIComponent(query)}`;
});

// 删除记录
function deleteRecord(id) {
    if (confirm('确定要删除这条记录吗？如果有赎回记录，将一并删除。')) {
        fetch(`/api/records/${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    alert('删除失败: ' + data.message);
                }
            });
    }
}
</script>
{% endblock %}
```

### 6.3 阶段三：仪表盘

#### 任务3.1：仪表盘数据接口

```python
@app.route('/api/dashboard')
def get_dashboard_data():
    """获取仪表盘数据"""
    from datetime import datetime, timedelta
    
    records = load_data()
    purchases = [r for r in records if r['type'] == 'purchase']
    redeems = [r for r in records if r['type'] == 'redeem']
    
    # 计算汇总指标
    total_assets = sum(r['amount'] for r in purchases)
    total_redeemed = sum(r['redeem_amount'] for r in redeems)
    total_profit = sum(r.get('actual_profit', 0) for r in redeems)
    holding_assets = total_assets - total_redeemed
    
    # 即将到期产品（未来30天）
    today = datetime.now()
    upcoming = []
    for p in purchases:
        end_date = datetime.strptime(p['end_date'], '%Y-%m-%d')
        days_remaining = (end_date - today).days
        if 0 < days_remaining <= 30:
            # 检查是否已全部赎回
            related_redeems = [r for r in redeems if r['purchase_record_id'] == p['id']]
            redeemed_amount = sum(r['redeem_amount'] for r in related_redeems)
            remaining = p['amount'] - redeemed_amount
            
            if remaining > 0:
                upcoming.append({
                    'product_name': p['product_name'],
                    'end_date': p['end_date'],
                    'remaining': remaining,
                    'days_remaining': days_remaining,
                    'expected_profit': remaining * p['annual_rate'] * p['duration'] / 365
                })
    
    # 按到期日排序
    upcoming.sort(key=lambda x: x['days_remaining'])
    
    # 月度收益趋势（近6个月）
    monthly_profits = {}
    for r in redeems:
        month = r['redeem_date'][:7]  # YYYY-MM
        monthly_profits[month] = monthly_profits.get(month, 0) + r.get('actual_profit', 0)
    
    # 按银行分布
    bank_distribution = {}
    for p in purchases:
        bank = p.get('bank_name', '未知银行')
        bank_distribution[bank] = bank_distribution.get(bank, 0) + p['amount']
    
    return jsonify({
        'summary': {
            'total_assets': total_assets,
            'holding_assets': holding_assets,
            'total_redeemed': total_redeemed,
            'total_profit': total_profit,
            'avg_rate': (total_profit / total_redeemed * 365 / 90 * 100) if total_redeemed > 0 else 0
        },
        'upcoming_maturities': upcoming[:5],
        'monthly_profits': monthly_profits,
        'bank_distribution': bank_distribution
    })
```

#### 任务3.2：仪表盘页面

**templates/index.html**
```html
{% extends "base.html" %}

{% block content %}
<h2 class="mb-4">投资仪表盘</h2>

<!-- 指标卡片 -->
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <h6 class="card-title">总资产</h6>
                <h2 id="totalAssets">--</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-success">
            <div class="card-body">
                <h6 class="card-title">持有中</h6>
                <h2 id="holdingAssets">--</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-info">
            <div class="card-body">
                <h6 class="card-title">已赎回</h6>
                <h2 id="totalRedeemed">--</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-warning">
            <div class="card-body">
                <h6 class="card-title">总收益</h6>
                <h2 id="totalProfit">--</h2>
            </div>
        </div>
    </div>
</div>

<!-- 图表区域 -->
<div class="row mb-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">收益趋势</div>
            <div class="card-body">
                <canvas id="profitChart" height="200"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">资产分布</div>
            <div class="card-body">
                <canvas id="allocationChart" height="200"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- 即将到期 -->
<div class="card">
    <div class="card-header">即将到期产品（未来30天）</div>
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>产品名称</th>
                    <th>到期日</th>
                    <th>剩余金额</th>
                    <th>预计收益</th>
                    <th>剩余天数</th>
                </tr>
            </thead>
            <tbody id="upcomingTable">
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// 加载仪表盘数据
fetch('/api/dashboard')
    .then(response => response.json())
    .then(data => {
        // 更新指标卡片
        document.getElementById('totalAssets').textContent = 
            data.summary.total_assets.toLocaleString() + '元';
        document.getElementById('holdingAssets').textContent = 
            data.summary.holding_assets.toLocaleString() + '元';
        document.getElementById('totalRedeemed').textContent = 
            data.summary.total_redeemed.toLocaleString() + '元';
        document.getElementById('totalProfit').textContent = 
            data.summary.total_profit.toLocaleString() + '元';
        
        // 绘制收益趋势图
        const months = Object.keys(data.monthly_profits).sort();
        const profits = months.map(m => data.monthly_profits[m]);
        new Chart(document.getElementById('profitChart'), {
            type: 'line',
            data: {
                labels: months,
                datasets: [{
                    label: '月度收益',
                    data: profits,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            }
        });
        
        // 绘制资产分布图
        const banks = Object.keys(data.bank_distribution);
        const amounts = banks.map(b => data.bank_distribution[b]);
        new Chart(document.getElementById('allocationChart'), {
            type: 'pie',
            data: {
                labels: banks,
                datasets: [{
                    data: amounts,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(153, 102, 255)'
                    ]
                }]
            }
        });
        
        // 填充即将到期表格
        const tbody = document.getElementById('upcomingTable');
        data.upcoming_maturities.forEach(item => {
            tbody.innerHTML += `
                <tr>
                    <td>${item.product_name}</td>
                    <td>${item.end_date}</td>
                    <td>${item.remaining.toLocaleString()}元</td>
                    <td>${item.expected_profit.toFixed(2)}元</td>
                    <td>${item.days_remaining}天</td>
                </tr>
            `;
        });
    });
</script>
{% endblock %}
```

---

## 七、测试计划

### 7.1 测试配置

**tests/conftest.py**
```python
"""测试配置和公共 Fixtures"""
import pytest
import tempfile
import os
import json
from datetime import datetime, timedelta

from app import app
from services.record_service import RecordService


@pytest.fixture
def app_instance():
    """创建测试用的 Flask 应用"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # 测试时禁用 CSRF
    return app


@pytest.fixture
def client(app_instance):
    """创建测试客户端"""
    with app_instance.test_client() as client:
        yield client


@pytest.fixture
def temp_data_file():
    """创建临时数据文件"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([], f)
        temp_path = f.name
    
    yield temp_path
    
    # 清理
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def record_service(temp_data_file):
    """创建测试用的 RecordService"""
    return RecordService(data_file=temp_data_file)
```

### 7.2 测试数据工厂

**tests/factories.py**
```python
"""测试数据工厂"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from constants import DATE_FORMAT


def create_purchase_record(**kwargs) -> Dict[str, Any]:
    """创建测试购买记录"""
    defaults = {
        'id': str(uuid.uuid4()),
        'type': 'purchase',
        'product_name': '测试理财产品',
        'amount': 100000.0,
        'annual_rate': 0.04,
        'duration': 90,
        'purchase_date': datetime.now().strftime(DATE_FORMAT),
        'end_date': (datetime.now() + timedelta(days=90)).strftime(DATE_FORMAT),
        'bank_name': '测试银行',
        'product_code': 'TEST001',
        'risk_level': 'medium',
        'category': '固定收益',
        'tags': ['测试'],
        'notes': '测试数据',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'deleted': False,
        'deleted_at': None
    }
    defaults.update(kwargs)
    return defaults


def create_redeem_record(
    purchase_id: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """创建测试赎回记录"""
    defaults = {
        'id': str(uuid.uuid4()),
        'type': 'redeem',
        'purchase_record_id': purchase_id or str(uuid.uuid4()),
        'redeem_amount': 100000.0,
        'redeem_date': (datetime.now() + timedelta(days=90)).strftime(DATE_FORMAT),
        'actual_profit': 1000.0,
        'profit_calc': 'manual',
        'redeem_type': 'maturity',
        'redeem_reason': '测试赎回',
        'fees': 0.0,
        'tax': 0.0,
        'net_profit': 1000.0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'deleted': False,
        'deleted_at': None
    }
    defaults.update(kwargs)
    return defaults


def create_investment_pair(
    purchase_kwargs: Optional[Dict] = None,
    redeem_kwargs: Optional[Dict] = None
) -> tuple:
    """创建一对购买和赎回记录"""
    purchase = create_purchase_record(**(purchase_kwargs or {}))
    redeem = create_redeem_record(
        purchase_id=purchase['id'],
        **(redeem_kwargs or {})
    )
    return purchase, redeem
```

### 7.3 单元测试

**tests/test_services.py**
```python
"""服务层单元测试"""
import pytest
from datetime import datetime, timedelta

from services.record_service import RecordService
from utils.error_handlers import NotFoundError, BusinessError
from tests.factories import create_purchase_record, create_redeem_record
from constants import DATE_FORMAT


class TestRecordService:
    """RecordService 测试类"""
    
    def test_get_grouped_records_empty(self, record_service):
        """测试空数据的分组查询"""
        result = record_service.get_grouped_records()
        assert result['groups'] == []
        assert result['total'] == 0
    
    def test_get_grouped_records_single(self, record_service):
        """测试单条记录的分组查询"""
        purchase = create_purchase_record()
        redeem = create_redeem_record(purchase_id=purchase['id'])
        record_service.records = [purchase, redeem]
        
        result = record_service.get_grouped_records()
        
        assert result['total'] == 1
        assert result['groups'][0]['purchase']['id'] == purchase['id']
        assert len(result['groups'][0]['redeems']) == 1
        assert result['groups'][0]['summary']['total_profit'] == 1000.0
    
    def test_get_grouped_records_with_filter(self, record_service):
        """测试带筛选条件的分组查询"""
        # 创建持有中的记录
        purchase1 = create_purchase_record(product_name='持有中产品')
        # 创建已完结的记录
        purchase2 = create_purchase_record(product_name='已完结产品')
        redeem = create_redeem_record(purchase_id=purchase2['id'])
        
        record_service.records = [purchase1, purchase2, redeem]
        
        # 筛选持有中
        result = record_service.get_grouped_records(status_filter='holding')
        assert result['total'] == 1
        assert result['groups'][0]['purchase']['product_name'] == '持有中产品'
        
        # 筛选已完结
        result = record_service.get_grouped_records(status_filter='completed')
        assert result['total'] == 1
        assert result['groups'][0]['purchase']['product_name'] == '已完结产品'
    
    def test_get_grouped_records_with_search(self, record_service):
        """测试带搜索条件的分组查询"""
        purchase1 = create_purchase_record(product_name='交通银行理财', bank_name='交通银行')
        purchase2 = create_purchase_record(product_name='民生银行理财', bank_name='民生银行')
        record_service.records = [purchase1, purchase2]
        
        # 搜索产品名
        result = record_service.get_grouped_records(search_query='交通')
        assert result['total'] == 1
        
        # 搜索银行名
        result = record_service.get_grouped_records(search_query='民生')
        assert result['total'] == 1
    
    def test_status_calculation(self, record_service):
        """测试状态计算"""
        # 持有中
        purchase = create_purchase_record(
            end_date=(datetime.now() + timedelta(days=30)).strftime(DATE_FORMAT)
        )
        status = record_service._determine_status(purchase, purchase['amount'])
        assert status == 'holding'
        
        # 部分赎回
        status = record_service._determine_status(purchase, purchase['amount'] / 2)
        assert status == 'partial'
        
        # 已完结
        status = record_service._determine_status(purchase, 0)
        assert status == 'completed'
        
        # 已到期
        expired_purchase = create_purchase_record(
            end_date=(datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT)
        )
        status = record_service._determine_status(expired_purchase, expired_purchase['amount'])
        assert status == 'expired'
    
    def test_calculate_real_rate(self, record_service):
        """测试真实年化收益率计算"""
        purchase = create_purchase_record(
            purchase_date='2025-01-01',
            annual_rate=0.04,
            duration=90
        )
        redeem = create_redeem_record(
            purchase_id=purchase['id'],
            redeem_date='2025-04-01',
            redeem_amount=100000,
            actual_profit=1000
        )
        
        real_rate = record_service._calculate_real_rate(purchase, [redeem])
        
        # 期望: (1000/100000) * (365/90) * 100 = 4.06%
        assert abs(real_rate - 4.06) < 0.01
    
    def test_delete_record_soft(self, record_service):
        """测试软删除"""
        purchase = create_purchase_record()
        record_service.records = [purchase]
        
        result = record_service.delete_record(purchase['id'], soft_delete=True)
        
        assert result is True
        assert len(record_service.records) == 0  # 已删除的记录被过滤
    
    def test_delete_record_not_found(self, record_service):
        """测试删除不存在的记录"""
        with pytest.raises(NotFoundError):
            record_service.delete_record('non-existent-id')
    
    def test_days_between(self, record_service):
        """测试日期天数计算"""
        days = record_service._days_between('2025-01-01', '2025-04-01')
        assert days == 90
```

### 7.4 集成测试

**tests/test_routes.py**
```python
"""路由集成测试"""
import pytest


class TestRoutes:
    """路由测试类"""
    
    def test_index_page(self, client):
        """测试首页"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_records_page(self, client):
        """测试记录列表页"""
        response = client.get('/records')
        assert response.status_code == 200
    
    def test_add_record_page(self, client):
        """测试添加记录页"""
        response = client.get('/records/add')
        assert response.status_code == 200
    
    def test_statistics_page(self, client):
        """测试统计页面"""
        response = client.get('/statistics')
        assert response.status_code == 200
    
    def test_export_page(self, client):
        """测试导出页面"""
        response = client.get('/export')
        assert response.status_code == 200
    
    def test_settings_page(self, client):
        """测试设置页面"""
        response = client.get('/settings')
        assert response.status_code == 200
    
    def test_404_page(self, client):
        """测试404页面"""
        response = client.get('/non-existent-page')
        assert response.status_code == 404


class TestAPIRoutes:
    """API 路由测试类"""
    
    def test_api_dashboard(self, client):
        """测试仪表盘API"""
        response = client.get('/api/dashboard')
        assert response.status_code == 200
        data = response.get_json()
        assert 'summary' in data
    
    def test_api_records(self, client):
        """测试记录列表API"""
        response = client.get('/api/records')
        assert response.status_code == 200
        data = response.get_json()
        assert 'groups' in data
```

### 7.5 数据验证测试

**tests/test_schemas.py**
```python
"""数据验证测试"""
import pytest
from datetime import datetime

from models.schemas import PurchaseSchema, RedeemSchema
from tests.factories import create_purchase_record, create_redeem_record


class TestPurchaseSchema:
    """购买记录 Schema 测试"""
    
    def test_valid_purchase(self):
        """测试有效购买记录"""
        data = create_purchase_record()
        schema = PurchaseSchema()
        result = schema.load(data)
        assert result['product_name'] == '测试理财产品'
        assert result['amount'] == 100000.0
    
    def test_invalid_amount(self):
        """测试无效金额"""
        data = create_purchase_record(amount=-100)
        schema = PurchaseSchema()
        with pytest.raises(Exception):
            schema.load(data)
    
    def test_missing_required_field(self):
        """测试缺少必填字段"""
        data = create_purchase_record()
        del data['product_name']
        schema = PurchaseSchema()
        with pytest.raises(Exception):
            schema.load(data)


class TestRedeemSchema:
    """赎回记录 Schema 测试"""
    
    def test_valid_redeem(self):
        """测试有效赎回记录"""
        data = create_redeem_record()
        schema = RedeemSchema()
        result = schema.load(data)
        assert result['redeem_amount'] == 100000.0
    
    def test_invalid_redeem_type(self):
        """测试无效赎回类型"""
        data = create_redeem_record(redeem_type='invalid')
        schema = RedeemSchema()
        with pytest.raises(Exception):
            schema.load(data)
```

### 7.6 测试用例清单

| 模块 | 测试项 | 预期结果 | 优先级 |
|------|--------|----------|--------|
| **数据模型** | 创建购买记录 | 记录正确创建 | P0 |
| **数据模型** | 创建赎回记录 | 记录正确创建，关联正确 | P0 |
| **数据模型** | 计算状态 | holding/completed/partial/expired正确 | P0 |
| **数据模型** | 计算收益率 | 结果准确，边界值正确 | P0 |
| **数据验证** | 有效数据验证 | 通过验证 | P0 |
| **数据验证** | 无效金额验证 | 拒绝负数和0 | P0 |
| **数据验证** | 缺少必填字段 | 拒绝并报错 | P0 |
| **数据验证** | 无效枚举值 | 拒绝并报错 | P0 |
| **记录服务** | 分组查询 | 正确分组 | P0 |
| **记录服务** | 筛选功能 | 结果正确 | P0 |
| **记录服务** | 搜索功能 | 结果正确 | P0 |
| **记录服务** | 软删除 | 记录标记为删除 | P0 |
| **记录服务** | 删除不存在记录 | 抛出 NotFoundError | P0 |
| **记录服务** | 分页功能 | 正确分页 | P1 |
| **路由** | 首页访问 | 200 OK | P0 |
| **路由** | 所有页面访问 | 200 OK | P0 |
| **路由** | 404页面 | 404 状态码 | P1 |
| **API** | 仪表盘API | 返回正确JSON | P0 |
| **API** | 记录列表API | 返回正确JSON | P0 |
| **边界值** | 金额为0 | 拒绝 | P0 |
| **边界值** | 金额为负数 | 拒绝 | P0 |
| **边界值** | 日期格式错误 | 拒绝 | P0 |
| **边界值** | 期限为0 | 拒绝 | P0 |

---

## 八、部署方案

### 8.1 Docker部署

**Dockerfile**
```dockerfile
# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser -d $APP_HOME -s /sbin/nologin appuser

# 设置工作目录
WORKDIR $APP_HOME

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录并设置权限
RUN mkdir -p data/backups && \
    chown -R appuser:appuser $APP_HOME

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# 启动命令
CMD ["python", "app.py"]
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  familyfinance:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: familyfinance
    ports:
      - "${PORT:-5000}:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_DEBUG=${FLASK_DEBUG:-False}
      - SECRET_KEY=${SECRET_KEY}
      - DATA_DIR=/app/data
    env_file:
      - .env
    restart: unless-stopped
    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### 8.2 传统部署

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 SECRET_KEY 等配置

# 4. 数据迁移（如果需要）
python migrate_data.py

# 5. 启动应用
python app.py

# 6. 访问
# http://localhost:5000
```

### 8.3 生产环境配置

**config.py**
```python
"""应用配置"""
import os
from typing import Type


class BaseConfig:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())
    DATA_DIR = os.environ.get('DATA_DIR', 'data')
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """测试环境配置"""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    DEBUG = False
    TESTING = False


def get_config() -> Type[BaseConfig]:
    """根据环境变量获取配置"""
    env = os.environ.get('FLASK_ENV', 'production')
    
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    
    return config_map.get(env, ProductionConfig)
```

### 8.4 Nginx 反向代理配置（可选）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/FamilyFinance/static/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 九、风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| 数据迁移失败 | 数据丢失 | 备份原数据，提供回滚脚本 |
| 性能问题 | 用户体验差 | 分页加载，缓存常用数据 |
| 浏览器兼容性 | 部分用户无法使用 | 使用成熟框架，测试主流浏览器 |
| 数据安全 | 隐私泄露 | 本地存储，不上传云端 |

---

## 十、后续迭代

### 10.1 第二阶段功能
- 投资组合分析
- 现金流预测
- 税务计算
- 复投管理

### 10.2 第三阶段功能
- 数据导入（银行对账单）
- 智能建议
- 移动端PWA
- 多用户支持

---

## 附录

### A. 依赖清单

**requirements.txt**
```
flask>=3.0.0
flask-wtf>=1.2.0
marshmallow>=3.20.0
python-dotenv>=1.0.0
openpyxl>=3.1.0
reportlab>=4.0.0
apscheduler>=3.10.0
bleach>=6.0.0
```

**开发依赖**
```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-flask>=1.3.0
```

### B. 环境变量

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| SECRET_KEY | Flask密钥 | 自动生成 | 生产环境必填 |
| DATA_DIR | 数据目录 | data | 否 |
| FLASK_DEBUG | 调试模式 | False | 否 |
| FLASK_ENV | 环境类型 | production | 否 |
| PORT | 端口号 | 5000 | 否 |
| LOG_LEVEL | 日志级别 | INFO | 否 |

### C. API接口清单

| 接口 | 方法 | 说明 | 认证 |
|------|------|------|------|
| / | GET | 首页/仪表盘页面 | 否 |
| /records | GET | 记录列表页面 | 否 |
| /records/add | GET/POST | 添加记录页面 | 否 |
| /statistics | GET | 统计分析页面 | 否 |
| /export | GET | 数据导出页面 | 否 |
| /settings | GET | 设置页面 | 否 |
| /api/dashboard | GET | 仪表盘数据 | CSRF |
| /api/records | GET | 记录列表 | CSRF |
| /api/records/<id> | GET | 记录详情 | CSRF |
| /api/records | POST | 创建记录 | CSRF |
| /api/records/<id> | PUT | 更新记录 | CSRF |
| /api/records/<id> | DELETE | 删除记录 | CSRF |
| /api/statistics | GET | 统计数据 | CSRF |
| /api/export | GET | 导出数据 | CSRF |

### D. 错误码说明

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | 检查请求参数 |
| 404 | 资源未找到 | 检查资源ID |
| 405 | 请求方法不允许 | 检查HTTP方法 |
| 500 | 服务器内部错误 | 检查服务器日志 |

### E. 数据迁移检查清单

- [ ] 备份原始数据文件
- [ ] 运行迁移脚本
- [ ] 验证迁移后的数据完整性
- [ ] 测试所有功能正常
- [ ] 确认软删除字段已添加

---

*文档版本：v1.1*
*最后更新：2026-06-27*
*修订内容：添加安全配置、错误处理、数据验证、软删除、测试用例*
