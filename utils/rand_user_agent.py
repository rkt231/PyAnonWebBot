from random_user_agent.user_agent import UserAgent

def rand_uagent():
    """
    From https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
    """
    user_agent_rotator = UserAgent(limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {'User-Agent': user_agent}
    return headers
