@echo off

cd %~dp0
py -3 tornado_server.py --robot roborio-2423-frc.local
pause