# PowerShell script to register Windows Task Scheduler job for NewsPulse Weekly Execution
param (
    [string]$DayOfWeek = "Monday",
    [string]$Time = "09:00",
    [string]$TaskName = "NewsPulse_Chargers_Weekly"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir
$BatFile = Join-Path $ScriptDir "run_weekly.bat"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "⚡ NewsPulse Windows 작업 스케줄러(Weekly) 자동 등록" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📁 실행 배치 파일: $BatFile"
Write-Host "⏰ 실행 주기: 매주 $DayOfWeek $Time"
Write-Host "📌 작업 이름: $TaskName"
Write-Host "------------------------------------------------------------"

try {
    # Check if task already exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "기존 등록된 작업이 있어 업데이트합니다..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    $Action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$BatFile`"" -WorkingDirectory $ProjectDir
    $Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DayOfWeek -At $Time
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "⚡ LA Chargers Weekly News Collection & Briefing Generator"

    Write-Host "`n🎉 Windows 작업 스케줄러 등록이 성공적으로 완료되었습니다!" -ForegroundColor Green
    Write-Host "매주 $DayOfWeek $Time 에 자동으로 뉴스가 전수 수집되고 최신 보고서가 생성됩니다."
}
catch {
    Write-Host "`n⚠️ 스케줄러 등록 중 오류 발생: $_" -ForegroundColor Red
    Write-Host "관리자 권한으로 PowerShell을 실행하거나, 'python -m newspulse.scheduler' 명령어를 사용하세요." -ForegroundColor Yellow
}
