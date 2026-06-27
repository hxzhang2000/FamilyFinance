# FamilyFinance 家庭增强版开发方案

> **版本：v2.0-unified** | 更新日期：2026-06-27
>
> **统一方案**：本方案整合了 `DEVELOPMENT_PLAN_HOME.md`（家庭增强）、`IMPROVEMENT_PLAN.md`（界面优化）、`DEVELOPMENT_PLAN_LITE.md`（精简版）的核心内容，取代上述所有版本。
>
> **适用场景**：家庭理财管理，专注核心功能 + 现代化的界面体验。

---

## 一、功能规划

### 1.1 功能清单

| 模块 | 功能 | 优先级 | 说明 |
|------|------|--------|------|
| **核心** | 买卖关联分组展示 | P0 | 按投资分组，展示完整生命周期 |
| **核心** | 添加/编辑/删除记录 | P0 | 基础CRUD操作 |
| **核心** | 收益计算（自动+手动） | P0 | 支持复利自动计算和手动输入收益 |
| **核心** | 产品名/银行/日期输入 | P0 | 表单含完整字段（含 bank_name） |
| **仪表盘** | 总投入/持有中/累计收益/平均年化 | P0 | 四大核心指标卡片 |
| **仪表盘** | 即将到期产品列表 | P0 | 未来30天到期提醒 |
| **仪表盘** | 持有中产品列表 | P0 | 快速查看当前投资（含预计收益） |
| **仪表盘** | 最近赎回记录 | P1 | 展示最近 5 条赎回 |
| **仪表盘** | 收益趋势迷你图 | P1 | 简单柱状图 |
| **列表** | 搜索功能 | P1 | 按产品名/银行搜索 |
| **列表** | 筛选功能 | P1 | 按状态筛选（持有中/已完结/部分赎回） |
| **列表** | 视图切换 | P1 | 分组视图 / 平铺视图 / 时间线视图 |
| **列表** | 展开/折叠 | P1 | 投资组可点击展开查看赎回明细 |
| **列表** | 删除保护 | P1 | 有赎回记录的购买记录删除前需确认 |
| **统计** | 月度收益趋势图 | P0 | 柱状图展示收益变化 |
| **统计** | 收益来源分布图 | P1 | 饼图展示各产品收益占比 |
| **统计** | 银行分布图 | P1 | 饼图展示各银行投资占比 |
| **统计** | 产品收益排行榜 | P1 | 按收益/年化双排序 |
| **统计** | 投资统计摘要 | P1 | 关键统计数据（笔数、平均持有、最高/最低收益） |
| **统计** | 时间范围筛选 | P1 | 全部/本年/本月/自定义 |
| **导出** | Excel导出 | P1 | 导出全部或筛选后的记录 |
| **导出** | CSV导出 | P2 | 简单的CSV格式导出 |

### 1.2 不做的功能

| 功能 | 原因 |
|------|------|
| 设置页面 | 家庭用户无需自定义配置 |
| 用户系统/多用户 | 家庭共用一台电脑 |
| 数据导入/银行对接 | 手动录入更可靠 |
| 投资组合分析 | 家庭用户不需要 |
| 现金流预测 | 过于复杂 |
| 税务计算 | 国内理财通常免税 |
| 风险评估 | 过于专业 |
| 批量操作 | 家庭记录量小，逐条即可 |
| 标签/分类系统 | 用银行名区分即可 |
| 主题切换 | 默认样式即可 |
| 数据备份/恢复 | 用户手动备份 JSON 文件即可 |
| 浏览器通知 | 需要在到期提醒页面查看即可 |
| PWA/离线支持 | 家庭内部使用，不需离线 |
| REST API | 单用户应用，无需 API |
| Marshmallow/Flask-WTF | 简单验证函数替代 |
| Docker安全加固 | 仅家庭内网使用 |
| Nginx配置 | 直接 Flask 运行即可 |

---

## 二、UI/UX 界面设计

### 2.1 仪表盘（Dashboard）

仪表盘作为首页，展示投资概览。

#### 2.1.1 指标卡片

页面顶部为四个关键指标卡片，使用不同颜色区分：

