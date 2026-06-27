# FamilyFinance - 家庭理财管理系统

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/hxzhang2000/FamilyFinance)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

一个简洁实用的家庭理财管理系统，用于记录和管理理财产品的购买与赎回。

## 功能特性

- **理财记录管理** - 记录理财产品的购买和赎回信息
- **收益计算** - 支持自动计算和手动输入两种收益计算方式
- **买卖关联** - 赎回记录自动关联购买记录，追踪投资生命周期
- **统计图表** - 月度/年度收益统计，产品分布饼图
- **真实收益率** - 自动计算真实年化收益率
- **数据持久化** - JSON格式本地存储，简单可靠

## 界面预览

### 首页 - 记录列表
显示所有理财记录，包括购买和赎回信息，以及收益汇总。

### 添加记录
支持添加购买记录和赎回记录，赎回时可选择关联的购买记录。

### 统计分析
提供月度收益、年度收益和产品分布的可视化图表。

## 快速开始

### 环境要求

- Python 3.8+
- pip (Python包管理器)

### 安装

```bash
# 克隆仓库
git clone https://github.com/hxzhang2000/FamilyFinance.git
cd FamilyFinance

# 安装依赖
pip install -r requirements.txt
```

### 运行

```bash
# 启动Web应用
python app.py

# 或使用CLI界面
python main.py
```

访问 http://localhost:5000 打开Web界面。

### Docker部署

```bash
# 构建镜像
docker build -t familyfinance .

# 运行容器
docker run -p 5000:5000 familyfinance
```

## 项目结构

```
FamilyFinance/
├── app.py                  # Flask Web应用主入口
├── main.py                 # CLI命令行界面
├── finance_manager.py      # CLI业务逻辑
├── finance_data.json       # 数据文件
├── requirements.txt        # Python依赖
├── Dockerfile              # Docker配置
├── static/
│   └── style.css          # 样式文件
├── templates/
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页
│   ├── add.html           # 添加记录
│   ├── edit.html          # 编辑记录
│   ├── redeem.html        # 赎回记录
│   └── statistics.html    # 统计页面
└── docs/
    ├── IMPROVEMENT_PLAN.md    # 改进方案
    └── DEVELOPMENT_PLAN.md    # 开发方案
```

## 数据模型

### 购买记录 (Purchase)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | UUID唯一标识 |
| type | string | 固定值 "purchase" |
| product_name | string | 产品名称 |
| amount | float | 投资金额 |
| annual_rate | float | 年化收益率 (小数形式，如0.0474表示4.74%) |
| duration | int | 投资期限（天） |
| purchase_date | string | 购买日期 (YYYY-MM-DD) |
| end_date | string | 到期日期 (YYYY-MM-DD) |

### 赎回记录 (Redeem)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | UUID唯一标识 |
| type | string | 固定值 "redeem" |
| purchase_record_id | string | 关联的购买记录ID |
| redeem_amount | float | 赎回金额 |
| redeem_date | string | 赎回日期 (YYYY-MM-DD) |
| actual_profit | float | 实际收益 |
| profit_calc | string | 计算方式: "auto" 或 "manual" |

## 收益计算说明

### 自动计算
使用复利公式计算：
```
日利率 = (1 + 年化收益率)^(1/365) - 1
收益 = 本金 × (1 + 日利率)^持有天数 - 本金
```

### 真实年化收益率
```
真实年化收益率 = (实际收益 / 赎回金额) × (365 / 持有天数) × 100%
```

## API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页，显示所有记录 |
| `/add` | GET/POST | 添加记录页面 |
| `/edit/<id>` | GET/POST | 编辑记录页面 |
| `/delete/<id>` | GET | 删除记录 |
| `/redeem` | GET/POST | 赎回记录页面 |
| `/statistics` | GET | 统计图表页面 |

## 开发计划

查看开发方案了解详细规划：
- **[家庭增强版](docs/DEVELOPMENT_PLAN_HOME.md)**（推荐）— v1.0-home，专注仪表盘和统计分析
- [完整版](docs/DEVELOPMENT_PLAN.md) — v1.1，含企业级配置
- [精简版](docs/DEVELOPMENT_PLAN_LITE.md) — v1.1-lite，基础功能
- [改进提案](docs/IMPROVEMENT_PLAN.md) — 功能建议收集

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- GitHub: [@hxzhang2000](https://github.com/hxzhang2000)
- 项目链接: [https://github.com/hxzhang2000/FamilyFinance](https://github.com/hxzhang2000/FamilyFinance)

## 致谢

- [Flask](https://flask.palletsprojects.com/) - Web框架
- [Chart.js](https://www.chartjs.org/) - 图表库
