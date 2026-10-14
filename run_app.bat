@echo off
setlocal enabledelayedexpansion
title SignatureLab — AI-Assisted Handwritten Signature Comparison

echo ======================================================================
echo    SignatureLab: AI-Assisted Handwritten Signature Comparison
echo    Compare handwritten signatures in seconds.
echo ======================================================================
echo.

:: Detect Python executable
set "PYTHON_EXE="

:: 1. Try standard 'python'
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

:: 2. Try 'py' launcher
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_EXE=py -3"
    goto :PYTHON_FOUND
)

:: 3. Try 'python3'
where python3 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set "PYTHON_EXE=python3"
    goto :PYTHON_FOUND
)

:: 4. Look in default Windows user AppData install path
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
    if exist "%%D\python.exe" (
        set "PYTHON_EXE=%%D\python.exe"
        goto :PYTHON_FOUND
    )
)

:: 5. Look in standard Program Files
for /d %%D in ("%ProgramFiles%\Python3*") do (
    if exist "%%D\python.exe" (
        set "PYTHON_EXE=%%D\python.exe"
        goto :PYTHON_FOUND
    )
)

:PYTHON_NOT_FOUND
echo [ERROR] Python was not found on this computer.
echo.
echo To run SignatureLab, please install Python (version 3.10 or newer):
echo   1. Visit https://www.python.org/downloads/
echo   2. Download the Windows installer.
echo   3. IMPORTANT: Make sure to check the box "Add python.exe to PATH" during installation.
echo   4. Once installed, double-click this file (run_app.bat) again.
echo.
pause
exit /b 1

:PYTHON_FOUND
echo [INFO] Using Python: %PYTHON_EXE%
echo [INFO] Launching universal runner (run.py)...
echo.

%PYTHON_EXE% run.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [NOTE] SignatureLab exited with code %ERRORLEVEL%.
    pause
)
