Dim fso, dir, scriptPath, WshShell
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
scriptPath = dir & "\comcigan_proxy.py"
Set WshShell = CreateObject("WScript.Shell")

' py (파이썬 런처) 먼저 시도, 없으면 python
Dim cmd
cmd = "py"
Dim ret
ret = WshShell.Run("py --version", 0, True)
If ret <> 0 Then cmd = "python"

WshShell.Run cmd & " """ & scriptPath & """", 0, False
