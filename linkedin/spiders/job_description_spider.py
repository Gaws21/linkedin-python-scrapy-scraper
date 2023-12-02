import logging
import scrapy
from spiders import configs
from spiders import helper_functions
from spiders.jobinfos import ParserJobs

class JobDescriptionSpider(scrapy.Spider):
    name = "job_description_spider"
    logging.basicConfig(
        filename=f'{name}.log',
        filemode='w',
        level=logging.DEBUG,
        format=configs.LOG_FORMAT
    )

    logger = logging.getLogger(f'{name}')
    def __init__(self, job_id=None, output=None, **kwargs):
        super().__init__(**kwargs)
        self.job_id = job_id
        self.output = output
        self.parser_jobs = ParserJobs(self.name)
    def start_requests(self):
        self.logger.info("Start Requests.")

        if len(self.job_id) < 10:
            raise self.output_callback(TypeError("TypeError for job_id. Input len is wrong"))
        
        yield scrapy.Request(url=f"{configs.JOB_URL_PREFIX}{self.job_id}/", headers=configs.HEADERS.copy(), callback=self.save_html_response)

    #adicionar logica de tratamento de erros 
    def save_html_response(self, response):
        self.logger.info("Saving Response as HTML.")

        if response is None:
            raise self.output_callback(TypeError("TypeError for response. The response is None"))
        helper_functions.save_html_response(response)
        return self.extract_job_infos(response)

    def extract_job_infos(self, reponse: bytes):
        self.logger.info("Extracting the Job infos.")
        job_infos = self.parser_jobs.get_all_infos(reponse, self.job_id)
        helper_functions.save_json(job_infos)
        job_infos["collectedStatus"] = 200
        yield self.output_callback(job_infos)
    
    


    







        

    

