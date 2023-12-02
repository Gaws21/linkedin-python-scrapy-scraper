import pdb
import sys
import requests

headers = {
    'authority': 'www.linkedin.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

params = {
    'keywords': 'Python',
    'location': 'Brasil',
    'locationId': '',
    'geoId': '106057199',
    'f_TPR': 'r86400',
    'f_WT': '2',
    'position': '1',
    'pageNum': '0',
    'start': '0',
}

#params["pageNum"] = sys.argv[1]
url = 'https://www.linkedin.com/jobs/search'
url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
for i in range(12,14):
    response = requests.get(url, params=params, headers=headers)
    url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search'
    params['start'] = str(i*25)
    headers['referer'] = response.url
    html = open(f"search_result_test_{i}.html", "wt")
    pdb.set_trace()

if __name__ == '__main__':
    requests.main(argv=[''], exit=False)