rem cmd
pushd %~dp0

pylint --output=MyErrors.txt ModTags.py

REM pylint --output-format=colorized ModTags.py
rem pylint --output=MyErrors.txt 
rem "C:\Program Files\Python39\python.exe"-i $(FULL_CURRENT_PATH)
rem > .pylintr
rem Pause