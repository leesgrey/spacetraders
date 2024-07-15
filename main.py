import api
from agent import Agent

def start_new_agent(symbol: str, faction: str = "COSMIC") -> Agent:
    try:
        token = api.register_new_agent(symbol, faction)
        print(token)
        if token is None:
            raise RuntimeError
        api.set_session_token(token)
        return Agent()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    try:
        """
        agent = start_new_agent("MITYA1")
        if agent is None:
            raise RuntimeError
        """
        api.set_session_token("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTUlUWUExIiwidmVyc2lvbiI6InYyLjIuMCIsInJlc2V0X2RhdGUiOiIyMDI0LTA2LTMwIiwiaWF0IjoxNzIxMDI0ODE2LCJzdWIiOiJhZ2VudC10b2tlbiJ9.itc6x_BBMafJ1G5obrFaPB5PWbsWE5SIr3mmXHCdfN9U9NPqjmOmy3-L8lqO6R2fNhUmexgcZnCOVCA0mzs57H-l_7VKkvhNFKmcIV3ZC_9Xgt9W6GSSGd-3nA6iqto-_JcnVHhyxMn4ASrQxwJ4i4pKQq4zmb5Pq_fgluYiDrX7NKZl-zvePly7TsLyrpNJjh8Uhn_rGj9i-B27YBQ2QWYvsCWlopGGdE3wgtX3MqzE50LTM77MVS0a2E70cTudROroFWuxQ8DM5ZtziPQG3eGmaxPoabk0Q50EQ1Hg7AXQwDwtnwUhdc1EtZAmgdTnL8dpHdS-kl0kbByBbYfp8A")
        agent = Agent()
        
        waypoints = api.get_system_waypoints(agent.headquarters.system_symbol, traits=['SHIPYARD'])

        for waypoint in waypoints:
            print(waypoint)
            print('\n')

    except Exception as e:
        print(e)
