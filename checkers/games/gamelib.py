
import random
import checklib
from checklib import BaseChecker
import requests
from bs4 import BeautifulSoup

PORT = 8785

class TestLib:
    @property
    def api_url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, checker: BaseChecker, port=PORT, host=None):
        self.c = checker
        self.port = port
        self.host = host or self.c.host

    def ping(self):
        try:
            requests.get(f'{self.api_url}')
            return 1
        except Exception as e:
            return 0

    def signup(self, session: requests.Session, username: str, password: str, status: checklib.Status = checklib.Status.MUMBLE):
        resp = session.post(f'{self.api_url}/register', data={
            'username': username,
            'password': password,
        }, timeout=5)
        self.c.assert_eq(resp.status_code, 200, 'Failed to signup',  status=status)
        resp_data = self.c.get_text(resp, 'Failed to signup')
        return resp_data

    def signin(self, session: requests.Session, username: str, password: str,
               status: checklib.Status = checklib.Status.MUMBLE):
        resp = session.post(f'{self.api_url}/login', data={
            'username': username,
            'password': password,
        }, timeout=5, allow_redirects=False)
        self.c.assert_eq(resp.status_code, 302, 'Invalid credentials', status=status)
        resp_data = self.c.get_text(resp, 'Failed to signin: invalid data')
        return resp_data
    

    def play(self, username: str, session: requests.Session, status: checklib.Status = checklib.Status.MUMBLE):
        gameid = random.randint(1,3)
        score = random.randint(1,50)
        timeplay = random.randint(score, 100)
        resp = session.post(f'{self.api_url}/score', json={
            'game_id': gameid,
            'score': score,
            'time': timeplay
        }, timeout=5)
        self.c.assert_eq(resp.status_code, 200, 'Cant play', status=status)
        status = self.c.get_json(resp, 'Cant play, invalid json')['status']
        if status != "ok":
            return 0
        resp = session.get(f'{self.api_url}/scoreboard/{gameid}')
        soup = BeautifulSoup(resp.text, 'html.parser')
        td = soup.find('td',string=username)
        if td:
            tr = td.findParent('tr')
            score_res = tr.findChildren('td')[1].text
            if score_res == str(score):
                return 1
        
        return 0


    def updatePass(self, newpass: str, session: requests.Session, status: checklib.Status = checklib.Status.MUMBLE):
        resp = session.post(f'{self.api_url}/change_password', data={
            "password":newpass
        },allow_redirects=False)
        self.c.assert_eq(resp.status_code, 302, 'update pass not work', status=status)

        
    def cheat(self, username: str, session: requests.Session, status: checklib.Status = checklib.Status.MUMBLE):
        gameid = random.randint(1,3)
        score = random.randint(100,1337)
        timeplay = random.randint(1, 99)
        resp = session.post(f'{self.api_url}/score', json={
            'game_id': gameid,
            'score': score,
            'time': timeplay
        }, timeout=5)
        self.c.assert_eq(resp.status_code, 403, 'Cant cheat', status=status)
        status = self.c.get_json(resp, 'Cant cheat, invalid json')['status']
        if status != "cheating":
            return 0
        resp = session.get(f'{self.api_url}/news')
        soup = BeautifulSoup(resp.text, 'html.parser')
        banned = soup.find('p', string=f"User {username} has been banned for cheating")
        if not(banned):
            return 0
        return 1




        
    def getUser(self, session: requests.Session, status: checklib.Status = checklib.Status.MUMBLE):
        resp = session.get(f'{self.api_url}/profile')
        soup = BeautifulSoup(resp.text, 'html.parser')
        id = soup.find(id="userid")['value']
        password = soup.find(id="password")['value']
        if not(id) or not(password):
            return 0, 0
        return id, password
        




    
        
