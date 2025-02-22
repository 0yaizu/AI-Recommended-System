@echo off
setlocal

set voicevox_path="C:\Users\OASIS\Desktop\Git\Nojima\AI Recommended System\voicevox_core_windows_cpu\run.exe"
set index_path="C:\Users\OASIS\Desktop\Git\Nojima\AI Recommended System\index.py"
set python_path="C:\Users\OASIS\Desktop\Git\Nojima\AI Recommended System\venv\Scripts\python.exe"

cd %~dp0

echo voicevox running...
echo path: %voicevox_path%
start "" %voicevox_path%

echo server running...
.venv\Scripts\python.exe -m streamlit run index.py

pause