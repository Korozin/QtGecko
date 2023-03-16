from lxml import etree
from PyQt5 import QtCore, QtGui, QtWidgets
from binascii import hexlify, unhexlify
import re, os, sys, math, socket, struct, base64, traceback, webbrowser, configparser

# --- TCPGecko Start --- #
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False
'''Example Use Case for switch:
for case in switch(variable):
    if case(0):
        #dostuff
    elif case(1):
        #dostuff
    else: #default
        #dodefaultstuff'''

def hexstr(data, length): #Pad hex to value for prettyprint
    return hex(data).lstrip("0x").rstrip("L").zfill(length).upper()
def hexstr0(data): #Uppercase hex to string
    return "0x" + hex(data).lstrip("0x").rstrip("L").upper()
def binr(byte): #Get bits as a string
    return bin(byte).lstrip("0b").zfill(8)
def uint8(data, pos):
    return struct.unpack(">B", data[pos:pos + 1])[0]
def uint16(data, pos):
    return struct.unpack(">H", data[pos:pos + 2])[0]
def uint24(data, pos):
    return struct.unpack(">I", "\00" + data[pos:pos + 3])[0] #HAX
def uint32(data, pos):
    return struct.unpack(">I", data[pos:pos + 4])[0]

def getstr(data, pos): #Keep incrementing till you hit a stop
    string = ""
    while data[pos] != 0:
        if pos != len(data):
            string += chr(data[pos])
            pos += 1
        else: break
    return string

def enum(**enums):
    return type('Enum', (), enums)

class TCPGecko:
    def __init__(self, *args):
        # Terminal Colors
        self.red = '\033[91m'
        self.dred = '\033[31m'
        self.yellow = '\033[93m'
        self.green = '\033[92m'
        self.default = '\033[0m'
        self.cyan = '\033[96m'
        self.magenta = '\033[95m'
        self.white = '\033[97m'
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.s.settimeout(5)
        print(f"{self.cyan}[TCPGecko]: {self.default}Attempting to connect to: {self.yellow}" + str(args[0]) + f"{self.white}:{self.yellow}7331{self.default}")
        self.s.connect((str(args[0]), 7331)) #IP, 1337 reversed, Cafiine uses 7332+
        print(f"{self.cyan}[TCPGecko]: {self.default}Connected successfully!{self.default}")

    def readmem(self, address, length): #Number of bytes
        if length == 0: raise BaseException("Reading memory requires a length (# of bytes)")
        if not self.validrange(address, length): raise BaseException("Address range not valid")
        if not self.validaccess(address, length, "read"): raise BaseException("Cannot read from address")
        ret = b""
        if length > 0x400:
            print(f"{self.cyan}[TCPGecko]: {self.default}Length is greater than 0x400 bytes, need to read in chunks")
            print(f"{self.cyan}[TCPGecko]: {self.default}Start address:   " + hexstr0(address))
            for i in range(int(length / 0x400)): #Number of blocks, ignores extra
                self.s.send(b"\x04") #cmd_readmem
                request = struct.pack(">II", address, address + 0x400)
                self.s.send(request)
                status = self.s.recv(1)
                if   status == b"\xbd": ret += self.s.recv(0x400)
                elif status == b"\xb0": ret += b"\x00" * 0x400
                else: raise BaseException("Something went terribly wrong")
                address += 0x400;length -= 0x400
                print(f"{self.cyan}[TCPGecko]: {self.default}Current address: " + hexstr0(address))
            if length != 0: #Now read the last little bit
                self.s.send(b"\x04")
                request = struct.pack(">II", address, address + length)
                self.s.send(request)
                status = self.s.recv(1)
                if   status == b"\xbd": ret += self.s.recv(length)
                elif status == b"\xb0": ret += b"\x00" * length
                else: raise BaseException("Something went terribly wrong")
            print(f"{self.cyan}[TCPGecko]: {self.default}Finished!")
        else:
            self.s.send(b"\x04")
            request = struct.pack(">II", address, address + length)
            self.s.send(request)
            status = self.s.recv(1)
            if   status == b"\xbd": ret += self.s.recv(length)
            elif status == b"\xb0": ret += b"\x00" * length
            else: raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Something went terribly wrong")
        return ret

    def readkern(self, address): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Cannot write to address")
        self.s.send(b"\x0C") #cmd_readkern
        request = struct.pack(">I", int(address))
        self.s.send(request)
        value  = struct.unpack(">I", self.s.recv(4))[0]
        return value

    def writekern(self, address, value): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Cannot write to address")
        self.s.send(b"\x0B") #cmd_readkern
        print(f"{self.cyan}[TCPGecko]: {self.default}" + value)
        request = struct.pack(">II", int(address), int(value))
        self.s.send(request)
        return

    def pokemem(self, address, value): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Cannot write to address")
        self.s.send(b"\x03") #cmd_pokemem
        request = struct.pack(">II", int(address), int(value))
        self.s.send(request) #Done, move on
        return
		
    def pokemem8(self, address, value): #Only takes 4 bytes, may need to run multiple times
        if not self.validrange(address, 4): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Address range not valid")
        if not self.validaccess(address, 4, "write"): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Cannot write to address")
        self.s.send(b"\x03") #cmd_pokemem
        request = struct.pack(">IB", int(address), int(value))
        self.s.send(request) #Done, move on
        return

    def search32(self, address, value, size):
        self.s.send(b"\x72") #cmd_search32
        request = struct.pack(">III", address, value, size)
        self.s.send(request)
        reply = self.s.recv(4)
        return struct.unpack(">I", reply)[0]

    def getversion(self):
        self.s.send(b"\x9A") #cmd_os_version
        reply = self.s.recv(4)
        return struct.unpack(">I", reply)[0]

    def writestr(self, address, string):
        if not self.validrange(address, len(string)): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Address range not valid")
        if not self.validaccess(address, len(string), "write"): raise BaseException(f"{self.cyan}[TCPGecko]: {self.default}Cannot write to address")
        if type(string) != bytes: string = bytes(string, "UTF-8") #Sanitize
        if len(string) % 4: string += bytes((4 - (len(string) % 4)) * b"\x00")
        pos = 0
        for x in range(int(len(string) / 4)):
            self.pokemem(address, struct.unpack(">I", string[pos:pos + 4])[0])
            address += 4;pos += 4
        return
        
    def memalign(self, size, align):
        symbol = self.get_symbol("coreinit.rpl", "MEMAllocFromDefaultHeapEx", True, 1)
        symbol = struct.unpack(">I", symbol.address)[0]
        address = self.readmem(symbol, 4)
        ret = self.call(address, size, align)
        return ret

    def freemem(self, address):
        symbol = self.get_symbol("coreinit.rpl", "MEMFreeToDefaultHeap", True, 1)
        symbol = struct.unpack(">I", symbol.address)[0]
        addr = self.readmem(symbol, 4)
        self.call(addr, address) #void, no return

    def memalloc(self, size, align, noprint=False):
        return self.function("coreinit.rpl", "OSAllocFromSystem", noprint, 0, size, align)

    def freealloc(self, address):
        return self.function("coreinit.rpl", "OSFreeToSystem", True, 0, address)

    def createpath(self, path):
        if not hasattr(self, "pPath"): self.pPath = self.memalloc(len(path), 0x20, True) #It'll auto-pad
        size = len(path) + (32 - (len(path) % 32))
        self.function("coreinit.rpl", "memset", True, 0, self.pPath, 0x00, size)
        self.writestr(self.pPath, path)

    def createstr(self, string):
        address = self.memalloc(len(string), 0x20, True) #It'll auto-pad
        size = len(string) + (32 - (len(string) % 32))
        self.function("coreinit.rpl", "memset", True, 0, address, 0x00, size)
        self.writestr(address, string)
        print(f"{self.cyan}[TCPGecko]: {self.default}String address: " + hexstr0(address))
        return address

    def FSInitClient(self):
        self.pClient = self.memalign(0x1700, 0x20)
        self.function("coreinit.rpl", "FSAddClient", True, 0, self.pClient)

    def FSInitCmdBlock(self):
        self.pCmd = self.memalign(0xA80, 0x20)
        self.function("coreinit.rpl", "FSInitCmdBlock", True, 0, self.pCmd)

    def FSOpenDir(self, path="/"):
        print(f"{self.cyan}[TCPGecko]: {self.default}Initializing...")
        self.function("coreinit.rpl",  "FSInit", True)
        if not hasattr(self, "pClient"): self.FSInitClient()
        if not hasattr(self, "pCmd"):    self.FSInitCmdBlock()
        print(f"{self.cyan}[TCPGecko]: {self.default}Getting memory ready...")
        self.createpath(path)
        self.pDh   = self.memalloc(4, 4, True)
        print(f"{self.cyan}[TCPGecko]: {self.default}Calling function...")
        ret = self.function("coreinit.rpl", "FSOpenDir", False, 0, self.pClient, self.pCmd, self.pPath, self.pDh, 0xFFFFFFFF)
        self.pDh = int(hexlify(self.readmem(self.pDh, 4)), 16)
        print(f"{self.cyan}[TCPGecko]: {self.default}Return value: " + hexstr0(ret))

    def SAVEOpenDir(self, path="/", slot=255):
        print(f"{self.cyan}[TCPGecko]: {self.default}Initializing...")
        self.function("coreinit.rpl",  "FSInit", True, 0)
        self.function("nn_save.rpl", "SAVEInit", True, 0, slot)
        print(f"{self.cyan}[TCPGecko]: {self.default}Getting memory ready...")
        if not hasattr(self, "pClient"): self.FSInitClient()
        if not hasattr(self, "pCmd"):    self.FSInitCmdBlock()
        self.createpath(path)
        self.pDh   = self.memalloc(4, 4, True)
        #print("pDh address: " + hexstr0(self.pDh))
        print(f"{self.cyan}[TCPGecko]: {self.default}Calling function...")
        ret = self.function("nn_save.rpl", "SAVEOpenDir", False, 0, self.pClient, self.pCmd, slot, self.pPath, self.pDh, 0xFFFFFFFF)
        self.pDh = int(hexlify(self.readmem(self.pDh, 4)), 16)
        print(f"{self.cyan}[TCPGecko]: {self.default}Return value: " + hexstr0(ret))

    def FSReadDir(self):
        global printe
        if not hasattr(self, "pBuffer"): self.pBuffer = self.memalign(0x164, 0x20)
        print(f"{self.cyan}[TCPGecko]: {self.default}pBuffer address: " + hexstr0(self.pBuffer))
        ret = self.function("coreinit.rpl", "FSReadDir", True, 0, self.pClient, self.pCmd, self.pDh, self.pBuffer, 0xFFFFFFFF)
        self.entry = self.readmem(self.pBuffer, 0x164)
        printe = getstr(self.entry, 100) + " "
        self.FileSystem().printflags(uint32(self.entry, 0), self.entry)
        self.FileSystem().printperms(uint32(self.entry, 4))
        print(f"{self.cyan}[TCPGecko]: {self.default}" + printe)
        return self.entry, ret

    def SAVEOpenFile(self, path="/", mode="r", slot=255):
        print(f"{self.cyan}[TCPGecko]: {self.default}Initializing...")
        self.function("coreinit.rpl",  "FSInit", True)
        self.function("nn_save.rpl", "SAVEInit", slot, True)
        print(f"{self.cyan}[TCPGecko]: {self.default}Getting memory ready...")
        if not hasattr(self, "pClient"): self.FSInitClient()
        if not hasattr(self, "pCmd"):    self.FSInitCmdBlock()
        self.createpath(path)
        self.pMode = self.createstr(mode)
        self.pFh   = self.memalign(4, 4)
        print(f"{self.cyan}[TCPGecko]: {self.default}Calling function...")
        print(f"{self.cyan}[TCPGecko]: {self.default}This function may have errors")

    def FSReadFile(self):
        if not hasattr(self, "pBuffer"): self.pBuffer = self.memalign(0x200, 0x20)
        print(f"{self.cyan}[TCPGecko]: {self.default}pBuffer address: " + hexstr0(self.pBuffer))
        ret = self.function("coreinit.rpl", "FSReadFile", False, 0, self.pClient, self.pCmd, self.pBuffer, 1, 0x200, self.pFh, 0, 0xFFFFFFFF)
        print(f"{self.cyan}[TCPGecko]: {self.default}" + ret)
        return tcp.readmem(self.pBuffer, 0x200)

    def get_symbol(self, rplname, symname, noprint=False, data=0):
        self.s.send(b"\x71") #cmd_getsymbol
        request = struct.pack(">II", 8, 8 + len(rplname) + 1) #Pointers
        request += rplname.encode("UTF-8") + b"\x00"
        request += symname.encode("UTF-8") + b"\x00"
        size = struct.pack(">B", len(request))
        data = struct.pack(">B", data)
        self.s.send(size) #Read this many bytes
        self.s.send(request) #Get this symbol
        self.s.send(data) #Is it data?
        address = self.s.recv(4)
        return ExportedSymbol(address, self, rplname, symname, noprint)

    def call(self, address, *args):
        arguments = list(args)
        if len(arguments)>8 and len(arguments)<=16: #Use the big call function
            while len(arguments) != 16:
                arguments.append(0)
            self.s.send(b"\x80")
            address = struct.unpack(">I", address)[0]
            request = struct.pack(">I16I", address, *arguments)
            self.s.send(request)
            reply = self.s.recv(8)
            return struct.unpack(">I", reply[:4])[0]
        elif len(arguments) <= 8: #Use the normal one that dNet client uses
            while len(arguments) != 8:
                arguments.append(0)
            self.s.send(b"\x70")
            address = struct.unpack(">I", address)[0]
            request = struct.pack(">I8I", address, *arguments)
            self.s.send(request)
            reply = self.s.recv(8)
            return struct.unpack(">I", reply[:4])[0]
        else: raise BaseException("Too many arguments!")

    #Data last, only a few functions need it, noprint for the big FS/SAVE ones above, acts as gateway for data arg
    def function(self, rplname, symname, noprint=False, data=0, *args):
        symbol = self.get_symbol(rplname, symname, noprint, data)
        ret = self.call(symbol.address, *args)
        return ret

    def validrange(self, address, length):
        if   0x01000000 <= address and address + length <= 0x01800000: return True
        elif 0x02000000 <= address and address + length <= 0x10000000: return True #Depends on game
        elif 0x10000000 <= address and address + length <= 0x50000000: return True #Doesn't quite go to 5
        elif 0xE0000000 <= address and address + length <= 0xE4000000: return True
        elif 0xE8000000 <= address and address + length <= 0xEA000000: return True
        elif 0xF4000000 <= address and address + length <= 0xF6000000: return True
        elif 0xF6000000 <= address and address + length <= 0xF6800000: return True
        elif 0xF8000000 <= address and address + length <= 0xFB000000: return True
        elif 0xFB000000 <= address and address + length <= 0xFB800000: return True
        elif 0xFFFE0000 <= address and address + length <= 0xFFFFFFFF: return True
        else: return True

    def validaccess(self, address, length, access):
        if   0x01000000 <= address and address + length <= 0x01800000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0x02000000 <= address and address + length <= 0x10000000: #Depends on game, may be EG 0x0E3
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0x10000000 <= address and address + length <= 0x50000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xE0000000 <= address and address + length <= 0xE4000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xE8000000 <= address and address + length <= 0xEA000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xF4000000 <= address and address + length <= 0xF6000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xF6000000 <= address and address + length <= 0xF6800000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xF8000000 <= address and address + length <= 0xFB000000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xFB000000 <= address and address + length <= 0xFB800000:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        elif 0xFFFE0000 <= address and address + length <= 0xFFFFFFFF:
            if access.lower() == "read":  return True
            if access.lower() == "write": return True
        else: return False
        
    class FileSystem: #TODO: Try to clean this up ????
        Flags = enum(
            IS_DIRECTORY    = 0x80000000,
            IS_QUOTA        = 0x40000000,
            SPRT_QUOTA_SIZE = 0x20000000, #Supports .quota_size field
            SPRT_ENT_ID     = 0x10000000, #Supports .ent_id field
            SPRT_CTIME      = 0x08000000, #Supports .ctime field
            SPRT_MTIME      = 0x04000000, #Supports .mtime field
            SPRT_ATTRIBUTES = 0x02000000, #Supports .attributes field
            SPRT_ALLOC_SIZE = 0x01000000, #Supports .alloc_size field
            IS_RAW_FILE     = 0x00800000, #Entry isn't encrypted
            SPRT_DIR_SIZE   = 0x00100000, #Supports .size field, doesn't apply to files
            UNSUPPORTED_CHR = 0x00080000) #Entry name has an unsupported character
        
        Permissions = enum( #Pretty self explanitory
            OWNER_READ  = 0x00004000,
            OWNER_WRITE = 0x00002000,
            OTHER_READ  = 0x00000400,
            OTHER_WRITE = 0x00000200)

        def printflags(self, flags, data):
            global printe
            if flags & self.Flags.IS_DIRECTORY:    printe += " Directory"
            if flags & self.Flags.IS_QUOTA:        printe += " Quota"
            if flags & self.Flags.SPRT_QUOTA_SIZE: printe += " .quota_size: " + hexstr0(uint32(data, 24))
            if flags & self.Flags.SPRT_ENT_ID:     printe += " .ent_id: " + hexstr0(uint32(data, 32))
            if flags & self.Flags.SPRT_CTIME:      printe += " .ctime: " + hexstr0(uint32(data, 36))
            if flags & self.Flags.SPRT_MTIME:      printe += " .mtime: " + hexstr0(uint32(data, 44))
            if flags & self.Flags.SPRT_ATTRIBUTES: pass #weh lol?
            if flags & self.Flags.SPRT_ALLOC_SIZE: printe += " .alloc_size: " + hexstr0(uint32(data, 20))
            if flags & self.Flags.IS_RAW_FILE:     printe += " Raw (Unencrypted) file"
            if flags & self.Flags.SPRT_DIR_SIZE:   printe += " .dir_size: " + hexstr0(uint64(data, 24))
            if flags & self.Flags.UNSUPPORTED_CHR: printe += " !! UNSUPPORTED CHARACTER IN NAME"

        def printperms(self, perms):
            global printe
            if perms & self.Permissions.OWNER_READ:  printe += " OWNER_READ"
            if perms & self.Permissions.OWNER_WRITE: printe += " OWNER_WRITE"
            if perms & self.Permissions.OTHER_READ:  printe += " OTHER_READ"
            if perms & self.Permissions.OTHER_WRITE: printe += " OTHER_WRITE"
                
