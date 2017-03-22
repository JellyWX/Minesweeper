import sys
import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]
images =["assets/images/1.png","assets/images/2.png","assets/images/3.png","assets/images/4.png","assets/images/5.png","assets/images/6.png","assets/images/7.png","assets/images/8.png","assets/images/tile.png","assets/images/mark.png","assets/images/mine.png","assets/images/overlay.png","assets/images/overlay_2.png","assets/images/background.png"]

cx_Freeze.setup(
    name="Minesweeper",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":images}},
    executables = executables

)
