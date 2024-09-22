import json
from rich import print

from classes import Agent
import api

def clean_agents():
    with open('config.json', 'r') as f:
        data = json.load(f)

    def token_is_valid(token):
        api.set_header_token(token)
        try:
            api.get_agent()
            return True
        except:
            return False

    data['agents'][:] = [agent for agent in data['agents'] if token_is_valid(agent['token'])]

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)


def start_agent_session():
    with open('config.json', 'r') as f:
        data = json.load(f)

    name = input("Enter new or existing agent name: ")

    matching_agent_token = None
    for agent in data['agents']:
        if agent['name'] == name:
            matching_agent_token = agent['token']
            break

    if matching_agent_token is not None:
        api.set_header_token(matching_agent_token)
        return True

    try:
        token = api.register_new_agent(name)
        data['agents'].append({'name': name, 'token': token['token']})
    except Exception as e:
        print(f"Could not register agent {name}: {e}")
        return False

    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    api.start_session()
    api.get_server_status(quiet=False)
    clean_agents()

    is_in_session = False
    while is_in_session == False:
        is_in_session = start_agent_session()

    agent = Agent(api.get_agent())
    print(agent)

    while True:
        user_input = input("c - contracts, s - ships")
        if user_input == 'c':
            print(agent.contracts)
        elif user_input == 's':
            print(agent.ships)