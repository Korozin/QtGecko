# Setup Guide

First load the TCP Gecko installer on your Wii U Console. You can find it either by downloading it [here](github.com/bullywiiplaza/tcpgecko/archive/master.zip), or via the `External Tools` tab in QtGecko.  

After loading TCP Gecko on the Wii U Console and pressing `A`, load into a Game and launch `QtGecko`.

```cmd
python QtGecko.py
```

Once `QtGecko` launches, you should see a menu like this.

<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/StartUp.png">  

Now enter your Wii U's IPv4 Address in the red bar below. Once the IP is Valid, it will turn from Red to Green, and the `Connect` button will turn to its Enabled state.

<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/ConnectionBar.png"> 

Once you press `Connect`, it should show a dialog stating as such and you can proceed with the next step.

<img src="https://github.com/Korozin/QtGecko/blob/main/Assets/ConnectDialog.png"> 

If you didn't have a codelist loaded already, you can either make one by editing your `null.xml` file, which is generated when you first run the program. `null.xml` is always loaded when the application starts, so you can put commonly used codes there to use without needing to load an external list.

Select the checkbox(es) that pretain to the code(s) that you'd like to send, and press `Send Codes`. If that passes without an error, check your game and it _SHOULD_ work.

> Keep in mind that this program is _EXTREMELY_ experimental, and is most likely prone to errors! This is why testing is needed!