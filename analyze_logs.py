"""
Log Analysis Script.

Analyzes server_logs.csv to identify performance bottlenecks,
failure patterns (503 errors), hourly trends, and correlations.
"""

import csv
import sys
import statistics
from collections import defaultdict
from typing import Dict, List


def pearson_correlation(xs: List[float], ys: List[float]) -> float:
    """Calculate Pearson correlation coefficient between two lists."""
    n = len(xs)
    if n < 2:
        return 0.0
    mean_x = statistics.mean(xs)
    mean_y = statistics.mean(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = (
        sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys)
    ) ** 0.5
    return numerator / denominator if denominator != 0 else 0.0


def analyze(file_path: str) -> None:
    print(f"Analyzing {file_path}...")

    endpoint_stats: Dict[str, Dict[str, List]] = defaultdict(
        lambda: {"response_times": [], "db_queries": [], "status_codes": []}
    )
    hourly_routes: Dict[int, Dict[str, List]] = defaultdict(
        lambda: {"response_times": [], "db_queries": [], "status_codes": []}
    )
    error_rows: List[dict] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                count += 1
                try:
                    endpoint = row["endpoint"]
                    resp_time = float(row["response_time_ms"])
                    db_queries = int(row["db_queries"])
                    status = int(row["status_code"])
                    timestamp = row["timestamp"]

                    endpoint_stats[endpoint]["response_times"].append(resp_time)
                    endpoint_stats[endpoint]["db_queries"].append(db_queries)
                    endpoint_stats[endpoint]["status_codes"].append(status)

                    # Track hourly stats for /api/routes
                    if endpoint == "/api/routes":
                        hour = int(timestamp.split(" ")[1].split(":")[0])
                        hourly_routes[hour]["response_times"].append(resp_time)
                        hourly_routes[hour]["db_queries"].append(db_queries)
                        hourly_routes[hour]["status_codes"].append(status)

                    # Track error rows
                    if status >= 400:
                        error_rows.append(row)

                except (ValueError, KeyError):
                    continue

        print(f"Processed {count} log entries.\n")

        # --- 1. Summary per Endpoint ---
        print("=" * 60)
        print("1. SUMMARY PER ENDPOINT")
        print("=" * 60)
        for endpoint, stats in sorted(endpoint_stats.items()):
            avg_resp = statistics.mean(stats["response_times"])
            max_resp = max(stats["response_times"])
            avg_db = statistics.mean(stats["db_queries"])
            total = len(stats["response_times"])
            errors = sum(1 for s in stats["status_codes"] if s >= 400)

            print(f"\n  Endpoint: {endpoint} ({total} requests)")
            print(f"    Avg Response Time: {avg_resp:.2f} ms")
            print(f"    Max Response Time: {max_resp:.2f} ms")
            print(f"    Avg DB Queries:    {avg_db:.2f}")
            print(f"    Error Count (4xx/5xx): {errors}")

        # --- 2. Error Analysis ---
        print(f"\n{'=' * 60}")
        print("2. ERROR ANALYSIS (HTTP 4xx/5xx)")
        print("=" * 60)
        if error_rows:
            print(f"\n  Total errors found: {len(error_rows)}")
            error_by_endpoint: Dict[str, int] = defaultdict(int)
            for row in error_rows:
                error_by_endpoint[row["endpoint"]] += 1
            for ep, cnt in sorted(error_by_endpoint.items()):
                print(f"    {ep}: {cnt} errors")

            print("\n  Sample error entries:")
            for row in error_rows[:5]:
                print(
                    f"    {row['timestamp']} | {row['endpoint']} | "
                    f"{row['response_time_ms']}ms | HTTP {row['status_code']} | "
                    f"{row['db_queries']} queries"
                )
            if len(error_rows) > 5:
                print(f"    ... and {len(error_rows) - 5} more errors")
        else:
            print("  No errors found in the dataset.")

        # --- 3. Hourly Breakdown for /api/routes ---
        print(f"\n{'=' * 60}")
        print("3. HOURLY BREAKDOWN — /api/routes")
        print("=" * 60)
        print(f"\n  {'Hour':<6} {'Avg Resp(ms)':<15} {'Max Resp(ms)':<15} {'Avg DB':<10} {'Errors':<8} {'Requests':<10}")
        print(f"  {'-'*6} {'-'*14} {'-'*14} {'-'*9} {'-'*7} {'-'*9}")
        for hour in sorted(hourly_routes.keys()):
            h_stats = hourly_routes[hour]
            avg_r = statistics.mean(h_stats["response_times"])
            max_r = max(h_stats["response_times"])
            avg_d = statistics.mean(h_stats["db_queries"])
            errs = sum(1 for s in h_stats["status_codes"] if s >= 400)
            total = len(h_stats["response_times"])
            flag = " <<<< PEAK" if avg_r > 1500 or errs > 0 else ""
            print(f"  {hour:02d}:00  {avg_r:<15.2f}{max_r:<15.2f}{avg_d:<10.2f}{errs:<8}{total:<10}{flag}")

        # --- 4. Correlation ---
        print(f"\n{'=' * 60}")
        print("4. CORRELATION ANALYSIS — /api/routes")
        print("=" * 60)
        if "/api/routes" in endpoint_stats:
            routes_resp = endpoint_stats["/api/routes"]["response_times"]
            routes_db = [float(q) for q in endpoint_stats["/api/routes"]["db_queries"]]

            corr_all = pearson_correlation(routes_db, routes_resp)
            print(f"\n  Overall Pearson Correlation (db_queries vs response_time): {corr_all:.4f}")

            # Separate normal vs peak hours
            normal_resp, normal_db = [], []
            peak_resp, peak_db = [], []
            for hour in hourly_routes:
                h = hourly_routes[hour]
                if 13 <= hour <= 13:
                    peak_resp.extend(h["response_times"])
                    peak_db.extend([float(q) for q in h["db_queries"]])
                else:
                    normal_resp.extend(h["response_times"])
                    normal_db.extend([float(q) for q in h["db_queries"]])

            if len(normal_resp) > 1:
                corr_normal = pearson_correlation(normal_db, normal_resp)
                print(f"  Normal Hours Correlation:  {corr_normal:.4f}")
            if len(peak_resp) > 1:
                corr_peak = pearson_correlation(peak_db, peak_resp)
                print(f"  Peak Hour (13:00) Correlation: {corr_peak:.4f}")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <log_file>")
        sys.exit(1)
    analyze(sys.argv[1])
