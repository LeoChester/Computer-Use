@echo off
cd /d "D:\ComputerUseAgent_Installer"
echo Computer Use Agent - Quick Install
echo ==================================
echo.
echo Installing from D drive...
echo.
if exist "ComputerUseAgent_Portable.zip" (
    echo Extracting portable package...
    powershell -Command "Expand-Archive -Path 'ComputerUseAgent_Portable.zip' -DestinationPath 'C:\ComputerUseAgent' -Force"
    cd /d "C:\ComputerUseAgent"
    call INSTALL.bat
) else (
    echo Running Python installer...
    python install_computer_agent.py
)
echo.
echo Installation complete!
pause
