if __name__ == "__main__":
    print("This is a module that is imported by 'QtGecko.py'. Don't run it directly.")
    exit()
else:
    import re

def IP_Verification(ip: str) -> bool:
	if not bool(re.compile(r'[^0-9.]').search(ip)):
		ip_split = ip.split('.')
		if len(ip_split) != 4: return False
		try: return all(0 <= int(p) < 256 for p in ip_split)
		except ValueError: return False
	else: return False
