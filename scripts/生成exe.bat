pyinstaller -F .\previewCurve.py --icon=..\icon\icon.ico -w
copy .\dist\previewCurve.exe ..\previewCurve.exe
del *.spec

rd  .\dist /s /q
rd  .\build /s /q
