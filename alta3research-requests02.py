import requests
import random

url= "http://127.0.0.1:2224/json"

data= requests.get(url).json()

quote= random.choice(data)

print(f'\"{quote["quote"]}\"')
print("   -", quote["speaker"])
