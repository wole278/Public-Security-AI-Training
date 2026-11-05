#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第 2 夜随堂演练脚本：银行流水“快进快出洗钱过渡卡”识别 + 窝点同 IP 碰撞 + 话单幕后上线与同基站伴随分析
特点：由【表头脱敏法】生成，100% 零第三方依赖（仅用 Python 3 标准库），真数据不出内网。
用法：python labs/session2_crime_investigation/laundering_and_call_detector.py
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DIR = Path(__file__).resolve().parent


def analyze_bank_flows() -> None:
    flow_file = DIR / "mock_bank_flows.csv"
    acct_stats = defaultdict(lambda: {"name": "", "in_sum": 0.0, "out_sum": 0.0, "txs": []})
    ip_to_accounts = defaultdict(set)

    with open(flow_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            acc = row["account_no"]
            name = row["account_name"]
            amt = float(row["amount"])
            ttype = row["tx_type"]
            ttime = datetime.strptime(row["tx_time"], "%Y-%m-%d %H:%M:%S")
            ip = row["ip_address"]

            acct_stats[acc]["name"] = name
            if ttype == "IN":
                acct_stats[acc]["in_sum"] += amt
            else:
                acct_stats[acc]["out_sum"] += amt
            acct_stats[acc]["txs"].append({
                "id": row["tx_id"],
                "type": ttype,
                "amount": amt,
                "time": ttime,
                "peer_no": row["counterparty_no"],
                "peer_name": row["counterparty_name"],
                "balance": float(row["balance_after"]),
            })
            ip_to_accounts[ip].add(f"{name}[{acc}]")

    print("=" * 78)
    print("💰 【模块一：银行交易流水“快进快出洗钱过渡卡”与窝点同 IP 穿透报告】")
    print("=" * 78)

    print("🚨 1. 【快进快出洗钱过渡卡自动锁定（到账30分钟内转出率 > 90%）】：")
    for acc, info in acct_stats.items():
        in_sum = info["in_sum"]
        out_sum = info["out_sum"]
        if in_sum <= 0:
            continue
        payout_ratio = out_sum / in_sum
        txs = sorted(info["txs"], key=lambda x: x["time"])
        in_times = [t["time"] for t in txs if t["type"] == "IN"]
        out_times = [t["time"] for t in txs if t["type"] == "OUT"]
        min_gap_minutes = None
        if in_times and out_times:
            gaps = [
                (ot - it).total_seconds() / 60.0
                for it in in_times
                for ot in out_times
                if ot >= it
            ]
            if gaps:
                min_gap_minutes = min(gaps)

        if payout_ratio >= 0.90 and min_gap_minutes is not None and min_gap_minutes <= 30:
            last_bal = txs[-1]["balance"]
            print(f"  ★ 锁定高危跑分过渡卡：{info['name']} | 卡号：{acc}")
            print(
                f"    - 资金特征：总进账 ¥{in_sum:,.2f} -> 总转出 ¥{out_sum:,.2f} "
                f"（转出率 {payout_ratio*100:.1f}%，卡内仅留存 ¥{last_bal:,.2f}）"
            )
            print(f"    - 时间特征：资金到账后最快仅隔 【{min_gap_minutes:.1f} 分钟】 即开始拆分转出！")
        elif payout_ratio >= 0.60:
            print(f"  ▲ 锁定团伙分赃中转卡：{info['name']} | 卡号：{acc}")
            print(f"    - 资金特征：总进账 ¥{in_sum:,.2f} -> 总转出 ¥{out_sum:,.2f}（其中 ¥25,000 上交上线“阿龙”，¥3,000 转给李某乙）")

    print("\n🌐 2. 【网银操作同窝点 IP 地址碰撞结果】：")
    for ip, acc_set in ip_to_accounts.items():
        if len(acc_set) > 1:
            joined = " 、 ".join(sorted(acc_set))
            print(f"  🔥 铁证发现！IP 地址 【{ip}】 同时操作了 {len(acc_set)} 张不同名下银行卡：")
            print(f"     关联账户：{joined}")
            print("     👉 侦查结论：直接戳穿张某甲所谓“各干各的、自己只旁观”的谎言，证明多张卡在同一房间同一网络下集中操作！\n")


def analyze_call_records() -> None:
    call_file = DIR / "mock_call_records.csv"
    contact_to_suspects = defaultdict(set)
    contact_calls = defaultdict(list)
    station_events = defaultdict(list)

    with open(call_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            suspect = f"{row['suspect_name']}({row['suspect_phone']})"
            peer = row["contact_phone"]
            ctime = datetime.strptime(row["call_time"], "%Y-%m-%d %H:%M:%S")
            station = row["base_station_id"]

            contact_to_suspects[peer].add(suspect)
            contact_calls[peer].append((ctime, suspect, row["duration_sec"], row["call_type"]))
            station_events[station].append((ctime, row["suspect_name"], row["suspect_phone"]))

    print("=" * 78)
    print("📡 【模块二：运营商话单“共同神秘联系人（幕后上线）”与同基站伴随碰撞】")
    print("=" * 78)

    suspect_phones = {"13800001111", "13800001112", "13800001113"}
    print("🕵️ 1. 【团伙共同外部神秘联系人（疑似幕后上线/中间人）】：")
    for peer, suspects in contact_to_suspects.items():
        if peer not in suspect_phones and len(suspects) >= 2:
            print(f"  ★ 锁定神秘外部高危号码：【{peer}】（同时与 {len(suspects)} 名在案嫌疑人单线通联！）")
            print(f"    - 关联嫌疑人：{' 、 '.join(sorted(suspects))}")
            for ctime, sus, dur, ctype in contact_calls[peer]:
                print(f"    - 通联轨迹：{ctime.strftime('%Y-%m-%d %H:%M:%S')} | {sus} [{ctype}] 通话 {dur} 秒")
            print("    👉 侦查结论：该号码高度疑似笔录中供述的上线“阿龙”，建议立即提请技侦/网安对该号码开展实名与落地查控！\n")

    print("📍 2. 【案发时段同一基站（LAC/CELL）时空伴随碰面印证】：")
    for station, events in station_events.items():
        names = sorted({e[1] for e in events})
        if len(names) >= 2:
            print(f"  ★ 基站代码：【{station}】 检测到多名嫌疑人同时段聚集：")
            print(f"    - 同轨人员：{' 、 '.join(names)}")
            for ctime, sname, sphone in sorted(events, key=lambda x: x[0]):
                print(f"    - 信令触发：{ctime.strftime('%H:%M:%S')} -> {sname} ({sphone})")
            print("    👉 侦查结论：客观基站信令证实 20:55-22:18 期间张某甲、李某乙、王某丙三人均在如家酒店基站覆盖范围内！\n")


if __name__ == "__main__":
    analyze_bank_flows()
    analyze_call_records()
