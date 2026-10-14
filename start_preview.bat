@echo off
title SignatureLab — 1-Click Offline Preview
echo ======================================================================
echo    SignatureLab: AI-Assisted Handwritten Signature Comparison
echo    1-Click Offline Preview
echo ======================================================================
echo.

:: Open the client-side Web application in default browser
echo Launching SignatureLab Web Application in your default browser...
start "" "%~dp0index.html"

:: Also offer to launch Python Streamlit server if Python is available
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    echo Python detected. Launching full Python Streamlit studio in background...
    start /b python run.py
)

echo.
echo Preview launched successfully.
pause
