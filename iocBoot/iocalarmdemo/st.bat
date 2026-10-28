@echo off

REM So previous PATH can be restored.
set OLD_PATH=%PATH%

set PINI="NO"
if not "%1"=="" set PINI=%1

set RVAL="VAL"
if not "%2"=="" set RVAL=%2

REM HASH defaults to # if PINI is NO.
REM It defaults to nothing if PINI is YES.
REM The empty string cannot be used as it creates an empty macro.
if "PINI"=="NO" (set HASH="#") else (set HASH=" ")
if not "%3"=="" set HASH=%3

call ..\env_vars.bat
call dllPath.bat
@echo on
%TOP%\bin\windows-x64\softIocPy%PY_VER%.exe st.cmd

@echo off
set PATH=%OLD_PATH%