```
┌─────────────────────────────────────────────────────────────────┐
│                        投资仪表盘                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  │   总投入      │  │   持有中      │  │   累计收益    │  │   平均年化    │
│  │   ￥500,000  │  │   ￥300,000  │  │   ￥3,250    │  │   3.85%      │
│  │   Total      │  │   Holding   │  │   Profit    │  │   Avg Rate  │
│  │   #4CAF50    │  │   #2196F3   │  │   #FF9800   │  │   #9C27B0   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

每个卡片包含：
- **图标**：左侧小图标直观表示指标类型
- **标签**：中文名称
- **数值**：大号字体居中显示
- **副标签**：英文说明小字
- **背景色**：四色区分（绿=总投入，蓝=持有中，橙=累计收益，紫=平均年化）
- **悬停效果**：鼠标悬停时轻微上浮阴影

#### 2.1.2 即将到期产品

```
┌─────────────────────────────────────────────────────────────────┐
│  🔔 即将到期产品（未来30天）                                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 交银理财90天      │ 2026-07-01 │ ￥100,000 │ ⏳ 3天后到期   ││
│  │ [状态: 持有中]    │ 到期日     │ 金额      │ 紧急度标签     ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │ 民生安心存        │ 2026-07-15 │ ￥100,000 │ ⏳ 17天后到期  ││
│  │ [状态: 持有中]    │ 到期日     │ 金额      │ 普通标签       ││
│  └─────────────────────────────────────────────────────────────┘│
│  颜色规则: ≤7天红色背景 │ 8-14天黄色 │ ≥15天正常                     │
└─────────────────────────────────────────────────────────────────┘
```

- 按到期日期排序，最近到期排最前
- 使用颜色标签区分紧急程度（≤7天红色，8-14天黄色，≥15天正常）
- 每行显示：产品名、到期日、剩余金额、剩余天数
- 点击可跳转到该产品的购买记录详情

#### 2.1.3 持有中产品

```
┌─────────────────────────────────────────────────────────────────┐
│  📋 持有中产品                      [查看全部]                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  ▼ 民生安心存                                                ││
│  │    金额: ￥100,000 │ 年化: 2.20% │ 期限: 1095天               ││
│  │    购买: 2024-09-23 │ 到期: 2027-09-23                      ││
│  │    预计收益: ￥6,600 │ [赎回] [编辑] [删除]                   ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │  ▲ 民生贵竹增利月月盈18号  ← 可折叠                          ││
│  │    (已折叠状态，只显示产品名和金额)                             ││
│  └─────────────────────────────────────────────────────────────┘│
│  交互: 点击标题行展开/折叠详情 │ 悬停显示操作按钮                    │
└─────────────────────────────────────────────────────────────────┘
```

- 默认展开所有投资的详情
- 点击标题可折叠/展开单个投资
- 每项投资显示：金额、年化率、期限、购买日、到期日、预计收益
- 持有中的投资直接显示【赎回】【编辑】【删除】操作按钮
- 按钮在整行悬停时显式高亮

#### 2.1.4 最近赎回

```
┌─────────────────────────────────────────────────────────────────┐
│  💰 最近赎回                          [查看全部 → 记录列表]      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 交银理财90天  │ 赎回: 2025-04-17 │ 收益: ￥511 │ 年化: 5.04% ││
│  │ 民生贵竹30天  │ 赎回: 2025-02-12 │ 收益: ￥175 │ 年化: 6.39% ││
│  │ ...仅显示最近 5 条                                            ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 记录管理（Record Management）

#### 2.2.1 视图模式

提供三种视图模式，用户可通过标签切换：

```
┌─────────────────────────────────────────────────────────────────┐
│  [📂 分组视图]  [📋 平铺视图]  [📅 时间线视图]     🔍 [搜索...]  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  ▼ 交银理财灵动慧利6号90天   状态: ● 已完结    ▼ 展开明细    ││
│  │    金额: ￥100,000 │ 年化: 4.74% │ 期限: 90天               ││
│  │    ┌─────────────────────────────────────────────────────┐  ││
│  │    │ ✅ 买入 2025-01-09 │ ￥100,000 │ 到期日: 2025-04-09  │  ││
│  │    │ 💰 赎回 2025-04-17 │ ￥100,000 │ 收益: ￥511          │  ││
│  │    └─────────────────────────────────────────────────────┘  ││
│  │    📊 汇总: 总收益 ￥511 │ 真实年化 5.04%                   ││
│  ├─────────────────────────────────────────────────────────────┤│
│  │  ▼ 民生安心存             状态: ● 持有中    ▼ 展开明细       ││
│  │    (无赎回记录，显示买入详情)                                ││
│  │    [🔄 赎回]  [✏️ 编辑]  [🗑️ 删除]                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                    │
│  [分页: < 1 2 3 ... 5 >]  每页 20 条                              │
└─────────────────────────────────────────────────────────────────┘
```

