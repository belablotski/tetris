# tetris

Mac OS:
	1. Install TCL
		a. tclsh
		b. info patchlevel
			i. 8.6.14
		c. brew install tcl-tk
	2. Install Python-Tk
		a. Above
	3. Create virtual environment
		a. python3 -m venv .venv
		b. source ./.venv/bin/activate
	4. Start
		a. Python3 main.py


>>> import tkinter
>>> tcl = tkinter.Tcl()
>>> print(tcl.call(“info”, “patchlevel”))
