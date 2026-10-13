@echo off
rem Double-click this file after editing any course text.
rem It packs all course files into course\dashboard.html again.
cd /d "%~dp0.."
python course\build_dashboard.py
echo.
echo Done. Press F5 in the dashboard to see your changes.
pause
