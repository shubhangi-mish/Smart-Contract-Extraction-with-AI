import requests
import json


def send_contract_to_zenskar(contract_data):
    url = "https://api.zenskar.com/contract_v2"

    payload = {
        "name": contract_data.get("Contract ID", {}).get("extracted_value"),  
        "description": f"Contract for {contract_data.get('Customer Name', {}).get('extracted_value')}",  
        "tags": contract_data.get("tags", ["contract", "professional services"]), 
        "status": contract_data.get("status", "draft"), 
        "currency": contract_data.get("Currency", {}),
        "start_date": contract_data.get("Contract Start Date", {}).get("extracted_value"),
        "end_date": contract_data.get("Contract End Date", {}).get("extracted_value"),
        "customer_id": contract_data.get("Customer ID", {}).get("extracted_value"),  
        "anchor_date": contract_data.get("Contract Start Date", {}).get("extracted_value"),  
        "plan_id": contract_data.get("plan_id", "default_plan"), 
        "phases": contract_data.get("phases", [
            {
                "name": "Phase 1",
                "description": "Initial phase of the contract",
                "start_date": contract_data.get("Contract Start Date", {}).get("extracted_value"),
                "end_date": contract_data.get("Contract End Date", {}).get("extracted_value")
            }
        ]),
        "renewal_policy": contract_data.get("renewal_policy", ""),  # 3 options renew_with_default_contract, renew_with_existing, do_not_renew
        "contract_link": contract_data.get("contract_link", ""),  
    }
    
    print("Payload:", payload)

   
    API_TOKEN = "ZENSKAR_API_TOKEN"   # Not available
    ORGANISATION_ID = "YOUR_ORGANISATION_ID"  # Unable to create
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
    

