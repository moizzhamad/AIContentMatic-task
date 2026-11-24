@echo off
title QuantumTrade - Virtual Stock Trading Platform
echo =================================================================
echo        QuantumTrade - Virtual Stock Trading Simulator
echo =================================================================
echo.

set PYTHON_CMD=python
python --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )
)

echo Installing requirements (if needed)...
"%PYTHON_CMD%" -m pip install -r backend\requirements.txt
echo.
echo Launching unified platform...
"%PYTHON_CMD%" run.py
pause
