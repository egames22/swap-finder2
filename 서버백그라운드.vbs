Dim fso, dir, batPath, WshShell
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = dir & "\자동배포.bat"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """" & batPath & """", 0, False
