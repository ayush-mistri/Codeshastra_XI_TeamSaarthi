import requests

url = 'http://127.0.0.1:5000/upload'
files = {'file': open("../Hackathon_Dataset.csv", 'rb')} #change by yourself
schema = open("../Schema.json").read() # change by yourself

data = {'schema': schema}
response = requests.post(url, files=files, data=data)
print(response.json())
