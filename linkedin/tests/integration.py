import pdb
import sys
import unittest
from scrapy.crawler import CrawlerProcess
from spiders import configs
from spiders import iofunctions
from spiders import job_description_spider
from scrapy.utils.project import get_project_settings


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.JOB_ID_LIST = iofunctions.read_file(configs.PATH_JOBS_ID_LIST)
        self.outputs = []
        self.process = CrawlerProcess(get_project_settings())

    def output_callback(self, output_spider):

        if isinstance(output_spider, str):
            self.outputs.append(dict(output_spider))
        else:
            return self.outputs.append(output_spider)
    
    #@unittest.skip("")
    def test_request_200_one_job(self):  
        job_id = self.JOB_ID_LIST[int(sys.argv[1])]
        self.process.crawl(job_description_spider.JobDescriptionSpider, job_id, output_callback=self.output_callback)
        self.process.start() 
        self.assertEqual(self.outputs[0].get("collectedStatus"), 200)
    
    @unittest.skip("")
    def test_request_200_many_jobs(self):    
        for job_id in self.JOB_ID_LIST[0]:
            process = CrawlerProcess(get_project_settings())
            process.crawl(job_description_spider.JobDescriptionSpider, job_id, output_callback=self.output_callback)
            process.start() 
            self.assertEqual(self.outputs[0].get("collectedStatus"), 200)
    
    @unittest.skip("")
    def test_request_fail(self):    
        self.process.crawl(job_description_spider.JobDescriptionSpider, '0', output_callback=self.output_callback)
        self.process.start() 
        self.assertRaises(TypeError, self.outputs[0])

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)