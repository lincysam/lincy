import requests
base_url='http://restcountries.eu/rest/v2/all'
resp=requests.get(base_url)
data=resp.json()
print(data)
