import os
import requests
import json
from requests_toolbelt import MultipartEncoder

username="pankaj"
password="pankaj@123"
auth_url="http://127.0.0.1:8000/auth/obtain_token_pair/"

headers1 = {
    'accept': 'application/json',
    'content-type': 'application/json',
}

r=requests.post(auth_url,data=json.dumps({"username":username,"password":password}),headers=headers1 )
acess_token=json.loads(r.text)["access"]
audio_paths=[]
url="http://127.0.0.1:8000/ratedaudios/"

for (root,dirs,files) in os.walk('data',topdown="true"):
    for f in files:
        audio_paths.append((os.path.join(root,f),f))

print(audio_paths)

headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': 'Bearer '+acess_token,
}

data={
  "rating_precision": 1,
  "lower_limit": 1,
  "upper_limit": 5,
  "label": "string",
  "avg_rating": 0,
  "status": 1,
  "rating_cnt": 0
}

i=0
n=len(audio_paths)
for (filepath,filename) in audio_paths:
  r = requests.post(url,data=json.dumps(data),headers=headers)
  response_json=json.loads(r.text)
  url2=url+str(response_json['id'])+"/audio/"
  data2 = MultipartEncoder(
      fields={
          "audio": (filename, open(filepath, 'rb')),
      }
  )
  headers2 = {
      "Accept-Encoding": "gzip, deflate",
      "Accept": "*/*",
      "Content-Type": data2.content_type,
      'Authorization': 'Bearer '+acess_token
  }
  r2 = requests.put(
      url2,
      data=data2,
      headers=headers2,
  )
  content = json.loads(r2.content.decode("utf-8"))
  print(content)
  i+=1
  print("Saved ",i, "files to database out of ",n)