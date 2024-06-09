class Agent:
    def __init__(self, agent_json):
        self.symbol = agent_json['symbol']
        self.headquarters = agent_json['headquarters']
        self.credits = agent_json['credits']
        self.starting_faction = agent_json['startingFaction']
        self.ship_count = agent_json['shipCount']
        self.ships = []
        self.contracts = []

        ships = get_ships()
        for ship in ships['data']:
            self.ships.append(Ship(ship))
        print(self.ships)
        
        contracts = get_contracts()
        print(contracts)
        for contract in contracts['data']:
            self.contracts.append(Contract(contract))
        print(self.contracts)

    def __rich__(self):
        display_str = dedent(f'''\
            Symbol: {self.symbol}
            Headquarters: {self.headquarters}
            Starting faction: {self.starting_faction}
            Ship count: {self.ship_count}
            Credits: {self.credits}''')

        ship_table = Table(title="SHIPS")
        ship_table.add_column("symbol")
        ship_table.add_column("waypoint")
        ship_table.add_column("status")
        ship_table.add_column("units")
        ship_table.add_column("capacity")

        for ship in self.ships:
            ship_table.add_row(ship.symbol, ship.nav['waypointSymbol'], ship.nav['status'], str(ship.cargo['units']), str(ship.cargo['capacity']))

        contract_table = Table(title="CONTRACTS") 
        contract_table.add_column("id")
        contract_table.add_column("type")
        contract_table.add_column("accepted")
        contract_table.add_column("fulfilled")
        contract_table.add_column("expiration")
        contract_table.add_column("deadline_to_accept")

        for contract in self.contracts:
            contract_table.add_row(contract.id, contract.type, str(contract.accepted), str(contract.fulfilled), contract.expiration, contract.deadline_to_accept)

        return Group(Panel.fit(display_str, title="AGENT SUMMARY"), ship_table, contract_table)

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