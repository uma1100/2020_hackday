import requests

joycon_data = requests.get('https://script.google.com/macros/s/AKfycbzCa4Xp_WHXIziduPKaa8kOZ_ZR9qc-XxWHMY0bcuLGYDXArojT/exec')
joycon_data = joycon_data.json()
print(joycon_data[0][1])