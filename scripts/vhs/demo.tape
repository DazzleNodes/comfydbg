# VHS demo recording for comfydbg README
# https://github.com/charmbracelet/vhs
#
# Run from ComfyUI project root:
#   PATH=C:\code-ext\ttyd-msvc-dist;%PATH% && vhs scripts/vhs/demo.tape
# Requires: pip install -e . (so comfydbg is importable)
# Note: Must use "cmd" shell on Windows (bash doesn't work under ConPTY)
#
# Post-processing:
#   gifsicle --no-loopcount -O3 docs/images/demo.gif -o docs/images/demo.gif

Output docs/images/demo.gif

Set Shell "cmd"
Set Theme "Dracula"
Set FontSize 22
Set Width 1728
Set Height 1000
Set TypingSpeed 200ms
Set Framerate 28
Set CursorBlink false
Set Padding 20

# -- Scene 1: Version check --
Type "comfydbg version"
Sleep 500ms
Enter
Sleep 4s

# -- Scene 2: Detect workflow from image --
Type "comfydbg detect output/my_image.webp"
Sleep 500ms
Enter
Sleep 5s

# -- Scene 3: Install with rollback from head --
Type "comfydbg install comfyui-frontend-package -U -HN 3"
Sleep 500ms
Enter
Sleep 6s

# -- Scene 4: Start bisect --
Type "comfydbg bisect start"
Sleep 500ms
Enter
Sleep 4s

# Let viewer read output
Sleep 5s
