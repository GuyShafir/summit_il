import vertexai
import vertexai.preview.generative_models as generative_models
from google.cloud import logging
from vertexai.generative_models import GenerativeModel

generation_config = {"max_output_tokens": 8192, "temperature": 1, "top_p": 0.95, }

project = "summit-il"

log = "b\'{\"insertId\":\"ids5grs55s11jgg8\",\"labels\":{\"compute.googleapis.com/resource_name\":\"" \
      "gke-cluster-1-default-pool-fd520333-eypy\",\"k8s-pod/component\":\"gke-metrics-agent\",\"k8s-pod/controller-" \
      "revision-hash\":\"c5789fb5d\",\"k8s-pod/k8s-app\":\"gke-metrics-agent\",\"k8s-pod" \
      "/pod-template-generation\":\"2\"},\"logName\":\"projects/summit-il/logs/stderr\",\"receiveTimestamp\":\"2024-05-18T14:12:19.040719618" \
      "Z\",\"resource\":{\"labels\":{\"cluster_name\":\"cluster-1\",\"container_name\":\"gke-metrics-agent\",\"location\":\"us-central1-c\",\"namespace_name\":\"kube-system\",\"pod_name\":\"" \
      "gke-metrics-agent-7pz9g\",\"project_id\":\"summit-il\"},\"type\":\"k8s_container\"},\"severity\":\"ERROR\",\"textPayload\":\"2024-05-18T14:12:17.238Z\\\\terror\\\\tuasexporter" \
      "/exporter.go:190\\\\tError exporting metrics to UAS\\\\t{\\\\\"kind\\\\\": \\\\\"exporter\\\\\", \\\\\"name\\\\\": \\\\\"uas\\\\\", \\\\\"error\\\\\": \\\\\"reading from stream failed: " \
      "rpc error: code = Internal desc = stream terminated by RST_STREAM with error code: INTERNAL_ERROR\\\\\"}\",\"timestamp\":\"2024-05-18T14:12:17.239355567Z\"}\'"

text1 = """Based on the following log, generate a GCP log filter expression to provide more context to the log based on timeframe, resource, resource type, without being too specific: {}""".format(
    log)
text1_instructions = """You will respond only with the filter without json in one line"""

text2 = """what is the meaning of the following GCP log and how to solve it?: {}



context logs:
""".format(log)

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE, }


def fetch_logs(expression):
    # Define project ID and log filter

    # Create a Logging client
    client = logging.Client(project=project)

    # Get logs from the specified filter
    logs = client.list_entries(filter_=expression, page_size=30)

    # Process each log entry (access log data, timestamp, etc.)
    response = ''
    for entry in logs:
        # print(f"Timestamp: {entry.timestamp}, Log: {entry.payload}")
        response += f"Timestamp: {entry.timestamp}, Log: {entry.payload}\n"

    return response


def generate(prompt, instructions):
    vertexai.init(project="summit-il", location="us-east1")
    model = GenerativeModel("gemini-1.5-pro-preview-0514",
                            system_instruction=[instructions])
    responses = model.generate_content([prompt], generation_config=generation_config, safety_settings=safety_settings,
                                       stream=False, )

    return responses.candidates[0].text


filter_ex = generate(text1, text1_instructions)

filter_ex = filter_ex.replace("`", "").replace("'", "").replace("json", "")

context_logs = fetch_logs(filter_ex)

print(generate(text2 + context_logs, ''))
