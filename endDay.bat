@echo off
if "%1"=="" (
    echo Usage: endDay.bat "Commit Message"
) else (
    git add .
    git commit -m "%1"
    git push origin main
)