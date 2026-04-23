@echo off
title NAROK
echo Building NAROK UNPUMPER to EXE...
pyinstaller --onefile --console --name "NAROK_Unpumper" --icon=NONE unpumper.py
echo.
echo Done! Check the "dist" folder.
pause