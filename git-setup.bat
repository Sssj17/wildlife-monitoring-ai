@echo off
echo ================================================
echo Git Setup Helper for Wildlife Monitoring AI
echo ================================================
echo.

echo Checking Git installation...
git --version
if errorlevel 1 (
    echo.
    echo ERROR: Git command not found in PATH
    echo.
    echo You might have GitHub Desktop but not Git CLI.
    echo.
    echo Option 1: Install Git for Windows
    echo   Download: https://git-scm.com/download/win
    echo   After installing, RESTART PowerShell
    echo.
    echo Option 2: Use GitHub Desktop GUI
    echo   Open GitHub Desktop
    echo   File -^> Add Local Repository
    echo   Select this folder
    echo.
    pause
    exit /b 1
)

echo Git found!
echo.

echo ================================================
echo Git Configuration
echo ================================================
echo.

echo Current Git configuration:
git config --global --list

echo.
echo If name and email are not set, run these commands:
echo   git config --global user.name "Your Name"
echo   git config --global user.email "your.email@example.com"
echo.

pause

echo.
echo ================================================
echo Initializing Git Repository
echo ================================================
echo.

if exist ".git" (
    echo Git repository already initialized!
) else (
    echo Initializing new Git repository...
    git init
    echo Git repository created!
)

echo.
echo ================================================
echo Adding Files to Git
echo ================================================
echo.

git add .
echo Files staged for commit

echo.
git status
echo.

pause

echo.
echo ================================================
echo Creating Initial Commit
echo ================================================
echo.

git commit -m "Initial commit - Wildlife Monitoring AI System"

echo.
echo ================================================
echo Next Steps
echo ================================================
echo.
echo 1. Create a repository on GitHub:
echo    - Go to https://github.com
echo    - Click '+' -^> New repository
echo    - Name: wildlife-monitoring-ai
echo    - DO NOT initialize with README
echo    - Click 'Create repository'
echo.
echo 2. After creating, run these commands:
echo    git remote add origin https://github.com/YOUR-USERNAME/wildlife-monitoring-ai.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. When prompted for password, use Personal Access Token:
echo    - GitHub Settings -^> Developer settings -^> Personal access tokens
echo    - Generate new token with 'repo' scope
echo    - Use token as password
echo.
pause
