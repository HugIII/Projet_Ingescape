@echo off

setlocal

if "%~1"=="" (
	set "device=Wi-Fi"
	set "port=5670"
	set "cinematique=True"
)else (
	set "device=%1"
	set "port=%2"
	set "cinematique=%3"
)


start /B python ./sandbox/Engine/main.py Engine %device% %port% %cinematique%
start /B python ./sandbox/Engine_Map/main.py Engine_Map %device% %port%
start /B python ./sandbox/Scorer/main.py Scorer %device% %port%
start /B python ./sandbox/Map/main.py Map %device% %port%
start /B python ./sandbox/Ennemies/main.py Ennemies %device% %port%
start /B python ./sandbox/Weapons/main.py Weapons %device% %port%
start /B python ./sandbox/Screamer/main.py Screamer %device% %port%
start /B python ./sandbox/Starter/main.py Starter %device% %port%
start /B python ./sandbox/Player/main.py Player %device% %port%
start /B python ./sandbox/EventKeyBoard/main.py EventKeyBoard %device% %port%
start /B python ./sandbox/Sound_Manager/main.py Sound_manager %device% %port%
start /B ./sandbox/whiteboard/Whiteboard.exe --device %device% --port %port%

endlocal