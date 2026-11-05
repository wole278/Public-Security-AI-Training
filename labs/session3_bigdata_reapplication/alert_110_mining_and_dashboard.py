#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 3 夜随堂演练脚本：110 接处警非结构化文本“防民转刑”高危重复报警挖掘 & 一键生成离线交互式态势 HTML 大屏
特点：100% 零第三方依赖（仅用 Python 3 标准库），运行后直接在当前目录生成单文件离线大屏 `dashboard_demo.html`。
用法：python labs/session3_bigdata_reapplication/alert_110_mining_and_dashboard.py
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIR = Path(__file__).resolve().parent

# 定义高危风险特征词库与权重（用于非结构化简要案情与处警反馈扫描）
RISK_KEYWORDS = {
    "持械/刀具威胁": (["菜刀", "水果刀", "持刀", "铁棍", "见血", "凶器"], 5),
    "扬言极端/报复": (["同归于尽", "报复", "拼命", "跳楼", "天台边缘"], 4),
    "涉酒滋事": (["喝酒", "酒气", "醉酒", "醒酒"], 2),
    "肢体暴力冲突": (["推搡", "踹门", "砸碎", "砸门", "拉扯", "擦伤流血", "打架"], 3),
    "群体聚集/堵门": (["拉横幅", "堵在", "堵住", "10余名", "12名"], 3),
}


def scan_risk_tags(text: str):
    matched_tags = []
    score = 1
    for tag_name, (words, weight) in RISK_KEYWORDS.items():
        for w in words:
            if w in text:
                matched_tags.append(f"{tag_name}({w})")
                score += weight
                break
    return matched_tags, min(score, 10)


def mine_110_alarms():
    csv_file = DIR / "mock_110_calls.csv"
    by_address = defaultdict(list)
    station_counts = defaultdict(int)
    category_counts = defaultdict(int)

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            full_text = f"{row['brief_text']} {row['feedback_text']}"
            tags, score = scan_risk_tags(full_text)
            record = {
                "id": row["call_id"],
                "time": row["call_time"],
                "station": row["station"],
                "phone": row["caller_phone"],
                "addr": row["standard_addr"],
                "category": row["category"],
                "brief": row["brief_text"],
                "feedback": row["feedback_text"],
                "tags": tags,
                "score": score,
            }
            by_address[row["standard_addr"]].append(record)
            station_counts[row["station"]] += 1
            category_counts[row["category"]] += 1

    high_risk_households = []
    for addr, items in by_address.items():
        items_sorted = sorted(items, key=lambda x: x["time"])
        count = len(items_sorted)
        max_score = max(x["score"] for x in items_sorted)
        all_tags = []
        for x in items_sorted:
            for t in x["tags"]:
                if t not in all_tags:
                    all_tags.append(t)

        # 重复报警 >= 3 次或单次风险极高，纳入红色一级预警
        if count >= 3 or max_score >= 7:
            composite_risk = min(100, count * 18 + max_score * 5)
            high_risk_households.append({
                "addr": addr,
                "station": items_sorted[-1]["station"],
                "phone": items_sorted[-1]["phone"],
                "count": count,
                "max_score": max_score,
                "composite_risk": composite_risk,
                "tags": all_tags,
                "timeline": items_sorted,
                "latest_brief": items_sorted[-1]["brief"],
            })

    high_risk_households.sort(key=lambda x: x["composite_risk"], reverse=True)
    return high_risk_households, station_counts, category_counts


def print_terminal_report(high_risk_households) -> None:
    print("=" * 80)
    print("🚨 【模块一：110 接处警大数据“防民转刑”高危重复报警自动挖掘战报】")
    print("=" * 80)
    print(f"▶ 扫描历史非结构化 110 警情工单，共锁定 【{len(high_risk_households)} 处】 红色一级高危风险点位：\n")

    for idx, h in enumerate(high_risk_households, 1):
        print(f"  🔴 [预警 TOP {idx}] 标准地址：【{h['addr']}】 | 管辖：{h['station']}")
        print(f"     累计报警：{h['count']} 次 | 综合危险指数：{h['composite_risk']} 分 | 识别高危标签：{' / '.join(h['tags'])}")
        print("     矛盾升级时间轴：")
        for step in h["timeline"]:
            tag_str = f" [{' '.join(step['tags'])}]" if step["tags"] else " [初期萌芽]"
            print(f"       - {step['time']} ({step['category']} | 烈度{step['score']}分){tag_str}：{step['brief']}")
        print("     💡 AI 情指行联勤指令：立即下发【红色一级督办单】，指令社区民警会同街道平安办、司法所24小时内上门联合排摸干预！\n")


