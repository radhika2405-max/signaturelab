@echo off
title Push SignatureLab to GitHub
echo ======================================================================
echo    Pushing SignatureLab to:
echo    https://github.com/radhika2405-max/signaturelab
echo ======================================================================
echo.

git push -u origin main

echo.
if %ERRORLEVEL% equ 0 (
    echo ======================================================================
    echo    SUCCESS! Code is live on GitHub!
    echo    Repository: https://github.com/radhika2405-max/signaturelab
    echo.
    echo    Deploy to Streamlit Cloud in 1 minute:
    echo    https://share.streamlit.io/deploy?repository=radhika2405-max/signaturelab&branch=main&mainModule=app.py
    echo ======================================================================
) else (
    echo [NOTE] If you haven't created the repository on GitHub yet,
    echo open this link in your browser and click "Create repository":
    echo https://github.com/new?name=signaturelab
)

pause
