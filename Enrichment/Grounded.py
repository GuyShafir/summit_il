from pprint import pprint

import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel, Tool


def generate():
    vertexai.init(project="summit-il", location="us-central1")
    tools = [
        Tool.from_retrieval(
            retrieval=generative_models.grounding.Retrieval(
                source=generative_models.grounding.VertexAISearch(
                    datastore="projects/summit-il/locations/global/collections/default_collection/dataStores/tf-state-unchunked_1716048324148"),
                disable_attribution=False,
            )
        ),
    ]
    model = GenerativeModel(
        "gemini-1.5-pro-preview-0514",
        tools=tools,
        system_instruction=["""You will respond in json format only with the following stracture:

{
\"result\": <result>
}"""]
    )
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    pprint(responses.candidates[0].text)


text1 = """Based on the following error log, explain what happened, use terraform for additional information

b\\\'{\\\"insertId\\\":\\\"ids5grs55s11jgg8\\\",\\\"labels\\\":{\\\"compute.googleapis.com/resource_name\\\":\\\"gke-cluster-1-default-pool-fd520333-eypy\\\",\\\"k8s-pod/component\\\":\\\"gke-metrics-agent\\\",\\\"k8s-pod/controller-revision-hash\\\":\\\"c5789fb5d\\\",\\\"k8s-pod/k8s-app\\\":\\\"gke-metrics-agent\\\",\\\"k8s-pod/pod-template-generation\\\":\\\"2\\\"},\\\"logName\\\":\\\"projects/summit-il/logs/stderr\\\",\\\"receiveTimestamp\\\":\\\"2024-05-18T14:12:19.040719618Z\\\",\\\"resource\\\":{\\\"labels\\\":{\\\"cluster_name\\\":\\\"cluster-1\\\",\\\"container_name\\\":\\\"gke-metrics-agent\\\",\\\"location\\\":\\\"us-central1-c\\\",\\\"namespace_name\\\":\\\"kube-system\\\",\\\"pod_name\\\":\\\"gke-metrics-agent-7pz9g\\\",\\\"project_id\\\":\\\"summit-il\\\"},\\\"type\\\":\\\"k8s_container\\\"},\\\"severity\\\":\\\"ERROR\\\",\\\"textPayload\\\":\\\"2024-05-18T14:12:17.238Z\\\\\\\\terror\\\\\\\\tuasexporter/exporter.go:190\\\\\\\\tError exporting metrics to UAS\\\\\\\\t{\\\\\\\\\\\"kind\\\\\\\\\\\": \\\\\\\\\\\"exporter\\\\\\\\\\\", \\\\\\\\\\\"name\\\\\\\\\\\": \\\\\\\\\\\"uas\\\\\\\\\\\", \\\\\\\\\\\"error\\\\\\\\\\\": \\\\\\\\\\\"reading from stream failed: rpc error: code = Internal desc = stream terminated by RST_STREAM with error code: INTERNAL_ERROR\\\\\\\\\\\"}\\\",\\\"timestamp\\\":\\\"2024-05-18T14:12:17.239355567Z\\\"}\\ 

These are additional logs:
Timestamp: 2024-05-18 14:10:10.283520+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:10:20.902917+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:10:30.773210+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:10:41.577125+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:10:51.209463+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:11:02.274505+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:11:12.048297+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:11:23.362260+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:11:33.525324+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:11:44.150335+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:11:44.757651+00:00, Log: {\'took\': \'2.943296ms\', \'component\': \'gcm_exporter\', \'seriesPurged\': 0.0, \'level\': \'info\', \'ts\': \'2024-05-18T14:11:44.734Z\', \'msg\': \'garbage collection completed\', \'caller\': \'series_cache.go:221\'}
Timestamp: 2024-05-18 14:11:54.208059+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:12:02.347091+00:00, Log: 2024-05-18T14:12:02.335Z	error	uasexporter/exporter.go:226	failed to get response from UAS	{\"kind\": \"exporter\", \"name\": \"uas\", \"error\": \"rpc error: code = Internal desc = stream terminated by RST_STREAM with error code: INTERNAL_ERROR\"}
Timestamp: 2024-05-18 14:12:04.517957+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:12:15.005910+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:12:17.239355+00:00, Log: 2024-05-18T14:12:17.238Z	error	uasexporter/exporter.go:190	Error exporting metrics to UAS	{\"kind\": \"exporter\", \"name\": \"uas\", \"error\": \"reading from stream failed: rpc error: code = Internal desc = stream terminated by RST_STREAM with error code: INTERNAL_ERROR\"}
Timestamp: 2024-05-18 14:12:17.248373+00:00, Log: 2024-05-18T14:12:17.248Z	error	uasexporter/exporter.go:212	failed to send metrics data to UAS	{\"kind\": \"exporter\", \"name\": \"uas\", \"error\": \"EOF\"}
Timestamp: 2024-05-18 14:12:20.729955+00:00, Log: {\'seriesPurged\': 0.0, \'level\': \'info\', \'ts\': \'2024-05-18T14:12:20.716983399Z\', \'msg\': \'garbage collection completed\', \'caller\': \'series_cache.go:221\', \'took\': \'3.394822ms\'}
Timestamp: 2024-05-18 14:12:25.021535+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:12:35.568603+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:12:47.354880+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:12:56.355819+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:13:05.972265+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:13:20.207773+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:13:26.521925+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:13:36.896999+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:13:50.311180+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:13:59.323723+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:14:08.155977+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:14:21.478704+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:14:29.694917+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:14:38.346941+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:14:53.883683+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:15:02.344443+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:15:10.604115+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:15:26.119132+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:15:34.181729+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:15:41.178288+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:15:58.657342+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:16:06.042461+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:16:12.832144+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:16:31.522880+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:16:37.642002+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:16:44.805182+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:17:04.069773+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:17:07.760230+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:17:15.564579+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:17:28.362131+00:00, Log: {\'took\': \'8.328µs\', \'component\': \'gcm_exporter\', \'seriesPurged\': 0.0, \'level\': \'info\', \'ts\': \'2024-05-18T14:17:28.361Z\', \'msg\': \'garbage collection completed\', \'caller\': \'series_cache.go:221\'}
Timestamp: 2024-05-18 14:17:34.617737+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:17:39.525977+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:17:46.676070+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:18:06.021376+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:18:10.674520+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:18:18.018356+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:18:37.812827+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:18:43.745667+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:18:49.861764+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:19:09.162937+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:19:13.811997+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:19:21.803436+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:19:40.947787+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}
Timestamp: 2024-05-18 14:19:44.272015+00:00, Log: {\'pid\': \'1\', \'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\'}
Timestamp: 2024-05-18 14:19:53.515090+00:00, Log: {\'message\': \'\"Connect to server\" serverID=\"115a245f-2401-40f3-9b40-b8aa18a81fd1\"\', \'pid\': \'1\'}"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

generate()
