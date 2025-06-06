@echo off
echo Computer Use Agent - Portable Setup
echo ===================================
echo.
echo This will install Python and dependencies if needed...
echo.
pause

python install_computer_agent.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python not found. Downloading installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'python_installer.exe'"
    echo Running Python installer...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    echo.
    echo Please restart this installer after Python installation completes.
    pause
    exit
)
