if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import os, configparser, colorama

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
            print(f"{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET} Connection Timeout: {colorama.Fore.YELLOW}'{self.connection_timeout_option}'{colorama.Fore.RESET}")
        else:
            print(f"{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET} Connection Timeout: {colorama.Fore.YELLOW}'{self.connection_timeout_option}'{colorama.Fore.RESET}")

        if self.last_used_ipv4:
            print(f"{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET} Last used IPv4: {colorama.Fore.YELLOW}'{self.last_used_ipv4}'{colorama.Fore.RESET}")
            
        if self.theme_option:
            print(f"{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET} Current theme: {colorama.Fore.YELLOW}'{self.theme_option}'{colorama.Fore.RESET}")

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
                    if option_name == "ipv4":
                        option_name = "IPv4"
                    else:
                        option_name = option_name
                    print(f"{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET} Wrote value: {colorama.Fore.YELLOW}'{option_value}'{colorama.Fore.RESET} to tag: {colorama.Fore.GREEN}'{option_name}'{colorama.Fore.RESET}")
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
