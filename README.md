# 上海市某区公安技术部门 · AI 实战赋能夜校培训系统（Public-Security-AI-Training）

> **标准继承**：`L0-security-compliance`（安全与合规底线）+ `L1-manufacturing-client`（客户私密、信息共享可控、安全）  
> **在线网页学习与实训靶场入口**：**[https://wole278.github.io/Public-Security-AI-Training/](https://wole278.github.io/Public-Security-AI-Training/)** （默认实训登录口令：`SHGA-2026`）  
> **适用模式**：**多班次夜校轮训（每班 1 小时 × 3 次课，共 3 小时）**  
> **核心教学设计**：**80% 直读课件即可独立掌握（45分钟/课） + 20% 最佳实践随堂带练（15分钟/课，支持网页在线沙盒免装环境直接跑通）**

---

## 🎯 一、 为什么这样设计？（针对传统技术人员与公安干警的痛点）

1. **多班次夜校兼容（缺课可补、自读即通）**：
   公安干警经常因突发勤务、值班备勤或专案出差无法固定时间参训。本仓库将**讲师逐字稿、正反提问对比、AI 真实输出全文、零依赖代码模板**100% 融进课件本身（[`index.html`](./index.html) 及 [`courseware/`](./courseware/)）。**学员哪怕不听讲，顺着读完课件就能完成 80% 的学习培训**；课堂最后 15 分钟聚焦 20% 动手带练，当场跑通、当场出战果。
2. **严守公安保密死线（真数据绝不出内网）**：
   首创并贯穿**【留壳去肉脱敏法】**（面向办案/综合民警）与**【表头脱敏代写法】**（面向科信/图侦/网安/经侦技术人员）——外网只发字段名与假样本让 AI 当“免费外包程序员”写零依赖 Python/SQL 脚本，拿回脚本在公安内网离线跑真实数据。
3. **100% 零第三方依赖（适配公安内网/老旧办公机）**：
   所有随堂演练脚本仅使用 Python 3 内置标准库编写，无需 `pip install` 任何外部包；网页课件与汇报大屏均为**单文件离线原生 HTML**，断网拷贝进内网即可双击全屏运行。

---

## 📅 二、 夜校 1 小时 × 3 次课标准课程表

| 课次 | 主题（每次 60 分钟 = 45m 直读 + 15m 带练） | 80% 直读核心教材（点击阅读） | 20% 随堂带练靶场与产出 |
| :--- | :--- | :--- | :--- |
| **第 1 夜** | **合规破冰 & 城市交通与社会面治安智能监控** | [`courseware/session1_traffic_and_security.md`](./courseware/session1_traffic_and_security.md) | 1. 暴雨早高峰/大客流三级熔断排堵安保预案推演<br>2. 运行 [`analyze_traffic_and_alerts.py`](./labs/session1_traffic_monitor/analyze_traffic_and_alerts.py) 过滤 60% 监控误报并诊断路口绿信比失衡 |
| **第 2 夜** | **犯罪调查、多人笔录矛盾雷达与资金/话单侦查** | [`courseware/session2_crime_investigation.md`](./courseware/session2_crime_investigation.md) | 1. 三名跑分嫌疑人冲突笔录（[`mock_interrogation_records.md`](./labs/session2_crime_investigation/mock_interrogation_records.md)）矛盾雷达与审讯提纲生成<br>2. 运行 [`laundering_and_call_detector.py`](./labs/session2_crime_investigation/laundering_and_call_detector.py) 3秒锁定洗钱过渡卡、同窝点 IP 与神秘上线号码 |
| **第 3 夜** | **警务大数据再应用、Text-to-SQL 与态势大屏生成** | [`courseware/session3_bigdata_reapplication.md`](./courseware/session3_bigdata_reapplication.md) | 1. Text-to-SQL 周末夜宵档寻衅滋事同比统计<br>2. 运行 [`alert_110_mining_and_dashboard.py`](./labs/session3_bigdata_reapplication/alert_110_mining_and_dashboard.py) 挖掘 110“防民转刑”高危重复报警户并自动生成离线大屏 [`dashboard_demo.html`](./labs/session3_bigdata_reapplication/dashboard_demo.html) |

---

## 🧰 三、 课后直接派发给学员的“三个一”高价值交付包

1. **一张桌垫速查卡**：[`handouts/police_ai_safety_and_prompt_card.md`](./handouts/police_ai_safety_and_prompt_card.md)（正面“三不准两神技”脱敏铁律，背面“R-C-T-F 万能提问公式”）。
2. **一本即插即用模板库**：[`handouts/prompt_and_script_library.md`](./handouts/prompt_and_script_library.md)（涵盖交警、治安、刑侦、经侦、网安、科信 12 个高频拿来即填模板）。
3. **一份内网私有化部署指南**：[`handouts/intranet_llm_deployment_guide.md`](./handouts/intranet_llm_deployment_guide.md)（指导传统技术科用 1 台显卡工作站 + Ollama + AnythingLLM 在公安内网离线搭建大模型与法规 RAG 知识库）。

---

## 🚀 四、 讲师开课与学员自检快速启动指南（Windows PowerShell）

### 1. 在线网页登录学习与沙盒演练（推荐学员手机/平板/办公电脑直接访问）
- **在线网址**：**[https://wole278.github.io/Public-Security-AI-Training/](https://wole278.github.io/Public-Security-AI-Training/)**
- **学员登录**：进入网页后选择所属警种条线、参训班次，输入默认实训口令 **`SHGA-2026`** 即可登录；支持在网页内直接点击 **【▶️ 在网页沙盒运行诊断脚本】** 完成全部 6 大靶场演练并领取结业凭证。
- **离线双击运行**：在断网公安内网环境中，直接双击根目录下的 **[`index.html`](./index.html)** 即可获得与线上完全一致的交互式实训体验。

### 2. 本地终端初始化并运行全套 3 期随堂演练脚本
```powershell
# 进入项目根目录
cd Public-Security-AI-Training

# 1. 生成/重置全套虚拟脱敏警务数据集
python labs/generate_mock_data.py

# 2. 运行第 1 夜带练：监控误报过滤与路口绿信比配时诊断
python labs/session1_traffic_monitor/analyze_traffic_and_alerts.py

# 3. 运行第 2 夜带练：洗钱过渡卡识别、窝点同 IP 与话单上线碰撞
python labs/session2_crime_investigation/laundering_and_call_detector.py

# 4. 运行第 3 夜带练：110“防民转刑”重复报警挖掘 + 自动生成离线可视化态势大屏
python labs/session3_bigdata_reapplication/alert_110_mining_and_dashboard.py
```
运行完第 4 步后，直接双击打开 [`labs/session3_bigdata_reapplication/dashboard_demo.html`](./labs/session3_bigdata_reapplication/dashboard_demo.html) 即可全屏展示生成的指挥中心态势大屏！
