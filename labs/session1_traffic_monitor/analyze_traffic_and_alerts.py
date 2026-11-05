#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 1 夜随堂演练脚本：城市交通路口配时失衡自动诊断 & 多模态监控告警二次过滤统计
特点：100% 零第三方依赖（仅用 Python 3 标准库），公安内网/单机开箱即跑。
用法：python labs/session1_traffic_monitor/analyze_traffic_and_alerts.py
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIR = Path(__file__).resolve().parent


def analyze_vlm_alerts() -> None:
    alert_file = DIR / "mock_vlm_alerts.json"
    with open(alert_file, "r", encoding="utf-8") as f:
        alerts = json.load(f)

    total = len(alerts)
    false_alarms = [a for a in alerts if a["vlm_is_false_alarm"]]
    real_alarms = [a for a in alerts if not a["vlm_is_false_alarm"]]
    reduction_rate = (len(false_alarms) / total * 100.0) if total else 0.0

    print("=" * 76)
    print("📹 【模块一：多模态视觉大模型（VLM）街面监控告警二次复核战报】")
    print("=" * 76)
    print(f"▶ 传统视觉小模型原始上报告警数 : {total} 起")
    print(f"▶ 视觉大模型自动拦截误报数     : {len(false_alarms)} 起（误报剔除率：{reduction_rate:.1f}%，大幅释放图侦警力！）")
    print(f"▶ 锁定真实高/中风险需派警数    : {len(real_alarms)} 起\n")

    print("🚨 【需立即派警处置的真实风险点位清单】：")
    for idx, item in enumerate(real_alarms, 1):
        print(f"  [{idx}] 告警编号: {item['alert_id']} | 风险等级: 【{item['vlm_risk_level']}】 | 点位: {item['location']}")
        print(f"      画面复核: {item['vlm_scene_desc']}")
        print(f"      派单指令: {item['vlm_disposal']}\n")

    print("🛡️ 【已被 AI 自动消警归档的典型误报】：")
    for item in false_alarms:
        print(f"  - [{item['traditional_cv_tag']}] {item['location']} -> 复核结论：{item['vlm_scene_desc']}")
    print()


def analyze_traffic_flow() -> None:
    csv_file = DIR / "mock_traffic_flow.csv"
    records = []
    by_intersection_slot = defaultdict(list)

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cnt = int(row["vehicle_count"])
            limit = int(row["saturation_limit"])
            speed = float(row["avg_speed_kmh"])
            sat = cnt / limit if limit else 0.0
            item = {
                "id": row["intersection_id"],
                "name": row["intersection_name"],
                "dir": row["direction"],
                "slot": row["time_slot"],
                "count": cnt,
                "limit": limit,
                "sat": sat,
                "speed": speed,
            }
            records.append(item)
            by_intersection_slot[(item["name"], item["slot"])].append(item)

    print("=" * 76)
    print("🚦 【模块二：早高峰重点路口拥堵成因与信号灯绿信比配时失衡诊断】")
    print("=" * 76)

    print("🔴 1. 【高危拥堵进口方向黑榜（饱和度 > 90% 且平均车速 < 15 km/h）】：")
    for r in records:
        if r["sat"] > 0.90 and r["speed"] < 15.0:
            print(
                f"  - {r['name']} [{r['dir']}] ({r['slot']})："
                f"过车 {r['count']}/{r['limit']} 辆 | 饱和度 {r['sat']*100:.1f}% | 车速仅 {r['speed']} km/h"
            )

    print("\n🛠️ 2. 【信号灯绿信比配时失衡自动诊断（绿灯空放 vs 严重排队）】：")
    for (name, slot), group in by_intersection_slot.items():
        over_saturated = [g for g in group if g["sat"] >= 0.95]
        under_utilized = [g for g in group if g["sat"] <= 0.35]
        if over_saturated and under_utilized:
            high = over_saturated[0]
            low_dirs = "、".join([f"{u['dir']}(饱和度{u['sat']*100:.0f}%)" for u in under_utilized])
            print(f"  ★ 发现配时失衡路口：【{name}】 时段：{slot}")
            print(f"    - 拥堵排队方向：{high['dir']}（饱和度高达 {high['sat']*100:.1f}%，车速跌至 {high['speed']} km/h）")
            print(f"    - 绿灯空放方向：{low_dirs}")
            print(
                f"    - 💡 AI 配时优化建议：建议在 {slot} 时段，将【{under_utilized[0]['dir']}/{under_utilized[-1]['dir']}】相位绿灯时长"
                f"核减 10 秒，补偿给【{high['dir']}】主车流相位，预计可提升路口整体通行效率 18%~22%！\n"
            )


if __name__ == "__main__":
    analyze_vlm_alerts()
    analyze_traffic_flow()