def hexstr0(data): #0xFFFFFFFF, uppercase hex string
    return "0x" + hex(data).lstrip("0x").rstrip("L").zfill(8).upper()

class ExportedSymbol(object):
    def __init__(self, address, rpc=None, rplname=None, symname=None, noprint=False):
        self.address = address
        self.rpc     = rpc
        self.rplname = rplname
        self.symname = symname
        if not noprint: #Make command prompt not explode when using FS or SAVE functions
            print(symname + " address: " + hexstr0(struct.unpack(">I", address)[0]))

    def __call__(self, *args):
        return self.rpc.call(self.address, *args) #Pass in arguments, run address
# --- TCPGecko End --- #

# --- QtGecko Start --- #
if not os.path.exists("codes/null.xml"):
    os.makedirs("codes", exist_ok=True)
    with open("codes/null.xml", "w") as f:
        f.write('<codes>\n</codes>')
    print("\033[38;2;255;72;0m[QtGecko]: \033[0mTemplate XML created\033[0m")
else:
    print("\033[38;2;255;72;0m[QtGecko]: \033[0mTemplate XML already exists\033[0m")


# Class to handle Config operations
class ConfigManager:
    SECTION_NAME = 'OPTIONS'
    TIMEOUT_OPTION_NAME = 'timeout'
    IPV4_OPTION_NAME = 'ipv4'
    THEME_OPTION_NAME = 'theme'

    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            self.create_config()
        self.config = self.read_config()

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        return config

    def print_config(self):
        self.connection_timeout_option = self.config.getboolean(self.SECTION_NAME, self.TIMEOUT_OPTION_NAME, fallback=True)
        self.last_used_ipv4 = self.config.get(self.SECTION_NAME, self.IPV4_OPTION_NAME, fallback="")
        self.theme_option = self.config.get(self.SECTION_NAME, self.THEME_OPTION_NAME, fallback="")

        if self.connection_timeout_option:
            print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mConnection Timeout: \033[93m{self.connection_timeout_option}\033[0m")
        else:
            print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mConnection Timeout: \033[93m{self.connection_timeout_option}\033[0m")

        if self.last_used_ipv4:
            print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mLast used IPv4: \033[93m{self.last_used_ipv4}\033[0m")
            
        if self.theme_option:
            print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mCurrent theme: \033[93m{self.theme_option}\033[0m")

    def create_config(self):
        config = configparser.ConfigParser()
        config[self.SECTION_NAME] = {
            self.TIMEOUT_OPTION_NAME: "True",
            self.IPV4_OPTION_NAME: "",
            self.THEME_OPTION_NAME: "Fusion",
        }

        with open(self.file_path, "w") as f:
            config.write(f)

    def print_config_values(self):
        self.print_config()

    def write_config_option(self, option_name, option_value):
        with open(self.file_path, 'r') as config_file:
            config_lines = config_file.readlines()

        with open(self.file_path, 'w') as config_file:
            for config_line in config_lines:
                if config_line.startswith(f"{option_name} ="):
                    config_file.write(f"{option_name} = {option_value}\n")
                    print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mWrote '\033[93m{option_value}\033[0m' to {option_name}\033[0m")
                else:
                    config_file.write(config_line)

    def write_ipv4(self, ipv4):
        self.write_config_option(self.IPV4_OPTION_NAME, str(ipv4))

    def write_timeout_true(self):
        self.write_config_option(self.TIMEOUT_OPTION_NAME, "True")
        
    def write_timeout_false(self):
        self.write_config_option(self.TIMEOUT_OPTION_NAME, "False")
        
    def write_theme(self, theme):
        self.write_config_option(self.THEME_OPTION_NAME, str(theme))


class CustomCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            if self.isChecked():
                pass
            elif not self.isChecked():
                self.setChecked(not self.isChecked())
        elif event.button() == QtCore.Qt.LeftButton:
            self.setChecked(not self.isChecked())
        else:
            super().mousePressEvent(event)
            

# Class for the contents of the Main Window
class QtGecko(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Config operations
        self.file_path = "config.ini"
        self.config_manager = ConfigManager(self.file_path)
        self.config_manager.print_config_values()
        self.set_theme = self.config_manager.theme_option
        
        # Initialize UI
        self.CreateMainWindow()
        self.CreateCodesTab()
        self.CreateMiscTab()
        self.CreateConversionTab()
        self.CreateAboutTab()
        self.CreateExtrnlToolsTab()
        
    def CreateMainWindow(self):
        # Set Window size
        self.setGeometry(0, 0, 1300, 600)
        self.setWindowTitle("QtGecko : KorOwOzin")
        
        # Create a QtCore.QTimer for use with connection timeouts
        self.connection_timeout_timer = QtCore.QTimer()
        
        # Make and set Font
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        
        # Create QtWidgets.QTabWidget and add Tabs to it
        self.tab_widget = QtWidgets.QTabWidget()
        self.codes_tab = QtWidgets.QWidget()
        self.conversion_tab = QtWidgets.QWidget()
        self.misc_tab = QtWidgets.QWidget()
        self.external_tools_tab = QtWidgets.QWidget()
        self.about_tab = QtWidgets.QWidget()
        self.tab_widget.addTab(self.codes_tab, "Codes")
        self.tab_widget.addTab(self.conversion_tab, "Conversions")
        self.tab_widget.addTab(self.misc_tab, "Miscellaneous")
        self.tab_widget.addTab(self.external_tools_tab, "External Tools")
        self.tab_widget.addTab(self.about_tab, "About")
        # Make sure the QTab is set as the main window
        self.setCentralWidget(self.tab_widget)
        
        #--- Global Items ---#
        # Create and format IPv4 Label
        IPv4_Label = QtWidgets.QLabel("IPv4 Address: ", self)
        IPv4_Label.move(10, 535)
        
        # Create and format Connect Button
        self.connect_button = QtWidgets.QPushButton("Connect", self)
        self.connect_button.resize(100, 25)
        self.connect_button.move(980, 540)
        self.connect_button.setEnabled(False)
        self.connect_button.clicked.connect(self.connect_press)
        
        # Create and format Disconnect Button
        self.disconnect_button = QtWidgets.QPushButton("Disconnect", self)
        self.disconnect_button.resize(100, 25)
        self.disconnect_button.move(1090, 540)
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.clicked.connect(self.disconnect_press)
        
        # Create and format Connection Bar
        self.connection_bar = QtWidgets.QLineEdit(self)
        self.connection_bar.resize(850, 16)
        self.connection_bar.move(120, 544)
        self.connection_bar.setStyleSheet("background-color: red;")
        self.connection_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.connection_bar.setFont(self.font)
        self.connection_bar.textChanged.connect(self.ip_update)
        self.connection_bar.setText(self.config_manager.last_used_ipv4)
        
        # Create and format Help Button
        self.help_button = QtWidgets.QPushButton("Help", self)
        self.help_button.resize(80, 25)
        self.help_button.move(1200, 540)
        self.help_button.clicked.connect(self.help_press)

        # Make GUI centered upon launch
        frame_geometry = self.frameGeometry()
        calculate_screen = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.move(frame_geometry.topLeft())
        #--- Global Items End ---#
        
    def CreateCodesTab(self):
        #--- Codes Tab Items ---#
        
        # Make vertical layout for use in self.codes_tab
        vbox = QtWidgets.QVBoxLayout()
        
        # Make several Horizontal Layouts to position items
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()
        hbox5 = QtWidgets.QHBoxLayout()
        
        # Create labels
        self.code_list_label = QtWidgets.QLabel("Code List:")
        self.code_select_label = QtWidgets.QLabel("Selected Code:")
        self.code_comment_label = QtWidgets.QLabel("Selected Code Comment:")
        
        # Create empty list for use with adding checkboxes from XML
        self.checkboxes = []
        
        # Create section to hold checboxes from parsed XML
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Create widget base to support creating items in scroll area
        self.scroll_areaWidgetContents = QtWidgets.QWidget()
        
        # Set the main widget area for the scroll area to previous QtWidgets.QWidget instance
        self.scroll_area.setWidget(self.scroll_areaWidgetContents)
        
        # Create vertical layout for adding checkboxes in the proper GUI format
        self.scroll_areaLayout = QtWidgets.QVBoxLayout(self.scroll_areaWidgetContents)
        
        self.scroll_area.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.scroll_area.customContextMenuRequested.connect(self.init_context_menu)
        
        # create actions for context menu
        self.edit_code_action = QtWidgets.QAction("Edit Selected Code", self.scroll_area)
        self.edit_code_action.triggered.connect(self.edit_selected_code)
        self.delete_code_action = QtWidgets.QAction("Delete Selected Code", self.scroll_area)
        self.delete_code_action.triggered.connect(self.delete_selected_code)
        self.copy_code_action = QtWidgets.QAction("Copy Selected Code", self.scroll_area)
        self.copy_code_action.triggered.connect(self.copy_selected_code)
        
        # Set width and height for the Codes: field
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(320)

        # Create and format the Selected Code: field
        self.code_text_edit = Editor()
        self.code_text_edit.setFixedWidth(420)
        self.code_text_edit.setFixedHeight(320)
        self.code_text_edit.setReadOnly(True)
        
        # Create and format the Selected Code Comment: field
        self.comment_text_edit = QtWidgets.QTextEdit()
        self.comment_text_edit.setFixedWidth(420)
        self.comment_text_edit.setFixedHeight(320)
        self.comment_text_edit.setReadOnly(True)

        # Create first row of buttons
        self.add_code_button = QtWidgets.QPushButton("Add Code")
        self.delete_all_codes_button = QtWidgets.QPushButton("Delete All Codes")
        self.download_codes_button = QtWidgets.QPushButton("Download Codes")
        self.documentation_button = QtWidgets.QPushButton("Code Types Documentation")
        self.list_start_button = QtWidgets.QPushButton("Code List Start")
        
        # Create second row of buttons
        self.send_codes_button = QtWidgets.QPushButton("Send Codes")
        self.send_codes_button.setEnabled(False)
        self.disable_codes_button = QtWidgets.QPushButton("Disable Codes")
        self.disable_codes_button.setEnabled(False)
        self.load_list_button = QtWidgets.QPushButton("Load Code List")
        self.export_list_button = QtWidgets.QPushButton("Export Code List")
        self.untick_all_button = QtWidgets.QPushButton("Untick All")
        
        # Create third row of buttons
        self.code_search_button = QtWidgets.QPushButton("Code Tile Search")
        self.search_window = None
        self.create_gctu_button = QtWidgets.QPushButton("Export GCTU")
        self.import_gctu_button = QtWidgets.QPushButton("Import GCTU")
        
        # Create label to use with formatting because I'm lazy, lol
        self.format_label = QtWidgets.QLabel("\n\n\n\n\n\n")
        
        # Add labels using horizontal layout
        hbox1.addWidget(self.code_list_label)
        hbox1.addWidget(self.code_select_label)
        hbox1.addWidget(self.code_comment_label)
        
        # Add Code fields using horizontal layout
        hbox2.addWidget(self.scroll_area)
        hbox2.addWidget(self.code_text_edit)
        hbox2.addWidget(self.comment_text_edit)
        
        # Add first row of buttons using horizontal layout
        hbox3.addWidget(self.add_code_button)
        hbox3.addWidget(self.delete_all_codes_button)
        hbox3.addWidget(self.download_codes_button)
        hbox3.addWidget(self.documentation_button)
        hbox3.addWidget(self.list_start_button)
        
        # Add second row of buttons using horizontal layout
        hbox4.addWidget(self.send_codes_button)
        hbox4.addWidget(self.disable_codes_button)
        hbox4.addWidget(self.load_list_button)
        hbox4.addWidget(self.export_list_button)
        hbox4.addWidget(self.untick_all_button)
        
        # Add third row of buttons using horizontal layout
        hbox5.addWidget(self.code_search_button)
        hbox5.addWidget(self.create_gctu_button)
        hbox5.addWidget(self.import_gctu_button)

        # Add all layouts to a main vertical layout
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        
        # Add formatting label to main vertical layout
        vbox.addWidget(self.format_label)

        # Set main vertical layout
        self.codes_tab.setLayout(vbox)

        # Connect buttons to their respective functions
        self.load_list_button.clicked.connect(self.select_code_list)
        self.add_code_button.clicked.connect(self.open_code_creator)
        self.delete_all_codes_button.clicked.connect(self.delete_codes)
        self.send_codes_button.clicked.connect(self.send_code)
        self.export_list_button.clicked.connect(self.export_code_list)
        self.download_codes_button.clicked.connect(self.open_code_archive)
        self.documentation_button.clicked.connect(self.open_code_docs)
        self.untick_all_button.clicked.connect(self.untick_checkboxes)
        self.disable_codes_button.clicked.connect(self.disable_code)
        self.create_gctu_button.clicked.connect(self.to_gctu)
        self.import_gctu_button.clicked.connect(self.import_gctu)
        self.code_search_button.clicked.connect(self.open_search_window)
        
        # Create timer for use with refreshing GUI
        self.timer = QtCore.QTimer()
        self.timer.start(5000)
        self.timer.timeout.connect(self.refresh_gui)
        #--- Codes Tab Items End ---#

    def CreateMiscTab(self):
        #--- Micellaneous Tab Items ---#
        # Create See Local IP Button
        self.local_ip_button = QtWidgets.QPushButton("Computer Local IP Address(es)", self.misc_tab)
        self.local_ip_button.clicked.connect(self.see_local_ip)
        self.local_ip_button.setToolTip("Displays the IP Address of this computer")
        self.local_ip_button.setFixedSize(635, 30)
        self.local_ip_button.move(3, 40)
        
        # Create Build Date Button
        self.build_date_button = QtWidgets.QPushButton("Build Date", self.misc_tab)
        self.build_date_button.clicked.connect(self.show_build_date)
        self.build_date_button.setToolTip("Tells you when this application has been built")
        self.build_date_button.setFixedSize(635, 30)
        self.build_date_button.move(3, 160)
        
        # Create Bug Tracker Button
        self.bug_tracker_button = QtWidgets.QPushButton("Bug Tracker", self.misc_tab)
        self.bug_tracker_button.clicked.connect(self.open_bug_tracker)
        self.bug_tracker_button.setToolTip("View the bug tracker")
        self.bug_tracker_button.setFixedSize(635, 30)
        self.bug_tracker_button.move(3, 200)
        
        # Create Connection Timeout Checkbox
        self.connection_timeout_box = QtWidgets.QCheckBox("Connection Timeouts", self.misc_tab)
        self.connection_timeout_box.stateChanged.connect(self.connection_timeout_changed)
        self.connection_timeout_box.setToolTip("Whether requests will time out or potentially wait forever")
        #connection_timeout_box.setFixedSize(635, 30)
        self.connection_timeout_box.move(3, 240)
        
        # Create a combo box to hold the themes
        self.theme_combobox = QtWidgets.QComboBox(self.misc_tab)
        self.theme_combobox.addItems(QtWidgets.QStyleFactory.keys())
        self.theme_combobox.move(3, 290)
        self.theme_combobox.currentIndexChanged.connect(self.on_theme_changed)
        self.theme_combobox.setCurrentText(self.config_manager.theme_option)
        
        # Create a Label for the combo box
        self.theme_label = QtWidgets.QLabel("Change Theme", self.misc_tab)
        self.theme_label.move(3, 270)
        
        # Set Connection Timeout Checkbox based on Config
        if str(self.config_manager.connection_timeout_option) == "True":
            self.connection_timeout_box.setChecked(True)
        elif str(self.config_manager.connection_timeout_option) == "False":
            self.connection_timeout_box.setChecked(False)
        #--- Micellaneous Tab Items End ---#
        
    def CreateConversionTab(self):
        #--- Conversion Tab Items ---#
        # Create UTF-8 Buttons
        self.hex_to_UTF8_button = QtWidgets.QPushButton("Hexadecimal -> UTF-8", self.conversion_tab)
        self.hex_to_UTF8_button.clicked.connect(self.open_hex_to_UTF8_window)
        self.hex_to_UTF8_button.setToolTip("Converts Hexadecimal to UTF-8 Text")
        self.hex_to_UTF8_button.setFixedSize(635, 30)
        self.hex_to_UTF8_button.move(3, 0)
        
        self.UTF8_to_hex_button = QtWidgets.QPushButton("UTF-8 -> Hexadecimal", self.conversion_tab)
        self.UTF8_to_hex_button.clicked.connect(self.open_UTF8_to_hex_window)
        self.UTF8_to_hex_button.setFixedSize(635, 30)
        self.UTF8_to_hex_button.move(655, 0)
        
        # Create Floating Point Buttons
        self.hex_to_float_button = QtWidgets.QPushButton("Hexadecimal -> Floating Point", self.conversion_tab)
        self.hex_to_float_button.clicked.connect(self.open_hex_to_float_window)
        self.hex_to_float_button.setFixedSize(635, 30)
        self.hex_to_float_button.move(3, 40)
        
        self.float_to_hex_button = QtWidgets.QPushButton("Floating Point -> Hexadecimal", self.conversion_tab)
        self.float_to_hex_button.clicked.connect(self.open_float_to_hex_window)
        self.float_to_hex_button.setFixedSize(635, 30)
        self.float_to_hex_button.move(655, 40)
        
        # Create Decimal Buttons
        self.hex_to_decimal_button = QtWidgets.QPushButton("Hexadecimal -> Decimal", self.conversion_tab)
        self.hex_to_decimal_button.clicked.connect(self.open_hex_to_decimal_window)
        self.hex_to_decimal_button.setFixedSize(635, 30)
        self.hex_to_decimal_button.move(3, 80)
        
        self.decimal_to_hex_button = QtWidgets.QPushButton("Decimal -> Hexadecimal", self.conversion_tab)
        self.decimal_to_hex_button.clicked.connect(self.open_decimal_to_hex_window)
        self.decimal_to_hex_button.setFixedSize(635, 30)
        self.decimal_to_hex_button.move(655, 80)
        
        # Create UTF-16 Buttons
        self.hex_to_UTF16_button = QtWidgets.QPushButton("Hexadecimal -> UTF-16", self.conversion_tab)
        self.hex_to_UTF16_button.clicked.connect(self.open_hex_to_UTF16_window)
        self.hex_to_UTF16_button.setFixedSize(635, 30)
        self.hex_to_UTF16_button.move(3, 120)
        
        self.UTF16_to_hex_button = QtWidgets.QPushButton("UTF-16 -> Hexadecimal", self.conversion_tab)
        self.UTF16_to_hex_button.clicked.connect(self.open_UTF16_to_hex_window)
        self.UTF16_to_hex_button.setFixedSize(635, 30)
        self.UTF16_to_hex_button.move(655, 120)
        #--- Conversion Tab Items End ---#
        
    def CreateAboutTab(self):
        #--- About Tab Items ---#
        self.header_label = QtWidgets.QLabel(self.about_tab)
        self.header_label.setText('<br/><b></b>This application is a wireless cheat code manager and development aid for Wii U titles.<br/><br/><u>Credits</u>:')
        
        self.bully_label = QtWidgets.QLabel(self.about_tab)
        self.bully_label.move(0, 80)
        self.bully_label.setText('<b>BullyWiiPlaza</b> for creating and programming the original <a href="https://github.com/bullywiiplaza/JGeckoU">JGecko U</a>')
        self.bully_label.setOpenExternalLinks(True)
        
        self.koro_label = QtWidgets.QLabel(self.about_tab)
        self.koro_label.move(0, 100)
        self.koro_label.setText('<b>Korozin</b> for making this <a href="https://github.com/Korozin/QtGecko">re-creation</a>')
        self.koro_label.setOpenExternalLinks(True)
        
        self.apple_label = QtWidgets.QLabel(self.about_tab)
        self.apple_label.move(0, 120)
        self.apple_label.setText('<b>Pop-Apple</b> for making <a href="https://github.com/Pop-Apple/JGeckoU-Reproduction">this</a> as inspiration')
        self.apple_label.setOpenExternalLinks(True)
        #--- About Tab Items End ---#
        
    def CreateExtrnlToolsTab(self):
        self.bully_label = QtWidgets.QLabel(self.external_tools_tab)
        self.bully_label.move(140, 5)
        self.bully_label.setText('<span style="font-size: 16pt; color: #bb0d00; font-weight: bold;">Make sure to use the TCP Gecko Installer below to avoid incompatibility problems</span>')
        
        self.dl_tcp_gecko_button = QtWidgets.QPushButton("TCP Gecko Installer", self.external_tools_tab)
        self.dl_tcp_gecko_button.clicked.connect(self.download_tcp_gecko)
        self.dl_tcp_gecko_button.setToolTip("Downloads the TCP Gecko Installer Homebrew Package")
        self.dl_tcp_gecko_button.setFixedSize(1235, 30)
        self.dl_tcp_gecko_button.move(30, 50)
        
    #--- Global Items Functions ---#
    # Function to determine if the IPv4 is valid using a Regex Pattern
    def ip_update(self):
    
        def is_valid_ipv4(address):
            pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
            match = pattern.search(address)
            return match is not None
    
        # Set QtWidgets.QLineEdit style based on IPv4 Validity
        if is_valid_ipv4(self.connection_bar.text()):
            self.connection_bar.setStyleSheet("background-color: #00FF00;")
            self.connect_button.setEnabled(True)
        else:
            self.connection_bar.setStyleSheet("background-color: red;")
            self.connect_button.setEnabled(False)

                    
    # Custom Error handling for Socket Timeout so the process won't hang forever
    def timeout_handler(self, signum, frame):
        raise TimeoutError("Connection timed out")
                    
    # Behavior for is the Connect button is pressed
    def connect_press(self):
        # Call function to write last used IPv4 to Config
        self.config_manager.write_ipv4(self.connection_bar.text())
        
        # Set tcp_socket as a global variable
        global tcp_socket
        
        # Attempt to connect
        try:
            
            # Determine whether or not to call the timeout function based on checkbox status
            if self.config_manager.connection_timeout_option == "False":
                pass
            elif self.config_manager.connection_timeout_option == "True":
                self.connection_timeout_timer.start(1800000) # 30 minute time-frame
                self.connection_timeout_timer.timeout.connect(self.connect_timeout)
            else:
                pass
        
            # Connect to IPv4
            tcp_socket = TCPGecko(self.connection_bar.text())
            
            # Set proper GUI elements based on connectivity
            self.send_codes_button.setEnabled(True)
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.connection_bar.deselect()
            self.disable_codes_button.setEnabled(True)
            
            self.window = InfoWindow()
            self.window.CreateWindow("Connection Success!", f"Connected successfully!.", 300, 150)
            self.window.show()
        
        # GUI error handling for connection errors
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Connection Error!", f"<b></b>Used IPv4: {self.connection_bar.text()}<br/>Error: {e}.<br/><br/>If you're unable to connect, then submit an issue on <a href='https://github.com/Korozin/QtGecko/issues'>GitHub</a>, or consult the <a href='https://github.com/Korozin/QtGecko/blob/main/SETUP-GUIDE.md'>Setup Guide</a>.", 500, 200)
            self.window.show()
            print(f"\033[96m[TCPGeckof]: \033[0mConnection attempt failed.. :(\033[0m")
        
    # Function to determine Disconnect behavior
    def disconnect_press(self):
    
        # Attempt to disconnect
        try:
            # Disconnect from IPv4
            tcp_socket.s.close()
            
            # Set GUI Elements based on success
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.connection_bar.deselect()
            self.send_codes_button.setEnabled(False)
            self.disable_codes_button.setEnabled(False)
        
        # GUI error handling if disoconnect fails
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"<b></b>Used IPv4: {self.connection_bar.text()}<br/>Error: {e}.", 500, 200)
            self.window.show()
        
    # Function for Help button behavior
    def help_press(self):
        self.window = InfoWindow()
        self.window.CreateWindow("Help", "If you can't connect, then make sure to follow the <a href='https://github.com/Korozin/QtGecko/blob/main/SETUP-GUIDE.md'>setup guide</a>.<br/><br/>If you're still having issues then please submit an issue on <a href='https://github.com/Korozin/QtGecko/issues'>GitHub</a>.", 500, 200)
        self.window.show()
        
    # function for auto-disconnection
    def connect_timeout(self):
    
        # If option is set to false, do nothing. If true, disconnect
        if self.config_manager.connection_timeout_option == "False":
            pass
        elif self.config_manager.connection_timeout_option == "True":
            try:
                tcp_socket.close()
            except Exception as e:
                print(f"\033[91m[Error]: \033[0m{e}\033[0m")
        else:
            pass
            
            
    def open_search_window(self):
        # create new window with line edit and search button
        if self.search_window is None:
            self.search_window = QtWidgets.QWidget()
            self.search_window.setWindowTitle('Search Window')
            self.search_window.setGeometry(200, 200, 300, 100)
            layout = QtWidgets.QVBoxLayout()
            line_edit = QtWidgets.QLineEdit()
            button = QtWidgets.QPushButton('Search')
            layout.addWidget(line_edit)
            layout.addWidget(button)
            self.search_window.setLayout(layout)

            # connect button to function that searches for checkbox on main window
            button.clicked.connect(lambda: self.scroll_to_checkbox(line_edit.text()))
            
        # Center search_window
        frame_geometry = self.search_window.frameGeometry()
        calculate_screen = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.search_window.move(frame_geometry.topLeft())

        # Make search_window visible
        self.search_window.show()

    def scroll_to_checkbox(self, text):
        checkboxes = self.findChildren(QtWidgets.QCheckBox)
        for checkbox in checkboxes:
            if text.lower() in checkbox.text().lower():
                scroll_bar = self.findChild(QtWidgets.QScrollArea).verticalScrollBar()
                scroll_bar.setValue(checkbox.pos().y())
                checkbox.setChecked(True) # Should I leave this on?
                break
        
        # Close search_window once scrollbar is moved.
        self.search_window.close()
        
    def gctu_update(self):
    
        def is_valid_hex_address(address):
            pattern = re.compile(r"^([0-9a-fA-F]{8}-[0-9a-fA-F]{8})$")
            match = pattern.search(address)
            return match is not None
    
        # Set QtWidgets.QLineEdit style based on IPv4 Validity
        if is_valid_hex_address(self.title_id_line_edit.text()):
            self.title_id_line_edit.setStyleSheet("background-color: #00FF00;")
            self.confirm_button.setEnabled(True)
        else:
            self.title_id_line_edit.setStyleSheet("background-color: red;")
            self.confirm_button.setEnabled(False)
            
    def on_confirm(self):
        enabled_checkboxes = [checkbox for checkbox in self.checkboxes if checkbox.isChecked()]
        text_list = []
        for checkbox in enabled_checkboxes:
            entry = checkbox.entry
            assembly_ram_writes_enabled = entry.find("assembly_ram_write").text == "false"
            if assembly_ram_writes_enabled:
                code = entry.find("code").text
                text_list.append(code)
      
        input_string = "\n".join(text_list)
    
        # Conver tthe input string be a straight string like "3000000010A0A624D0000000DEADCAFE"
        input_str = input_string.replace(" ", "").replace("\n", "")
        output_str = ""
        for i in range(0, len(input_string), 17):
            output_str += input_string[i:i+17]

        # Convert the forammted string to binary data
        binary_data = bytes.fromhex(output_str)

        # Write the binary data to a file
        file_name = self.title_id_line_edit.text().upper().replace("-", "") + ".gctu"
        with open(file_name, 'wb') as f:
            f.write(binary_data)
        self.gctu_window.close()
        
    def open_title_database(self):
        webbrowser.open("https://korozin.github.io/titlekey")
        
    def open_save_gctu_window(self):
        # create new window with line edit and search button
        if self.gctu_window is None:
            self.gctu_window = QtWidgets.QWidget()
            self.gctu_window.setWindowTitle('Export GCTU')
            self.gctu_window.setFixedSize(600, 100)
            
            main_layout = QtWidgets.QVBoxLayout()
            row1_layout = QtWidgets.QHBoxLayout()
            row2_layout = QtWidgets.QHBoxLayout()
            
            header_label = QtWidgets.QLabel("Specify the (dashed) Title-ID")
            main_layout.addWidget(header_label)
            
            title_id_label = QtWidgets.QLabel("Title ID:")
            self.title_id_line_edit = QtWidgets.QLineEdit()
            self.title_id_line_edit.textChanged.connect(self.gctu_update)
            row1_layout.addWidget(title_id_label)
            row1_layout.addWidget(self.title_id_line_edit)
            
            self.confirm_button = QtWidgets.QPushButton("Confirm")
            self.confirm_button.clicked.connect(self.on_confirm)
            self.title_database = QtWidgets.QPushButton("Wii U Title Database")
            self.title_database.clicked.connect(self.open_title_database)
            row2_layout.addWidget(self.confirm_button)
            row2_layout.addWidget(self.title_database)
            
            main_layout.addLayout(row1_layout)
            main_layout.addLayout(row2_layout)
            self.gctu_window.setLayout(main_layout)
            
            self.gctu_update()

            # connect button to function that searches for checkbox on main window
            #button1.clicked.connect(lambda: self.scroll_to_checkbox(line_edit.text()))
            
        # Center gctu_window
        frame_geometry = self.gctu_window.frameGeometry()
        calculate_screen = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(calculate_screen)
        self.gctu_window.move(frame_geometry.topLeft())

        # Make gctu_window visible
        self.gctu_window.show()
        
    def to_gctu(self):      
        self.gctu_window = None
        self.open_save_gctu_window()
            
    def import_gctu(self):
        try:
            # Create a dialog to allow the user to select their file
            dialog = QtWidgets.QFileDialog(self)
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)

            # Add filters for XML and All files
            filters = ["GCTU Files (*.gctu)", "All Files (*.*)"]
            dialog.setNameFilters(filters)
            dialog.selectNameFilter(filters[0])

            # Sets the XML File Path if successfully selected, if not leave path empty
            if dialog.exec_():
                file_name = dialog.selectedFiles()[0]
                
            # Open the .gctu file
            with open(file_name,'rb') as f:
                output_string = f.read()
                f.close()

            # Read the file as upper-case Hex
            output_string = output_string.hex().upper()

            # Format the .gctu Contents into proper Code format
            new_output_string = ""
            for i in range(0, len(output_string), 16):
                new_output_string += output_string[i:i+8] + " " + output_string[i+8:i+16] + "\n"

            # Print the output string without an extra line break at the end
            new_output_string = new_output_string.strip("\n")
            self.edit_selected_code(new_output_string, "10")
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"Error: {e}<br/><br/>Make sure you select a GCTU File!", 320, 150)
            self.window.show()


    #--- Global Items Functions End ---#
        
    #--- Codes Tab Functions ---#
    
    # Function to initialize Context Menu
    def init_context_menu(self, pos):
        # get selected item(s) from scroll_area
        
        menu = QtWidgets.QMenu(self)

        # add actions to context menu
        menu.addAction(self.edit_code_action)
        menu.addAction(self.delete_code_action)
        menu.addAction(self.copy_code_action)

        # show context menu
        menu.exec_(self.scroll_area.viewport().mapToGlobal(pos))
    

    # Function to populate Code List: section
    def populate_section1(self):
        # Open the XML file and parse it
        with open(file_path, 'r') as xmlFile:
            xml_string = xmlFile.read()
        root = etree.fromstring(xml_string)
        entries = root.findall("entry")

        # Add a checkbox for each entry in section 1
        for entry in entries:
            name = entry.get("name")
            author = entry.find("authors").text
            enabled = entry.find("enabled").text == "true"
            if author is None:
                author = ""
            else:
                author = f"[{author}]"
            checkbox = CustomCheckBox(f"{name} {author}")
            checkbox.setChecked(enabled)
            checkbox.stateChanged.connect(self.checkbox_state_changed)
            checkbox.entry = entry
            self.checkboxes.append(checkbox)
            self.scroll_areaLayout.addWidget(checkbox)
            
        # Find the last selected checkbox
        last_checked_checkbox = None
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                self.last_checked_checkbox = checkbox

    
    # Function to populate Selected Code Comment: section
    def populate_section2(self, entry=None):
        if entry is None:
            self.code_text_edit.setPlainText("")
            self.comment_text_edit.setPlainText("")
            self.code_select_label.setText(f"Selected Code:")
        else:
            # Set the contents of the text edits in section 2
            self.code_select_label.setText(f"Selected Code: \"{entry.get('name')}\"\nAssembly RAM Writes: {entry.find('assembly_ram_write').text.capitalize()}")
            self.code_text_edit.setPlainText(entry.find("code").text)
            comment_text = ""
            asm_label_text = ""
            for tag in ["comment"]:
                value = entry.find(tag).text
                if value:
                    comment_text += f"{value}\n"
                    
            self.comment_text_edit.setPlainText(comment_text)
            
    # Behavior based on code checkbox status
    def checkbox_state_changed(self):
        # Clear section 2 if no checkboxes are selected
        checked_checkboxes = [checkbox for checkbox in self.checkboxes if checkbox.isChecked()]
        if not checked_checkboxes:
            self.populate_section2()
            return

        # Update the corresponding entry's enabled status in the XML
        sender = self.sender()
        entry = sender.entry
        enabled = "true" if sender.isChecked() else "false"
        entry_enabled = entry.find("enabled")
        entry_enabled.text = enabled

        # Update the XML file with the new entry enabled status
        with open(file_path, 'r') as f:
            xml_content = f.read()
        root = etree.fromstring(xml_content)
        for entry in root.findall(".//entry"):
            if entry.attrib['name'] == sender.entry.attrib['name']:
                entry_enabled = entry.find("enabled")
                entry_enabled.text = enabled
                break

        test = etree.tostring(root)
        test2 = test.decode("utf-8")
        
        with open(file_path, 'w') as f:
            f.write(test2)

        # Update the list of checked checkboxes
        if sender.isChecked():
            checked_checkboxes.append(sender)
        else:
            try:
                checked_checkboxes.remove(sender)
            except ValueError:
                pass

        # Find the last selected checkbox
        self.last_checked_checkbox = checked_checkboxes[-1]

        # Populate section 2 with the last selected checkbox's entry's data
        self.populate_section2(self.last_checked_checkbox.entry)

                
    # Function to refresh GUI elements
    def refresh_gui(self):
        # Clear section 1
        
        try:
            for checkbox in self.checkboxes:
                self.scroll_areaLayout.removeWidget(checkbox)
                checkbox.deleteLater()
            self.checkboxes = []

            # Repopulate section 1
            self.populate_section1()
            self.populate_section2(self.last_checked_checkbox.entry)

        except:
            pass
        
    # Function to send codes
    def send_code(self):
        # Get the list of enabled checkboxes
        enabled_checkboxes = [checkbox for checkbox in self.checkboxes if checkbox.isChecked()]

        try:
            # Loop through the checkboxes and send code if arw is enabled
            for checkbox in enabled_checkboxes:
                entry = checkbox.entry
                assembly_ram_writes_enabled = entry.find("assembly_ram_write").text == "true"
                if assembly_ram_writes_enabled:
                    code = entry.find("code").text
                    for line in code.split("\n"):
                        if not line.startswith("#"):
                            tcp_socket.s.send(bytes.fromhex('03'))
                            tcp_socket.s.send(bytes.fromhex(line))
        
            pre_cafe_code = []
            cafe_code = ""

            for checkbox in enabled_checkboxes:
                entry = checkbox.entry
                assembly_ram_writes_enabled = entry.find("assembly_ram_write").text == "false"
                if assembly_ram_writes_enabled:
                    code = entry.find("code").text
                    for line in code.split("\n"):
                        if not line.startswith("#"):
                            pre_cafe_code.append(line)
            
            if not pre_cafe_code == []:
                cafe_code = ''.join(pre_cafe_code).replace(' ', '')
                tcp_socket.s.send(bytes.fromhex('03'))
                tcp_socket.s.send(bytes.fromhex('10014CFC00000000'))
                    
                for x in range(math.floor(len(cafe_code)/8)):
                    tcp_socket.s.send(bytes.fromhex('03'))
                    tcp_socket.s.send(bytes.fromhex('0'+format(0x01133000+x*4,'X')+cafe_code[x*8:x*8+8]))
                    print(cafe_code)
                tcp_socket.s.send(bytes.fromhex('03'))
                tcp_socket.s.send(bytes.fromhex('10014CFC00000001'))  
            else:
                pass
                
            self.window = InfoWindow()
            self.window.CreateWindow("Codes Sent!", f"Codes Sent Successfully!", 300, 150)
            self.window.show()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"<b></b>Used IPv4: {self.connection_bar.text()}<br/>Error: {e}.", 500, 200)
            self.window.show()
                    
    # Function to disable codes (only works with Undo lines eg: #101D9D00 3F000000)
    def disable_code(self):
        # Get the list of enabled checkboxes
        enabled_checkboxes = [checkbox for checkbox in self.checkboxes if checkbox.isChecked()]
        count = 0

        # Loop through the checkboxes and disable code if arw is enabled
        try:
            for checkbox in enabled_checkboxes:
                entry = checkbox.entry
                assembly_ram_writes_enabled = entry.find("assembly_ram_write").text == "true"
                if assembly_ram_writes_enabled:
                    code = entry.find("code").text
                    for line in code.split("\n"):
                        if line.startswith("#"):
                            code = line.replace("#", "")
                            tcp_socket.s.send(bytes.fromhex('03'))
                            tcp_socket.s.send(bytes.fromhex(code))
                            count += 1
                        else:
                            pass
                        
            # Loop through checkboxes and disable code if arw is disabled
            pre_cafe_code = []

            for checkbox in enabled_checkboxes:
                entry = checkbox.entry
                assembly_ram_writes_enabled = entry.find("assembly_ram_write").text == "false"
                if assembly_ram_writes_enabled:
                    code = entry.find("code").text
                    for line in code.split("\n"):
                        if line.startswith("#"):
                            pre_cafe_code.append(line)
                            count += 1

            if not pre_cafe_code == []:
                cafe_code = ''.join(pre_cafe_code).replace(' ', '')
                cafe_code = cafe_code.replace('#', '')
                
                tcp_socket.s.send(bytes.fromhex('03'))
                tcp_socket.s.send(bytes.fromhex('10014CFC00000000'))
                
                for x in range(math.floor(len(cafe_code)/8)):
                    tcp_socket.s.send(bytes.fromhex('03'))
                    tcp_socket.s.send(bytes.fromhex('0'+format(0x01133000+x*4,'X')+cafe_code[x*8:x*8+8]))
                    
                tcp_socket.s.send(bytes.fromhex('03'))
                tcp_socket.s.send(bytes.fromhex('10014CFC00000001'))
            else:
                pass

            self.window = InfoWindow()
            self.window.CreateWindow("Codes Sent!", f"Codes Disabled Successfully!<br/><br/>{count} undo-lines executed", 350, 150)
            self.window.show()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"<b></b>Used IPv4: {self.connection_bar.text()}<br/>Error: {e}.", 500, 200)
            self.window.show()
    
    # Function to open the add code menu
    def open_code_creator(self):
        entry_name = None
        entry_code = None
        entry_author = None
        entry_asm = None
        entry_arw = None
        entry_comment = None
        entry_enabled = None
        self.Code_Creator_Window = CodeCreator(entry_name, entry_code, entry_author, entry_asm, entry_arw, entry_comment, entry_enabled)
        self.Code_Creator_Window.show()
        
    def edit_selected_code(self, external_code=None, external_name=None):
        try:
            if external_code == False:
                entry_code = self.last_checked_checkbox.entry.find("code").text
            else:
                entry_code = external_code
                
            if external_name == "10":
                entry_name = "Imported GCTU Codes"
                entry_author = "QtGecko"
            else:
                entry_name = self.last_checked_checkbox.entry.get("name")
                entry_author = self.last_checked_checkbox.entry.find("authors").text

            entry_asm = self.last_checked_checkbox.entry.find("raw_assembly").text
            entry_arw = self.last_checked_checkbox.entry.find("assembly_ram_write").text
            entry_comment = self.last_checked_checkbox.entry.find("comment").text
            entry_enabled = self.last_checked_checkbox.entry.find("enabled").text
            if entry_author == None:
                entry_author = ""
            self.Code_Creator_Window = CodeCreator(entry_name, entry_code, entry_author, entry_asm, entry_arw, entry_comment, entry_enabled)
            self.Code_Creator_Window.show()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"Error: {e}<br/><br/>Make sure you have a code selected!", 320, 150)
            self.window.show()
        
    def copy_selected_code(self):
        try:
            entry_code = self.last_checked_checkbox.entry.find("code").text
            lines = entry_code.split("\n")
            count = 0
            for line in lines:
                count += 1
            clip = QtWidgets.QApplication.clipboard()
            clip.setText(entry_code)
        
            self.window = InfoWindow()
            self.window.CreateWindow("Copy Success", f"Code copied successfully<br/>Lines copied: {count}", 320, 150)
            self.window.show()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"Error: {e}<br/><br/>Make sure you have a code selected!", 320, 150)
            self.window.show()
        
    def delete_selected_code(self):
        try:
            entry_name = self.last_checked_checkbox.entry.get("name")
        
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            start_index = -1
            end_index = -1

            for i, line in enumerate(lines):
                if '<entry name="' + entry_name + '">' in line:
                    start_index = i
                elif '</entry>' in line and start_index != -1:
                    end_index = i
                    break
                
            if start_index == -1 or end_index == -1:
                print('\033[38;2;255;72;0m[QtGecko]: \033[0mEntry not found or invalid entry format')
            
            del lines[start_index:end_index+1]
        
            with open(file_path, 'w') as f:
                f.write(''.join(lines))
            
            self.refresh_gui()
        except Exception as e:
            self.window = ErrorWindow()
            self.window.CreateWindow("Error!", f"Error: {e}<br/><br/>Make sure you have a code selected!", 320, 150)
            self.window.show()
    
    # Function to open code list
    def select_code_list(self):
        global file_path

        # Create a dialog to allow the user to select their file
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        dialog.setDirectory("codes")

        # Add filters for XML and All files
        filters = ["XML Files (*.xml)", "All Files (*.*)"]
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(filters[0])

        # Sets the XML File Path if successfully selected, if not leave path empty
        if dialog.exec_():
            file_path = dialog.selectedFiles()[0]
        else:
            file_path = "codes/null.xml"

        # Open the file and read its contents
        with open(file_path, "r") as file:
            contents = file.read()

        # Define the regular expression pattern to search for
        pattern = r"<\?xml version=\"1.0\"( encoding=\"(UTF-16|utf-16|UTF-8|utf-8|[Uu][Tt][Ff]-?8)\")?\s*\?>"

        # Replace any matches of the pattern with an empty string
        cleaned_contents = re.sub(pattern, "", contents)

        # Write the cleaned contents back to the file
        with open(file_path, "w") as file:
            file.write(cleaned_contents)
        
        # Call functions to parse XML and populate Code areas
        try:
            self.populate_section1()
            if self.checkboxes:
                try:
                    self.populate_section2(self.last_checked_checkbox.entry)
                except:
                    pass
            self.refresh_gui()
        except Exception:
            pass
            
        print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mLoaded \033[93m{file_path}\033[0m")
        
    # Function to open null.xml
    def open_null_on_start(self):
        global file_path
        file_path = "codes/null.xml"
        
        # Open the file and read its contents
        with open(file_path, "r") as file:
            contents = file.read()

        # Define the regular expression pattern to search for
        pattern = r"<\?xml version=\"1.0\"( encoding=\"(UTF-16|utf-16|UTF-8|utf-8|[Uu][Tt][Ff]-?8)\")?\s*\?>"

        # Replace any matches of the pattern with an empty string
        cleaned_contents = re.sub(pattern, "", contents)

        # Write the cleaned contents back to the file
        with open(file_path, "w") as file:
            file.write(cleaned_contents)
        
        self.populate_section1()
        if self.checkboxes:
            try:
                self.populate_section2(self.last_checked_checkbox.entry)
            except:
                pass
                
        print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mLoaded \033[93m{file_path}\033[0m")
                
    # Function to save current codelist to new file
    def export_code_list(self):
        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "XML Files (*.xml)", options=options)

        if file_name:
            with open(file_path, 'r') as f:
                contents = f.read()

            with open(file_name, 'w') as f:
                f.write(contents)
        
    # Function for Download Codes button
    def open_code_archive(self):
        webbrowser.open("https://github.com/MinecraftWiiUCodes/MinecraftWiiUPlaza")
        
    # Function for Code Types Documentation button
    def open_code_docs(self):
        webbrowser.open("http://web.archive.org/web/20171108014746/http://cosmocortney.ddns.net:80/enzy/cafe_code_types_en.php")
        
    # Function for Untick All button
    def untick_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
        self.checkbox_state_changed()
        
    def delete_codes(self):
        # Return the modified XML string
        with open(file_path, "w") as f:
            f.write('<codes>\n</codes>')
        self.refresh_gui()

        
    #--- Codes Tab Functions End ---#
        
    #--- Conversion Tab Functions ---#
    def open_hex_to_UTF8_window(self):
        self.hex_to_UTF8_Window = hex_to_UTF8_window()
        self.hex_to_UTF8_Window.show()
        
    def open_UTF8_to_hex_window(self):
        self.UTF8_to_hex_Window = UTF8_to_hex_window()
        self.UTF8_to_hex_Window.show()
        
    def open_hex_to_float_window(self):
       self.hex_to_float_Window = hex_to_float_window()
       self.hex_to_float_Window.show()
        
    def open_float_to_hex_window(self):
        self.float_to_hex_Window = float_to_hex_window()
        self.float_to_hex_Window.show()
        
    def open_hex_to_decimal_window(self):
       self.hex_to_decimal_Window = hex_to_decimal_window()
       self.hex_to_decimal_Window.show()
        
    def open_decimal_to_hex_window(self):
        self.decimal_to_hex_Window = decimal_to_hex_window()
        self.decimal_to_hex_Window.show()
        
    def open_hex_to_UTF16_window(self):
        self.hex_to_UTF16_Window = hex_to_UTF16_window()
        self.hex_to_UTF16_Window.show()
        
    def open_UTF16_to_hex_window(self):
        self.UTF16_to_hex_Window = UTF16_to_hex_window()
        self.UTF16_to_hex_Window.show()
    #--- Conversion Tab Functions end ---#
    
    #--- Miscellaneous Tab Functions ---#
    def see_local_ip(self):
        self.window = InfoWindow()
        self.window.CreateWindow("Local IPv4", f"Host name: {socket.gethostname()}<br/>Host IPv4: {socket.gethostbyname(socket.gethostname())}", 320, 150)
        self.window.show()
        
    def show_build_date(self):
        self.window = InfoWindow()
        self.window.CreateWindow("Build Date", "Mar 16, 2023, 08:34:29", 280, 150)
        self.window.show()
        
    def open_bug_tracker(self):
        webbrowser.open("https://github.com/Korozin/QtGecko/issues")
        
    def connection_timeout_changed(self):
        if self.connection_timeout_box.isChecked():
            self.config_manager.write_timeout_true()
        elif not self.connection_timeout_box.isChecked():
            self.config_manager.write_timeout_false()
        else:
            print("\033[38;2;255;72;0m[QtGecko]: \033[0mHow the hell did you even get this error?")
            pass
            
    def on_theme_changed(self, index):
        theme_name = self.theme_combobox.currentText()
        app.setStyle(theme_name)
        print(f"\033[38;2;255;72;0m[QtGecko]: \033[0mTheme changed to: \033[93m{theme_name}\033[0m")
        self.config_manager.write_theme(theme_name)
        
    #--- Miscellaneous Tab Functions End ---#
    
    #--- External Tools Tab Functions ---#
    def download_tcp_gecko(self):
         webbrowser.open("https://github.com/BullyWiiPlaza/tcpgecko/archive/master.zip")
    #--- External Tools Tab Functions End ---#


#--- Code Creator Class ---#
class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor("#EAEAEA")
        painter.fillRect(event.rect(), color)

        fontMetrics = painter.fontMetrics()
        currentBlock = self.editor.firstVisibleBlock()
        top = self.editor.blockBoundingGeometry(currentBlock).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(currentBlock).height()
        lineNumber = currentBlock.blockNumber() + 1

        while currentBlock.isValid() and top <= event.rect().bottom():
            if bottom >= event.rect().top():
                # Draw the line number
                lineNumberText = str(lineNumber)
                lineNumberRect = QtCore.QRect(0, int(top), self.width() - 6, fontMetrics.height())
                painter.drawText(lineNumberRect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, lineNumberText)

            currentBlock = currentBlock.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(currentBlock).height()
            lineNumber += 1


class Editor(QtWidgets.QPlainTextEdit, object):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        # Highlight the current line immediately
        self.highlightCurrentLine()
        

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        count = max(1, self.blockCount())
        space = 20 + self.fontMetrics().horizontalAdvance('10') + 10
        return space

    def updateLineNumberAreaWidth(self, newBlockCount):
        width = self.lineNumberAreaWidth()
        self.setViewportMargins(width, 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super(Editor, self).resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

class CodeCreator(QtWidgets.QMainWindow):
    def __init__(self, entry_name, entry_code, entry_author, entry_asm, entry_arw, entry_comment, entry_enabled):
        super().__init__()

        self.entry_name = entry_name
        self.entry_code = entry_code
        self.entry_author = entry_author
        self.entry_asm = entry_asm
        self.entry_arw = entry_arw
        self.entry_comment = entry_comment
        self.entry_enabled = entry_enabled

        self.InitUI()

    def InitUI(self):
        self.setGeometry(0, 0, 650, 550)
        self.setWindowTitle("Code Creator | KorOwOzin")

        # Create elements
        self.title_label = QtWidgets.QLabel("Title:", self)
        self.title_label.move(5, 5)
        
        self.title_edit = QtWidgets.QLineEdit(self)
        self.title_edit.resize(635, 18)
        self.title_edit.move(5, 30)
        self.title_edit.setText(self.entry_name)
        
        self.author_label = QtWidgets.QLabel("Author(s):", self)
        self.author_label.move(5, 55)
        
        self.author_edit = QtWidgets.QLineEdit(self)
        self.author_edit.resize(635, 18)
        self.author_edit.move(5, 85)
        self.author_edit.setText(self.entry_author)
        
        self.code_label = QtWidgets.QLabel("Code:", self)
        self.code_label.move(5, 110)
        
        self.code_edit = Editor(self)
        self.code_edit.resize(350, 200)
        self.code_edit.move(5, 145)
        self.code_edit.insertPlainText(self.entry_code)
        self.code_edit.textChanged.connect(self.is_code_valid)
        
        self.comment_label = QtWidgets.QLabel("Comment:", self)
        self.comment_label.move(360, 110)
        
        self.comment_edit = QtWidgets.QTextEdit(self)
        self.comment_edit.resize(285, 290)
        self.comment_edit.move(360, 145)
        self.comment_edit.setText(self.entry_comment)

        self.format_button = QtWidgets.QPushButton("Format", self)
        self.format_button.resize(350, 30)
        self.format_button.move(5, 350)
        self.format_button.clicked.connect(self.format_code)
        
        self.raw_assembly_checkbox = QtWidgets.QCheckBox("RAW Machine Code", self)
        self.raw_assembly_checkbox.setEnabled(False)
        self.raw_assembly_checkbox.resize(160, 30)
        self.raw_assembly_checkbox.move(5, 380)
        
        self.assembly_ram_write_checkbox = QtWidgets.QCheckBox("Assembly RAM Write", self)
        self.assembly_ram_write_checkbox.resize(175, 30)
        self.assembly_ram_write_checkbox.move(180, 380)
        
        if self.entry_arw == "true":
            self.assembly_ram_write_checkbox.setChecked(True)
        else:
            self.assembly_ram_write_checkbox.setChecked(False)
        
        self.total_lines_label = QtWidgets.QLabel("Total Lines: 0", self)
        self.total_lines_label.resize(175, 40)
        self.total_lines_label.move(5, 400)
        
        self.code_wizard_button = QtWidgets.QPushButton("Code Wizard", self)
        self.code_wizard_button.resize(350, 30)
        self.code_wizard_button.move(5, 435)
        self.code_wizard_button.clicked.connect(self.open_code_wizard)
        
        self.status_label = QtWidgets.QLabel("Status: OK!", self)
        self.status_label.resize(350, 40)
        self.status_label.move(5, 460)
        
        self.ok_button = QtWidgets.QPushButton("OK", self)
        self.ok_button.resize(635, 30)
        self.ok_button.move(5, 500)
        self.ok_button.clicked.connect(self.save_xml)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.code_edit.setFocus()
        self.is_code_valid()
        
        
    def check_validity(self, input_string):
        lines = input_string.strip().split('\n')
        for line in lines:
            if '#' in line:
                if len(line.strip()) != 18:
                    return False
            else:
                if len(line.strip()) != 17:
                    return False
                parts = line.strip().split()
                if len(parts) != 2:
                    return False
                if len(parts[0]) != 8 or len(parts[1]) != 8:
                    return False
                if not all(c in '0123456789ABCDEFabcdef' for c in (parts[0]+parts[1])):
                    return False
        return True


    def is_code_valid(self):

        if self.check_validity(self.code_edit.toPlainText()):
            self.ok_button.setEnabled(True)
            self.code_edit.setStyleSheet("background-color: #00FF00;")
            self.code_edit.verticalScrollBar().setStyleSheet("background-color: lightGray;")
            self.status_label.setText("Status: OK!")
        else:
            self.ok_button.setEnabled(False)
            self.code_edit.setStyleSheet("background-color: red;")
            self.code_edit.verticalScrollBar().setStyleSheet("background-color: lightGray;")
            self.status_label.setText("Status: Incorrect number of spaces/line breaks!")
            

    def format_code(self):
        code = self.code_edit.toPlainText()
        input_string = code.replace(" ", "").replace("\n", "")
        output_string = ""
        i = 0
        while i < len(input_string):
            if input_string[i] == "#":
                output_string += "#" + input_string[i+1:i+17]
                i += 17
            else:
                output_string += input_string[i:i+17]
                i += 17

        new_output_string = ""
        i = 0
        while i < len(output_string):
            if output_string[i] == "#":
                new_output_string += "#" + output_string[i+1:i+9] + " " + output_string[i+9:i+17]
                i += 17
            else:
                new_output_string += output_string[i:i+8] + " " + output_string[i+8:i+16]
                i += 16
            if i < len(output_string):
                new_output_string += "\n"
        self.code_edit.setPlainText(new_output_string.upper())

                  
    def save_xml(self):
        global file_path
    
        # Create root element if file doesn't exist
        if file_path == "":
            file_path = "codes/null.xml"
        else:
            pass
    
        entry_name = self.entry_name
        
        if entry_name == None:
            entry_name = self.title_edit.text()

        edited_entry = f"""<entry name="{self.title_edit.text()}">
        <code>{self.code_edit.toPlainText()}</code>
        <codeInputType>Cheat Code</codeInputType>
        <authors>{self.author_edit.text()}</authors>
        <raw_assembly>{str(self.raw_assembly_checkbox.isChecked()).lower()}</raw_assembly>
        <assembly_ram_write>{str(self.assembly_ram_write_checkbox.isChecked()).lower()}</assembly_ram_write>
        <comment>{self.comment_edit.toPlainText()}</comment>
        <enabled>{self.entry_enabled}</enabled>
    </entry>"""
    
        appended_entry = f"""    <entry name="{self.title_edit.text()}">
        <code>{self.code_edit.toPlainText()}</code>
        <codeInputType>Cheat Code</codeInputType>
        <authors>{self.author_edit.text()}</authors>
        <raw_assembly>{str(self.raw_assembly_checkbox.isChecked()).lower()}</raw_assembly>
        <assembly_ram_write>{str(self.assembly_ram_write_checkbox.isChecked()).lower()}</assembly_ram_write>
        <comment>{self.comment_edit.toPlainText()}</comment>
        <enabled>false</enabled>
    </entry>
"""

        with open(file_path, 'r') as f:
            content = f.read()

            start_index = content.find('<entry name="' + entry_name + '">')
            end_index = content.find('</entry>', start_index) + len('</entry>')

            if end_index == -1:
                print(f'\033[38;2;255;72;0m[QtGecko]: \033[0mInvalid XML Format!')
            elif start_index == -1:
                print(f'\033[38;2;255;72;0m[QtGecko]: \033[0mEntry: \033[93m{entry_name} \033[0mdoes not exist. Creating it.')
                new_content = content.replace('</codes>', appended_entry + '</codes>')
                with open(file_path, 'w') as f:
                    f.write(new_content)
            else:
                print(f'\033[38;2;255;72;0m[QtGecko]: \033[0mEdited entry: \033[93m{entry_name}\033[0m')
                new_content = content[:start_index] + edited_entry + content[end_index:]
                with open(file_path, 'w') as f:
                    f.write(new_content)

        self.close()
        
    def open_code_wizard(self):
            self.window = ErrorWindow()
            self.window.CreateWindow("Welp..", f"This feature doesn't exist yet..", 280, 150)
            self.window.show()

#--- Code Creator Class End ---#


#--- Conversion Window Classes ---#
class hex_to_UTF8_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hex to UTF-8 Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: #00FF00;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: OK!\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_bytes = bytes.fromhex(input_str)
            hex_str = hex_bytes.decode("utf-8")
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            indicator_label.setText("Result: OK!\n\n")
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText(f"Result: Invalid input (begin 0, end {len(input_str)}, length {len(input_str)})\n\n")
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            indicator_label.setText("Result: OK!\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class UTF8_to_hex_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("UTF-8 to Hex Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: #00FF00;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: OK!\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = "".join("{:02X}".format(ord(c)) for c in input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            indicator_label.setText("Result: OK!\n\n")
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid!\n\n")
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            indicator_label.setText("Result: OK!\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class hex_to_float_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hex to Float-Point Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: red;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: Invalid input (For input string: '')\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def hex_to_float(self, hex_str):
        try:
            hex_int = int(hex_str, 16)
            float_val = struct.unpack('!f', struct.pack('!i', hex_int))[0]
            return float_val
        except:
            pass

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = self.hex_to_float(input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(str(hex_str).replace(".0", ""))
            indicator_label.setText("Result: OK!\n\n")
        except ValueError:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 9:
                label_str = input_str[0:9] + "..."
            indicator_label.setText(f'Result: Invalid input (For input string: "{label_str}")\n\n')
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid input (For input string: '')\n\n")
        if self.output_text.toPlainText() == 'None':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid input (For type: 'None')\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class float_to_hex_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Float-Point to Hex Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: red;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: Invalid input (empty String)\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def float_to_hex(self, f):
        try:
            return format(struct.pack('!f', f).hex().zfill(8)).upper()
        except OverflowError:
            f_str = str(f)
            if "-" in f_str:
                return "FF800000"
            else:
                return "7F800000"

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            input_float = float(input_str)
            hex_str = self.float_to_hex(input_float)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            indicator_label.setText("Result: OK!\n\n")
        except ValueError:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 9:
                label_str = input_str[0:9] + "..."
            indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n\n')
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid input (empty String)\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class hex_to_decimal_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hex to Decimal Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: red;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: Invalid input (Zero length Bitinteger)\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def hex_to_decimal(self, hex_string):
        decimal = int(hex_string, 16)
        return decimal

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = self.hex_to_decimal(input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(str(hex_str))
            indicator_label.setText("Result: OK!\n\n")
        except ValueError:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 7:
                label_str = input_str[:7] + "..."
            indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n\n')
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid input (Zero length Bitinteger)\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class decimal_to_hex_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Decimal to Hex Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: red;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: Invalid input (Zero length Bitinteger)\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            input_int = int(input_str)
            hex_str = format(input_int, 'X')
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            indicator_label.setText("Result: OK!\n\n")
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 9:
                label_str = input_str[:9] + "..."
            indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n\n')
        if input_str == '':
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid input (Zero length Bitinteger)\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class hex_to_UTF16_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hex to UTF-16 Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: #00FF00;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: OK!\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_pairs = [input_str[i:i+4] for i in range(0, len(input_str), 4)]
            hex_pairs = [p[2:] + p[:2] for p in hex_pairs]
            hex_str = bytearray.fromhex("".join(hex_pairs)).decode('utf-16')
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            indicator_label.setText("Result: OK!\n\n")
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            label_str = input_str
            if len(input_str) > 4:
                label_str = input_str[0:4] + "..."
            indicator_label.setText(f'Result: Invalid input (for input string: "{label_str}")\n\n')
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            indicator_label.setText("Result: OK!\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
        
        
class UTF16_to_hex_window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("UTF-16 to Hex Conversion | KorOwOzin")

        self.font = QtGui.QFont()
        self.font.setPointSize(10)

        # Create the input label
        input_label = QtWidgets.QLabel("Input:", self)

        # Create the input text edit
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setFixedHeight(107)
        self.input_text.setFixedWidth(440)
        self.input_text.setFont(self.font)

        # Create the output label
        output_label = QtWidgets.QLabel("Converted:", self)

        # Create the output text browser
        self.output_text = QtWidgets.QTextBrowser(self)
        self.output_text.setReadOnly(True)
        self.output_text.setFixedHeight(107)
        self.output_text.setFixedWidth(440)
        self.output_text.setStyleSheet("background-color: #00FF00;")
        self.output_text.setFont(self.font)
        
        # Create the output indication label
        global indicator_label
        indicator_label = QtWidgets.QLabel("Result: OK!\n\n", self)

        # Create the copy button
        copy_button = QtWidgets.QPushButton("Copy Result", self)
        copy_button.clicked.connect(self.copy_result)

        # Create the cancel button
        cancel_button = QtWidgets.QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Add widgets to the layout
        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_text)

        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(indicator_label)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Connect the text changed signal to the update_output function
        self.input_text.textChanged.connect(self.update_output)

    def update_output(self):
        input_str = self.input_text.toPlainText()
        try:
            hex_str = "".join("{:04X}".format(ord(c)) for c in input_str)
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.verticalScrollBar().setStyleSheet("background-color: #999999;")
            self.output_text.setText(hex_str)
            indicator_label.setText("Result: OK!\n\n")
        except:
            self.output_text.setStyleSheet("background-color: red;")
            self.output_text.setText("")
            indicator_label.setText("Result: Invalid!\n\n")
        if input_str == '':
            self.output_text.setStyleSheet("background-color: #00FF00;")
            self.output_text.setText("")
            indicator_label.setText("Result: OK!\n\n")

    def copy_result(self):
        clip = QtWidgets.QApplication.clipboard()
        clip.setText(self.output_text.toPlainText())
        self.close()
#--- Conversion Window Classes End ---#


#--- Error / Info Window Classes ---#
class ErrorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.error_icon = "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"
        
        self.decoded_data = base64.b64decode(self.error_icon)
        
    def CreateWindow(self, WindowText, LabelText, x_size, y_size):
        self.setWindowTitle(WindowText)
        self.setFixedSize(x_size, y_size)
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        main_layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel(LabelText)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        
        filler_label = QtWidgets.QLabel()
        filler_label.setFixedWidth(10)

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.decoded_data)
        pixmap = pixmap.scaled(50, 50)
        pixmap_label = QtWidgets.QLabel()
        pixmap_label.setFixedSize(50, 50)
        pixmap_label.setPixmap(pixmap)
        self.setWindowIcon(QtGui.QIcon(pixmap))
        
        button = QtWidgets.QPushButton("OK")
        button.clicked.connect(self.close)

        hbox.addWidget(pixmap_label)
        hbox.addWidget(filler_label)
        hbox.addWidget(label)
        vbox.addWidget(button)

        main_layout.addLayout(hbox)
        main_layout.addLayout(vbox)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
        
        
class InfoWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.info_icon = "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"
        
        self.decoded_data = base64.b64decode(self.info_icon)
        
    def CreateWindow(self, WindowText, LabelText, x_size, y_size):
        self.setWindowTitle(WindowText)
        self.setFixedSize(x_size, y_size)
        self.setWindowIcon(QtGui.QIcon("info.png"))
        
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
        hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        main_layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel(LabelText)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        
        filler_label = QtWidgets.QLabel()
        filler_label.setFixedWidth(10)

        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.decoded_data)
        pixmap = pixmap.scaled(50, 50)
        pixmap_label = QtWidgets.QLabel()
        pixmap_label.setFixedSize(50, 50)
        pixmap_label.setPixmap(pixmap)
        self.setWindowIcon(QtGui.QIcon(pixmap))
        
        button = QtWidgets.QPushButton("OK")
        button.clicked.connect(self.close)

        hbox.addWidget(pixmap_label)
        hbox.addWidget(filler_label)
        hbox.addWidget(label)
        vbox.addWidget(button)

        main_layout.addLayout(hbox)
        main_layout.addLayout(vbox)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
#--- Error / Info Window Classes End ---#


if __name__ == "__main__":
    global app
    app = QtWidgets.QApplication(sys.argv)
    # Encoded image data
    encoded_data = "/9j/4AAQSkZJRgABAQAAAQABAAD//gA7Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcgSlBFRyB2ODApLCBxdWFsaXR5ID0gOTAK/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUEBAUKBwcGCAwKDAwLCgsLDQ4SEA0OEQ4LCxAWEBETFBUVFQwPFxgWFBgSFBUU/9sAQwEDBAQFBAUJBQUJFA0LDRQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU/8AAEQgCcgJyAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A/VKiiigAooooAKKKKACiiigAooooAKWiigBKKWkoAWikpaACikpaACkoooABS0lFABS0lFAC0lFFABS0lFABS0lFABRRRQAtJRRQAUUUUAFFFBoAWikooAKKKKACiiigAo70UUAFFFFAC0lFHegAooooAWkoooAKKKKACiiigApaSigApaKSgApaSigAooooAKKKKAFpKKKACg0UUALSUtJQAtJRRQAtFJRQAtFJ+FFABRRRQAtFFJQAUUUUALSUUUAFFFFABS0lFABS0lFAC0UlFAC0lFFAC0lFFABRRRQAtFFFABSUtJQAUUUUAFFFFABS0lFABRRRQAUUUUALSUtJQAUUUUAFFFFABRRRQAtJRRQAUUUtABSUUUAFHaiigAooooAWiikoAKWkooAKKKKACiiigBaSiigAooooAKKKKACiiloASiiigBaSiigAooooAKKKKADFFFFABRRRQAUUUUAFFFFABRS0UAJRRS0AJRRRQAtFJRQAtFJRQAtFFJQAtJRRQAUtJRQAtJRRQAUUUUAFFFFABRRRQAUUUUAFFFFAC0lFFAC0lFFABS0lFABS0lFABS0lFABRRRQAUUUUAFLSUUALSUUUAFFFFAC0lFFAC0lFFABS0lFAC0lFFAC0UlFABRRRmgBaSiigBaSiigBaSiigBaSiigBaQUUUALSdqKKAFopM+1FABRRRQAUUUtACUUUtABRRSUAFLSUtACUUtFACUtFFACUtFFABRRRQAUlLSUAFFFGKACiiigAooooAKKKKAClpKKACiiigAooooAKKKKAClpKKACiiigAoo60UAFFFFABRRX5n/wDBRX/gpHrHwv8AFOo/C/4ZSxW+r20Spqmvg7pLWRhu8qEdAwUrljnBJGOMkA/RXxB458N+E57aDXPEGl6NNcttgj1C9jgaU+iB2BY/StmKRJo1kjdZI2AZWU5BB6EGv5efFPxA8S+N9Xk1TXtdv9W1Bzlri6nZmz+fFe9fs4f8FBvit+zncQWtnqh8ReG1YF9F1Vy8e3v5b9UJ9efpQB/QdRXmP7Ov7QXhj9pX4Zad4x8MylIp1C3VjKwMtnMPvRPj0OcHuMGvTqACivF/2rf2ovDf7KfwyufFGtob+/kPk6bpMcgSS8mPRc4O1R1ZsHAHQnAr8lvGf/BXD47+I9YuLnS7vSfDtizkxWdrZ+Z5a9gXcksffAoA/dGgV+Pv7Nf/AAWE8YaZ4rsNJ+LNnZaz4euZVik1exiMN1aBiB5jLkrIo6kYU4zyelfrzpmp2us6dbX9lOlzZ3MaywzRnKujDIIPoRQBZooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigBaKSigAooooAKKKKACilooAKSlooASloooASloooASilooASilooASilooASilpKACiiigAooooADRRRQAUUUUAFFFFABQaKKACiiigAooooAKKK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SiigBaSiigAopaKAEpaSigApaSigBaSiigAooooAWkoooAKKKKAFopKKAFpKKKAFpKKKAFopKKAClpKKACiiigBaKSigBaKKKACkoooAKWkooAWkoooAKKKKACg0UUAFAoooAO1FFFABR1oooAKKKKACiiloASiiigAooooAKKKKACiiigAooooAKKKWgBKKKKACiiigApaSigAopaKAEooooAKKKKAClpKKACiiigAooooAKKWkoAKKKKAFpKKKACiiigAooooAKKKKACloooASiiigAooooAKKKKACiiloASiiloAKSlpKACiiigAopaKAEooooAKKMUUAFFFFABRRRigAooooAKKKKACiiigAooooAKKKKADrRRRQAUUGigAooooAKKKKACiiigApaSigBaKSloASiiigAoopaAEoopaAEooooAWkoooAWikooAKKKOlABRRRQAtJRRQAtJRRQAUUUUALRSUUALSUUUAFFFFAC0UlFAC0UlFAC0lFFAC0lFFABRRRQAUUUUAFLSUUAFBoooAWkoooAWikz70UALSUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABR3oooAKKKKACiiigAooooAKKKKACiiloAKKSigAooooAKKKKAClpKKAClpKKAClpKWgApKWkoAKWikoAKKKWgApKKKAFpKWkoAKKKKAClpKKAClpKWgBKWkooAKKKKAFpKWigBKWkooAWkopaAEpaKKACkoooAWkpaKAEpaSigBaSlooAKSlpKAFooooAKT0oooABRRRQAtIaKKAFpPWiigA70CiigBaaKKKAF70UUUAB6Ud6KKAFpPSiigANLRRQAUUUUAIKWiigApD0oooAO9LRRQAUUUUAFFFFABSd6KKAA0tFFACUtFFABRRRQAUnrRRQAtFFFACGloooAKTvRRQAtIKKKAFpB0oooAKWiigAooooAKTvRRQAUUUUALRRRQAUUUUAFIOlFFAB60tFFACCg0UUALRRRQAlLRRQAUnrRRQAtFFFABRRRQB//Z"
    # Decode the encoded image data
    decoded_data = base64.b64decode(encoded_data)
    # Create a QtGui.QPixmap from the decoded image data
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(decoded_data)
    # Set the application icon using the QtGui.QPixmap
    app.setWindowIcon(QtGui.QIcon(pixmap))
    main_window = QtGecko()
    app.setStyle(main_window.set_theme)
    # Call function to load null.xml on start
    main_window.open_null_on_start()
    main_window.show()
    sys.exit(app.exec_())
# --- QtGecko End --- #