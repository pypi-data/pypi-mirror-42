import requests
import re
from urllib.parse import urlparse


class EventGateway:
    def __init__(self, url="http://localhost:4000", space="default",
                 configurationUrl="", accessKey="", connectorUrl=""):
        self.space = space
        self.accessKey = accessKey
        if self.isHosted(url):
            self.clientUrl = url
            self.configurationUrl = "https://config.{}".format(
                urlparse(url).netloc)
            self.connectorUrl = self.configurationUrl
        else:
            self.clientUrl = url
            if configurationUrl:
                self.configurationUrl = configurationUrl
            else:
                self.configurationUrl = self.generateUrl(
                    self.clientUrl, "config")
            if connectorUrl:
                self.connectorUrl = self.generateUrl(
                    self.clientUrl, "connector")
            else:
                self.connectorUrl = connectorUrl

    # UTILS #

    def generateUrl(self, url, urlType):
        parsed = urlparse(url)
        port = "4001" if urlType == "config" else "4002"
        return "{}://{}:{}".format(parsed.scheme, parsed.hostname, port)

    def isHosted(self, url):
        reg = re.compile(r"(.+)\.(eventgateway[a-z-]*.io|slsgateway.com)")
        return True if reg.match(url) else False

    def checkConnection(self):
        egHealthCheckUrl = "{}/v1/status".format(self.configurationUrl)
        try:
            r = requests.get(egHealthCheckUrl)
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            print("Cannot connect to {}".format(egHealthCheckUrl))
            return False

    def getAdminUrl(self, rsrc):
        if rsrc == "connections":
            return "{}/v1/spaces/{}".format(
                self.connectorUrl, self.space)
        else:
            return "{}/v1/spaces/{}".format(
                self.configurationUrl, self.space)

    def printConfig(self):
        return """
            Event-gateway information:
            clientUrl: {}
            configUrl: {}
            connectorUrl: {}
            Space: {}""".format(self.clientUrl,
                                self.configurationUrl,
                                self.connectorUrl,
                                self.space)

    def getHeaders(self, header):
        if self.accessKey:
            header["Authorization"] = "bearer {}".format(self.accessKey)
        return header

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
        url = self.getAdminUrl(resourceType) + "/" + resourceType
        headers = self.getHeaders({})
        if (rsrcId):
            url += "/" + rsrcId
        r = requests.get(url, headers=headers)
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
        url = self.getAdminUrl(resourceType) + "/" + resourceType
        headers = self.getHeaders({"Content-type": "application/json"})
        r = requests.post(url, json=params, headers=headers)
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
        url = self.clientUrl + path
        r = requests.post(url, json=cloudEvent, headers=headers)
        return r
