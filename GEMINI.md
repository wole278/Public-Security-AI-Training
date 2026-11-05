# GEMINI.md · 公安警务 AI 实战夜校培训系统（Public-Security-AI-Training）

> **标准继承**：L0 安全与合规底线 + L1-manufacturing（客户私密、信息共享可控、安全）｜真源：`D:\github\project\ai-ops-hub\standards\`
> **默认数据级别**：P0（100% 程序合成虚拟脱敏实训数据，无任何真实警务/公民信息）　**发布模式**：公开仓库 + GitHub Pages 在线实训门户（`https://wole278.github.io/Public-Security-AI-Training/`）
> **冲突规则**：L0 不可放宽；L1 与本文件冲突时以本文件为准，并在此注明差异。

---

## 1. 项目定位与教学设计规约（夜校轮训模式）

- **目标受众**：上海市某区公安技术部门及一线业务干警（传统科信/图侦/网安技术人员 + 交警/治安/刑侦/派出所民警）。
- **排班学制**：**夜校多班次轮训制**，每班次 **1 小时 × 3 次课（共 180 分钟）**，支持不同批次、不同岗位人员滚动参训或缺课补学。
- **80/20 黄金教学法（核心刚性指标）**：
  - **80% 自读即会（每课 45 分钟，全详尽自包含课件）**：拒绝“大纲式/口号式 PPT”。课件本身必须是**完整可读的图文实战教材**，内置【警务痛点还原 → 错误提问反例 vs 满分结构化提示词 → AI 完整输出样例 → 底层原理解析 → 一键复制模板】。学员无需讲师解释，**仅凭顺读课件即可独立完成 80% 的知识吸收与依葫芦画瓢实操**。
  - **20% 最佳实践带练（每课 15 分钟，随堂演练沙盒）**：每节课最后 15 分钟聚焦 2 个高频实战靶场（1 个面向全员民警的提示词工作流 + 1 个面向技术人员的自动化脚本/看板生成），利用随堂全脱敏仿真数据包当场跑通、当场出战果。

---

## 2. 警务安全与涉密合规死线（L0 + 公安纪律双重锁定）

1. **严禁真实警务数据入库（P3 零容忍）**：
   - 本仓库中所有案例、笔录、车牌、银行流水、话单、110 警情工单**100% 必须为程序合成的虚拟脱敏数据（Synthetic Mock Data）**，人名统一使用 `张某甲/李某乙/王某丙`，证件号/卡号/车牌全部使用虚构号段（如 `31019919900101XXXX`、`62220000XXXX`、`沪A·88X99（虚拟）`）。
   - 严禁出现具体客户单位内部真实 IP、专网拓扑、真实案件编号及未公开警务部署细节。
2. **内外网双轨教学规范**：
   - 课件中凡涉及互联网大模型操作，必须强制标注**【留壳去肉脱敏法】**或**【表头脱敏代写脚本法】**（即：只发字段名与假样本让外网 AI 写离线 Python/SQL 代码，拿回代码在公安内网/单机离线运行真数据）。

---

## 3. 目录架构与模块分层

```text
Public-Security-AI-Training/
├── GEMINI.md                                  # 项目开发与安全规约（本文件）
├── README.md                                  # 项目总览、夜校排课表与讲师/学员快速启动指南
├── index.html                                 # 【核心交付】单文件离线交互式夜校自学与带练系统（80%自读+20%沙盒+一键复制+45/15倒计时）
├── courseware/                                # 【80% 自读全详尽教材】每课独立成篇，直读即通
│   ├── session1_traffic_and_security.md       # 第1夜（60min）：合规破冰 + 城市交通与社会面治安智能监控
│   ├── session2_crime_investigation.md        # 第2夜（60min）：犯罪调查、多人笔录矛盾雷达与资金/话单自动化侦查
│   └── session3_bigdata_reapplication.md      # 第3夜（60min）：警务大数据再应用、Text-to-SQL 与态势大屏一键生成
├── handouts/                                  # 【随堂可打印/派发速查件】
│   ├── police_ai_safety_and_prompt_card.md    # 公安干警 AI 安全脱敏口诀与四步提问法桌垫卡
│   ├── prompt_and_script_library.md           # 交通/治安/刑侦/科信 20 个高频即插即用提示词与脚本模板库
│   └── intranet_llm_deployment_guide.md       # 传统技术科专用：公安内网/单机离线大模型（Ollama+RAG法规库）极简部署指南
└── labs/                                      # 【20% 最佳实践带练靶场】含合成仿真数据与零依赖 Python 标准库脚本
    ├── generate_mock_data.py                  # 一键生成/重置全套 3 次课虚拟脱敏警务数据集
    ├── session1_traffic_monitor/              # 第1夜带练：路口过车流量拥堵诊断与多模态监控告警二次过滤
    │   ├── mock_traffic_flow.csv
    │   ├── mock_vlm_alerts.json
    │   └── analyze_traffic_and_alerts.py
    ├── session2_crime_investigation/          # 第2夜带练：三人冲突笔录样本 + 银行流水洗钱过渡卡与话单共现碰撞脚本
    │   ├── mock_interrogation_records.md
    │   ├── mock_bank_flows.csv
    │   ├── mock_call_records.csv
    │   └── laundering_and_call_detector.py
    └── session3_bigdata_reapplication/        # 第3夜带练：110 重复报警“防民转刑”挖掘 + 一键生成离线治安态势 HTML 大屏
        ├── mock_110_calls.csv
        ├── alert_110_mining_and_dashboard.py
        └── dashboard_demo.html                # 脚本自动生成的交互式领导汇报大屏成品
```

---

## 4. 技术栈与本地自检标准

- **零第三方依赖原则（适配公安内网/传统办公机）**：
  - 考虑到公安干警及传统技术科电脑往往无法随意 `pip install` 外部包或处于离线环境，`labs/` 下所有演练 Python 脚本**优先使用 Python 3 标准库（`csv`, `json`, `collections`, `datetime`, `re`, `math`, `pathlib`）编写**，确保任何装有基础 Python 3 的办公机**开箱即跑、100% 零报错**；同时在课件中提供对应的 `Pandas` / `SQL` 进阶对照版。
  - `index.html` 与 `dashboard_demo.html` 采用**纯原生 HTML5 + CSS3 + Vanilla JS + SVG/Canvas 内联图表**，无需联网加载外部 CDN，断网拷贝进内网电脑双击即可全屏演示。
- **验收指标**：
  1. 运行 `python labs/generate_mock_data.py` 及三堂课的 `labs/session*/...py` 全部退出码为 `0`，输出结构化研判报告与可视化 HTML。
  2. 敏感词扫描：仓库中无任何真实个人身份证、真实手机号或涉密标识。
  3. 课件自包含度检查：三份 `courseware/*.md` 及 `index.html` 均包含完整的“背景-提示词全文-AI输出全文-带练步骤”，直接阅读即可完成 80% 培训目标。
