import requests
import sys
import os


class TickFile:
    def __init__(self):
        self.path = "/tmp/ip_tick.txt"

    def get(self):
        try:
            with open(self.path, "r") as f:
                r = f.read()
                if not r:
                    r = "0"

                return int(r)
        except FileNotFoundError:
            return 0
            
    def update(self, tick):
        with open(self.path, "w") as f:
            return f.write(str(tick))


def show_ip():
    headers = {
        "User-Agent": "curl/7.37.0"
    }
    resp = requests.get('https://2ip.ru/', headers=headers)

    if resp.status_code == 200:
        print(resp.text)
    else:
        print("network error")


def main():
    tf = TickFile()

    if len(sys.argv) > 1:
        tf.update(3)

    if not tf.get():
        print("show ip")
    else:
        tf.update(tf.get() - 1)
        show_ip()


if __name__ == "__main__":
    main()
