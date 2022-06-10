import requests
import sys


def sendGet(whoisDomain):
    IP2WHOIS_APIKEY = ""
    IP2WHOIS_URL = ""
    authParams = {"key": IP2WHOIS_APIKEY, "domain": whoisDomain}
    response = requests.get(IP2WHOIS_URL, params=authParams)
    print("Developer: noimai.com\nService provided by ip2whois.com")
    print("whois on: ", whoisDomain)
    print("\n")
    return response.content.decode('utf-8')


# END sendGet

def getInputDomain():
    return sys.argv.pop()


# END getInputDomain

def whoisDomain(args):
    domainToCheck = getInputDomain()
    print('2. whoisDomain executing.....', domainToCheck)
    getReturn = sendGet(domainToCheck)
    print(getReturn)
    return 0
