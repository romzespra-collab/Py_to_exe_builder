@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title Сборка py_to_exe_builder v0.8.3

rem ============================================================
rem  build_exe.bat  v0.8.3 — сборка py_to_exe_builder.exe
rem  Результат: dist\py_to_exe_builder.exe
rem ============================================================

echo.
echo === [1/4] Проверка Python ===
set "PY=python"
python --version >nul 2>nul
if errorlevel 1 set "PY=py -3"
%PY% --version
if errorlevel 1 (
    echo ОШИБКА: Python не найден. Установи Python 3.10+ с python.org, галка "Add to PATH".
    pause & exit /b 1
)

echo.
echo === [2/4] Установка библиотек: requirements.txt + PyInstaller ===
%PY% -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: не удалось установить библиотеки из requirements.txt
    pause & exit /b 1
)
%PY% -m pip install --disable-pip-version-check pyinstaller
if errorlevel 1 (
    echo ОШИБКА: не удалось установить PyInstaller
    pause & exit /b 1
)

echo.
echo === [3/4] Сборка PyInstaller: py_to_exe_builder.spec ===
%PY% -m PyInstaller --noconfirm --clean py_to_exe_builder.spec
if errorlevel 1 (
    echo ОШИБКА: PyInstaller завершился с ошибкой — смотри вывод выше.
    pause & exit /b 1
)
if not exist "dist\py_to_exe_builder.exe" (
    echo ОШИБКА: dist\py_to_exe_builder.exe не создан.
    pause & exit /b 1
)

echo.
echo === [4/4] Самопроверка: dist\py_to_exe_builder.exe --selftest ===
if exist "dist\selftest.txt" del /q "dist\selftest.txt"
start "" /wait "dist\py_to_exe_builder.exe" --selftest
set "RC=%errorlevel%"
if exist "dist\selftest.txt" type "dist\selftest.txt"
if not "%RC%"=="0" (
    echo ОШИБКА: самопроверка не прошла, код %RC%.
    pause & exit /b 1
)

echo.
echo Готово: dist\py_to_exe_builder.exe
pause
exit /b 0
