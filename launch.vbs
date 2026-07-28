Set WShell = CreateObject("WScript.Shell")
WShell.Run "cmd.exe /c run.bat", 0, False
Set WShell = Nothing