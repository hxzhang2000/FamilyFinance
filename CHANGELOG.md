# Changelog

本文件记录 FamilyFinance 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中
- 界面美化，引入Bootstrap框架
- 买卖记录分组展示
- 搜索和筛选功能
- 数据导出功能
- 到期提醒功能

---

## [1.1.0] - 2026-06-27

### 新增
- **代码模块化**
  - 拆分出 `services/record_service.py`（数据层）
  - 拆分出 `utils/helpers.py` 和 `utils/validators.py`（工具层）
  - 新增 `config.py` 集中管理配置
- **记录列表页**
  - 卡片/表格双视图切换
  - 按日期、金额、年化、状态排序
  - 按状态筛选（持有中/部分赎回/已完结/已到期）
  - 搜索产品名或银行
- **测试基础**
  - 新增 `tests/test_basic.py` 基础测试

### 变更
- **仪表盘**：所有列表改为按购买日期排序
- **筛选/排序**：分两行布局，搜索筛选为第一行，排序为第二行
- **PyInstaller 打包**：改为单文件 exe，数据自动保存在 exe 同级 `data/` 目录
- **路径兼容**：支持 PyInstaller onefile 模式下的模板和数据路径寻址
- **.gitignore**：排除 `.obsidian/`、`data/`、迁移脚本等无关文件

### 移除
- `templates/redeem.html`：功能合并到添加页面

---

## [1.0.0] - 2026-06-27

### 新增
- **Web界面**
  - 首页显示所有理财记录列表
  - 添加购买记录功能
  - 添加赎回记录功能
  - 编辑购买记录功能
  - 删除记录功能
  - 统计图表页面（月度收益、年度收益、产品分布）

- **收益计算**
  - 自动计算收益（复利公式）
  - 手动输入实际收益
  - 真实年化收益率计算

- **数据管理**
  - JSON格式本地数据存储
  - 买卖记录关联（purchase_record_id）

- **CLI界面**
  - 交互式命令行菜单
  - 添加、查看、计算收益、赎回等功能

- **部署支持**
  - Docker容器化部署
  - PyInstaller打包为可执行文件

- **文档**
  - AGENTS.md - Agent指南
  - 改进方案文档
  - 开发方案文档

### 技术细节
- Flask 3.0+ Web框架
- Chart.js 图表库
- 响应式基础样式
- 信号处理（SIGINT/SIGTERM）用于优雅关闭

---

## 版本说明

### 版本号规则

采用语义化版本号 `MAJOR.MINOR.PATCH`：

- **MAJOR** - 不兼容的API变更
- **MINOR** - 向后兼容的功能性新增
- **PATCH** - 向后兼容的问题修正

### 变更类型

- **新增 (Added)** - 新功能
- **变更 (Changed)** - 现有功能的变更
- **弃用 (Deprecated)** - 即将移除的功能
- **移除 (Removed)** - 已移除的功能
- **修复 (Fixed)** - Bug修复
- **安全 (Security)** - 安全相关的变更

---

## 模板

```markdown
## [X.Y.Z] - YYYY-MM-DD

### 新增
- 新功能描述

### 变更
- 变更描述

### 修复
- Bug修复描述
```
