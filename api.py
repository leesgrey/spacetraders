#  api wrapper

import json
from requests import Request, Session, exceptions

url = 'https://api.spacetraders.io/v2'

s = Session()
s.headers.update(
    {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })

def _send_request(
        method: str, endpoint: str, params: dict = None, data: dict = None):
    try:
        req = Request(method, url + endpoint)
        preq = s.prepare_request(req);
        if params:
            print("uh oh")
            print(params)
            print(url)
            preq.prepare_url(params=params, url=url + endpoint)
            print("yippee")
        if data:
            preq.prepare_body(json.dumps(data), files=None)

        r = s.send(preq)

        print(r.request.url)

        r.raise_for_status()
        return r.json()

    except exceptions.ConnectionError as e:
        print("! ConnectionError")
        print("! " + e.args[0])
    except exceptions.HTTPError as e:
        print("! HTTPError")
        print("! " + e.args[0])
    except exceptions.Timeout as e:
        print("! Timeout")
        print("! " + e.args[0])
    except exceptions.TooManyRedirects as e:
        print("! TooManyRedirects")
        print("! " + e.args[0])
    except exceptions.RequestException as e:
        print("! RequestException")
        print("! " + e.args[0])
    except Exception as e:
        print("! Exception")
        print("! " + e.args[0])

def get_server_status() -> dict:
    """return the status of the game server"""
    try:
        r = _send_request('GET', '/')
        return r
    except Exception:
        print("! could not get server status")

def register_new_agent(symbol: str, faction: str = "COSMIC") -> str:
    """register a new agent with call sign symbol and faction.
    returns the new agent's authentication token
    """
    print(f"Registering new agent {symbol.upper()} in faction {faction}")
    try:
        r = _send_request(
            'POST', '/register',
            data = {
                'symbol': symbol,
                'faction': faction
            })

        if r is None:
            raise RuntimeError

        return r['data']['token']
    except RuntimeError:
        print(f"! Failed to register new agent {symbol} in faction {faction}")

def set_session_token(token: str) -> bool:
    s.headers.update({"Authorization": f"Bearer {token}"})

def get_session_token() -> str:
    try:
        auth_str = s.headers['Authorization']
        return auth_str.split()[-1]
    except KeyError:
        print('=' * 10 + "\nno authorization header found\n" + '=' * 10)

def has_session_token() -> bool:
    return 'Authorization' in s.headers

def get_agent() -> dict:
    """retrieves agent information from the current authorization token"""
    try:
        if not has_session_token():
            raise RuntimeError("! no authorization header set")

        r = _send_request(
            'GET', '/my/agent'
        )

        if r is None:
            raise RuntimeError("! no agent found for current token")

        return r['data']

    except RuntimeError as e:
        print(e)

def get_waypoint(waypoint: str) -> dict:
    try:
        parts = waypoint.split('-')
        if (len(parts) != 3):
            raise ValueError
        system = parts[0] + '-' + parts[1]

        r = _send_request('GET', f'/systems/{system}/waypoints/{waypoint}')

        if r is None:
            raise RuntimeError
        
        return r['data']

    except ValueError:
        print(f"! invalid waypoint format \"{waypoint}\"")
    except RuntimeError:
        print(f"! could not find waypoint {waypoint}")

def get_contracts() -> list:
    try:
        r = _send_request('GET', '/my/contracts')

        if r is None:
            raise RuntimeError

        return r['data']
    except RuntimeError:
        print("! could not find contracts")
        return []

def accept_contract(id: str) -> bool:
    try:
        _send_request('POST', f'/my/contracts/{id}/accept')
        return True
    except Exception as e:
        print(f"! could not accept contract {id}")
        return False

def get_system_waypoints(system: str, traits: list = None) -> list:
    r = _send_request('GET', f'/systems/{system}/waypoints', params={'traits': traits})
    return r['data']

if __name__ == "__main__":
    print("api.py")