import api
from collections import namedtuple

class Agent:
    def __init__(self):
        data = api.get_agent()

        self.account_id = data["accountId"]
        self.symbol = data["symbol"]
        self.headquarters = Waypoint(data["headquarters"])
        self.credits = data["credits"]
        self.starting_faction = data["startingFaction"]
        self.shipCount = data["shipCount"]

        self.contracts = []
        for contract in api.get_contracts():
            self.contracts.append(Contract(contract))

        self._dict = data # this sucks

    def __repr__(self):
        return f"Agent({self._dict})"  # this sucks

class Contract:
    def __init__(self, data):
        self.id = data['id']
        self.faction_symbol = data['factionSymbol']
        self.type = data['type']

        terms = data['terms']
        payment = terms['payment']
        delivers = terms['deliver']
        self.terms = Terms(
            terms['deadline'],
            Payment(payment['onAccepted'], payment['onFulfilled']),
            map(lambda d: Deliver(d['tradeSymbol'], d['destinationSymbol'],
                                  d['unitsRequired'], d['unitsFulfilled']),
                delivers))

        self.accepted = data['accepted']
        self.fulfilled = data['fulfilled']
        self.expiration = data['expiration']
        self.deadline_to_accept = data['deadlineToAccept']

        self._dict = data

    def __repr__(self):
        return f"Contract({self._dict})"  # this still sucks

    def accept(self):
        self.accepted = api.accept_contract(self.id)


Terms = namedtuple('Terms', ['deadline', 'payment', 'deliver'])
Payment = namedtuple('Payment', ['on_accepted', 'on_fulfilled'])
Deliver = namedtuple(  # rename 
    'Deliver',
    ['trade_symbol', 'destination_symbol', 'units_required', 'units_fulfilled'])

class Waypoint:
    def __init__(self, waypoint: str):
        data = api.get_waypoint(waypoint)
        self.symbol = data['symbol']
        self.type = data['type']
        self.system_symbol = data['systemSymbol']
        self.x = data['x']
        self.y = data['y']
        self.orbitals = data['orbitals']  # expand
        self.faction = data['faction']
        self.traits = data['traits']  # expand
        self.modifiers = data['modifiers']  # expand
        self.chart = data['chart']
        self.is_under_construction = data['isUnderConstruction']