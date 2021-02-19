import requests


def main():
    ip_site_url = "https://2ip.ru"
    curl_user_agent = "curl/7.58.0"

    headers = {
        "User-Agent": curl_user_agent
    }

    try:
        resp = requests.get(ip_site_url, headers=headers)
    except:
        print_error()
        return

    if resp.status_code != 200:
        print_error()
        return

    print(resp.text)

def print_error():
    print('absent')

if __name__ == "__main__":
    main()
