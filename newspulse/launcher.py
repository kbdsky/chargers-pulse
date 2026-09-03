"""Interactive Launcher for LA Chargers NewsPulse."""

import os
import sys
import webbrowser
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Set working directory to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from newspulse.cli import run_generate


def main():
    print("=" * 65)
    print("⚡ [NewsPulse] LA 차저스 최신 뉴스 전수 수집 및 브리핑 생성기")
    print("=" * 65)
    print("🌐 실시간 뉴스를 전수 수집하고 중요도 분석을 시작합니다...\n")

    try:
        run_generate()
    except Exception as e:
        print(f"\n⚠️ 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()

    latest_html = PROJECT_ROOT / "reports" / "chargers_briefing_latest.html"

    if latest_html.exists():
        print(f"\n✨ 브라우저에서 최신 보고서를 엽니다: {latest_html}")
        try:
            webbrowser.open(latest_html.as_uri())
        except Exception:
            os.system(f'start "" "{str(latest_html)}"')
    else:
        print("\n⚠️ 보고서 파일을 찾을 수 없습니다.")

    print("\n" + "-" * 65)
    print(" [1] 🌐 Streamlit 웹 대시보드 실행")
    print(" [2] 📁 보고서 저장 폴더 열기 (Explorer)")
    print(" [3] ❌ 종료")
    print("-" * 65)

    try:
        choice = input("선택 번호를 입력하세요 (엔터 시 종료): ").strip()
        if choice == "1":
            print("\n🌐 Streamlit 웹 대시보드를 실행합니다...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "newspulse/ui/app.py"])
        elif choice == "2":
            reports_dir = PROJECT_ROOT / "reports"
            os.system(f'explorer "{str(reports_dir)}"')
    except Exception:
        pass


if __name__ == "__main__":
    main()
