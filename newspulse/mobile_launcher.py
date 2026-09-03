"""Mobile PWA Server Launcher with automatic Cloudflare Public Tunnel and QR Code.
Allows smartphone access from anywhere in the world on LTE/5G without sharing a Wi-Fi router.
"""

import os
import sys
import time
import socket
import logging
import threading
import subprocess
import re
import uvicorn
import qrcode

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CLOUDFLARED_PATH = os.path.join(os.getcwd(), "cloudflared.exe")


def start_cloudflare_tunnel(port: int = 8000) -> tuple[subprocess.Popen, str]:
    """Start cloudflared quick tunnel and extract public HTTPS URL."""
    if not os.path.exists(CLOUDFLARED_PATH):
        return None, ""

    try:
        proc = subprocess.Popen(
            [CLOUDFLARED_PATH, "tunnel", "--url", f"http://localhost:{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        tunnel_url = ""
        t0 = time.time()
        while time.time() - t0 < 12:
            line = proc.stderr.readline()
            if not line:
                time.sleep(0.2)
                continue
            m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if m:
                tunnel_url = m.group(0)
                break

        return proc, tunnel_url
    except Exception as e:
        print(f"(터널 생성 안내: {e})", flush=True)
        return None, ""


def get_local_ip() -> str:
    """Detect local LAN IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def print_banner(public_url: str, local_ip: str, port: int):
    active_url = public_url if public_url else f"http://{local_ip}:{port}"

    print("\n" + "=" * 65, flush=True)
    print("📱 [NewsPulse Mobile] LA 차저스 모바일 앱 (전 세계 어디서든 접속)", flush=True)
    print("=" * 65, flush=True)
    if public_url:
        print(f"🌍 [LTE / 5G / 외부 어디서나 접속 주소 (HTTPS)]:", flush=True)
        print(f"   👉 {public_url}", flush=True)
    print(f"💻 [PC 로컬 접속 주소]: http://localhost:{port}", flush=True)
    print("-" * 65, flush=True)
    print("📲 스마트폰 연결 및 앱 설치 방법:", flush=True)
    print("  1. 공유기 연결 필요 없음! LTE, 5G, 외부 어디서든 연결 가능합니다.", flush=True)
    print("  2. 스마트폰 카메라로 아래 QR 코드를 스캔하세요.", flush=True)
    print("  3. 열린 화면 상단의 [설치] 버튼을 누르면 스마트폰 앱으로 설치됩니다!", flush=True)
    print("-" * 65, flush=True)

    try:
        qr = qrcode.QRCode()
        qr.add_data(active_url)
        qr.print_ascii(invert=True)
    except Exception as e:
        print(f"(QR 코드 생성 생략: {e})", flush=True)

    print("=" * 65 + "\n", flush=True)


def main():
    port = int(os.getenv("PORT", 8000))
    local_ip = get_local_ip()

    print("\n⚡ 모바일 보안 터널을 연결하는 중입니다 (LTE/5G 전용 공용 주소 생성 중)...", flush=True)
    tunnel_proc, public_url = start_cloudflare_tunnel(port)

    print_banner(public_url, local_ip, port)

    try:
        # Start uvicorn server
        uvicorn.run(
            "newspulse.mobile.server:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="warning",
        )
    finally:
        if tunnel_proc:
            try:
                tunnel_proc.terminate()
            except Exception:
                pass


if __name__ == "__main__":
    main()