def generate_html_dashboard(high_risk_households) -> Path:
    out_path = DIR / "dashboard_demo.html"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    rows_html = ""
    for h in high_risk_households:
        badges = "".join(
            f'<span class="tag-badge">{t}</span>' for t in h["tags"]
        )
        timeline_steps = "".join(
            f'<div class="tl-item"><span class="tl-time">{s["time"][5:16]}</span> '
            f'<span class="tl-cat">[{s["category"]}]</span> {s["brief"]}</div>'
            for s in h["timeline"]
        )
        rows_html += f"""
        <tr>
          <td><div class="addr-title">{h['addr']}</div><div class="sub-meta">{h['station']} · 报警电话 {h['phone']}</div></td>
          <td class="center"><span class="count-pill">{h['count']} 次</span></td>
          <td class="center"><span class="score-pill">{h['composite_risk']} 分</span></td>
          <td>{badges}</td>
          <td><div class="tl-box">{timeline_steps}</div></td>
          <td><span class="action-status">已派发社区民警+司法所24h联勤包干</span></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>上海市某区公安分局 · AI 智慧情指行与大数据态势研判大屏（离线演示版）</title>
<style>
  :root {{
    --bg-dark: #060b19;
    --card-bg: #0d162d;
    --card-border: #1e3264;
    --accent-cyan: #00f5d4;
    --accent-blue: #3a86ff;
    --accent-red: #ff4d4f;
    --accent-amber: #ffbe0b;
    --text-main: #e2eafc;
    --text-muted: #8d99ae;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: radial-gradient(circle at top, #102048 0%, var(--bg-dark) 70%);
    color: var(--text-main);
    font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
    min-height: 100vh;
    padding: 18px 24px;
  }}
  header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--card-border);
    padding-bottom: 14px;
    margin-bottom: 18px;
  }}
  .title-box h1 {{
    font-size: 24px;
    letter-spacing: 1.5px;
    background: linear-gradient(90deg, #ffffff, var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .title-box p {{ color: var(--text-muted); font-size: 13px; margin-top: 4px; }}
  .badge-live {{
    background: rgba(0, 245, 212, 0.12);
    border: 1px solid var(--accent-cyan);
    color: var(--accent-cyan);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 18px;
  }}
  .kpi-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
  }}
  .kpi-card::before {{
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0; width: 4px;
    background: var(--accent-cyan);
  }}
  .kpi-card.danger::before {{ background: var(--accent-red); }}
  .kpi-label {{ color: var(--text-muted); font-size: 13px; }}
  .kpi-val {{ font-size: 30px; font-weight: 700; margin: 6px 0; color: #fff; }}
  .kpi-sub {{ font-size: 12px; color: var(--accent-cyan); }}
  .kpi-card.danger .kpi-sub {{ color: var(--accent-red); }}
  .main-grid {{
    display: grid;
    grid-template-columns: 1.1fr 1.9fr;
    gap: 18px;
  }}
  .panel {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 18px;
  }}
  .panel h2 {{
    font-size: 16px;
    color: var(--accent-cyan);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .bar-row {{ margin-bottom: 12px; }}
  .bar-head {{ display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; }}
  .bar-track {{ background: #162447; height: 10px; border-radius: 6px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 6px; background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)); }}
  .bar-fill.warn {{ background: linear-gradient(90deg, #ff9f1c, var(--accent-red)); }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th, td {{ padding: 11px 10px; border-bottom: 1px solid #1a2a52; text-align: left; vertical-align: top; }}
  th {{ color: var(--accent-cyan); background: rgba(30, 50, 100, 0.35); font-weight: 600; }}
  .center {{ text-align: center; }}
  .addr-title {{ font-weight: 700; color: #fff; font-size: 14px; }}
  .sub-meta {{ color: var(--text-muted); font-size: 12px; margin-top: 3px; }}
  .count-pill {{ background: rgba(255, 77, 79, 0.2); border: 1px solid var(--accent-red); color: #ff7875; padding: 3px 9px; border-radius: 12px; font-weight: 700; display: inline-block; }}
  .score-pill {{ background: var(--accent-red); color: #fff; padding: 3px 9px; border-radius: 12px; font-weight: 700; display: inline-block; }}
  .tag-badge {{ display: inline-block; background: rgba(255, 190, 11, 0.15); border: 1px solid var(--accent-amber); color: var(--accent-amber); padding: 2px 7px; border-radius: 4px; font-size: 11px; margin: 2px 4px 2px 0; }}
  .tl-box {{ font-size: 12px; line-height: 1.55; color: #cbd5e1; }}
  .tl-item {{ margin-bottom: 4px; }}
  .tl-time {{ color: var(--accent-cyan); font-family: monospace; }}
  .tl-cat {{ color: var(--accent-amber); }}
  .action-status {{ display: inline-block; background: rgba(0, 245, 212, 0.12); border: 1px solid var(--accent-cyan); color: var(--accent-cyan); padding: 4px 8px; border-radius: 6px; font-size: 12px; }}
  .insight-list li {{ margin-bottom: 10px; line-height: 1.6; font-size: 13.5px; list-style: none; padding-left: 14px; border-left: 3px solid var(--accent-blue); }}
  .insight-list strong {{ color: var(--accent-cyan); }}
</style>
</head>
<body>
  <header>
    <div class="title-box">
      <h1>🛡️ 上海市某区公安分局 · AI 智慧情指行与警务大数据态势研判大屏</h1>
      <p>数据安全等级：全脱敏仿真演示数据（100% 离线单文件零依赖生成） | 统计刷新时间：{now_str}</p>
    </div>
    <div class="badge-live">● 内网离线引擎运行正常 · 第3夜实战演练生成产物</div>
  </header>

  <section class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">本周全区 110 接报总警情（起）</div>
      <div class="kpi-val">1,428</div>
      <div class="kpi-sub">▼ 环比上周下降 6.2% | 社会面总体平稳</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">监控大模型（VLM）告警误报剔除率</div>
      <div class="kpi-val">84.5%</div>
      <div class="kpi-sub">▲ 每日为图侦辅警节约 4.5 小时无效消警时间</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">早高峰重点路口绿信比 AI 优化点位</div>
      <div class="kpi-val">12 处</div>
      <div class="kpi-sub">▲ 核心干道排队长度平均缩短 19.4%</div>
    </div>
    <div class="kpi-card danger">
      <div class="kpi-label">“防民转刑”高危重复报警一级预警户</div>
      <div class="kpi-val">{len(high_risk_households)} 户</div>
      <div class="kpi-sub">⚠️ 含涉酒/持械/扬言报复苗头 · 已100%生成督办单</div>
    </div>
  </section>

  <section class="main-grid">
    <div>
      <div class="panel">
        <h2><span>📊 重点路口早高峰饱和度与配时失衡监控</span><span>AI 信号配时诊断</span></h2>
        <div class="bar-row">
          <div class="bar-head"><span>世纪大道-杨高南路(东向西) · 车速 11.2km/h</span><span style="color:#ff4d4f">饱和度 98.3% (建议+10秒绿灯)</span></div>
          <div class="bar-track"><div class="bar-fill warn" style="width:98%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-head"><span>中山北路-共和新路(北向南) · 车速 9.8km/h</span><span style="color:#ff4d4f">饱和度 98.5% (建议+12秒绿灯)</span></div>
          <div class="bar-track"><div class="bar-fill warn" style="width:98.5%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-head"><span>金沙江路-真北路(西向东) · 车速 12.6km/h</span><span style="color:#ffbe0b">饱和度 97.4% (大车占比15%)</span></div>
          <div class="bar-track"><div class="bar-fill warn" style="width:97%"></div></div>
        </div>
        <div class="bar-row">
          <div class="bar-head"><span>世纪大道-杨高南路(北向南) · 绿灯空放相位</span><span style="color:#00f5d4">饱和度 26.0% (可核减绿信比)</span></div>
          <div class="bar-track"><div class="bar-fill" style="width:26%"></div></div>
        </div>
      </div>

      <div class="panel">
        <h2><span>🧠 AI 自动生成：本周情指行三大研判结论与用警建议</span></h2>
        <ul class="insight-list">
          <li><strong>1. 严防婚恋/邻里矛盾“民转刑”升级：</strong>AI 文本挖掘发现【宁康苑12号301室】与【云景花园5号402室】在近1个月内连续报警3~4次，且风险词从“口角”升级至“醉酒踹门、持刀威胁、头部流血”，已触发红色熔断，请治安支队督导辖区派出所落实所领导包案。</li>
          <li><strong>2. 夜间餐饮聚集区街面屯警精准偏移：</strong>星光夜市每周五、周六 22:00-24:00 涉酒推搡与外卖违停警情占全天 68%，建议将该时段步巡组与交警铁骑驻点前移至地铁3号口与烧烤街中段。</li>
          <li><strong>3. 跑分洗钱案件跨警种合成作战：</strong>经侦/刑侦流水碰撞脚本本周识别出同一窝点 IP（114.88.201.99）操控多张过渡卡及神秘上线号码（139****9999），已移交网安与技侦支队开展落地收网。</li>
        </ul>
      </div>
    </div>

    <div>
      <div class="panel">
        <h2>
          <span>🚨 110 非结构化警情深度挖掘：“防民转刑 & 群体性苗头”高危重复报警督办表</span>
          <span style="font-size:12px;color:#ff7875;">AI 自动聚合自由文本 · 按风险指数排序</span>
        </h2>
        <table>
          <thead>
            <tr>
              <th style="width:19%">高危标准地址 / 管辖</th>
              <th style="width:9%" class="center">报警频次</th>
              <th style="width:10%" class="center">风险指数</th>
              <th style="width:18%">AI 提取高危升级标签</th>
              <th style="width:29%">历史警情升级时间轴（自动串联）</th>
              <th style="width:15%">联勤处置状态</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
      </div>
    </div>
  </section>
</body>
</html>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return out_path


if __name__ == "__main__":
    high_risk, _, _ = mine_110_alarms()
    print_terminal_report(high_risk)
    html_file = generate_html_dashboard(high_risk)
    print("=" * 80)
    print(f"🎉 离线可视化态势汇报大屏已自动生成：{html_file}")
    print("👉 请直接在资源管理器中双击打开 `dashboard_demo.html` 全屏体验汇报效果！")
    print("=" * 80)
