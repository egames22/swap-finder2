Dim fso, dir, scriptPath, WshShell
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
scriptPath = dir & "\comcigan_proxy.py"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python """ & scriptPath & """", 0, False
