from fake_useragent import UserAgent

def fake_agent():
    """
    Basic function to generate a fake User Agent
    """
    # Creates an instance of the UserAgent class
    u_ag = UserAgent()
    # Generates a random user agent string
    user_agent = u_ag.random
    headers = {'User-Agent': user_agent}
    return headers
