# Minimal VHS test for comfydbg (cmd shell)
# Verifies VHS + comfydbg work together under Windows cmd

Output minimal-cmd.gif

Set Shell "cmd"
Set FontSize 16
Set Width 600
Set Height 300
Set Framerate 30
Set TypingSpeed 225ms
Set CursorBlink false

Type "comfydbg version"
Sleep 1s
Enter
Sleep 5s
