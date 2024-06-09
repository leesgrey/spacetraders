import json
import requests
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
import time
from datetime import datetime, timezone
from textwrap import dedent
import sys

s = requests.Session()
api = 'https://api.spacetraders.io/v2'

def get_ships():
    r = s.get(api + '/my/ships')
    return r.json()

def get_contracts():
    r = s.get(api + '/my/contracts')
    return r.json()
    
def statusCheck():
    r = requests.get(api)
    print(r.request)
    status = r.json()
    last_reset = datetime.fromisoformat(status["resetDate"])
    last_reset_str = f"{last_reset.strftime("%c")} UTC ({datetime.now() - last_reset})"
    next_reset = datetime.fromisoformat(status["serverResets"]["next"])
    next_reset_str = f"{next_reset.strftime("%c")} UTC ({next_reset - datetime.now(timezone.utc)})"
    status_str = dedent(f'''\
        {status["status"]}
        Version: {status["version"]}
        Last reset: {last_reset_str}
        Next reset: {next_reset_str}''')
    print(Panel.fit(status_str, title="STATUS"))

def start_session():
    # display saved agents
    f = open('config.json')
    data = json.load(f)
    f.close()
    agent_str = ""
    for agent in data['agents']:
        agent_str += agent['name'] + '\n'
    print(Panel.fit(agent_str[:-1], title="AGENTS"))

    # choose agent to load
    print("START SESSION FOR AGENT:")
    agent_name = input()

    matching_agent = None
    for agent in data['agents']:
        if agent['name'] == agent_name:
            matching_agent = agent['token']
            break

    if matching_agent is None:
        print(f"Could not find agent with name {agent_name}")
        return

    s.headers.update({"Authorization": f"Bearer {matching_agent}"})
    print(f"Started session for agent {agent_name}")
    return 

def registerNewAgent(callSign, faction = "COSMIC"):
    response = requests.post(
        api + '/register',
        data = '{'
            f'"symbol": "{callSign}",'
            f'"faction": "{faction}"'
        '}'
    )
    print(response)

def getWaypoint(waypoint):
    address = getAddressFromWaypoint(waypoint)
    r = s.get(api + f'/systems/{address['system']}/waypoints/{address['waypoint']}')
    print(r.json())

def getAgent():
    response = s.get(
        api + '/my/agent',
    )
    response.raise_for_status()
    return response.json()['data']

def getAddressFromWaypoint(waypoint):
    sections = waypoint.split('-')
    return {
        "sector": sections[0],
        "system": sections[0] + '-' + sections[1],
        "waypoint": waypoint
    }

def acceptContract(id):
    r = s.post(api + f"/my/contracts/{id}/accept")
    print(r.json())

def getWaypointsInSystem(system, traits=None):
    r = s.get(
        api + f'/systems/{system}/waypoints',
        params = {
            'traits': traits
        }
    )
    print(r.json())

def buyShip(shipType, waypoint):
    r = s.post(
        api + '/my/ships',
        data = {
            'shipType': shipType,
            'waypointSymbol': waypoint
        }
    )
    print(r.json())

def getAvailableShipsAtShipyard(waypoint):
    r = s.get(
        api + f'/systems/{getAddressFromWaypoint(waypoint)['system']}/waypoints/{waypoint}/shipyard'
    )
    print(r.json())


def extract(ship):
    r = s.post(api + f'my/ships/{ship}/extract')
    print(r.json())
    return r.json()

def main():
    if len(sys.argv) > 1:
        print('contract attempt')

    else:
        statusCheck()
        start_session()
        try:
            agent = Agent(getAgent())
            print(agent)
        except:
            print("uh oh")
        #getWaypoint(agent['headquarters'])
        #getContracts()
        #getWaypointsInSystem(getAddressFromWaypoint(agent['headquarters'])['system'], "SHIPYARD")
        #getAvailableShipsAtShipyard("X1-PQ10-H54")
        #buyShip("SHIP_MINING_DRONE", "X1-PQ10-H54")
        #getShips()

        #data = None
        #data = extract("BREAD-3")['data']
        #while (data is not None and data['cargo']['units'] < data['cargo']['capacity']):
        #    time.sleep(data['cooldown']['remainingSeconds'])
        #    data = extract("BREAD-3")['data']

if __name__ == '__main__':
    main()