**分组视图（默认）**：
- 以购买记录为组，展示该投资及其所有赎回记录
- 每组的头部显示：产品名、银行名、金额、年化、状态徽章
- 展开状态下显示完整的买入→赎回时间线和收益汇总
- 状态徽章颜色：持有中=蓝色，已完结=绿色，部分赎回=橙色，已到期=灰色

**平铺视图**：
- 传统表格模式，所有记录按日期倒序排列
- 可点击列头排序（日期、金额、收益）
- 适用于快速浏览和导出

**时间线视图**：
- 按时间轴展示所有交易
- 买入显示为绿色节点，赎回显示为橙色节点
- 适合查看资金流动的时间序列

#### 2.2.2 搜索与筛选

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 [输入产品名或银行名...]   状态: [全部 ▼]    [搜索] [重置]   │
├─────────────────────────────────────────────────────────────────┤
│  筛选条件:                                                       │
│  ● 全部记录  ○ 持有中  ○ 已完结  ○ 部分赎回  ○ 已到期          │
│  日期范围: [2025-01-01] 至 [2025-12-31]                        │
└─────────────────────────────────────────────────────────────────┘
```

- 实时搜索：输入即搜索（可配置防抖 300ms）
- 筛选条件：状态按钮组（单选）+ 日期范围选择
- 高级筛选（可折叠）：金额范围、银行选择
- 搜索范围：产品名、银行名

#### 2.2.3 交互细节

| 交互 | 行为 |
|------|------|
| **状态徽章** | 四种颜色区分投资状态，一目了然 |
| **展开/折叠** | 点击卡片标题切换展示赎回明细 |
| **悬停操作** | 鼠标悬停在记录上时显示操作按钮 |
| **快速赎回** | 持有中/部分赎回状态直接显示【赎回】按钮 |
| **删除保护** | 有赎回记录的购买记录，删除时弹出确认对话框"该产品有 X 条赎回记录，确认删除？" |
| **空状态** | 无记录时显示引导提示"还没有理财记录，点击这里添加第一条" |
| **加载状态** | 数据加载时显示骨架屏 |
| **分页** | 超过 20 条记录时自动分页 |

### 2.3 表单设计（添加/编辑记录）

#### 2.3.1 购买记录表单

```
┌─────────────────────────────────────────────────────────────┐
│                   添加购买记录                               │
├─────────────────────────────────────────────────────────────┤
│  📋 产品信息                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 产品名称: [交银理财灵动慧利6号90天          ]       │   │
│  │ 银行/机构: [交通银行 ▼]  也可手动输入               │   │
│  │           [工商银行] [建设银行] [农业银行] [其他]      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💰 投资金额                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 投资金额: [100,000   ] 元    ← 自动千分位格式化      │   │
│  │ 年化利率: [4.74      ] %                             │   │
│  │ 投资期限: [90        ] 天                            │   │
│  │ 购买日期: [📅 2025-01-09]                           │   │
│  │ 到期日期: 2025-04-09 (自动计算，不可编辑)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [取消]  [保存]                                             │
└─────────────────────────────────────────────────────────────┘
```

- 银行名使用 `<select>` 下拉框 + 可手动输入（datalist）
- 金额输入时自动千分位显示
- 年化利率输入支持百分比格式（用户输入 `4.74` 自动转为 `0.0474`）
- 购买日期使用日期选择器
- 到期日期根据购买日期+期限自动计算

#### 2.3.2 赎回记录表单

```
┌─────────────────────────────────────────────────────────────┐
│                   添加赎回记录                               │
├─────────────────────────────────────────────────────────────┤
│  🔗 选择产品                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ▼ 交银理财灵动慧利6号90天  │ 剩余: ￥100,000        │   │
│  │   金额: ￥100,000 │ 年化: 4.74% │ 到期: 2025-04-09   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ ○ 民生安心存                 │ 剩余: ￥100,000        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💵 赎回信息                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 赎回金额: [100,000   ] 元  (最大: ￥100,000)          │   │
│  │ 赎回日期: [📅 2025-04-17]                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📊 收益计算                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ○ 自动计算  ● 手动输入                               │   │
│  │ 实际收益: [511       ] 元                            │   │
│  │ 预计收益参考: ￥1,185 (按年化 4.74% 计算)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [取消]  [保存]                                             │
└─────────────────────────────────────────────────────────────┘
```

- 产品选择：列出所有持有中的购买记录，显示剩余金额
- 赎回金额不能超过剩余金额
- 手动输入收益时显示预计收益参考值
- 两种计算方式：自动（复利公式）/ 手动（用户输入实际收益）

### 2.4 统计分析页面

#### 2.4.1 时间范围筛选

```
┌─────────────────────────────────────────────────────────────┐
│  时间范围: [全部时间] [本年] [本月] [📅 自定义 2025-01 至 2025-06]  │
└─────────────────────────────────────────────────────────────┘
```

四种时间范围选项，切换时各图表联动更新。

#### 2.4.2 月度收益趋势图

```
┌─────────────────────────────────────────────────────────────┐
│              月度收益趋势（2025年）                          │
│    ▲                                                        │
│    │      ██                                                │
│    │   ██ ██ ██                                             │
│    │██ ██ ██ ██ ██                                          │
│    │██ ██ ██ ██ ██ ██                                       │
│    └─────────────────────────────────────▶                   │
│      1月 2月 3月 4月 5月 6月 7月 8月 9月 10月 11月 12月       │
│                                                               │
│  图表类型: 柱状图，蓝色主题                                    │
│  交互: 点击柱子显示该月详情（收益金额、相关产品）                │
│  功能: 鼠标悬停显示数值提示                                   │
└─────────────────────────────────────────────────────────────┘
```

#### 2.4.3 收益来源与银行分布

```
┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
│         收益来源分布                 │  │         银行投资分布                 │
│                                     │  │                                     │
│    ██████████ 交银理财  ￥511       │  │    ██████████████ 民生银行  ￥200,000 │
│    ██████     民生贵竹  ￥175       │  │    ██████████     交通银行  ￥100,000 │
│    ████       民生固收  ￥598       │  │    ██████         建设银行  ￥50,000  │
│                                     │  │                                     │
│  图表类型: 水平条形图                │  │  图表类型: 水平条形图                 │
│  按收益从高到低排序                  │  │  按投资金额从高到低排序               │
│  点击跳转到对应产品的详情             │  │  点击查看该银行所有投资               │
└─────────────────────────────────────┘  └─────────────────────────────────────┘
```

- 使用水平条形图替代饼图，可读性更好
- 显示具体数值标签
- 点击跳转到对应筛选视图

#### 2.4.4 产品收益排行榜

```
┌─────────────────────────────────────────────────────────────┐
│  产品收益排行榜              [按收益 ▼] [按年化 ▼]           │
├─────────────────────────────────────────────────────────────┤
│  🥇 民生固收91天     │ ￥598  │ 年化 2.41% │ 持有 91天     │
│  🥈 交银理财90天     │ ￥511  │ 年化 5.04% │ 持有 90天     │
│  🥉 民生贵竹30天     │ ￥175  │ 年化 6.39% │ 持有 30天     │
└─────────────────────────────────────────────────────────────┘
```

- 支持按"总收益"和"年化收益率"两种排序
- 前三名显示奖牌图标（🥇🥈🥉）
- 显示每项投资的持有天数

#### 2.4.5 投资统计摘要

```
┌─────────────────────────────────────────────────────────────┐
│  投资统计摘要                                                │
├───────────────────────┬─────────────────────────────────────┤
│  总投资笔数: 12笔     │  平均持有天数: 85天                  │
│  平均年化收益: 3.85%  │  最高年化收益: 6.39%                │
│  单笔最高收益: ￥681  │  单笔最低收益: ￥125                │
│  总收益: ￥3,250      │  收益最好产品: 民生固收91天          │
└───────────────────────┴─────────────────────────────────────┘
```

---

## 三、数据模型

### 3.1 购买记录

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

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | UUID 唯一标识 |
| type | string | 固定值 "purchase" |
| product_name | string | 产品名称 |
| amount | float | 投资金额 |
| annual_rate | float | 年化收益率（小数，如 0.0474） |
| duration | int | 投资期限（天） |
| purchase_date | string | 购买日期 YYYY-MM-DD |
| end_date | string | 到期日期 YYYY-MM-DD |
| bank_name | string | 银行/金融机构 |

### 3.2 赎回记录

> 注意：赎回记录反规范化冗余存储购入时的产品名、年化等信息，避免每次展示都做 JOIN 查询。

```json
{
  "id": "uuid",
  "type": "redeem",
  "purchase_record_id": "购买记录ID",
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

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | UUID 唯一标识 |
| type | string | 固定值 "redeem" |
| purchase_record_id | string | 关联的购买记录 ID |
| product_name | string | 冗余：产品名称 |
| purchase_date | string | 冗余：购买日期 |
| annual_rate | float | 冗余：年化收益率 |
| duration | int | 冗余：投资期限 |
| redeem_amount | float | 赎回金额 |
| redeem_date | string | 赎回日期 YYYY-MM-DD |
| actual_profit | float | 实际收益金额 |
| profit_calc | string | 计算方式: "auto" / "manual" |

### 3.3 关联关系

```
购买记录 (purchase)  1 ──── N  赎回记录 (redeem)
  │                                        │
  │  id = purchase_record_id              │
  │                                        │
  ├── 无赎回 → 持有中 (holding)            │
  ├── 部分赎回 → 部分赎回 (partial)         │
  └── 全部赎回 → 已完结 (completed)        │
```

### 3.4 状态计算规则

```python
def get_status(purchase: dict, redeems: list) -> str:
    """计算投资状态"""
    total_redeemed = sum(r['redeem_amount'] for r in redeems)
    remaining = purchase['amount'] - total_redeemed

    if remaining <= 0:
        return 'completed'            # 已完结
    elif total_redeemed > 0:
        return 'partial'              # 部分赎回
    elif is_expired(purchase):
        return 'expired'              # 已到期
    else:
        return 'holding'              # 持有中
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
├── services/               # 业务逻辑
│   ├── __init__.py
│   ├── record_service.py   # 记录服务（CRUD + 分组）
│   └── statistics_service.py # 统计服务
│
├── utils/                  # 工具函数
│   ├── __init__.py
│   ├── validators.py       # 简单验证函数（替代 Marshmallow）
│   └── helpers.py          # 日期格式化、金额格式化等
│
├── static/                 # 静态资源
│   ├── css/style.css
│   └── js/app.js
│
├── templates/              # 模板
│   ├── base.html           # Bootstrap 5 基础模板 + 导航栏
│   ├── index.html          # 仪表盘（指标卡片 + 到期提醒 + 持有列表）
│   ├── records/
│   │   ├── list.html       # 记录管理（三视图 + 搜索筛选 + 分页）
│   │   ├── add.html        # 添加记录（购买/赎回切换表单）
│   │   └── edit.html       # 编辑记录（含 bank_name 字段）
│   └── statistics/
│       └── index.html      # 统计分析（图表 + 排行榜 + 摘要）
│
├── data/                   # 数据目录
│   └── finance_data.json
│
├── tests/                  # 测试（使用 pytest）
│   ├── test_services.py
│   └── test_routes.py
│
├── migrate_data.py         # 数据迁移脚本
├── CHANGELOG.md            # 版本历史
├── README.md               # 项目说明
└── LICENSE                 # MIT 许可证
```

### 4.2 路由规划

#### 4.2.1 路由表

| 路由 | 方法 | 用途 | 模板 | 说明 |
|------|------|------|------|------|
| `/` | GET | 仪表盘 | `index.html` | 指标卡片 + 到期提醒 + 持有列表 |
| `/records` | GET | 记录列表 | `records/list.html` | 支持视图切换、搜索筛选、分页 |
| `/records/add` | GET/POST | 添加记录 | `records/add.html` | 购买/赎回切换 |
| `/records/edit/<id>` | GET/POST | 编辑记录 | `records/edit.html` | 含 bank_name 字段 |
| `/records/delete/<id>` | POST | 删除记录 | - | 有赎回记录时二次确认 |
| `/statistics` | GET | 统计分析 | `statistics/index.html` | 图表+排行榜+摘要 |
| `/export` | GET/POST | 数据导出 | - | Excel / CSV |

#### 4.2.2 路由清理（重要）

当前代码存在**两条冲突的赎回路径**，必须统一：

| 路径 | 当前行为 | 处理方式 |
|------|----------|----------|
| `/add` type=redeem | 创建独立赎回记录 ✅ | 保留并增强，移至 `/records/add` |
| `/redeem` | 原地修改 purchase.amount ❌ | **删除此路由及对应模板** |

统一策略：所有赎回操作统一通过 `POST /records/add` 提交，创建独立的 redeem 记录。删除旧的 `/redeem` 路由和 `templates/redeem.html`。

### 4.3 依赖清单

```
flask>=3.0.0
openpyxl>=3.1.0      # Excel 导出
pytest>=7.0.0         # 测试框架
```

⚠️ **注意**：当前 `requirements.txt` 错误地列出了 `uuid` 和 `datetime`——这俩是 Python 标准库，pip 安装同名包会装错。需清理为以上条目。

### 4.4 核心代码示例

#### 4.4.1 简单验证（替代 Marshmallow）

```python
# utils/validators.py
def validate_purchase(data: dict) -> list:
    """验证购买记录，返回错误列表"""
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
```

#### 4.4.2 统一错误处理

```python
# app.py 或 utils/error_handlers.py
@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', error='页面未找到'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('base.html', error='服务器内部错误'), 500
```

#### 4.4.3 统计分析服务

```python
"""services/statistics_service.py"""
from datetime import datetime
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
        holding_principal = total_invested - total_redeemed
        total_assets = holding_principal + total_profit if holding_principal > 0 else total_profit

        # 平均年化收益率
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
            'holding_principal': round(holding_principal, 2),
            'total_assets': round(total_assets, 2),
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
                monthly[redeem_date.strftime('%Y-%m')] += r.get('actual_profit', 0)
        return dict(sorted(monthly.items()))

    def get_profit_by_product(self) -> List[Dict[str, Any]]:
        """按产品统计收益（从购买记录反查产品名）"""
        product_profits = defaultdict(float)
        product_info = {}
        for r in self.redeems:
            purchase = self._find_purchase(r['purchase_record_id'])
            if not purchase:
                continue
            name = purchase['product_name']
            product_profits[name] += r.get('actual_profit', 0)
            if name not in product_info:
                days = self._days_between(purchase['purchase_date'], r['redeem_date'])
                rate = (r['actual_profit'] / r['redeem_amount']) * (365 / days) * 100 if days > 0 else 0
                product_info[name] = {'days': days, 'rate': round(rate, 2)}
        result = []
        for name, profit in sorted(product_profits.items(), key=lambda x: x[1], reverse=True):
            info = product_info.get(name, {'days': 0, 'rate': 0})
            result.append({
                'product_name': name,
                'profit': profit,
                'rate': info['rate'],
                'days': info['days'],
                'sort_by_rate': info['rate']
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
            return {'total_count': 0, 'avg_days': 0, 'avg_rate': 0,
                    'max_rate': 0, 'max_profit': 0, 'min_profit': 0}
        profits = [r.get('actual_profit', 0) for r in self.redeems]
        rates, days_list = [], []
        for r in self.redeems:
            purchase = self._find_purchase(r['purchase_record_id'])
            if purchase:
                days = self._days_between(purchase['purchase_date'], r['redeem_date'])
                if days > 0:
                    rates.append((r['actual_profit'] / r['redeem_amount']) * (365 / days) * 100)
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
        return next((p for p in self.purchases if p['id'] == purchase_id), None)

    def _get_remaining_amount(self, purchase_id: str) -> float:
        purchase = self._find_purchase(purchase_id)
        if not purchase:
            return 0
        redeemed = sum(r['redeem_amount'] for r in self.redeems
                       if r['purchase_record_id'] == purchase_id)
        return purchase['amount'] - redeemed

    @staticmethod
    def _days_between(date1_str: str, date2_str: str) -> int:
        d1 = datetime.strptime(date1_str, DATE_FORMAT)
        d2 = datetime.strptime(date2_str, DATE_FORMAT)
        return (d2 - d1).days
```

---

## 五、开发计划

> 当前代码功能约 **80% 已完成**，主要工作为：前端 Bootstrap 5 重构 + 仪表盘/统计增强 + 路由清理 + 搜索筛选 + 导出 + 测试。

### 5.1 阶段划分

| 阶段 | 时间 | 内容 | 交付物 |
|------|------|------|--------|
| **一：基础架构** | 2天 | 目录重构、路由清理、数据迁移、依赖修复 | 新目录结构、删除 `/redeem` 路由、修复 requirements.txt |
| **二：核心功能** | 3天 | 买卖关联卡片式展示、表单增强（加 bank_name）、搜索筛选、状态徽章、删除保护 | 卡片式分组视图、搜索筛选栏、完整CRUD |
| **三：仪表盘** | 3天 | 四大指标卡片、到期提醒（紧急度颜色）、持有产品列表、最近赎回、收益迷你图 | 仪表盘完成 |
| **四：统计分析** | 2天 | 月度趋势图、收益/银行分布图、排行榜（双排序）、统计摘要、时间范围筛选 | 统计页面完成 |
| **五：导出+测试** | 1天 | Excel/CSV 导出、pytest 基础测试 | 功能全部完成、可上线 |
| **总计** | **11天（约2-3周）** | | |

### 5.2 里程碑

| 里程碑 | 时间 | 交付物 |
|--------|------|--------|
| M1 | 第2天 | 基础架构完成，路由清理完毕 |
| M2 | 第5天 | CRUD + 分组视图 + 搜索筛选上线 |
| M3 | 第8天 | 仪表盘完成 |
| M4 | 第10天 | 统计分析完成 |
| M5 | 第11天 | 全部完成，可上线 |

---

## 六、其他说明

### 6.1 CLI 入口处理

当前项目有 `main.py`（CLI 菜单界面）和 `finance_manager.py`（CLI 业务逻辑），使用整型 ID 而非 UUID。

- **保留不变**：与 Web 端数据文件共用 `finance_data.json`，各自独立操作
- **不主动重构 CLI**：家庭用户通常只用 Web 端，CLI 作为备用入口保持最小可维护状态

### 6.2 数据迁移脚本要点

迁移脚本 `migrate_data.py` 需处理：

1. **数据目录迁移**：将根目录的 `finance_data.json` 复制到 `data/finance_data.json`
2. **补全 bank_name**：旧数据可能缺 `bank_name`，设为 `"未知银行"` 兜底
3. **清理错误依赖**：删除 `requirements.txt` 中的 `uuid` 和 `datetime`
4. **兼容性**：不改动现有数据结构，只增字段

### 6.3 编辑页面缺失字段

当前 `templates/edit.html` 只编辑实际收益，产品名称/金额为 `disabled`。重构后：

- `product_name`、`amount`、`annual_rate`、`duration` 改为可编辑
- 添加 `bank_name` 下拉框（带 `{{ record.get('bank_name', '未知银行') }}` 回显）
- 到期日期根据新输入自动重新计算

### 6.4 技术选型

| 技术 | 用途 | 版本 |
|------|------|------|
| Flask | Web框架 | 3.x |
| Bootstrap 5 | UI框架 | 5.3.x（通过 CDN 引入） |
| Chart.js | 图表库 | 4.x（通过 CDN 引入） |
| openpyxl | Excel导出 | 3.x |
| pytest | 测试框架 | 7.x |
| JSON文件 | 数据存储 | - |

### 6.5 快速开始

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

## 七、本方案与其他方案的关系

本方案（v2.0-unified）整合并取代了以下文档：

| 旧文档 | 整合内容 | 状态 |
|--------|----------|------|
| `DEVELOPMENT_PLAN_HOME.md` v1.0-home | 核心框架、数据模型、开发计划 | ✅ 全部保留 |
| `IMPROVEMENT_PLAN.md` | 界面设计详图、交互细节、视图切换、删除保护 | ✅ 关键内容合并 |
| `DEVELOPMENT_PLAN_LITE.md` | 简单验证、错误处理 | ✅ 部分合入 |
| `DEVELOPMENT_PLAN.md` v1.1 | 企业级功能（Marshmallow、CSRF、Docker安全等） | ❌ 对家庭版不适用 |

---

*家庭增强版 v2.0-unified - 专注核心功能 + 现代化界面体验*
