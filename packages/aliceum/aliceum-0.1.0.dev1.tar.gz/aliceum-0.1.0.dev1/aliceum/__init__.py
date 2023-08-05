import requests
import json


class Alicia:
    '''Creates an instance of Alicia object.'''

    def __init__(self, url):
        request = requests.get(url)
        self.json = request.json()
        self.status = request.status_code

        # self.application = data["application"]
        # self.environment = data["environment"]
        # self.variables = data["variables"]
    def data(self):
        data = self.json
        return data


p = Alicia("https://injector.dev.cleanchoiceenergy.io/")
print(p.data())
