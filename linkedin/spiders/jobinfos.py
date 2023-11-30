import pdb
import re
from bs4 import BeautifulSoup
from spiders import configs
import logging

class ParserJobs(BeautifulSoup):
    def __init__(self, name):
        name = "job_description_spider"
        logging.basicConfig(
            filename=f'{name}.log',
            filemode='w',
            level=logging.DEBUG,
            format=configs.LOG_FORMAT
        )

        self.logger = logging.getLogger(f'{name}')
    def create_soup(self, response):
        soup_response = BeautifulSoup(response.text, 'html.parser')
        self.logger.info("Created Soup")
        if soup_response is None:
            
            return None
        return soup_response 
        
    def find_class(self, soup_response, re_class_name):
        tag_find = soup_response.find(class_=re.compile(re_class_name))
        return tag_find

    def remove_tags(self, div_tag):
        tag_to_remove = ["p","span","u", "em", "strong", "ul", "li", "br"]
        for tag_remove in tag_to_remove:
            for tag in div_tag.find_all(tag_remove):
                tag.unwrap()
        
    def get_job_id(self, response):
        if response.text is None:
            return ValueError(f"Error to get text from response. Expected string, atual: {response.text}")
        
        job_url_splited = response.text.split(configs.JOB_URL_PREFIX)
        if len(job_url_splited) < 2:
            return IndexError(f"Error get index 1. Expected list, atual: {job_url_splited}")
        job_id = job_url_splited[1][0:10]

        if len(job_id) < 10:
            return ValueError(f"Error to verify job_id. Expected len equal 10, atual: {response.text}")
        return job_id

    def get_job_title(self, soup_response):
        class_find = "top-card-layout__title"
        tag_class_find = self.find_class(soup_response, class_find)

        if tag_class_find is None:
            return TypeError(f"Error to get corret class tag. Expected {class_find} atual {tag_class_find}")
        
        job_title_text = tag_class_find.text
        if job_title_text is None:
            return ValueError(f"Error to get text from tag. Expected tag, atual: {tag_class_find}")
        
        return job_title_text.strip()

    def get_job_company(self, soup_response):
        re_class_find = "topcard__org-name-link"
        tag_class_find = self.find_class(soup_response, re_class_find)

        if tag_class_find is None:
            return TypeError(f"Error to get corret class tag. Expected {re_class_find} atual {tag_class_find}")
        
        job_company = tag_class_find.text
        if job_company is None:
            return ValueError(f"Error to get text from tag. Expected tag, atual: {tag_class_find}")
        
        return job_company.strip()

    def get_job_locale(self, soup_response):
        re_class_find = "topcard__flavor topcard__flavor--bullet"
        tag_class_find = self.find_class(soup_response, re_class_find)
        if tag_class_find is None:
            return TypeError(f"Error to get corret class tag. Expected {re_class_find} atual {tag_class_find}")
        
        job_locale = tag_class_find.text
        if job_locale is None:
            return ValueError(f"Error to get text from tag. Expected tag, atual: {tag_class_find}")
        return job_locale.strip()

    def get_text_job_description(self, soup_response):
        full_text = ''
        re_class_find = "show-more-less-html"
        tag_class_find = self.find_class(soup_response, configs.RE_CLASS_NAME)
        if tag_class_find is None:
            return TypeError(f"Error to get corret class tag. Expected {re_class_find} atual {tag_class_find}")
        
        div_tag = tag_class_find.find('div')
            
        if div_tag is None or len(div_tag) < 2:
            return TypeError(f"Error to get corret div tag. Expected div, atual {div_tag}")
        
        self.remove_tags(div_tag)
        for text in div_tag:
            #pdb.set_trace()
            if text[0].isupper():
                full_text = f"{full_text}\n{text.strip()}"
            else:
                full_text = f"{full_text} {text.strip()}"
        return full_text

    def get_job_criteria_infos(self, soup_response):
        re_class_find = "description__job-criteria-list"
        tag_class_find = self.find_class(soup_response, re_class_find)

        if tag_class_find is None:
            return TypeError(f"Error to get corret class tag. Expected {re_class_find} atual {tag_class_find}")
        
        tag_span_list = tag_class_find.find_all("span")

        if tag_span_list is None or len(tag_span_list) < 4:
            return TypeError(f"Error to get corret span list. Expected list, atual {tag_span_list}")
        
        criteria_list = {
            "seniority_level":"",
            "employment_type":"",
            "job_function":"",
            "industries":"",
        }
        criteria_index = {
            0:"seniority_level",
            1:"employment_type",
            2:"job_function",
            3:"industries"
        }
        for index, tag_class_find in enumerate(tag_span_list):
            criteria_list[criteria_index.get(index)] = tag_class_find.text.strip()
        
        return criteria_list

    def get_all_infos(self, response, id):
        soup_response = self.create_soup(response)

        if isinstance(soup_response, TypeError):
            return soup_response
        
        _id = id.strip()

        if len(_id) < 10:
            return ValueError(f"Error to get value job_id. Expected len 10, atual: {_id}")
        
        job_infos = {
            "id":_id,
            "title": self.get_job_title(soup_response),
            "company": self.get_job_company(soup_response),
            "locale": self.get_job_locale(soup_response),
            "description": self.get_text_job_description(soup_response),
            "criteria": self.get_job_criteria_infos(soup_response),
        }

        return job_infos


