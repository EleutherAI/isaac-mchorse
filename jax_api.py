import requests
import json


def jax_complete(text, top_p=0.9, temp=0.75):
    resp = requests.post(headers={"content-type": "application/json"},
                         url="http://34.90.220.168:5000/complete",
                         data=json.dumps({"context": text,
                                          "top_p": top_p,
                                          "temp": temp}))
    return resp.json()['completion']
