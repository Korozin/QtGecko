if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import sys, PyQt5

html_content = '''<!DOCTYPE html>
<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Type Docs - From BullyWiiPlaza's site</title>
    <script type="text/javascript">
        document.addEventListener('fullscreenchange', function() {
            fullscreen = document.getElementById("fullscreen");

            if (document.fullscreenElement != null) {
                fullscreen.classList.add("fullscreenExit")
            } else {
                fullscreen.classList.remove("fullscreenExit")
            }
        });
    </script>
</head>
<body dir="ltr">
    <div id="mainContent" class="main" role="main">
        <!--Navigation-->
        <div class="sidebar no-select" id="TOC">
            <h2>Memory Writes</h2>
            <ul>
                <li class=""><a href="#00">RAM Writes<span>[00]</span></a></li>
                <li class=""><a href="#01">String Writes<span>[01]</span></a></li>
                <li class=""><a href="#02">Skip Writes<span>[02]</span></a></li>
                <li class=""><a href="#20">Memory Fill<span>[20]</span></a></li>
                <li class=""><a href="#F0">Corruptor<span>[F0]</span></a></li>
            </ul>
            <h2>Logical Operators</h2>
            <ul>
                <li class=""><a href="#03">If equal<span>[03]</span></a></li>
                <li class=""><a href="#04">If not equal<span>[04]</span></a></li>
                <li class=""><a href="#05">If greater<span>[05]</span></a></li>
                <li class=""><a href="#06">If lower<span>[06]</span></a></li>
                <li class=""><a href="#07">If greater or equal<span>[07]</span></a></li>
                <li class=""><a href="#08">If lower or equal<span>[08]</span></a></li>
                <li class=""><a href="#09">Conditional logical AND<span>[09]</span></a></li>
                <li><a href="#0A">Conditional logical OR<span>[0A]</span></a></li>
                <li class=""><a href="#0B">If value between<span>[0B]</span></a></li>
                <li><a href="#0C">Add Time-Dependence<span>[0C]</span></a></li>
                <li><a href="#0D">Reset Timer<span>[0D]</span></a></li>
            </ul>
            <h2>Arithmetic Operators</h2>
            <ul>
                <li class=""><a href="#10">Load Integer<span>[10]</span></a></li>
                <li class=""><a href="#11">Store Integer<span>[11]</span></a></li>
                <li class=""><a href="#12">Load Float<span>[12]</span></a></li>
                <li class=""><a href="#13">Store Float<span>[13]</span></a></li>
                <li class=""><a href="#14">Integer Operations<span>[14]</span></a></li>
                <li class=""><a href="#15">Float Operations<span>[15]</span></a></li>
            </ul>
            <h2>Memory Access</h2>
            <ul>
                <li class=""><a href="#30">Load Pointer<span>[30]</span></a></li>
                <li class=""><a href="#31">Add Offset to Pointer<span>[31]</span></a></li>
            </ul>
            <h2>Execute</h2>
            <ul>
                <li class="focused"><a href="#C0">Execute ASM<span>[C0]</span></a></li>
                <li><a href="#C1">Perform Cafe OS Syscalls<span>[C1]</span></a></li>
            </ul>
            <h2>Termination</h2>
            <ul>
                <li><a href="#D0">Termination<span>[D0]</span></a></li>
                <li><a href="#D1">No Operation<span>[D1]</span></a></li>
                <li><a href="#D2">Timer Termination<span>[D2]</span></a></li>
            </ul>
        </div>
        <div class="wrapper" id="contentPanel">
            <div class="pageEditor no-select hide" id="pageEditor">
                <ul>
                    <li><button title="Zoom In" type="button" onclick="changeFontSize(1)" tabindex="-1"><i class="icon zoomIn"></i></button></li>
                    <li><button title="Zoom Out" type="button" onclick="changeFontSize(-1)" tabindex="-1"><i class="icon zoomOut"></i></button></li>
                    <li><button title="Reset Zoom" type="button" onclick="resetFontSize()" tabindex="-1"><i class="icon zoomReset"></i></button></li>
                    <li><button title="Toggle Fullscreen" type="button" onclick="toggleFullscreen()" id="fullscreen" tabindex="-1"><i class="icon fullscreen"></i></button></li>
                    <li><button title="Go To Top" type="button" onclick="window.location.href='#general'" tabindex="-1"><i class="icon upArrow"></i></button></li>
                </ul>
            </div>
            <!--Content-->
            <div class="content" id="Content">
                <a name="general"></a>
                <div class="container">
                    <h1>General Information <span class="no-select ghost category">TCP Gecko 2.51</span></h1>
                    <p>Cafe codetypes is a feature from TCP Gecko to simplify the making of cheat codes for the Nintendo Wii U.

This documentation breaks down all available cafe codetypes into components, describes what those components do and shows available parameters.
Each component is assigned a letter and color for better visualization how each cafe codetype functions.</p>
                    <table class="demo lined">
                        <thead>
                            <tr class="no-select">
                                <td>Representation</td>
                                <td>Description</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">CC</span></b></code></td>
                                <td><code>cafe codetype</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="pointer">P</span></b></code></td>
                                <td><code>Utalizes a pointer? Yes = 1; No = 0</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="dataSize">S</span></b></code></td>
                                <td><code>Data Size: 8-bit = 0; 16-bit = 1; 32-bit = 2</code></td></tr>
                            <tr>
                                <td><code><b><span class="volatileOffset">KKKK</span></b>, <b><span class="volatileOffset">KKKKKKKK</span></b></code></td>
                                <td><code>Unsigned volatile offset</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="amount">NNNN</span></b>, <b><span class="amount">NNNNNNNN</span></b></code></td>
                                <td><code>Amount of something.</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="offset">QQQQQQQQ</span></b></code></td>
                                <td><code>Signed non-volatile offset.</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="address">LLLLLLLL, EEEEEEEE</span></b></code></td>
                                <td><code>Memory address</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="value">VV</span></b>, <b><span class="value">VVVV</span></b>, <b><span class="value">VVVVVVVV</span></b>, <b><span class="value">WW</span></b>, <b><span class="value">WWWW</span></b>, <b><span class="value">WWWWWWWW</span></b>, <b><span class="value">XXXX</span></b></code></td>
                                <td><code>Value</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="range">RANGE_ST</span></b>, <b><span class="range">RANGE_EN</span></b></code></td>
                                <td><code>Dereference memory address range.<br>Max possible range = 0x10000000 to 0x50000000.</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="varOffset">YY</span></b>, <b><span class="varOffset">YYYY</span></b>, <b><span class="varOffset">YYYYYYYY</span></b>, <b><span class="varOffset">MMMMMMMM</span></b></code></td>
                                <td><code>Offset variable</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="increment">II</span></b>, <b><span class="increment">IIII</span></b>, <b><span class="increment">IIIIIIII</span></b></code></td>
                                <td><code>Incrementer after each memory write.</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="intRegister">R</span></b>, <b><span class="intRegister">S</span></b></code></td>
                                <td><code>Integer register</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="floatRegister">R</span></b>, <b><span class="floatRegister">S</span></b></code></td>
                                <td><code>Float register</code></td>
                            </tr>
                            <tr>
                                <td><code><b><span class="operation">O</span></b></code></td>
                                <td><code>Operation type</code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Letters with washed out colours represent codelines that are required for a cafe codetype to work.</p>
                    <p><i class="icon notice inlineIcon"></i><b> NOTICE</b>: All cafe codetypes follow a specific sequence of Hexadecimal values. Failure to follow the structure of any codetypes may crash the console. Also, accessing or writing to invalid addresses can crash the console. When you crash, you may unplug your Wii U, plug it back in, start your Wii U by pressing the power button and run the TCP Gecko Installer again.</p>
                </div>
                <div class="container">
                    <h1>Q&amp;As <span class="no-select ghost category">TCP Gecko 2.51</span></h1>

                    <h3>What is a pointer?</h3>
                    <blockquote>A pointer is an object in many
programming languages that stores a memory address. A pointer references
 a location in memory, and obtaining the value stored at that location
is known as dereferencing (Load) the pointer.</blockquote>

                    <h3>What is an offset?</h3>
                    <blockquote>An offset within an array or other data
structure object is an integer indicating the distance (displacement)
between the beginning of the object and a given element or point,
presumably within the same object.</blockquote>

                    <h3>What is a "volatile offset"?</h3>
                    <blockquote>A volatile offset is a offset only active within the codetype that requested its use. Following codelines will not be affected.</blockquote>

                    <h3>What is a integer value?</h3>
                    <blockquote>A number which is not a fraction; a whole number.</blockquote>

                    <h3>What is a float value?</h3>
                    <blockquote>A float is a data type composed of a
number that is not an integer, because it includes a fraction
represented in decimal format.</blockquote>

                    <h3>Data sizes *</h3>
                    <blockquote>A 8-bit Hexadecimal value has 256 possible values. (Hex: 0 to FF)
A 16-bit Hexadecimal value has 65'536 possible values. (Hex: 0 to FFFF)
A 32-bit Hexadecimal value has 4'294'967'296 possible values. (Hex: 0 to FFFFFFFF)</blockquote>

                    <h3>Signed vs unsigned value *</h3>
                    <blockquote>Signedness is a property of data types representing numbers in computer programs. For example, a two's complement <u>signed</u> 16-bit integer can hold the values −32768 to 32767 inclusively, while an <u>unsigned</u> 16 bit integer can hold the values 0 to 65535.</blockquote>

                    <h3>What does "two's complement" mean?</h3>
                    <blockquote>Two's complement is a mathematical
operation on binary numbers. It is used in computing as a method of
signed number representation. The two's complement is calculated by
inverting the bits and adding one.</blockquote>

                    <p class="references">* Use a Decimal to Hexadecimal calculator for ease of value convertion.</p>
                </div>
                <div class="container">
                    <h1>Sources <span class="no-select ghost category">TCP Gecko 2.51</span></h1>
                    <p><a href="https://www.techopedia.com/definition/23980/float-computer-science">https://www.techopedia.com/definition/23980/float-computer-science</a>
<a href="https://en.wikipedia.org/wiki/Offset_(computer_science)">https://en.wikipedia.org/wiki/Offset_(computer_science)</a>
<a href="https://en.wikipedia.org/wiki/Signedness">https://en.wikipedia.org/wiki/Signedness</a>
<a href="https://en.wikipedia.org/wiki/Pointer_(computer_programming)">https://en.wikipedia.org/wiki/Pointer_(computer_programming)</a>
<a href="https://en.wikipedia.org/wiki/Two%27s_complement">https://en.wikipedia.org/wiki/Two%27s_complement</a></p>
                </div>
                <a name="00"></a>
                <div class="container">
                    <h1>RAM Writes <b>[00]</b><span class="no-select ghost category">Memory Writes</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">00</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000</b></code></td>
                                <td><code><b><span class="codetype">00</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000</b></code></td>
                                <td><code><b><span class="codetype">00</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">00</span><span class="pointer">1</span><span class="dataSize">0</span><span class="volatileOffset">KKKK</span> 000000<span class="value">VV</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">00</span><span class="pointer">1</span><span class="dataSize">1</span><span class="volatileOffset">KKKK</span> 0000<span class="value">VVVV</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">00</span><span class="pointer">1</span><span class="dataSize">2</span><span class="volatileOffset">KKKK</span> <span class="value">VVVVVVVV</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Writes a 8-bit (<code><b><span class="value">VV</span></b></code>), 16-bit (<code><b><span class="value">VVVV</span></b></code>) or 32-bit (<code><b><span class="value">VVVVVVVV</span></b></code>) value to memory address (<code><b><span class="address">LLLLLLLL</span></b></code>). *
<code><b><span class="volatileOffset">KKKK</span></b></code> adds a unsigned volatile offset to the computed pointer.</p>

                    <p class="references">* Writing value to a pointer must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="01"></a>
                <div class="container">
                    <h1>String Writes <b>[01]</b><span class="no-select ghost category">Memory Writes</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                                <td>Sample 1</td>
                                <td>Sample 2</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">01</span><span class="pointer">0</span>0<span class="amount">NNNN</span> <span class="address">LLLLLLLL</span><br>00000000 000000FF</b></code></td>
                                <td><code><b><span class="codetype">01</span><span class="pointer">0</span>0<span class="amount">0001</span> <span class="address">LLLLLLLL</span><br><span class="value">VV</span>000000 000000FF</b></code></td>
                                <td><code><b><span class="codetype">01</span><span class="pointer">0</span>0<span class="amount">0008</span> <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV VVVVVVVV</span><br>00000000 000000FF</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format (Pointer)</td>
                                <td>Sample 1 (Pointer)</td>
                                <td>Sample 2 (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">01</span><span class="pointer">1</span>0<span class="amount">NNNN</span> <span class="volatileOffset">KKKKKKKK</span><br>00000000 000000FF<span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">01</span><span class="pointer">1</span>0<span class="amount">0001</span> <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VV</span>000000 000000FF<span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">01</span><span class="pointer">1</span>0<span class="amount">0008</span> <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV VVVVVVVV</span><br>00000000 000000FF<span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Writes <code><b><span class="amount">NNNN</span></b></code> amount of bytes (<code><b><span class="value">VV</span></b></code>) to memory address <code><b><span class="address">LLLLLLLL</span></b></code>. If a pointer is in use, a signed volatile offset (<code><b><span class="volatileOffset">KKKKKKKK</span></b></code>) is added to the computed pointer. *
If a codeline is filled, a new line can be added.
To terminate the codetype, the last byte has to end with a value of <code><b>FF</b></code>.</p>

                    <p class="references">* Writing value to a pointer must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>

                </div>
                <a name="02"></a>
                <div class="container">
                    <h1>Skip Writes <b>[02]</b><span class="no-select ghost category">Memory Writes</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">02</span><span class="pointer">0</span><span class="dataSize">0</span><span class="amount">NNNN</span> <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> <span class="varOffset">YYYYYYYY</span><br>000000<span class="increment">II</span> 00000000</b></code></td>
                                <td><code><b><span class="codetype">02</span><span class="pointer">0</span><span class="dataSize">1</span><span class="amount">NNNN</span> <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> <span class="varOffset">YYYYYYYY</span><br>0000<span class="increment">IIII</span> 00000000</b></code></td>
                                <td><code><b><span class="codetype">02</span><span class="pointer">0</span><span class="dataSize">2</span><span class="amount">NNNN</span> <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> <span class="varOffset">YYYYYYYY</span><br><span class="increment">IIIIIIII</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">02</span><span class="pointer">1</span><span class="dataSize">0</span><span class="amount">NNNN</span> <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> <span class="varOffset">YYYYYYYY</span><br>000000<span class="increment">II</span> 00000000<span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">02</span><span class="pointer">1</span><span class="dataSize">1</span><span class="amount">NNNN</span> <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> <span class="varOffset">YYYYYYYY</span><br>0000<span class="increment">IIII</span> 00000000<span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">02</span><span class="pointer">1</span><span class="dataSize">2</span><span class="amount">NNNN</span> <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> <span class="varOffset">YYYYYYYY</span><br><span class="increment">IIIIIIII</span> 00000000<span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Consecutively writes 8-bit (<code><b><span class="value">VV</span></b></code>), 16-bit (<code><b><span class="value">VVVV</span></b></code>) or 32-bit (<code><b><span class="value">VVVVVVVV</span></b></code>) value <code><b><span class="amount">NNNN</span></b></code> amount of times.
Memory writes start at address <code><b><span class="address">LLLLLLLL</span></b></code> or at computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code>. *
<code><b><span class="varOffset">YYYYYYYY</span></b></code> determines the offset between each write.
Integer value <code><b><span class="increment">II</span></b></code> (8-bit), <code><b><span class="increment">IIII</span></b></code> (16-bit), <code><b><span class="increment">IIIIIIII</span></b></code> (32-bit) constantly adds to <code><b><span class="value">VV</span>, <span class="value">VVVV</span>, <span class="value">VVVVVVVV</span></b></code> each write.</p>

                    <p class="references">* Writing value to a pointer must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="20"></a>
                <div class="container">
                    <h1>Memory Fill <b>[20]</b><span class="no-select ghost category">Memory Writes</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">20</span><span class="pointer">0</span>00000 <span class="value">VVVVVVVV</span><br><span class="address">LLLLLLLL</span> <span class="varOffset">MMMMMMMM</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">20</span><span class="pointer">1</span>00000 <span class="value">VVVVVVVV</span><br><span class="volatileOffset">KKKKKKKK</span> <span class="varOffset">MMMMMMMM</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Repeatedly writes a 32-bit value (<code><b><span class="value">VVVVVVVV</span></b></code>) starting at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code>. *
Range between the first and last range is determined by offset <code><b><span class="varOffset">MMMMMMMM</span></b></code>.</p>

                    <p class="references">* Writing value to a pointer must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="F0"></a>
                <div class="container">
                    <h1>Corruptor <b>[F0]</b><span class="no-select ghost category">Memory Writes</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">F0</span>000000 <span class="address">LLLLLLLL</span><br><span class="address">EEEEEEEE</span> <span class="value">VVVVVVVV</span><br><span class="value">WWWWWWWW</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Searches for value <code><b><span class="value">VVVVVVVV</span></b></code> between memory address <code><b><span class="address">LLLLLLLL</span></b></code> to <code><b><span class="address">EEEEEEEE</span></b></code>.
If the value equals to the current inspected memory address, value <code><b><span class="value">WWWWWWWW</span></b></code> will be stored to that address.</p>
                </div>
                <a name="03"></a>
                <div class="container">
                    <h1>If Equal <b>[03]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">03</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">03</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">03</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">03</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">03</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">03</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If both values are equal, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="04"></a>
                <div class="container">
                    <h1>If Not Equal <b>[04]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">04</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">04</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">04</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">04</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">04</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">04</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If both values are not equal, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="05"></a>
                <div class="container">
                    <h1>If Greater <b>[05]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">05</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">05</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">05</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">05</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">05</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">05</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If the value at the computed address is greater than <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="06"></a>
                <div class="container">
                    <h1>If Lower <b>[06]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">06</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">06</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">06</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">06</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">06</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">06</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If the value at the computed address is lower than <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="07"></a>
                <div class="container">
                    <h1>If Greater Or Equal <b>[07]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">07</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">07</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">07</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">07</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">07</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">07</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If the value at the computed address is greater than or equal to <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="08"></a>
                <div class="container">
                    <h1>If Lower Or Equal <b>[08]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">08</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">08</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">08</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">08</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">08</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">08</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If the value at the computed address is lower than or equal to <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="09"></a>
                <div class="container">
                    <h1>Conditional Logical AND <b>[09]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">09</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">09</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">09</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">09</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">09</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">09</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If the value at the computed address has the same true bits as <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="0A"></a>
                <div class="container">
                    <h1>Conditional Logical OR <b>[0A]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">0A</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">0A</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">0A</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">0A</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">0A</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">0A</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> 00000000<span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit). *
If the value at the computed address has at least one true bit as <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="0B"></a>
                <div class="container">
                    <h1>If Value Between <b>[0B]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">0B</span><span class="pointer">0</span><span class="dataSize">0</span>0000 <span class="address">LLLLLLLL</span><br>000000<span class="value">VV</span> 000000<span class="value">WW</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">0B</span><span class="pointer">0</span><span class="dataSize">1</span>0000 <span class="address">LLLLLLLL</span><br>0000<span class="value">VVVV</span> 0000<span class="value">WWWW</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="codetype">0B</span><span class="pointer">0</span><span class="dataSize">2</span>0000 <span class="address">LLLLLLLL</span><br><span class="value">VVVVVVVV</span> <span class="value">WWWWWWWW</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">0B</span><span class="pointer">1</span><span class="dataSize">0</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>000000<span class="value">VV</span> 000000<span class="value">WW</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">0B</span><span class="pointer">1</span><span class="dataSize">1</span>0000 <span class="volatileOffset">KKKKKKKK</span><br>0000<span class="value">VVVV</span> 0000<span class="value">WWWW</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">0B</span><span class="pointer">1</span><span class="dataSize">2</span>0000 <span class="volatileOffset">KKKKKKKK</span><br><span class="value">VVVVVVVV</span> <span class="value">WWWWWWWW</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Compares the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> with value <code><b><span class="value">VV</span></b></code> (8-bit), <code><b><span class="value">VVVV</span></b></code> (16-bit), <code><b><span class="value">VVVVVVVV</span></b></code> (32-bit) and value <code><b><span class="value">WW</span></b></code> (8-bit), <code><b><span class="value">WWWW</span></b></code> (16-bit), <code><b><span class="value">WWWWWWWW</span></b></code> (32-bit). *
If the computed value is between <code><b><span class="value">VV</span></b></code>, <code><b><span class="value">VVVV</span></b></code> or <code><b><span class="value">VVVVVVVV</span></b></code> and value <code><b><span class="value">WW</span></b></code>, <code><b><span class="value">WWWW</span></b></code> or <code><b><span class="value">WWWWWWWW</span></b></code>, codetypes below will be executed.
If the condition is false, codetypes below will be skipped. Codetype <code><b><span class="codetype">D0</span></b></code> determines when to continue code execution.</p>

                    <p class="references">* Comparing a pointer's value must have a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="0C"></a>
                <div class="container">
                    <h1>Add Time-Dependence <b>[0C]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">0C</span>000000 <span class="amount">NNNNNNNN</span><span class="no-select ghost"><br>...<br>D2000000 CAFEBABE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>If global frame counter reaches <code><b><span class="amount">NNNNNNNN</span></b></code> amount of frames, codetypes below will be skipped.
cafe codetype <code><b><span class="codetype">D2</span></b></code> determines when to continue code execution.</p>
                </div>
                <a name="0D"></a>
                <div class="container">
                    <h1>Reset Timer <b>[0D]</b><span class="no-select ghost category">Logical Operators</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">0D</span>00<span class="value">VVVV</span> <span class="address">LLLLLLLL</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Resets global frame counter if value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> is equal to <code><b><span class="value">VVVV</span></b></code>.</p>
                </div>
                <a name="10"></a>
                <div class="container">
                    <h1>Load Integer <b>[10]</b><span class="no-select ghost category">Arithmetic Operations</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">10</span><span class="pointer">0</span><span class="dataSize">0</span>000<span class="intRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                                <td><code><b><span class="codetype">10</span><span class="pointer">0</span><span class="dataSize">1</span>000<span class="intRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                                <td><code><b><span class="codetype">10</span><span class="pointer">0</span><span class="dataSize">2</span>000<span class="intRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">10</span><span class="pointer">1</span><span class="dataSize">0</span>000<span class="intRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">10</span><span class="pointer">1</span><span class="dataSize">1</span>000<span class="intRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">10</span><span class="pointer">1</span><span class="dataSize">2</span>000<span class="intRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Loads the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> into integer register <code><b><span class="intRegister">R</span></b></code>
There are 8 available integer registers: <code><b><span class="intRegister">0</span></b></code>, <code><b><span class="intRegister">1</span></b></code>, <code><b><span class="intRegister">2</span></b></code>, <code><b><span class="intRegister">3</span></b></code>, <code><b><span class="intRegister">4</span></b></code>, <code><b><span class="intRegister">5</span></b></code>, <code><b><span class="intRegister">6</span></b></code> and <code><b><span class="intRegister">7</span></b></code>.</p>
                    <p class="references">* Loading a value from a pointer requires a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="11"></a>
                <div class="container">
                    <h1>Store Integer <b>[11]</b><span class="no-select ghost category">Arithmetic Operations</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit</td>
                                <td>16-bit</td>
                                <td>32-bit</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">11</span><span class="pointer">0</span><span class="dataSize">0</span>000<span class="intRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                                <td><code><b><span class="codetype">11</span><span class="pointer">0</span><span class="dataSize">1</span>000<span class="intRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                                <td><code><b><span class="codetype">11</span><span class="pointer">0</span><span class="dataSize">2</span>000<span class="intRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>8-bit (Pointer)</td>
                                <td>16-bit (Pointer)</td>
                                <td>32-bit (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">11</span><span class="pointer">1</span><span class="dataSize">0</span>000<span class="intRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">11</span><span class="pointer">1</span><span class="dataSize">1</span>000<span class="intRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">11</span><span class="pointer">1</span><span class="dataSize">2</span>000<span class="intRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Stores the value from integer register <code><b><span class="intRegister">R</span></b></code> to memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code>.
There are 8 available integer registers: <code><b><span class="intRegister">0</span></b></code>, <code><b><span class="intRegister">1</span></b></code>, <code><b><span class="intRegister">2</span></b></code>, <code><b><span class="intRegister">3</span></b></code>, <code><b><span class="intRegister">4</span></b></code>, <code><b><span class="intRegister">5</span></b></code>, <code><b><span class="intRegister">6</span></b></code> and <code><b><span class="intRegister">7</span></b></code>.</p>
                    <p class="references">* Storing a value to a pointer requires a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="12"></a>
                <div class="container">
                    <h1>Load Float <b>[12]</b><span class="no-select ghost category">Arithmetic Operations</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">12</span><span class="pointer">0</span>0000<span class="floatRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">12</span><span class="pointer">1</span>0000<span class="floatRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Loads the value at memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code> into float register <code><b><span class="floatRegister">R</span></b></code>.
There are 8 available float registers: <code><b><span class="floatRegister">0</span></b></code>, <code><b><span class="floatRegister">1</span></b></code>, <code><b><span class="floatRegister">2</span></b></code>, <code><b><span class="floatRegister">3</span></b></code>, <code><b><span class="floatRegister">4</span></b></code>, <code><b><span class="floatRegister">5</span></b></code>, <code><b><span class="floatRegister">6</span></b></code> and <code><b><span class="floatRegister">7</span></b></code>.</p>
                    <p class="references">* Loading a value from a pointer requires a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="13"></a>
                <div class="container">
                    <h1>Store Float <b>[13]</b><span class="no-select ghost category">Arithmetic Operations</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">13</span><span class="pointer">0</span>0000<span class="floatRegister">R</span> <span class="address">LLLLLLLL</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format (Pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">13</span><span class="pointer">1</span>0000<span class="floatRegister">R</span> <span class="volatileOffset">KKKKKKKK</span><span class="no-select ghost"><br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Stores the value from float register <code><b><span class="floatRegister">R</span></b></code> to memory address <code><b><span class="address">LLLLLLLL</span></b></code> or computed pointer + signed volatile offset <code><b><span class="volatileOffset">KKKKKKKK</span></b></code>.
There are 8 available float registers: <code><b><span class="floatRegister">0</span></b></code>, <code><b><span class="floatRegister">1</span></b></code>, <code><b><span class="floatRegister">2</span></b></code>, <code><b><span class="floatRegister">3</span></b></code>, <code><b><span class="floatRegister">4</span></b></code>, <code><b><span class="floatRegister">5</span></b></code>, <code><b><span class="floatRegister">6</span></b></code> and <code><b><span class="floatRegister">7</span></b></code>.</p>
                    <p class="references">* Storing a value to a pointer requires a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="14"></a>
                <div class="container">
                    <h1>Integer Operations <b>[14]</b><span class="no-select ghost category">Arithmetic Operations</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Register operations</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">14</span>0<span class="operation">O</span>0<span class="intRegister">R</span>0<span class="intRegister">S</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Direct value</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">14</span>0<span class="operation">O</span>0<span class="intRegister">R</span>00 <span class="value">VVVVVVVV</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Operates two integer values, <code><b><span class="operation">O</span></b></code> represents the type of operation:
0 = Addition (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> + <code><b><span class="intRegister">S</span></b></code>)
1 = Subtraction (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> - <code><b><span class="intRegister">S</span></b></code>)
2 = Multiplication (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> * <code><b><span class="intRegister">S</span></b></code>)
3 = Division (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> / <code><b><span class="intRegister">S</span></b></code>)
4 = Addition (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> + <code><b><span class="value">VVVVVVVV</span></b></code>)
5 = Subtraction (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> - <code><b><span class="value">VVVVVVVV</span></b></code>)
6 = Multiplication (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> * <code><b><span class="value">VVVVVVVV</span></b></code>)
7 = Division (<code><b><span class="intRegister">R</span></b></code> = <code><b><span class="intRegister">R</span></b></code> / <code><b><span class="value">VVVVVVVV</span></b></code>)</p>
                    <p class="references">* Usage of a pointer requires a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="15"></a>
                <div class="container">
                    <h1>Float Operations <b>[15]</b><span class="no-select ghost category">Arithmetic Operations</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Register operations</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">15</span>0<span class="operation">O</span>0<span class="floatRegister">R</span>0<span class="floatRegister">S</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Direct value</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">15</span>0<span class="operation">O</span>0<span class="floatRegister">R</span>00 <span class="value">VVVVVVVV</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Float to int convertion</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">15</span>0<span class="operation">O</span>0<span class="floatRegister">R</span>0<span class="intRegister">R</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Operates two integer values, <code><b><span class="operation">O</span></b></code> represents the type of operation:
0 = Addition (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> + <code><b><span class="floatRegister">S</span></b></code>)
1 = Subtraction (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> - <code><b><span class="floatRegister">S</span></b></code>)
2 = Multiplication (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> * <code><b><span class="floatRegister">S</span></b></code>)
3 = Division (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> / <code><b><span class="floatRegister">S</span></b></code>)
4 = Addition (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> + <code><b><span class="value">VVVVVVVV</span></b></code>)
5 = Subtraction (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> - <code><b><span class="value">VVVVVVVV</span></b></code>)
6 = Multiplication (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> * <code><b><span class="value">VVVVVVVV</span></b></code>)
7 = Division (<code><b><span class="floatRegister">R</span></b></code> = <code><b><span class="floatRegister">R</span></b></code> / <code><b><span class="value">VVVVVVVV</span></b></code>)
8 = Convert float to integer (Integer register <code><b><span class="intRegister">R</span></b></code> = Converted float register <code><b><span class="floatRegister">R</span></b></code>)</p>
                    <p class="references">* Usage of a pointer requires a loaded pointer beforehand. See cafe codetype "<a href="#30" title="Jump to: Load Pointer [30]">Load Pointer [30]</a>" to learn more.</p>
                </div>
                <a name="30"></a>
                <div class="container">
                    <h1>Load Pointer <b>[30]</b><span class="no-select ghost category">Memory Access</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">30</span><span class="pointer">0</span>00000 <span class="address">LLLLLLLL</span><br><span class="range">RANGE_ST</span> <span class="range">RANGE_EN</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format (Pointer-in-pointer)</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="no-select ghost">30000000 LLLLLLLL<br>RANGE_ST RANGE_EN<br></span><span class="codetype">30</span><span class="pointer">1</span>00000 00000000<br><span class="range">RANGE_ST</span> <span class="range">RANGE_EN</span><span class="no-select ghost"><br>...<br>D0000000 DEADCAFE</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Load a pointer from memory address <code><b><span class="address">LLLLLLLL</span></b></code>.
Loading a pointer-in-pointer is possible by placing the "Pointer-in-pointer" format as many times needed. *
<code><b><span class="range">RANGE_ST</span></b></code> represents the start of reliable memory range the pointed address is located.
<code><b><span class="range">RANGE_EN</span></b></code> represents the end of reliable memory range the pointed address is located.
If the pointer or pointer-in-pointer is invalid, codetypes below will be skipped. Code execution will resume right after cafe codetype <code><b><span class="codetype">D0</span></b></code>.</p>
                    <p class="references">* Loading a pointer-in-pointer with an offset is possible by placing cafe codetype "<a href="#31" title="Jump to: Add Offset To Pointer [31]">Add Offset To Pointer [31]</a>" right after a previously loaded pointer.</p>
                </div>
                <a name="31"></a>
                <div class="container">
                    <h1>Add Offset To Pointer <b>[31]</b><span class="no-select ghost category">Memory Access</span></h1>
                    <table class="demo">
                        <thead>
                            <tr class="no-select">
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">31</span>000000 <span class="offset">QQQQQQQQ</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Adds a non-volatile offset (defined by <code><b><span class="offset">QQQQQQQQ</span></b></code>) to the previously computed pointer.</p>
                </div>
                <a name="C0"></a>
                <div class="container">
                    <h1>Execute ASM <b>[C0]</b><span class="no-select ghost category">Execute</span></h1>
                    <table class="demo">
                        <thead>
                            <tr>
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">C0</span>00<span class="amount">NNNN</span> <span class="value">490F6AE6</span></b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <table class="demo">
                        <thead>
                            <tr>
                                <td>Sample</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">C0</span>00<span class="amount">0002</span> <span class="value">3D801100</span><br><span class="value">38600001</span> <span class="value">906C0000</span><br><span class="value">490F6AE6</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Executes machine code. *
<code><b><span class="amount">NNNN</span></b></code> defines the amount of codelines (excluding the first one).
The last instruction must end with <code><b>ba 0x010F6AE4</b></code> (<code><b><span class="value">490F6AE6</span></b></code>).
All registers are available if used properly.</p>
                    <p class="references">* Refer to this documentation for writing PowerPC Assembly code: <a href="https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/assembler_pdf.pdf" title="View assembly documentation">https://www.ibm.com/support/knowledgecenter/ssw_aix_72/assembler/assembler_pdf.pdf</a>.</p>
                </div>
                <a name="C1"></a>
                <div class="container">
                    <h1>Perform Cafe OS Syscalls <b>[C1]</b><span class="no-select ghost category">Execute</span></h1>
                    <table class="demo">
                        <thead>
                            <tr>
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">C1</span>00<span class="value">XXXX</span> 00000000</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Perform a system call. <code><b><span class="value">XXXX</span></b></code> = SysCall value.*</p>
                    <p class="references">* Visit <a href="http://wiiubrew.org/wiki/Cafe_OS_syscalls" title="Visit WiiUBrew.org">WiiUBrew.org</a> to find all available SysCall values.</p>
                </div>
                <a name="D0"></a>
                <div class="container">
                    <h1>Terminator <b>[D0]</b><span class="no-select ghost category">Termination</span></h1>
                    <table class="demo">
                        <thead>
                            <tr>
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">D0</span>000000 DEADCAFE</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Resumes code execution.
Termination is required for pointers and conditional codetypes.</p>
                </div>
                <a name="D1"></a>
                <div class="container">
                    <h1>No Operation <b>[D1]</b><span class="no-select ghost category">Termination</span></h1>
                    <table class="demo">
                        <thead>
                            <tr>
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">D1</span>000000 DEADCODE</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>This line of code does nothing.</p>
                </div>
                <a name="D2"></a>
                <div class="container">
                    <h1>Timer Termination <b>[D2]</b><span class="no-select ghost category">Termination</span></h1>
                    <table class="demo">
                        <thead>
                            <tr>
                                <td>Format</td>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><code><b><span class="codetype">D2</span>000000 CAFEBABE</b></code></td>
                            </tr>
                        </tbody>
                    </table>
                    <p>Resumes code execution.
This line of code is required at the end of Time-Dependence codetypes.</p>
                </div>
            </div>
        </div>
    </div>

</body></html>'''

class HTMLViewer(PyQt5.QtWidgets.QWidget):
    def __init__(self, html_content):
        super().__init__()

        # create a QTextBrowser widget
        browser = PyQt5.QtWidgets.QTextBrowser()
        browser.setOpenExternalLinks(True)

        # set the text browser content to the loaded HTML
        browser.setHtml(html_content)
        self.center_screen()
        
        button = PyQt5.QtWidgets.QPushButton("Close Window")
        button.clicked.connect(self.close)

        # set the main window properties
        vbox = PyQt5.QtWidgets.QVBoxLayout()
        vbox.addWidget(browser)
        vbox.addWidget(button)
        self.setLayout(vbox)
        self.setWindowTitle('HTML Viewer')
        self.setGeometry(100, 100, 800, 600)
        
    def center_screen(self):
        frame_geometry = self.frameGeometry()
        calculate_screen = PyQt5.QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.move(frame_geometry.topLeft())
