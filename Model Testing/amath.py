import requests

LAPTOP_IP = "10.18.98.0"
PORT = "8000"

def offload_to_laptop(lean_statement):
    url = "http://{LAPTOP_IP}:{PORT}/lean-response"
    response = requests.post(url, json={"lean" : lean_statement})
    return response.json()["message"]