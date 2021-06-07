import zerorpc
import requests

class StreamingRPC(object):
    
    # @zerorpc.stream
    def get_bot_response(self, bot_id, message):

        url = "http://127.0.0.1:8000/api/ask-question/"

        payload = "id={}&question={}".format(bot_id, message)
        print("payload ==> ", payload)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'Accept': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        return response.text
    

zerorpc_server = zerorpc.Server(StreamingRPC(), heartbeat=None)
zerorpc_server.bind("tcp://0.0.0.0:4242")
zerorpc_server.run()