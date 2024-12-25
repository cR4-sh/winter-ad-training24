#!/usr/bin/env -S python3
import random
import sys
import json

if True:
    saved_args = sys.argv.copy()

from checklib import * 
from pwn import PwnlibException

import minions_lib

ALPH = [chr(i) for i in range(65, 65 + 26)] + [chr(i) for i in range(97, 97 + 26)]

class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 15
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.lib = minions_lib.MinionLib(self)
    
    @property
    def _random_length(self) -> int:
        return random.randint(3,15)

    @property
    def _random_chars(self) -> str:    
        return rnd_string(self._random_length, ALPH)

    def check(self):
        self.lib.connect()

        username1, password1, secret1 = rnd_username(), rnd_password(), self._random_chars
        username2, password2, secret2 = rnd_username(), rnd_password(), self._random_chars

        family_name, family_password = rnd_username(), rnd_password()

        self.lib.register(username1, password1, secret1)
        self.lib.register(username2, password2, secret2)

        self.lib.login(username1, password1)

        profile: str = self.lib.get_profile()
        self.assert_in(username1, profile,
                         'Failed to get username from profile', status=Status.MUMBLE)
        self.assert_in(secret1, profile,
                         'Failed to get secret from profile', status=Status.MUMBLE)
        
        self.lib.create_family(family_name, family_password)
        family_info: str = self.lib.get_family_info()
        self.assert_in(username1, family_info,
                         'Failed to get username from family info', status=Status.MUMBLE)
        self.assert_in(secret1, family_info,
                         'Failed to get secret from family info', status=Status.MUMBLE)
        
        self.lib.logout()
        self.lib.login(username2, password2)
        
        profile: str = self.lib.get_profile()
        self.assert_in(username2, profile,
                         'Failed to get username from profile', status=Status.MUMBLE)
        self.assert_in(secret2, profile,
                         'Failed to get secret from profile', status=Status.MUMBLE)
        
        self.lib.join_family(family_name, family_password)
        family_info: str = self.lib.get_family_info()
        self.assert_in(username1, family_info,
                         'Failed to get username from family info', status=Status.MUMBLE)
        self.assert_in(secret1, family_info,
                         'Failed to get secret from family info', status=Status.MUMBLE)
        self.assert_in(username2, family_info,
                         'Failed to get username from family info', status=Status.MUMBLE)
        self.assert_in(secret2, family_info,
                         'Failed to get secret from family info', status=Status.MUMBLE)
        
        family_member_info: str = self.lib.get_family_member_info(username1)
        self.assert_in(username1, family_member_info,
                         'Failed to get username from family member info', status=Status.MUMBLE)
        self.assert_in(secret1, family_member_info,
                         'Failed to get secret from family member info', status=Status.MUMBLE)

        self.cquit(Status.OK)
        
    def put(self, flag_id: str, flag: str, vuln: str):
        self.lib.connect()
        username1, password1 = rnd_username(), rnd_password()
        username2, password2, secret2 = rnd_username(), rnd_password(), self._random_chars
        
        family_name, family_password = rnd_username(), rnd_password()

        self.lib.register(username1, password1, flag)
        self.lib.register(username2, password2, secret2)

        self.lib.login(username1, password1)
        self.lib.create_family(family_name, family_password)

        self.lib.logout()
        self.lib.login(username2, password2)

        self.lib.join_family(family_name, family_password)

        public_data = {
            "minion_1": username1,
            "minion_2": username2,
            "family_name": family_name
        }

        private_data = f"{username1}:{username2}:{password1}:{password2}"
        self.cquit(Status.OK, json.dumps(public_data), private_data)

    def get(self, private_data: str, flag: str, vuln: str):
        username1, username2, password1, password2 = private_data.split(":")

        self.lib.connect()

        self.lib.login(username1, password1, Status.CORRUPT)
        profile: str = self.lib.get_profile()
        self.assert_in(flag, profile,
                         'Flag not found in user profile', status=Status.CORRUPT)
        
        self.lib.logout(Status.CORRUPT)
        self.lib.login(username2, password2, Status.CORRUPT)

        family_info: str = self.lib.get_family_info()
        self.assert_in(flag, family_info,
                         'Flag not found in family info', status=Status.CORRUPT)
        
        family_member_info: str = self.lib.get_family_member_info(username1)
        self.assert_in(flag, family_member_info,
                         'Flag not found in family member info', status=Status.CORRUPT)

        self.cquit(Status.OK)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except (PwnlibException, EOFError):
            self.cquit(Status.DOWN, "Connection error", "Got pwntools connection error")

if __name__ == '__main__':
    c = Checker(saved_args[2])

    try:
        c.action(saved_args[1], *saved_args[3:])
    except c.get_check_finished_exception() as e:
        cquit(Status(c.status), c.public, c.private)