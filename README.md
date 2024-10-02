# Project for MHacks 24
See the devpost [here](https://devpost.com/software/wili-watch)
Project is pending a rewrite - code was written in a weekend with 3 hours of sleep shared among the team (:

## errors
Mostly a note during development. We ran into issues with opening weather/gcal. This fixed that issue.

```
Traceback (most recent call last):
  File "/home/orangepi/mhacks24/main_file.py", line 11, in <module>
    import pyautogui
  File "/home/orangepi/mhacks24/myenv/lib/python3.12/site-packages/pyautogui/__init__.py", line 246, in <module>
    import mouseinfo
  File "/home/orangepi/mhacks24/myenv/lib/python3.12/site-packages/mouseinfo/__init__.py", line 223, in <module>
    _display = Display(os.environ['DISPLAY'])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/orangepi/mhacks24/myenv/lib/python3.12/site-packages/Xlib/display.py", line 80, in __init__
    self.display = _BaseDisplay(display)
                   ^^^^^^^^^^^^^^^^^^^^^
  File "/home/orangepi/mhacks24/myenv/lib/python3.12/site-packages/Xlib/display.py", line 62, in __init__
    display.Display.__init__(*(self, ) + args, **keys)
  File "/home/orangepi/mhacks24/myenv/lib/python3.12/site-packages/Xlib/protocol/display.py", line 129, in __init__
    raise error.DisplayConnectionError(self.display_name, r.reason)
Xlib.error.DisplayConnectionError: Can't connect to display ":0": b'Authorization required, but no authorization protocol specified\n'
```

Fix:
`xhost +local:`
