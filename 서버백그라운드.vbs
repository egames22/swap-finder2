Dim fso, dir, scriptPath, WshShell, pyExe, ret
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
scriptPath = dir & "\comcigan_proxy.py"
Set WshShell = CreateObject("WScript.Shell")

pyExe = ""

' py 런처 확인
ret = WshShell.Run("cmd /c where py >nul 2>&1", 0, True)
If ret = 0 Then pyExe = "py"

' python 확인
If pyExe = "" Then
    ret = WshShell.Run("cmd /c where python >nul 2>&1", 0, True)
    If ret = 0 Then pyExe = "python"
End If

' 설치 경로 직접 탐색
If pyExe = "" Then
    Dim localApp, pyFolder
    localApp = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%")
    pyFolder = localApp & "\Programs\Python"
    If fso.FolderExists(pyFolder) Then
        Dim subf
        For Each subf In fso.GetFolder(pyFolder).SubFolders
            If fso.FileExists(subf.Path & "\python.exe") Then
                pyExe = """" & subf.Path & "\python.exe" & """"
                Exit For
            End If
        Next
    End If
End If

If pyExe = "" Then
    MsgBox "Python을 찾을 수 없습니다. python.org에서 설치 후 다시 시도하세요.", 16, "오류"
Else
    WshShell.Run pyExe & " """ & scriptPath & """", 0, False
End If
