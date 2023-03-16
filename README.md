# QtGecko

QtGecko aims to be an open-sourced implementation of [JGecko U](github.com/bullywiiplaza/JGeckoU/) in Python using the Qt5 Framework.  
This project is by no means finished, and is a _MAJOR_ work in progress.

## Requirements
- lxml
- PyQt5  

All other dependencies should already be installed with the base Python package, but I'll list them anyway just in case they aren't.
- re
- os
- sys
- math
- socket
- struct
- base64
- traceback
- webbrowser
- configparser  

All modules can be installed by using `pip install <module_name>`

## How to Run
```cmd
python3 QtGecko.py
```

## Working features!
- Automatic XML and Config parsing
- Adding and Deleting code(s) to <file_name>.xml
- Data-Type Conversions
- TCP Socket connection
- Code sending via TCP Connection (This still needs more testing from users as I'm unable to do so myself)
- Connection timeouts
- Export and Import of GCTU Files
- Code Tile searching (I.E: You can jump to a code's position in the GUI based on it's name)
- Clean GUI Error handling
- CLI Logging
- And I plan to add more!
