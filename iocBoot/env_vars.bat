@echo off
REM This script extracts the:
REM     PATH to the Python install. On Windows, this is not a system path.
REM     The value of the used Python version makefile variable. It is applied to the executable to be loaded.
set TOP=%~dp0..
set CONFIG_PY=%TOP%\cfg\os\CONFIG_PY.Common.windows-x64
REM https://stackoverflow.com/questions/232747/read-environment-variables-from-file-in-windows-batch-cmd-exe
setlocal EnableDelayedExpansion
for /F "tokens=1,2 delims==" %%i in ('type %CONFIG_PY%') do (
    set rawtoken=%%i
    REM rawtoken still ends with the " :" of the " := " text.
    set token=!rawtoken:~0,-2%!
    set rawvalue=%%j
    REM rawvalue still begins with the " " of the " := " text.
    set value=!rawvalue:~1%!
    if "!token!"=="PY_VER" (
        set PY_VER="!value!"
    )
    if "!token!"=="PY_LIBDIRS" (
        REM remove the "\libs" from the end of the string
        set PYTHON=!value:~0,-5%!
    )
)
REM https://stackoverflow.com/questions/15494688/batch-script-make-setlocal-variable-accessed-by-other-batch-files
endlocal & set PATH=%PYTHON%;C:\Windows & set PY_VER=%PY_VER%
