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

python ./sandbox/mapper/main.py mapper %device% %port%

endlocal