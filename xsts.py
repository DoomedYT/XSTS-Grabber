import requests
import threading

try:
    with open("user_tokens.txt") as f:
        tokens = f.read().splitlines()
        if len(tokens) < 1: exit("No token found in user_tokens.txt")
except FileNotFoundError: exit("user_tokens.txt not found.")


def make(session, token):
    try:
        payload = {
            "RelyingParty":"http://xboxlive.com",
            "TokenType":"JWT",
            "Properties":{
                "SandboxId":"RETAIL",
                "UserTokens":[token]
                }
            }
        r = session.post("https://xsts.auth.xboxlive.com/xsts/authorize", json=payload)

        if r.status_code == 200:
            token = r.json()['Token']
            uhs = r.json()['DisplayClaims']['xui'][0]['uhs']
            print("Token Grabbed. Saving to tokens.txt...")
            with open("tokens.txt", "a") as f:
                f.write(f"XBL3.0 x={uhs};{token}\n")
         #elif r.status_code == 401:
         #    if "start.ui." in r.text:
         #        with open("ms.txt", "a+") as f:
         #            f.write(f"{token}\n")
        elif r.status_code == 408:
            with open("failed_to_check.txt", "a+") as f:
                f.write(f"{token}\n")
        else:
            with open("invalid.txt", "a+") as f:
                f.write(f"{token}\n")
            print(f"Unable to grab XSTS Token. | Status Code: {r.status_code} | Response: {r.text}")
    except Exception as e:
        print(e)

for token in tokens:
    try:
        t = threading.Thread(target=make, args=(requests.Session(), token))
        t.start()
    except:
        pass
