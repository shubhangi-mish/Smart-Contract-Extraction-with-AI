import openai
import json
import requests
from openai import OpenAI

client = OpenAI(api_key='OPENAI_API_KEY') #removed while submission

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
    
'''
tools = [
    {
        "type": "function",
        "function": {
            "name": "send_contract_to_zenskar",
            "description": "Send the contract data to Zenskar for creation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contract_data": {
                        "type": "object",
                        "description": "The contract data to be sent to Zenskar.",
                    }
                },
                "required": ["contract_data"],
                "additionalProperties": False,
            },
        }
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Use the supplied tools to assist the user, including sending contract data to Zenskar."
    },
    {
        "role": "user",
        "content": "I need to create a contract for Acme Corp. The contract details are as follows..."
    }
]

response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=tools,
    tool_choice= "auto"
)

tool_call = response.choices[0].message.tool_calls
arguments = json.loads(tool_call['arguments'])

contract_data = arguments.get('contract_data')

contract_response = send_contract_to_zenskar(contract_data)

function_call_result_message = {
    "role": "tool",
    "content": json.dumps({
        "contract_id": contract_response.get("id"),
        "status": "Contract successfully created"
    }),
    "tool_call_id": tool_call['id']
}

completion_payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I need to create a contract for Acme Corp. The contract details are as follows..."},
        response['choices'][0]['message'],
        function_call_result_message
    ]
}

response = openai.ChatCompletion.create(
    model=completion_payload["model"],
    messages=completion_payload["messages"]
)

print(response)
'''