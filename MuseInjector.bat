@echo off
setlocal enabledelayedexpansion

set temp_text_file=~Muse_Injector_Temp_Output.txt
set temp_exported_xml=base\sound\soundbanks\pc\muse_injector_working_xml.xml
set path_pck=base\sound\soundbanks\pc\mus.pck
set path_pck_backup=base\sound\soundbanks\pc\mus.pck.backup

TITLE mus.pck Pseudo-Injector
ECHO/
ECHO 	[44;96m                                         [0m 
ECHO 	[44;96m  Terrible mus.pck Pseudo-Injector v1.0  [0m 
ECHO 	[44;96m      by FlavorfulGecko5                 [0m 
ECHO 	[44;96m                                         [0m 
ECHO/
ECHO/

:: Verify FusionTools.exe exists and that it's the correct version
if exist FusionTools.exe ( 
    call :CompareHash FusionTools.exe 8f31f9b30ec39e1cc2c0d6d35d9b3794 0 "You must use FusionTools version [101;93m2.4.2[0m"
) else ( call :Err "Cannot find FusionTools.exe")

:: Perform initial .pck validation/restoration/backup
if not exist %path_pck% (call :Err "Cannot find mus.pck")
if exist %path_pck_backup% (
    echo Restoring mus.pck from vanilla backup file...
    call :CompareHash %path_pck_backup% a56c49f03d43fc2e2f3a4585a5749c85 1 "The backup file is modded or corrupt. Backup file deleted and restoration cancelled."
    del %path_pck%
    copy %path_pck_backup% %path_pck% > NUL
    echo      Restored successfully
) else (
    echo Creating backup of vanilla mus.pck...
    call :CompareHash %path_pck% a56c49f03d43fc2e2f3a4585a5749c85 0 "Cannot create a backup from a modded mus.pck file. Validate game files then retry"
    copy %path_pck% %path_pck_backup% > NUL
    echo      Backup created successfully
)


:: Execute Injection script
echo/
ECHO Injection will begin in 5 seconds.
ECHO [1;31mDO NOT TOUCH YOUR MOUSE AND KEYBOARD UNTIL THIS FINISHES [0m
echo/
timeout /t 5 /nobreak > NUL
python test.py


:: Report success and terminate
echo Injection Successful - You may touch your keyboard and mouse again. 
goto Exit


:Err
echo [101;93mERROR:[0m %~1
echo Injection cancelled due to the above error.
echo/
:Exit
if exist %temp_text_file% (del %temp_text_file%)
if exist %temp_exported_xml% (del %temp_exported_xml%)
pause
exit

:: A Function for comparing a file's real hash to an expected hash
:: %~1 = Filepath
:: %~2 = Expected hash
:: %~3 = If 1, delete the file if validation fails
:: %~4 = Error message to terminate with if the hashes don't match
:CompareHash
certutil -hashfile %~1 MD5 | find /i /v "md5" | find /i /v "certutil" > %temp_text_file%
set /p HashResult=<%temp_text_file%
if %~2 == !HashResult! (
    exit /B 0
) else (
    if %~3 EQU 1 (del %~1)
    call :Err "%~4"
)