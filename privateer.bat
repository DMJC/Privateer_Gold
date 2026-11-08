@echo off
rem Privateer Gemini Gold launcher for Windows: run the engine from the game folder.
cd /d "%~dp0"
start "" "bin\vegastrike-engine.exe" -d. %*
