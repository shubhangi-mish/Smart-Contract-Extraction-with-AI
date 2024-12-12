from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import json

client = OpenAI(api_key='OPENAI_API_KEY') #removed while submission

assistant = client.beta.assistants.create(
    name="Contract Analyzer Assistant",
    instructions=(
        "Do not provide any sentences or explanations. Only return the relevant values for each field in the specified format. Give the output in JSON format strictly"
        "Contract ID: Provide the contract ID and only the ID. "
        "Customer Name: Provide the customer's name. "
        "Contract Start Date: Provide the start date in yyyy-mm-dd format. "
        "Contract End Date: Provide the end date in yyyy-mm-dd format. "
        "Payment Terms: Provide the payment terms (e.g., 'Net 30'). "
        "Contract Amount: Provide the contract amount with currency. "
        "Billing Frequency: Provide the billing frequency. "
        "Contract Type: Provide the contract type."
    ),
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
)

vector_store = client.beta.vector_stores.create(name="Contracts")

file_path = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\Contracts\zenskar_SM.pdf"
file_stream = open(file_path, "rb")

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=[file_stream]
)

assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)

message_file = client.files.create(
    file=open(file_path, "rb"), purpose="assistants"
)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Extract the following fields from the attached contract: Contract ID, Customer Name, Contract Start Date, Contract End Date, Payment Terms, Contract Amount, and Metadata fields such as billing frequency and contract type.",
            "attachments": [
                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ],
        }
    ]
)

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > {text}", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

        with open("contract_extracted_details.json", "w") as json_file:
            json.dump(message_content.value, json_file, indent=4)

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()

run_details = client.beta.threads.retrieve(
    thread_id=thread.id, 
    include=["step_details.tool_calls[*].file_search.results[*].content"]
)

print(run_details)

with open("pdf_to_llm.json", "w") as output_file:
    json.dump(run_details, output_file, indent=4)
