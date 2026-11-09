@echo off
setlocal enabledelayedexpansion

echo.
echo ==================================================================
echo    CLONE ANY UI (CAU) — Universal Windows Setup
echo ==================================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    where py >nul 2>nul
    if errorlevel 1 (
        echo [ERROR] Python 3 is not installed or not in PATH.
        echo Please install Python 3.10+ from https://python.org
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

echo [1/4] Checking Python version...
%PYTHON_CMD% --version

echo [2/4] Installing Python dependencies...
%PYTHON_CMD% -m pip install --upgrade pip --quiet
%PYTHON_CMD% -m pip install -r requirements.txt --quiet
%PYTHON_CMD% -m pip install -e . --quiet

echo [3/4] Integrating with AI Coding Agents...
set "TARGET_DIR=%~dp0"
if "%TARGET_DIR:~-1%"=="\" set "TARGET_DIR=%TARGET_DIR:~0,-1%"

:: Antigravity
if exist "%USERPROFILE%\.gemini" (
    if not exist "%USERPROFILE%\.gemini\config\skills" mkdir "%USERPROFILE%\.gemini\config\skills"
    xcopy /E /I /Y /Q "%TARGET_DIR%" "%USERPROFILE%\.gemini\config\skills\clone-any-ui" >nul 2>&1
    echo   [+] Configured for Google Antigravity
)

:: Claude Code
if exist "%USERPROFILE%\.claude" (
    if not exist "%USERPROFILE%\.claude\skills" mkdir "%USERPROFILE%\.claude\skills"
    xcopy /E /I /Y /Q "%TARGET_DIR%" "%USERPROFILE%\.claude\skills\clone-any-ui" >nul 2>&1
    echo   [+] Configured for Claude Code
)

:: Cursor
if exist "%USERPROFILE%\.cursor" (
    if not exist "%USERPROFILE%\.cursor\skills" mkdir "%USERPROFILE%\.cursor\skills"
    xcopy /E /I /Y /Q "%TARGET_DIR%" "%USERPROFILE%\.cursor\skills\clone-any-ui" >nul 2>&1
    echo   [+] Configured for Cursor
)

echo [4/4] Installation complete!
echo.
echo ==================================================================
echo   SUCCESS: CLONE ANY UI is ready to use!
echo.
echo   Prompt any AI Agent:
echo     "Clone https://example.com using the clone-any-ui skill"
echo.
echo   Or run from Command Line:
echo     cau --url https://example.com --out ./my-clone --all
echo.
echo   Launch Visual Studio GUI:
echo     cau-studio
echo ==================================================================
echo.
pause
