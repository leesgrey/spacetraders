import api
class Agent:
    def __init__(self, agent_json):
        self.symbol = agent_json['symbol']
        self.headquarters = agent_json['headquarters']
        self.credits = agent_json['credits']
        self.starting_faction = agent_json['startingFaction']
        self.ship_count = agent_json['shipCount']
        self.ships = []
        self.contracts = []

        ships_data = api.get_ships()
        for ship in ships_data:
            self.ships.append(Ship(ship))

        contracts_data = api.get_contracts()
        for contract in contracts_data:
            self.contracts.append(Contract(contract))

    def __repr__(self):
        return f"Agent({self.symbol})"


class Ship:
    def __init__(self, ship_json):
        self.symbol = ship_json['symbol']
        self.registration = ship_json['registration']
        self.nav = ship_json['nav']
        self.crew = ship_json['crew']
        self.frame = ship_json['frame']
        self.reactor = ship_json['reactor']
        self.engine = ship_json['engine']
        self.cooldown = ship_json['cooldown']
        self.modules = ship_json['modules']
        self.mounts = ship_json['mounts']
        self.cargo = ship_json['cargo']
        self.fuel = ship_json['fuel']
    
    def __repr__(self):
        return f"Ship({self.symbol})"

class Contract:
    def __init__(self, contract_json):
        self.id = contract_json['id']
        self.factionSymbol = contract_json['factionSymbol']
        self.type = contract_json['type']
        self.terms = contract_json['terms']
        self.accepted = contract_json['accepted']
        self.fulfilled = contract_json['fulfilled']
        self.expiration = contract_json['expiration']
        self.deadline_to_accept = contract_json['deadlineToAccept']

    def __repr__(self):
        return f"Contract({self.id})"