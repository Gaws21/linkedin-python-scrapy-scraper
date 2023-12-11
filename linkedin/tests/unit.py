import os 
import pdb
import re
import sys
import unittest
from spiders import configs
from spiders.jobinfos import ParserJobs
from spiders import helper_functions
from scrapy.http import HtmlResponse
from database import Storage
import psycopg2
class TestUnit(unittest.TestCase):

    try:
        best_jobs = open('/home/linkedin-python-scrapy-scraper/best_jobs_10.txt', 'wt')
        secundary_jobs = open('/home/linkedin-python-scrapy-scraper/secundary_jobs_10.txt', 'wt')
    except:
        best_jobs.close()
        secundary_jobs.close()
        
    ParserJobs = ParserJobs()
    #adicionar no helper_functions
    def read_file(self, file_path):
        response = None
        with open(file_path,'r') as html_response:
            _body = html_response.read()
            response = HtmlResponse(url=file_path,body=_body, encoding='utf-8')
        return response
    
    #adicioar no helper_functions
    def get_job_files(self, path=configs.PATH_JOBS_HTML_COLLECT):
        job_files = os.listdir(path)
        full_job_files = [f"{path}/{job}" for job in job_files]
        return full_job_files
    
    #melhorar essa logica
    def get_html_files_test(self, path=configs.PATH_JOBS_HTML_COLLECT, index_initial=0, index_final=1):
        files = self.get_job_files(path)
        for file in files[index_initial:index_final]:
            response = self.read_file(file)
        return response
    
    def get_all_html_files_test(self, path=configs.PATH_JOBS_HTML_COLLECT):
        files = self.get_job_files(path)
        response_list = []
        for file in files:
            response = self.read_file(file)
            response_list.append(response)
        return response_list
    
    def get_html_files_by_id_test(self, id):
        files = self.get_job_files()
        for file in files:
            if id in file:
                response = self.read_file(file)
                return response
    
    #adicionar esses caminhos de forma curta no arquivo de configs
    @unittest.skip('')
    def test_parser_description(self):
        text_job_description_file = helper_functions.read_file('/home/linkedin-python-scrapy-scraper/linkedin/tests/expect_files/parser_description_expected.txt')
        text_job_description_expected = ''.join(text_job_description_file)

        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
        soup_response = self.ParserJobs.create_soup(response)
        text_job_description_result =  self.ParserJobs.get_text_job_description(soup_response)

        self.assertEqual(text_job_description_result, text_job_description_expected)
    @unittest.skip('')
    def test_get_job_criteria_infos(self):
        #a logica dessa funcao get_html_files_test pode ir para o setup do teste
        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
         #a logica dessa funcao create_soup pode ir para o setup do teste
        soup_response =  self.ParserJobs.create_soup(response)
        job_criteria_infos_result =  self.ParserJobs.get_job_criteria_infos(soup_response)
        job_criteria_infos_expected = {
            'seniority_level': 'Entry level', 
            'employment_type': 'Full-time', 
            'job_function': 'Information Technology', 
            'industries': 'Financial Services'
        }
        self.assertEqual(job_criteria_infos_result, job_criteria_infos_expected)
    @unittest.skip('')
    def test_job_title(self):
        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
        soup_response =  self.ParserJobs.create_soup(response)
        job_title_result =  self.ParserJobs.get_job_title(soup_response)
        job_title_expected = 'Engenheiro de Dados'
        self.assertEqual(job_title_result, job_title_expected)
    @unittest.skip('')
    def test_get_job_company(self):
        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
        soup_response =  self.ParserJobs.create_soup(response)
        job_company_result =  self.ParserJobs.get_job_company(soup_response)
        job_company_expected = 'Cielo'
        self.assertEqual(job_company_result, job_company_expected)
    @unittest.skip('')
    def test_get_job_locale(self):
        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
        soup_response =  self.ParserJobs.create_soup(response)
        job_locale_atual =  self.ParserJobs.get_job_locale(soup_response)
        job_locale_expected = 'Barueri, São Paulo, Brazil'
        self.assertEqual(job_locale_atual, job_locale_expected)
    @unittest.skip('')
    def test_get_all_infos(self):
        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
        #esse id pode ser setado no setup
        job_all_infos_atual =  self.ParserJobs.get_all_infos(response,'3761065603')
        json_expected_expected = helper_functions.read_json('/home/linkedin-python-scrapy-scraper/linkedin/tests/expect_files/all_infos_expected.json')
        self.assertEqual(job_all_infos_atual, json_expected_expected)
    @unittest.skip('')
    def test_job_id(self):
        response = self.get_html_files_test()
        #response = self.get_html_files_by_id_test("3766808423")
        job_id_atual =  self.ParserJobs.get_job_id(response)
        job_id_expected = "3755870000"
        self.assertEqual(job_id_atual, job_id_expected)
    
    @unittest.skip('')
    def test_get_searched_jobs(self):

        def clear_text(tag):
            text = tag.text.strip()
            return text
        
        def find_title_job(div_tag_root):
            tag_find = 'div'
            class_find = 'base-search-card__info'
            #pdb.set_trace()
            titulo = div_tag_root.a
            clear_title = clear_text(titulo)
            return clear_title
        
        def find_job_id(div_tag_root):
            tag_find = 'div'
            first_div_tag = div_tag_root.find('div',{'data-view-name':'job-card'})
            atribute_tag = first_div_tag.get('data-job-id')
            
            ##pdb.set_trace()
            job_id = atribute_tag.split(':')[-1]
            return job_id
        
        def find_job_company(div_tag_root):
            tag_find = 'span'
            class_find = 'job-card-container__primary-description'

            ##pdb.set_trace()
            job_company = div_tag_root.find(tag_find, {'class':class_find})
            clear_title = clear_text(job_company)
            return clear_title
        
        def find_location_job(div_tag_root):
            tag_find = 'li'
            class_find = 'job-card-container__metadata-item'
            location = div_tag_root.find(tag_find, {'class':class_find})

            if not location:
                return None
            #pdb.set_trace()
            location_clear = clear_text(location)
            return location_clear
        
        def find_publish_time(div_tag_root):
            tag_find = 'time'
            publish_time = div_tag_root.find(tag_find)
            
            if not publish_time:
                return None
            if publish_time.span:
                publish_time.span.decompose()
            
            publish_time_clear = clear_text(publish_time)
            return publish_time_clear
        
        def find_result_new_jobs(soup):
            tag_class_root = self.ParserJobs.find_class(soup,'results-context-header')
            tag_span_text = tag_class_root.find('span', {'class':'results-context-header__new-jobs'})
            result_new_jobs_clear = clear_text(tag_span_text)
            result_new_jobs_only_number = re.sub(r'\D','',result_new_jobs_clear)
            return result_new_jobs_only_number
        
        def check_title(job):
            title = job['title']
            string_list = ['engenheir.*dados','python','data engineer','analista.*dados']
            
            contains_word = lambda title_string, string_list: map(lambda regex: re.search(regex, title_string), string_list)
            constains_word_result = contains_word(title.lower(), string_list)

            if not any(constains_word_result):
                return False
            return True
        
        def group_jobs(jobs_search_list):
            for job in jobs_search_list:
                if check_title(job) and job.get('company') not in ['Netvagas','GeekHunter']:
                    self.best_jobs.write(f'{str(job)}\n')
                else:
                    self.secundary_jobs.write(f'{str(job)}\n')
            #pdb.set_trace()

        
        #response = self.read_file(f'/home/linkedin-python-scrapy-scraper/search_result_test_{sys.argv[1]}.html')
        
        
        def get_all_infos_search_jobs_result(response):
            soup = self.ParserJobs.create_soup(response)
            class_find = self.ParserJobs.find_class(soup,'scaffold-layout__list-container')

            #pdb.set_trace()
            tag_ul_root = class_find.find_all('li', recursive=False)
            
            if not tag_ul_root:
                raise ValueError
            
            jobs_searched_list = []
            #result_new_jobs = find_result_new_jobs(soup)
            ##pdb.set_trace()
            for index, tag_li in enumerate(tag_ul_root):
                title = find_title_job(tag_li)
                job_id = find_job_id(tag_li)
                company = find_job_company(tag_li)
                location = find_location_job(tag_li)
                
                publish_time = find_publish_time(tag_li)
                

                jobs_searched = {
                    "index":index,
                    "job_id":job_id,
                    "title":title,
                    "company":company,
                    "location":location,
                    "publish_time":publish_time,
                }

                jobs_searched_list.append(jobs_searched)
            
            return jobs_searched_list
        
        html_files = self.get_all_html_files_test(f'/home/vagas-10')
        for index, file in enumerate(html_files):
            #pdb.set_trace()
            #response = self.read_file(file)
            jobs_searched_list = get_all_infos_search_jobs_result(file)
            group_jobs(jobs_searched_list)

    @unittest.skip("")
    def test_strip(self):
        result = re.sub(r'\D','','(290 novas)')
        qtd_paginations = int(result)//25 + 1
    
    def test_database(self):
        #conn = psycopg2.connect("dbname='myjobs' user='username' host='localhost' password='password'") 
        storage = Storage() 
        query_1 = """
            DROP TABLE IF EXISTS LinkedinJobs;
            CREATE TABLE LinkedinJobs(
                job_id VARCHAR,
                title VARCHAR,
                company VARCHAR,
                location VARCHAR, 
                publish_time VARCHAR);
        """

        query_2 = "INSERT INTO LinkedinJobs VALUES ('123','', '','','');"

        query_3 = 'SELECT * FROM LinkedinJobs;'
        resturn_query = storage.execute_query(query_3)
        storage.close()
        print(resturn_query)
        
        #print(storage.execute_query("insert into jobs(job_id) values ('alguma_coisa_2');"))
        #pdb.set_trace()
        
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)