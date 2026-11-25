@echo off
rem Double-click this file after editing any course text.
rem It packs all course files into course\dashboard.html again.
cd /d "%~dp0.."
python course\build_dashboard.py
set "build_status=%errorlevel%"
if not "%build_status%"=="0" (
  echo.
  echo Dashboard build failed. See the error above.
  pause
  exit /b %build_status%
)
echo.
echo Done. Press F5 in the dashboard to see your changes.
pause
