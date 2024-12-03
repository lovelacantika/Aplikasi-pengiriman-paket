import json

with open("harga.json", "r") as file:
 data = json.load(file)
    
print(data["distance_prices"][0].keys())