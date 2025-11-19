Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to script directory and run pythonw from venv
WshShell.CurrentDirectory = scriptDir
WshShell.Run "venv\Scripts\pythonw.exe ai_grammar_checker.pyw", 0, False

Set fso = Nothing
Set WshShell = Nothing
