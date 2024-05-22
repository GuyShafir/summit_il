import base64
import json

import functions_framework
import requests
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, }

generation_config = {"max_output_tokens": 8192, "temperature": 1, "top_p": 0.95, }

#Replace with own functions

manifast_dict = {
    1: 'https://us-central1.cloudfunctions.net/sizer',
    2: 'https://us-central1.cloudfunctions.net/disk_size',
    3: 'https://us-central1.cloudfunctions.net/loc_change'
}

manifast_txt = """
1: Changes the size of the vm and increases memory
2: Changes disk space
3: Changes the location of the vm
"""


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print(base64.b64decode(cloud_event.data["message"]["data"]))

    msg = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    main(msg)


def generate(prompt, instructions):
    print('Gemini Called')
    vertexai.init(project="summit-il", location="us-east1")
    model = GenerativeModel("gemini-1.5-pro-preview-0514",
                            system_instruction=[instructions])
    responses = model.generate_content([prompt], generation_config=generation_config, safety_settings=safety_settings,
                                       stream=False, )

    return responses.candidates[0].text


def main(msg):
    prompt = "Based on error {} chose from manifast the approprate action: {}".format(
        msg, manifast_txt
    )

    instructions = """You will respond in json format only with the following stracture:
    {"action_number": <action_number>,
    "vm_name": <vm_name>,
    "zone": <zone>,
    "project": <project>}"""

    result = generate(prompt, instructions)
    result = result.replace("```json", "").replace("```", "")
    result = json.loads(result)

    action_number = result["action_number"]
    vm_name = result["vm_name"]
    zone = result["zone"]
    project = result["project"]

    request_data = {"project": project, "zone": zone, "vm": vm_name}
    url = manifast_dict[int(action_number)]

    print(request_data)

    print('invoking', url)
    response = requests.post(url, json=request_data)

    print(response.text)
