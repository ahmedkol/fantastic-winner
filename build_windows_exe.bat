@echo off
REM Build Windows executables for Rona and tests using external venv

REM If a venv is provided as first arg, use it; else default to D:\Expand\Ai\venv
set VENV_DIR=%1
if "%VENV_DIR%"=="" set VENV_DIR=D:\Expand\Ai\venv

REM Activate venv if it exists
if exist "%VENV_DIR%\Scripts\activate.bat" (
  call "%VENV_DIR%\Scripts\activate.bat"
) else (
  echo Warning: venv not found at %VENV_DIR%\Scripts\activate.bat. Using current Python.
)

REM Move to the script directory
pushd %~dp0

REM Ensure UTF-8 to avoid encoding issues
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM Ensure pyinstaller is available
python -m pip install --upgrade pip pyinstaller | cat

REM Build Rona executable
pyinstaller --noconfirm --clean --onefile --name Rona --add-data "README_EN.md;." run_rona.py | cat

REM Build tests executable
pyinstaller --noconfirm --clean --onefile --name RonaTests run_all_tests.py | cat

REM Restore directory
popd

echo Build finished. Executables in .\dist\