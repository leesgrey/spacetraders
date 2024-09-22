import requests
from rich import print
from rich.panel import Panel

s = None
api = 'https://api.spacetraders.io/v2'


def _get(endpoint, print_fn=None):
    r = s.get(api + endpoint)
    r.raise_for_status()
    if print_fn:
        print_fn(r.json())
    return r.json()


def _post(endpoint, data, print_fn=None):
    r = s.post(api + endpoint, data=data)
    r.raise_for_status()
    if print_fn:
        print_fn(r.json())
    return r.json()


# Session management

def start_session():
    global s
    s = requests.Session()

def update_header(data):
    global s
    s.headers.update(data)


def set_header_token(agent_token):
    global s
    s.headers.update({"Authorization": f"Bearer {agent_token}"})


# Game calls

def register_new_agent(callSign, faction="COSMIC"):
    update_header({"Authorization": None})
    data = {"symbol": callSign, "faction": faction}
    return _post('/register', data)


def get_agent(quiet=True):
    def print_fn(r):
        print("agent!")
        print(r)

    return _get('/my/agent', None if quiet else print_fn)['data']


def get_ships(quiet=True):
    def print_fn(r):
        print("ships!")
        print(r)

    return _get('/my/ships', None if quiet else print_fn)['data']


def get_contracts(quiet=True):
    def print_fn(r):
        print("contracts!")
        print(r)

    return _get('/my/contracts', None if quiet else print_fn)['data']


def get_server_status(quiet=True):
    def print_fn(r):
        body = f"{r['status']}\nNext reset: {r['serverResets']['next']}\nReset frequency: {r['serverResets']['frequency']}"
        print(Panel(body, title="SpaceTraders API", subtitle=r['version']))

    return _get('', None if quiet else print_fn)