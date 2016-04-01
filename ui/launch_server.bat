@echo off

cd %~dp0
py -3 tornado_server.py --dashboard
pause