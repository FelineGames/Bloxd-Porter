@echo off
chcp 65001 >nul
title 🟩 Texture Conversion Utility - Minecraft → Bloxd
color 0A
setlocal enabledelayedexpansion

echo ===========================================================
echo             Minecraft → Bloxd Texture Converter
echo ===========================================================
echo.

:: Check if "textures" folder exists
if not exist "textures" (
    echo [ERROR] "textures" folder not found in this directory.
    echo Please make sure your folder is named exactly 📁 "textures".
    pause
    exit /b
)

:: Check if whitelist.txt exists
if not exist "whitelist.txt" (
    echo [ERROR] whitelist.txt not found.
    echo Please place 📄 whitelist.txt in the same folder as this .bat file.
    pause
    exit /b
)

:: Create destination folder
set "output=bloxd_textures"
if not exist "%output%" mkdir "%output%"

echo.
echo --- Starting Conversion ---
echo.

:: Read whitelist.txt line by line
for /f "tokens=1,2 delims==" %%A in (whitelist.txt) do (
    set "source=%%A"
    set "dest=%%B"

    :: Use call + delayed expansion to safely handle copied flag
    call :ProcessFile
)

echo.
echo --- Conversion Complete! ---
echo All converted files are now inside "%output%" folder.
pause
exit /b

:ProcessFile
set "copied="
for %%P in (
    "textures\items"
    "textures\blocks"
    "textures\ui"
    "textures\gui"
    "textures\entity"
    "textures\map"
    "textures\painting"
    "textures\misc"
    "textures\environment"
) do (
    if exist "%%~P\!source!" (
        if not defined copied (
            echo Converting: !source! → !dest!
            copy /y "%%~P\!source!" "%output%\!dest!" >nul
            set "copied=1"
        )
    )
)
exit /b
