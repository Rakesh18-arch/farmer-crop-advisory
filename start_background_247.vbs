Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strCurDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strCurDir

' Launch unified supervisor in detached background mode (0 = Hidden window, False = Do not wait)
WshShell.Run Chr(34) & strCurDir & "\backend\.venv\Scripts\python.exe" & Chr(34) & " " & Chr(34) & strCurDir & "\unified_server.py" & Chr(34), 0, False
