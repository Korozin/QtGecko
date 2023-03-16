# QtGecko

QtGecko aims to be an open-sourced implementation of [JGecko U](github.com/bullywiiplaza/JGeckoU/) in Python using the Qt5 Framework.  
This project is by no means finished, and is a _MAJOR_ work in progress.

## Requirements
- [lxml](https://pypi.org/project/lxml/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [configparser](https://pypi.org/project/configparser/)  

All other dependencies should already be installed with the base Python package, but I'll list them anyway just in case they aren't.
- [re](https://docs.python.org/3/library/re.html)
- [os](https://docs.python.org/3/library/os.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [math](https://docs.python.org/3/library/math.html)
- [socket](https://docs.python.org/3/library/socket.html)
- [struct](https://docs.python.org/3/library/struct.html)
- [base64](https://docs.python.org/3/library/base64.html)
- [traceback](https://docs.python.org/3/library/traceback.html)
- [webbrowser](https://docs.python.org/3/library/webbrowser.html)  

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
- GUI Themes
- And I plan to add more!

## Images

#### Main Menu
<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/MainApp.png">  

#### Code Editor
<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/CodeEditor.png" width="250px" height="240px">  

#### Conversion Example
<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/Conversions.png" width="250px" height="240px">  

#### Error Handling example
<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/ErrorHandling.png" width="250px" height="240px">  

## License

All released under the [MIT](https://github.com/Korozin/QtGecko/blob/master/LICENSE) License

> **Warning**  
This is a reproduction of JGeckoU  
I in no way take credit for the original product.