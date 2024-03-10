@echo off

REM Make a directory and copy a file into it
set "directory_name=C:\XMLsender"
set "file_to_copy=schedule_main.exe"
mkdir "%directory_name%"
copy "%file_to_copy%" "%directory_name%"

REM Create a shortcut file in the startup directory
@echo off
set "sourceFilePath=C:\XMLsender\schedule_main.exe" 
set "shortcutName=xmlsender.lnk"
set "startupFolderPath=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

set "shortcutTarget=%sourceFilePath%"
set "shortcutPath=%startupFolderPath%\%shortcutName%"

echo Creating shortcut...
echo Target: %shortcutTarget%
echo Path: %shortcutPath%

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\CreateShortcut.vbs"
echo sLinkFile = "%shortcutPath%" >> "%temp%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\CreateShortcut.vbs"
echo oLink.TargetPath = "%shortcutTarget%" >> "%temp%\CreateShortcut.vbs"
echo oLink.Save >> "%temp%\CreateShortcut.vbs"

cscript /nologo "%temp%\CreateShortcut.vbs"
del "%temp%\CreateShortcut.vbs"

echo Shortcut created successfully.
