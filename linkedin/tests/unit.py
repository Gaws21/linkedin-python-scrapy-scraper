import os 
import pdb
import unittest
from spiders import configs
from spiders.jobinfos import ParserJobs
from spiders import iofunctions
from scrapy.http import HtmlResponse

class TestUnit(unittest.TestCase):

    ParserJobs = ParserJobs("unittes")
    #adicionar no iofunctions
    def read_file(self, file_path):
        response = None
        with open(file_path,'r') as html_response:
            _body = html_response.read()
            response = HtmlResponse(url=file_path,body=_body, encoding='utf-8')
        return response
    
    #adicioar no iofunctions
    def get_job_files(self):
        job_files = os.listdir(configs.PATH_JOBS_HTML_COLLECT)
        full_job_files = [f"{configs.PATH_JOBS_HTML_COLLECT}/{job}" for job in job_files]
        return full_job_files
    
    #melhorar essa logica
    def get_html_files_test(self, index_initial=0, index_final=1):
        files = self.get_job_files()
        for file in files[index_initial:index_final]:
            response = self.read_file(file)
        return response
    
    def get_html_files_by_id_test(self, id):
        files = self.get_job_files()
        for file in files:
            if id in file:
                response = self.read_file(file)
                return response
    
    #adicionar esses caminhos de forma curta no arquivo de configs
    def test_parser_description(self):
        text_job_description_file = iofunctions.read_file('/home/linkedin-python-scrapy-scraper/linkedin/tests/expect_files/parser_description_expected.txt')
        text_job_description_expected = ''.join(text_job_description_file)

        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
        soup_response = self.ParserJobs.create_soup(response)
        text_job_description_result =  self.ParserJobs.get_text_job_description(soup_response)

        self.assertEqual(text_job_description_result, text_job_description_expected)
    
    def test_get_job_criteria_infos(self):
        #a logica dessa funcao get_html_files_test pode ir para o setup do teste
        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
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
    
    def test_job_title(self):
        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
        soup_response =  self.ParserJobs.create_soup(response)
        job_title_result =  self.ParserJobs.get_job_title(soup_response)
        job_title_expected = 'Engenheiro de Dados'
        self.assertEqual(job_title_result, job_title_expected)
    
    def test_get_job_company(self):
        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
        soup_response =  self.ParserJobs.create_soup(response)
        job_company_result =  self.ParserJobs.get_job_company(soup_response)
        job_company_expected = 'Cielo'
        self.assertEqual(job_company_result, job_company_expected)
    
    def test_get_job_locale(self):
        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
        soup_response =  self.ParserJobs.create_soup(response)
        job_locale_atual =  self.ParserJobs.get_job_locale(soup_response)
        job_locale_expected = 'Barueri, São Paulo, Brazil'
        self.assertEqual(job_locale_atual, job_locale_expected)
    
    def test_get_all_infos(self):
        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
        #esse id pode ser setado no setup
        job_all_infos_atual =  self.ParserJobs.get_all_infos(response,'3761065603')
        json_expected_expected = iofunctions.read_json('/home/linkedin-python-scrapy-scraper/linkedin/tests/expect_files/all_infos_expected.json')
        self.assertEqual(job_all_infos_atual, json_expected_expected)
    
    def test_job_id(self):
        response = self.get_html_files_test()
        response = self.get_html_files_by_id_test("3766808423")
        job_id_atual =  self.ParserJobs.get_job_id(response)
        job_id_expected = "3755870000"
        self.assertEqual(job_id_atual, job_id_expected)

        
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)