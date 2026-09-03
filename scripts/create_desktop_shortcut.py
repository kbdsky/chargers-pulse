"""Create Windows Desktop shortcut for NewsPulse."""

import os
import sys
from pathlib import Path


def create_shortcut():
    desktop = Path(os.environ.get("USERPROFILE", "C:\\Users\\master")) / "Desktop"
    target_bat = Path(__file__).resolve().parent / "launch_and_open.bat"
    working_dir = Path(__file__).resolve().parent.parent

    shortcut_path = desktop / "⚡ LA Chargers 뉴스 브리핑.lnk"

    # Use PowerShell via script or comtypes/win32com
    ps_cmd = f"""
    $WshShell = New-Object -ComObject WScript.Shell;
    $Shortcut = $WshShell.CreateShortcut('{str(shortcut_path)}');
    $Shortcut.TargetPath = '{str(target_bat)}';
    $Shortcut.WorkingDirectory = '{str(working_dir)}';
    $Shortcut.Description = '⚡ LA 차저스 최신 뉴스 전수 수집 및 브리핑 보고서 생성 (NewsPulse)';
    $Shortcut.IconLocation = 'shell32.dll,238';
    $Shortcut.Save();
    """

    import subprocess
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True)
    if shortcut_path.exists():
        print(f"🎉 바탕화면 바로가기 생성 완료: {shortcut_path}")
        return True
    else:
        print(f"⚠️ 바로가기 생성 실패: {result.stderr}")
        return False


if __name__ == "__main__":
    create_shortcut()
