# Поиск вакансий
import requests
import pprint
import time
from pycbrf.toolbox import ExchangeRates

url = 'https://api.hh.ru/vacancies'


name = input("Задайте наименование вакансии: ")
region = input("В каком регионе ищем: ")
req_name = f'NAME: ({name}) AND {region}'
#print(req_name)
params = {
    'text': req_name
}

result = requests.get(url, params=params).json()

pages_num = result['pages']
vac_num = 0


items = result['items']
skills = []
skills = set()
sal = 0
rate = ExchangeRates() # загрузка текущих курсов валют

for page in range(pages_num):
    params = {
        'text': req_name,
        # теперь идем по страницам
        'page': page
    }
    result_p = requests.get(url, params=params).json()

    for item in result_p['items']:
        vac_num += 1
        if not item['salary'] is None:
            if item['salary']['currency'] is None or item['salary']['currency']=='None':
                code_cur = 'RUR'
            else:
                code_cur = item['salary']['currency']

            rate_cur = 1 if code_cur == 'RUR' else float(rate[code_cur].value)
            sal_from = 0 if (item['salary']['from'] == 0 or item['salary']['from'] is None or item['salary']['from'] == 'None') else item['salary']['from']
            sal_to = 0 if (item['salary']['to'] == 0 or item['salary']['to'] is None or item['salary']['to'] == 'None') else item['salary']['to']
            if sal_from == 0:
                sal += sal_to*rate_cur
            else:
                if sal_to:
                    sal += sal_from*rate_cur
                else:
                    sal += (sal_from + sal_to)*rate_cur/2
        res_key_skills = requests.get(item[url]).json()
        skills.add(res_key_skills['key_skills'])
        time.sleep(1)

print('По запросу ', name, ' в регионе ', region, ' нашли ', vac_num, ' вак.')
av_sal = sal/vac_num if vac_num != 0 else 0
#    print('Средняя зарплата', sal/vac_num, ' руб.')
to_print = {
        'keywords': name,
        'region': region,
        'count': vac_num,
        'ave_salary': round(av_sal),
        'skills': skills}
#with open('result.json', mode='w') as f:
#    jdump([to_print], f)
pprint.pprint(to_print)
#print(result['items'][0]['url'])
#print(result['items'][0]['alternate_url'])