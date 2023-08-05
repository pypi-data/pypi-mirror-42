import requests


class EventGateway:
    def __init__(self, url="http://localhost", space="default", adminPort=4001,
                 clientPort=4000):
        self.url = url
        self.space = space
        self.adminPort = adminPort
        self.clientPort = clientPort

    # UTILS #

    def checkConnection(self):
        egHealthCheckUrl = "{}:{}/v1/status".format(
            self.url, str(self.adminPort))
        try:
            r = requests.get(egHealthCheckUrl)
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            print("Cannot connect to {}".format(egHealthCheckUrl))
            return False

    def getAdminUrl(self):
        return "{}:{}/v1/spaces/{}".format(
            self.url, str(self.adminPort), self.space)

    def getClientUrl(self):
        return "{}:{}".format(self.url, str(self.clientPort))

    def printConfig(self):
        return """
            Event-gateway information:
            URL: {}
            Admin port: {}
            Client port: {}
            Space: {}""".format(
                self.url, self.adminPort, self.clientPort, self.space)

    # CREATE STUFF #

    def createEventType(self, params):
        return self.makePostRequest("eventtypes", params, rsrcId="name")

    def createFunction(self, params):
        return self.makePostRequest("functions", params)

    def createSubscription(self, params):
        return self.makePostRequest("subscriptions", params)

    def createCORS(self, params):
        return self.makePostRequest("cors", params, rsrcId="path")

    def createConnection(self, params):
        return self.makePostRequest("connections", params, rsrcId="type")

    # GET STUFF #

    def getAllEventType(self):
        return self.makeGetRequest("eventtypes")

    def getEventType(self, rsrcId):
        return self.makeGetRequest("eventtypes", rsrcId=rsrcId)

    def getAllFunction(self):
        return self.makeGetRequest("functions")

    def getFunction(self, rsrcId):
        return self.makeGetRequest("functions", rsrcId=rsrcId)

    def getAllSubscription(self):
        return self.makeGetRequest("subscriptions")

    def getSubscription(self, rsrcId):
        return self.makeGetRequest("subscriptions", rsrcId=rsrcId)

    # GENERIC GET REQUEST #

    def makeGetRequest(self, resourceType, rsrcId=""):
        url = self.getAdminUrl() + "/" + resourceType
        if (rsrcId):
            url += "/" + rsrcId
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            print("{} {} not found".format(
                resourceType, rsrcId))
            return False
        else:
            print("Issue while getting {} {}\n".format(
                resourceType, rsrcId))
            print(r.json())
            return False

    # GENERIC POST REQUEST #

    def makePostRequest(self, resourceType, params, rsrcId="functionId"):
        url = self.getAdminUrl() + "/" + resourceType
        r = requests.post(url, json=params)
        if r.status_code == 201:
            print("{} {} created successfully".format(
                resourceType.title(), params[rsrcId]))
            return r.json()
        elif r.status_code == 409:
            print("{} {} already exists".format(
                resourceType.title(), params[rsrcId]))
            return False
        else:
            print("Issue while creating {} {}\n".format(
                resourceType.title(), params[rsrcId]))
            print(r.json())
            return False

    # EMIT #

    def emit(self, cloudEvent, path="/",
             headers={"Content-type": "application/json"}):
        url = self.getClientUrl() + path
        r = requests.post(url, json=cloudEvent, headers=headers)
        return r
