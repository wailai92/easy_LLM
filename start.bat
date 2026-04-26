@echo off

cd /d %~dp0

call venv\Scripts\activate
python main_v2.py

pause