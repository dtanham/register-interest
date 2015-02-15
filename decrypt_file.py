import os, sys
from cryptography.fernet import Fernet

key = os.environ.get("FERNET_KEY",'')
if(not key):
	print "Please provide the key in the FERNET_KEY environment variable"
	quit(1)

if len(sys.argv) < 2:
	print "Usage: decrypt_addresses.py <encrypted_address_file>"
	quit(1)

with open(sys.argv[1]) as f:
	data = bytes(f.read())

f = Fernet(key)
token = f.decrypt(data, 600)

print token
