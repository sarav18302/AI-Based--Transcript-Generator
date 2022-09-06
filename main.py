#entities.txt - contains entity type and the corresponding text


import pprint
import time
from configure import auth_key
import requests

def poll(transcript_id):
    polling_endpoint=endpoint+"/"+transcript_id
    polling_response=requests.get(polling_endpoint,headers=headers)
    return polling_response.json()

def update_file(data):
    for item in data["entities"]:
        entity_type=item["entity_type"]
        text=item["text"]
        with open('entities.txt', 'a') as f:
            f.write(entity_type+": "+text+"\n")

def processing(transcript_id):
    while True:
        data=poll(transcript_id)
        if data["status"]=="completed" :
            pprint.pprint(data)
            break
        elif data["status"]=="error":
            print("error",data["error"])
            break
        print("processing")
        time.sleep(30)
    update_file(data)


if __name__ == '__main__':
    endpoint = "https://api.assemblyai.com/v2/transcript"


    json={
        "audio_url": "https://bit.ly/3rBnQ8i",
        "entity_detection": True
    }
    headers = {
      "authorization": auth_key,
      "content-type": "application/json"
    }
    response=requests.post(endpoint,json=json,headers=headers)
    transcript_id=response.json()['id']
    processing(transcript_id)






