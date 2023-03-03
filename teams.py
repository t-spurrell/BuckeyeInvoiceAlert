from requests import post


class TeamsConfig:
    def __init__(self, url):
        self.url = url
        self.payload = {}

    def text(self, text):
        self.payload["text"] = text
        return self

    def color(self, color):
        self.payload["themeColor"] = color
        return self

    def send(self):
        headers = {"Content-Type": "application/json"}
        return post(self.url, json=self.payload, headers=headers)

