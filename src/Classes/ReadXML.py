if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import colorama

# Functions for reading XML file
def read_names(file_path):
    # Open the XML file
    with open(file_path, "r") as file:
        xml = file.read()

    with open(file_path, "r") as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        modified_lines.append(line.replace("<code/>", "<code></code>"))

    with open(file_path, "w") as file:
        file.writelines(modified_lines)

    # Split the XML into lines
    lines = xml.split("\n")
    names = []
    authors = []

    # Loop through each line and print the name of each entry
    for line in lines:
        if "<entry" in line:
            name_start = line.index("name=") + 6
            name_end = line.index('"', name_start)
            name = line[name_start:name_end]
            names.append(name)
    return names
    
def see_enabled_codes(file_path):
    # Open the XML file
    with open(file_path, "r") as file:
        xml = file.read()

    # Split the XML into lines
    lines = xml.split("\n")
    enabled_list = []

    # Loop through each line and print the name of each entry
    for line in lines:
        if "<enabled>" in line:
            enabled_start = line.index("<enabled>") + 9
            enabled_end = line.index('</enabled>', enabled_start)
            enabled = line[enabled_start:enabled_end]
            enabled_list.append(enabled)
    return enabled_list

def read_codes(file_path, entry_name):
    # Open the XML file
    with open(file_path, "r") as file:
        data = file.read()

    # Find the start and end positions of the specified entry name
    entry_start_tag = '<entry name="{}">'.format(entry_name)
    entry_end_tag = '</entry>'
    entry_start = data.find(entry_start_tag)
    entry_end = data.find(entry_end_tag, entry_start)

    # If specified entry name is not found in the file, print an error message
    if entry_start == -1:
        return

    # Find all the <code> tags within the specified entry and extract their text content
    codes = []
    start_tag = "<code>"
    end_tag = "</code>"
    start = data.find(start_tag, entry_start, entry_end)
    end = data.find(end_tag, start)
    while start != -1 and end != -1:
        # Extract the text content and add it to the `codes` list
        codes.append(data[start+len(start_tag):end].strip())
        # Find the next <code> tag
        start = data.find(start_tag, end, entry_end)
        end = data.find(end_tag, start, entry_end)

    return codes
    
def read_ram_writes_only(file_path, entry_name):
    # Open the XML file
    with open(file_path, 'r') as file:
        data = file.read()

    # Find the entry tag with the specified name
    entry_start_tag = '<entry name="' + entry_name + '">'
    entry_end_tag = '</entry>'
    entry_start = data.find(entry_start_tag)

    # If specified entry name is not found in the file, print an error message
    if entry_start == -1:
        print(f'{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET} Entry name {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET} not found in XML')
        return []

    entry_end = data.find(entry_end_tag, entry_start)

    # If specified entry name is not found in the file, print an error message
    if entry_end == -1:
        print(f'{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET}Entry name {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET} not found in XML')
        return []

    # Check if the entry's assembly_ram_write flag is true
    arw_start_tag = '<assembly_ram_write>true</assembly_ram_write>'
    arw_start = data.find(arw_start_tag, entry_start, entry_end)

    # If the assembly_ram_write flag is not true, return an empty list
    if arw_start == -1:
        return []

    # Find the code content within the entry
    code_start_tag = '<code>'
    code_end_tag = '</code>'
    code_start = data.find(code_start_tag, entry_start, entry_end)
    code_end = data.find(code_end_tag, code_start)

    # If there is no code content within the entry, return an empty list
    if code_start == -1 or code_end == -1:
        return []

    # Extract the code content and add to the list
    code = data[code_start+len(code_start_tag):code_end]
    codes = [code.strip()]

    return codes
    
def read_cafe_codes_only(file_path, entry_name):
    # Open the XML file
    with open(file_path, 'r') as file:
        data = file.read()

    # Find the entry tag with the specified name
    entry_start_tag = '<entry name="' + entry_name + '">'
    entry_end_tag = '</entry>'
    entry_start = data.find(entry_start_tag)

    # If specified entry name is not found in the file, print an error message
    if entry_start == -1:
        print(f'{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET}Entry name {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET} not found in XML')
        return []

    entry_end = data.find(entry_end_tag, entry_start)

    # If specified entry name is not found in the file, print an error message
    if entry_end == -1:
        print(f'{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET}Entry name {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET} not found in XML')
        return []

    # Check if the entry's assembly_ram_write flag is true
    arw_start_tag = '<assembly_ram_write>false</assembly_ram_write>'
    arw_start = data.find(arw_start_tag, entry_start, entry_end)

    # If the assembly_ram_write flag is not true, return an empty list
    if arw_start == -1:
        return []

    # Find the code content within the entry
    code_start_tag = '<code>'
    code_end_tag = '</code>'
    code_start = data.find(code_start_tag, entry_start, entry_end)
    code_end = data.find(code_end_tag, code_start)

    # If there is no code content within the entry, return an empty list
    if code_start == -1 or code_end == -1:
        return []

    # Extract the code content and add to the list
    code = data[code_start+len(code_start_tag):code_end]
    codes = [code.strip()]

    return codes
    
def remove_extra_lines(text):
    lines = text.strip().split('\n')
    return '\n'.join(line.strip() for line in lines)
    
def read_code_comments(file_path, entry_name):
    # Open the XML file
    with open(file_path, "r") as file:
        data = file.read()

    # Find the start and end positions of the specified entry name
    entry_start_tag = '<entry name="{}">'.format(entry_name)
    entry_end_tag = '</entry>'
    entry_start = data.find(entry_start_tag)
    entry_end = data.find(entry_end_tag, entry_start)

    # If specified entry name is not found in the file, print an error message
    if entry_start == -1:
        print(f'{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET}Entry name {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET} not found in XML')
        return

    # Find all the <code> tags within the specified entry and extract their text content
    comments = []
    start_tag = "<comment>"
    end_tag = "</comment>"
    start = data.find(start_tag, entry_start, entry_end)
    end = data.find(end_tag, start)
    while start != -1 and end != -1:
        # Extract the text content and add it to the `codes` list
        comments.append(data[start+len(start_tag):end].strip())
        # Find the next <code> tag
        start = data.find(start_tag, end, entry_end)
        end = data.find(end_tag, start, entry_end)

    return comments
    
def read_code_authors(file_path, entry_name):
    # Open the XML file
    with open(file_path, "r") as file:
        data = file.read()

    # Find the start and end positions of the specified entry name
    entry_start_tag = '<entry name="{}">'.format(entry_name)
    entry_end_tag = '</entry>'
    entry_start = data.find(entry_start_tag)
    entry_end = data.find(entry_end_tag, entry_start)

    # If specified entry name is not found in the file, print an error message
    if entry_start == -1:
        print(f'{colorama.Fore.MAGENTA}[QtGecko]:{colorama.Fore.RESET}Entry name {colorama.Fore.YELLOW}\'{entry_name}\'{colorama.Fore.RESET} not found in XML')
        return

    # Find all the <code> tags within the specified entry and extract their text content
    authors = []
    start_tag = "<authors>"
    end_tag = "</authors>"
    start = data.find(start_tag, entry_start, entry_end)
    end = data.find(end_tag, start)
    while start != -1 and end != -1:
        # Extract the text content and add it to the `codes` list
        authors.append(data[start+len(start_tag):end].strip())
        # Find the next <code> tag
        start = data.find(start_tag, end, entry_end)
        end = data.find(end_tag, start, entry_end)

    return authors
