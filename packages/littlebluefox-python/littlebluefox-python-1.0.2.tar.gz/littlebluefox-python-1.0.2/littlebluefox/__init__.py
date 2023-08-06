import json
import urllib3

DefaultEndpointUrl = 'https://events.littlebluefox.io'

class LittleBlueFoxClient(object):

    def __init__(self, access_token, endpoint_url = None):
        self.access_token = access_token

        if endpoint_url is None:
            self.endpoint_url = DefaultEndpointUrl
        else:
            self.endpoint_url = endpoint_url

    def push(self, event):
        encoded_data = json.dumps(event).encode('utf-8')

        headers = {}
        headers['Authorization'] = 'Bearer {}'.format(self.access_token)
        headers['Content-Type'] = 'application/json'

        resp = http.request(
                'POST',
                self.endpoint_url,
                body=encoded_data,
                headers=headers)

        if resp.status < 200 or resp.status >= 300:
            raise Exception('Unexpected response code: {}'.format(resp.status_code))

        return True
