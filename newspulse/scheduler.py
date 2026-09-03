"""Automated periodic execution scheduler for NewsPulse."""

import time
import datetime
import argparse
import sys
import os
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from .cli import run_generate


def start_scheduler(interval_days: int = 7, run_immediately: bool = True):
    """Run the report generator periodically every interval_days."""
    print("=" * 65)
    print(f"⏰ [NewsPulse Scheduler] 주간 자동 실행 스케줄러 시작")
    print(f"🔄 실행 주기: {interval_days}일마다 (매주 정기 수집 및 브리핑 생성)")
    print(f"⚡ 첫 실행: {'즉시 실행' if run_immediately else f'{interval_days}일 후'}")
    print("⏹️  종료하려면 Ctrl+C를 누르세요.")
    print("=" * 65 + "\n")

    if run_immediately:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 정기 주간 리포트 생성 시작...")
        try:
            run_generate()
        except Exception as e:
            print(f"⚠️ 리포트 생성 중 오류 발생: {e}")

    interval_seconds = interval_days * 86400

    while True:
        try:
            next_run = datetime.datetime.now() + datetime.timedelta(seconds=interval_seconds)
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⏳ 다음 실행 예정 일시: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(interval_seconds)

            print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 정기 주간 리포트 생성 시작...")
            run_generate()

        except KeyboardInterrupt:
            print("\n🛑 스케줄러가 사용자에 의해 중지되었습니다.")
            break
        except Exception as e:
            print(f"⚠️ 오류 발생 (10분 후 재시도): {e}")
            time.sleep(600)


def main():
    parser = argparse.ArgumentParser(description="NewsPulse Weekly Periodic Scheduler")
    parser.add_argument(
        "--interval-days", "-d",
        type=int,
        default=7,
        help="Execution interval in days (default: 7 for weekly)"
    )
    parser.add_argument(
        "--no-immediate",
        action="store_true",
        help="Do not run immediately on startup"
    )

    args = parser.parse_args()
    start_scheduler(
        interval_days=args.interval_days,
        run_immediately=not args.no_immediate
    )


if __name__ == "__main__":
    main()
