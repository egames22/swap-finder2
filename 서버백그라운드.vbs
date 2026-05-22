Dim fso, dir, scriptPath, WshShell, pyExe, localApp
Set fso = CreateObject("Scripting.FileSystemObject")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
scriptPath = dir & "\comcigan_proxy.py"
Set WshShell = CreateObject("WScript.Shell")

pyExe = ""
localApp = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%")

' 1단계: 알려진 경로 직접 확인
Dim directPath
directPath = localApp & "\Python\bin\python.exe"
If fso.FileExists(directPath) Then pyExe = """" & directPath & """"

' 2단계: 표준 설치 경로 탐색
If pyExe = "" Then
    Dim pyFolder
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

' 3단계: PATH 탐색 — WindowsApps(가짜) 제외
If pyExe = "" Then
    Dim tmpFile, line
    tmpFile = localApp & "\Temp\_pyfind.txt"
    WshShell.Run "cmd /c where python 2>nul | findstr /v /i WindowsApps > """ & tmpFile & """", 0, True
    If fso.FileExists(tmpFile) Then
        Dim ts
        Set ts = fso.OpenTextFile(tmpFile, 1)
        Do While Not ts.AtEndOfStream
            line = Trim(ts.ReadLine())
            If line <> "" Then
                pyExe = """" & line & """"
                Exit Do
            End If
        Loop
        ts.Close
        fso.DeleteFile tmpFile
    End If
End If

If pyExe = "" Then
    MsgBox "Python을 찾을 수 없습니다. python.org에서 설치 후 다시 시도하세요.", 16, "오류"
Else
    WshShell.Run pyExe & " """ & scriptPath & """", 0, False
End If
