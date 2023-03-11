import json, random, time, threading, base64
try:
    from colorama import Fore, init 
    from websocket import WebSocketApp
except:
    import os
    os.system("pip install websocket colorama")
from colorama import Fore, init
init(True, True)

print_lock = threading.Lock()
def print_with_lock(text):
    print_lock.acquire()
    print(text)
    print_lock.release()
class Printer():
    def content(text, content):
        print_with_lock(f"({Fore.LIGHTCYAN_EX}+{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET}: {Fore.CYAN}{content}{Fore.RESET}")
    def cinput(text):
        content = input(f"({Fore.CYAN}~{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET}")
        return content
    def error(text):
        print_with_lock(f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.RED}{text}{Fore.RESET}")
class Onliner():
    def __init__(self, token,i):
        self.token = token 
        self.i = i
        self.connect_to_ws(token)

    def get_random_presence(self):
        status = random.choice(["online","dnd","idle"])
        return {"status":status,"since":0,"activites":[],"afk":False}
    
    def connect_to_ws(self, token):
        from websocket import WebSocketApp
        def on_message(ws:WebSocketApp,msg):
            msg = json.loads(msg)
            if msg["op"] == 10:
                payload = {
                    "op":2,
                    "d":{
                        "token":token,
                        "properties":{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-US","os_version":"10"},
                        "presence":self.get_random_presence(),
                        "compress": False,
                    }
                }
                ws.send(json.dumps(payload))
                Printer.content("Onlined",token+f" {Fore.RESET}|{Fore.BLUE} {self.i}")
        WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9",on_message=on_message).run_forever()
if __name__ == "__main__":
    for i,token in enumerate(open("tokens.txt", "r+").read().splitlines()):
        threading.Thread(target=Onliner,args=(token,i)).start()

