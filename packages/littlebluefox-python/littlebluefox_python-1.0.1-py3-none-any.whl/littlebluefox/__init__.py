import requests

DefaultEndpointUrl = 'https://events.littlebluefox.io'

class LittleBlueFoxClient(object):

    def __init__(self, access_token, endpoint_url = None):
        self.access_token = access_token

        if endpoint_url is None:
            self.endpoint_url = DefaultEndpointUrl
        else:
            self.endpoint_url = endpoint_url

    def push(self, event):
        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.access_token)

        resp = requests.post(self.endpoint_url, json=event, headers=headers)

        if resp.status_code < 200 or resp.status_code >= 300:
            raise Exception('Unexpected response code: {}'.format(resp.status_code))

        return True
