import requests
import json

def send_contract_to_zenskar(contract_data):
   
    url = "https://api.zenskar.com/contract_v2"

    
    payload = {
        "name": contract_data.get("Contract ID"),  
        "description": f"Contract for {contract_data.get('Customer Name')}",  
        "tags": ["contract", "professional services"], 
        "status": "draft", 
        "currency": "USD",  
        "start_date": contract_data.get("Contract Start Date"),
        "end_date": contract_data.get("Contract End Date"),
        "customer_id": contract_data.get("Customer Name"),  
        "anchor_date": contract_data.get("Contract Start Date"),  
        "plan_id": "default_plan",  
        "phases": [
            {
                "name": "Phase 1",
                "description": "Initial phase of the contract",
                "start_date": contract_data.get("Contract Start Date"),
                "end_date": contract_data.get("Contract End Date")
            }
        ], 
    }


    API_TOKEN = "ZENSKAR_API_TOKEN"   #which I cannot make because i am not an org
    ORGANISATION_ID = "YOUR_ORGANISATION_ID"  

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {API_TOKEN}",
        "organisation": ORGANISATION_ID
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Contract successfully created in Zenskar!")
        print("Response:", response.json())
    else:
        print("Failed to create contract. Status code:", response.status_code)
        print("Error:", response.text)

    return response
