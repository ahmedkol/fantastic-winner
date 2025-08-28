@echo off
REM Run all tests for Rona_v5 with Windows venv support

REM If a venv path is provided as first arg, use it; else default to D:\Expand\Ai\venv
set VENV_DIR=%1
if "%VENV_DIR%"=="" set VENV_DIR=D:\Expand\Ai\venv

REM Activate venv if exists
if exist "%VENV_DIR%\Scripts\activate.bat" (
  call "%VENV_DIR%\Scripts\activate.bat"
) else (
  echo Warning: venv not found at %VENV_DIR%\Scripts\activate.bat. Using current Python.
)

REM Move to the script directory
pushd %~dp0

REM Ensure UTF-8 console to avoid encoding issues
chcp 65001 > nul

REM Optional: install requirements
REM python -m pip install -r requirements.txt

python run_all_tests.py

popd