from checklib import * 
from pwn import context, remote

context.timeout = 10
context.log_level = 'FATAL'

PORT = 7771

REGISTER = b'1'
LOGIN = b'2'
PROFILE = b'3'

CREATE_FAMILY = b'4'
JOIN_FAMILY = b'5'
GET_FAMILY_INFO = b'6'
GET_MEMBER_INFO = b'7'

LOGOUT = b'8'
EXIT = b'9'

class MinionLib:
    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT
    
    def connect(self):
        self.r = remote(self.c.host, self.port)
        self.r.recvuntil(b'Enter command: ')

    
    def register(self, 
                 username: str, 
                 password: str, 
                 secret: str, 
                 status: Status = Status.MUMBLE):
        self.r.sendline(REGISTER)

        self.r.recvuntil(b'Enter minions name: ')
        self.r.sendline(username.encode())

        self.r.recvuntil(b'Enter minions password: ')
        self.r.sendline(password.encode())

        self.r.recvuntil(b'Enter minions secret: ')
        self.r.sendline(secret.encode())

        response: str = self.r.recvuntil(b'Enter command: ').decode()
        self.c.assert_in('Minion successfully registered!', response,
                         'Registration failed', status=status)
        
    def login(self, 
              username: str, 
              password: str, 
              status: Status = Status.MUMBLE):
        self.r.sendline(LOGIN)

        self.r.recvuntil(b'Enter minions name: ')
        self.r.sendline(username.encode())

        self.r.recvuntil(b'Enter minions password: ')
        self.r.sendline(password.encode())

        response: str = self.r.recvuntil(b'Enter command: ').decode()
        self.c.assert_in('Logged in your minion!', response,
                         'Login failed', status=status)

    def get_profile(self) -> str:         
        self.r.sendline(PROFILE)
        return self.r.recvuntil(b'Enter command: ').decode()
        
    def create_family(self, 
                      family_name: str, 
                      family_password: str, 
                      status: Status = Status.MUMBLE):
        self.r.sendline(CREATE_FAMILY)

        self.r.recvuntil(b'Enter family name: ')
        self.r.sendline(family_name.encode())

        self.r.recvuntil(b'Enter family password: ')
        self.r.sendline(family_password.encode())

        response: str = self.r.recvuntil(b'Enter command: ').decode()
        self.c.assert_in('Family successfully created!', response,
                         'Failed to create family', status=status)
        
    def join_family(self, 
                    family_name: str, 
                    family_password: str, 
                    status: Status = Status.MUMBLE):
        self.r.sendline(JOIN_FAMILY)

        self.r.recvuntil(b'Enter family name: ')
        self.r.sendline(family_name.encode())

        self.r.recvuntil(b'Enter family password: ')
        self.r.sendline(family_password.encode())

        response: str = self.r.recvuntil(b'Enter command: ').decode()
        self.c.assert_in('Successfully joined to the family!', response,
                         'Failed to join family', status=status)
        
    def get_family_info(self) -> str:
        self.r.sendline(GET_FAMILY_INFO)
        return self.r.recvuntil(b'Enter command: ').decode()

    def get_family_member_info(self, minion_name: str) -> str:
        self.r.sendline(GET_MEMBER_INFO)

        self.r.recvuntil(b'Enter minion\'s name to get info: ')
        self.r.sendline(minion_name.encode())
        return self.r.recvuntil(b'Enter command: ').decode()

    def logout(self, status: Status = Status.MUMBLE):
        self.r.sendline(LOGOUT)
        response: str = self.r.recvuntil(b'Enter command: ').decode()
        self.c.assert_in('Logged out!', response,
                         'Failed to logout', status=status)
        
    def exit(self, status: Status = Status.MUMBLE):
        self.r.sendline(EXIT)
        response: str = self.r.recvuntil(b'See you later!').decode()
