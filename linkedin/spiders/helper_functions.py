import json
from spiders import configs
from spiders.jobinfos import ParserJobs

parser_jobs = ParserJobs()
def read_file(path):
    job_id_list = None
    with open(path,"r") as job_ids:
        job_id_list = job_ids.readlines()
    return job_id_list

def read_json(path):
    json_expected_read = None
    with open(path, 'r') as json_expected:
        json_expected_read = json.load(json_expected)
    return json_expected_read

def save_html(response: bytes, job_id: str) -> None:
    with open(f"{configs.PATH_JOBS_HTML_COLLECT}/job-{job_id}.html",'w') as job_file:
       job_file.writelines(response.text)

def save_json(data: dict) -> None:
    with open(f"{configs.PATH_JOBS_JSON_COLLECT}/job-{data.get('id')}.json",'w') as job_infos:
       json.dump(data, job_infos, indent=4,  ensure_ascii=False)

def save_html_response(response: bytes) -> None:
    job_id = parser_jobs.get_job_id(response)
    save_html(response, job_id)