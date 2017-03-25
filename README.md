# Minesweeper
Pygame Minesweeper _for Python Pygame 3.x_

## Running Minesweeper
This game can be run on Linux by executing the executable file `main`. Either do this from a terminal (recommended) by doing `./main` from the directory, or by right-clicking and selecting `run` from the options. On Windows, execute `main.exe` with either a double click or by opening a shell and typing `main.exe` from the directory. On Mac OS X, it can be run with the latest version of Wine. Install Wine and run `main.exe` using Wine. If you want to run it in Python (for debugging or modification), read below:

## Installing Pygame
You can install pygame using `pip3`.

### On Ubuntu:

`sudo apt install python3-pip`

*enter your password*

`sudo pip3 install pygame`

This should work similarly on different distros; just replace `apt install` with your available package manager.

## Running Minesweeper
__Please note this game is not complete and I am aware it is buggy. Put any bugs under the *issues* tab for me to review please.__

```
sudo apt install git
git clone https://github.com/JellyWX/Minesweeper.git -b master
cd Minesweeper/
python3 main.py
```

On Windows systems, you may have to use `python main.py` rather than `python3 main.py`, depending on how you set up your path. You'll also have to manually install `git` and I recommend using the git shell for it. __If it doesn't work, make sure your python version is Python 3 and that you installed Pygame for Python 3__
