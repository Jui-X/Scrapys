import requests


def requests_test(ip, port):
    http_url = "http://httpbin.org/ip"
    proxy_url = "http://{0}:{1}".format(ip, port)

    proxy_dict = {
        "http": proxy_url
    }
    response = requests.get(http_url, proxies=proxy_dict)
    print(response.text)


if __name__ == "__main__":
    requests_test("60.189.144.226", "4241")
