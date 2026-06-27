# FamilyFinance - 家庭理财管理系统

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/hxzhang2000/FamilyFinance)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

一个简洁实用的家庭理财管理系统，用于记录和管理理财产品的购买与赎回。

## 功能特性

- **理财记录管理** - 记录理财产品的购买和赎回信息
- **记录列表** - 卡片/表格双视图，支持搜索、筛选、排序
- **收益计算** - 支持自动计算和手动输入两种收益计算方式
- **买卖关联** - 赎回记录自动关联购买记录，追踪投资生命周期
- **仪表盘** - 持有中产品、即将到期、最近赎回一目了然
- **统计图表** - 月度/年度收益趋势图，产品分布饼图
- **真实收益率** - 自动计算真实年化收益率
- **数据持久化** - JSON格式本地存储，简单可靠
- **单文件分发** - PyInstaller 打包为独立 exe，无需 Python 环境

## 快速开始

### 下载即用（推荐）

从 [Releases](https://github.com/hxzhang2000/FamilyFinance/releases) 下载最新的 `FamilyFinance.exe`，双击运行，访问 http://localhost:5000 即可。

数据文件自动保存在 exe 同级的 `data/finance_data.json`。

### 源码运行

```bash
# 克隆仓库
git clone https://github.com/hxzhang2000/FamilyFinance.git
cd FamilyFinance

# 安装依赖
pip install -r requirements.txt

# 启动Web应用
python app.py
```

访问 http://localhost:5000 打开Web界面。

### Docker部署

```bash
# 构建镜像
docker build -t familyfinance .

# 运行容器
docker run -d -p 5000:5000 -v %cd%/data:/FamilyFinance/data familyfinance
```

### PyInstaller 打包

```bash
pip install pyinstaller
pyinstaller FamilyFinance.spec
```

生成 `dist/FamilyFinance.exe`，单文件可直接分发。

## 项目结构

```
FamilyFinance/
├── app.py                  # Flask Web应用主入口
├── main.py                 # CLI命令行界面
├── config.py               # 应用配置（数据路径、密钥）
├── FamilyFinance.spec      # PyInstaller 打包配置
├── requirements.txt        # Python依赖
├── Dockerfile              # Docker配置
│
├── services/
│   ├── __init__.py
│   └── record_service.py   # 数据层（CRUD、分组）
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py          # 工具函数（收益计算、日期等）
│   └── validators.py       # 表单验证
│
├── tests/
│   └── test_basic.py       # 基础测试
│
├── templates/
│   ├── base.html           # 基础模板
│   ├── index.html          # 仪表盘
│   ├── add.html            # 添加记录
│   ├── edit.html           # 编辑记录
│   ├── records/
│   │   └── list.html       # 记录列表（卡片/表格视图）
│   └── statistics.html     # 统计页面
│
├── static/
│   └── style.css           # 样式文件
│
└── docs/
    ├── IMPROVEMENT_PLAN.md     # 改进方案
    └── DEVELOPMENT_PLAN.md     # 开发方案
```

## 数据模型

### 购买记录 (Purchase)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | UUID唯一标识 |
| type | string | 固定值 "purchase" |
| product_name | string | 产品名称 |
| bank_name | string | 银行名称 |
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
| `/` | GET | 仪表盘，显示汇总及持有中产品 |
| `/records` | GET | 记录列表（支持搜索、筛选、排序） |
| `/add` | GET/POST | 添加记录（购买/赎回） |
| `/edit/<id>` | GET/POST | 编辑购买记录 |
| `/delete/<id>` | GET | 删除记录 |
| `/statistics` | GET | 统计图表页面 |
| `/export` | GET | 导出 Excel/CSV |

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
- [Bootstrap](https://getbootstrap.com/) - UI框架
