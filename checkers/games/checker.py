#!/usr/bin/env -S python3
import random
import sys

from checklib import *
from checklib import status

import gamelib


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 25
    uses_attack_data: bool = True

    req_ua_agents = ['python-requests/2.{}.0'.format(x) for x in range(15, 28)]

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.lib = gamelib.TestLib(self)

    def session_with_req_ua(self):
        sess = get_initialized_session()
        if random.randint(0, 1) == 1:
            sess.headers['User-Agent'] = random.choice(self.req_ua_agents)
        return sess

    def random_route_name(self):
        return 'Expedition #{}'.format(random.randint(1, 10000))

    def check(self):
        session = self.session_with_req_ua()
        username, password = rnd_username(), rnd_password()

        ping = self.lib.ping()
        if not ping:
            self.cquit(Status.DOWN)

        self.lib.signup(session, username, password)
        self.lib.signin(session, username, password)

        #check play func
        can_play = self.lib.play(username,session)
        if can_play != 1:
            self.cquit(Status.MUMBLE)


        # Check update pass
        new_pass = rnd_password()
        self.lib.updatePass(new_pass, session)
        sess2 = self.session_with_req_ua()
        self.lib.signin(sess2, username, new_pass) 

        # Check cheated
        cheated = self.lib.cheat(username,sess2)
        if cheated != 1:
            self.cquit(Status.MUMBLE)


        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        sess = self.session_with_req_ua()
        u = rnd_username()
        p = flag

        self.lib.signup(sess, u, p)
        self.lib.signin(sess, u, p)

        id, password = self.lib.getUser(sess)
        if id != 0:
            self.cquit(Status.OK, f"{id}:{u}", f"{u}:{p}:{id}")

        self.cquit(Status.MUMBLE)

    def get(self, flag_id: str, flag: str, vuln: str):
        u, p, userid = flag_id.split(':')
        sess = self.session_with_req_ua()
        self.lib.signin(sess, u, p, status=Status.CORRUPT)

        id, password = self.lib.getUser(sess)
        if id == 0 or password == 0:
            self.cquit(Status.CORRUPT)
        
        if password != flag:
            self.cquit(Status.CORRUPT)
        
        self.cquit(Status.OK)

if __name__ == '__main__':
    c = Checker(sys.argv[2])
    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception() as e:
        cquit(status.Status(c.status), c.public, c.private)