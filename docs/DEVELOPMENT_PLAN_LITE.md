# FamilyFinance 开发方案（精简版）

> **版本：v1.1-lite** | 更新日期：2026-06-27
> 
> 本方案去掉了企业级安全配置，专注于家庭应用的核心功能。

---

## 一、技术架构

### 1.1 目录结构
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
│   └── record_service.py  # 记录服务
│
├── utils/                  # 工具函数
│   ├── __init__.py
│   └── helpers.py         # 辅助函数
│
├── static/                 # 静态资源
│   ├── css/
│   └── js/
│
├── templates/              # 模板
│   ├── base.html
│   ├── index.html
│   └── records/
│
├── data/                   # 数据目录
│   └── finance_data.json
│
└── tests/                  # 测试
    ├── test_services.py
    └── test_routes.py
```

### 1.2 技术栈
| 技术 | 用途 |
|------|------|
| Flask 3.x | Web框架 |
| Bootstrap 5 | UI框架 |
| Chart.js | 图表 |
| JSON文件 | 数据存储 |

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
  "bank_name": "交通银行",
  "risk_level": "medium",
  "created_at": "2025-01-09T10:30:00"
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

## 三、核心功能

### 3.1 买卖关联展示
```
┌─────────────────────────────────────────────────────────┐
│ 📦 交银理财灵动慧利6号90天                                │
│    金额: 100,000元 │ 年化: 4.74% │ 状态: ● 已完结        │
├─────────────────────────────────────────────────────────┤
│    买入 2025-01-09 │ 100,000元 │ 到期日: 2025-04-09     │
│    赎回 2025-04-17 │ 100,000元 │ 收益: 511元            │
├─────────────────────────────────────────────────────────┤
│    汇总: 总收益 511元 │ 真实年化 5.04%                    │
└─────────────────────────────────────────────────────────┘
```

### 3.2 仪表盘
- 总资产/持有中/已赎回/总收益 四大指标
- 收益趋势图
- 即将到期提醒

### 3.3 搜索筛选
- 按状态筛选（持有中/已完结/部分赎回）
- 按产品名/银行搜索

### 3.4 数据导出
- CSV 导出
- Excel 导出

---

## 四、简化实现

### 4.1 简单验证（替代 Marshmallow）

```python
# utils/validators.py
def validate_purchase(data):
    """验证购买记录"""
    errors = []
    
    if not data.get('product_name'):
        errors.append('产品名称不能为空')
    
    amount = data.get('amount', 0)
    if amount <= 0:
        errors.append('金额必须大于0')
    
    rate = data.get('annual_rate', 0)
    if not (0 < rate < 1):
        errors.append('年化利率必须在0-1之间')
    
    return errors
```

### 4.2 简单错误处理

```python
# app.py
@app.errorhandler(404)
def not_found(error):
    return {'error': '资源未找到'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': '服务器错误'}, 500
```

### 4.3 配置文件（替代环境变量）

```python
# config.py
import os

class Config:
    SECRET_KEY = 'family-finance-secret-key-2026'
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    DEBUG = True
```

### 4.4 简单测试

```python
# tests/test_services.py
import pytest
from services.record_service import RecordService

def test_get_grouped_records():
    service = RecordService()
    service.records = [
        {
            "id": "test-1",
            "type": "purchase",
            "product_name": "测试产品",
            "amount": 100000,
            "annual_rate": 0.04,
            "duration": 90,
            "purchase_date": "2025-01-01",
            "end_date": "2025-04-01"
        }
    ]
    
    result = service.get_grouped_records()
    assert result['total'] == 1
```

---

## 五、开发计划

### 阶段一：基础架构（1周）
- [ ] 项目目录重构
- [ ] 数据模型设计
- [ ] 基础路由和模板
- [ ] 数据迁移脚本

### 阶段二：核心功能（2周）
- [ ] 买卖关联展示
- [ ] 添加/编辑/删除记录
- [ ] 搜索筛选功能

### 阶段三：仪表盘（1周）
- [ ] 指标卡片
- [ ] 图表展示
- [ ] 即将到期提醒

### 阶段四：导出与优化（1周）
- [ ] CSV/Excel 导出
- [ ] 响应式适配
- [ ] 基础测试

---

## 六、依赖清单

**requirements.txt**
```
flask>=3.0.0
openpyxl>=3.1.0
```

> 去掉了：flask-wtf, marshmallow, python-dotenv, apscheduler, bleach

---

## 七、快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问
# http://localhost:5000
```

---

*精简版方案 - 专注核心功能，去除企业级配置*
