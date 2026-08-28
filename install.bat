@echo off
REM  Wolkskool content pipeline — double-click this.
REM
REM  It only exists so nobody has to know about PowerShell execution policy or
REM  administrator rights. It re-launches itself elevated if needed, then hands
REM  over to install.ps1, which does the actual work.

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Asking for administrator rights, needed to install Tesseract and Poppler...
    powershell -NoProfile -Command "Start-Process -Verb RunAs -FilePath '%~f0'"
    exit /b
)

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"

echo.
pause
