# Tetris

## Run the app

There is no pre-packaged version as of now, so the only way to launch the app is to run its code. This is quite easy though, most likely you already have Python installed in your machine. However you'll need a couple of more things: Tcl/Tk and tkinter. Tcl is a programming language and Tk is its "toolkit" for rapid GUI apps development. Tkinter is nothing else but a Python library, which wraps Tcl/Tk calls into Python objects.

The installation of these components depends on your system. 

### MacOS

Unfortunately Tcl version pre-installed with Mac OS is way too old. Most likely you'll have 8.5.9, but we need something better, like 8.6.14.

The process:

1. Install Tcl/Tk
    1. Start Tcl console `tclsh`
    2. Type `info patchlevel`
        * If you see "8.6.14" (generally speaking 8.6.x), you're good and can skip the rest of Tcl installation.
    3. Run `brew install tcl-tk`
    4. Restart console and check Tcl version again. Expected to be "8.6.14" or above.
2. Install Python-Tk
    1. Run `brew install python-tk`
    2. To check tkinter you might want to use the Python code fragment below
3. Create Python virtual environment (not necessary)
    1. python3 -m venv .venv
    2. source ./.venv/bin/activate
4. Start the app
    1. In terminal window with active virtual environment type `python3 main.py`

```
# Check Tk-interface (expected to return your new Tcl version "8.6.14")
import tkinter
tcl = tkinter.Tcl()
print(tcl.call(“info”, “patchlevel”))
```

### Debian Linux / ChromeOS

1. Check you Python version - type `python` in terminal. Excected to be "3.11" or something above 3.9.
2. Run `sudo apt-get install python3.11-tk` for your Python version ("3.11" here).

Most likely it will be enough. If no, use the MacOS procedure for troubleshooting (check Tcl version, upgrade if necessary, check `tkinter` using the Python code fragment above, re-install if necessary).
