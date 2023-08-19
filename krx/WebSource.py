# web_source.py
import time
import pandas as pd
from IO import BytesIO

class WebSource:
    def __init__(self):
        self.request_frequency = 1  # 기본적인 요청 간격을 1초로 설정합니다.

    def set_request_frequency(self, seconds):
        """요청 간격을 설정하는 메서드입니다."""
        self.request_frequency = seconds

    def krx_b(self,index_name,tdate):
        #STK = 코스피
        #KSQ = 코스닥
        gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
        query_str_parms = {
            'mktId': index_name,
            'trdDd': str(tdate),
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
            'name': 'fileDown',
            'url': 'dbms/MDC/STAT/standard/MDCSTAT01501'
        }
        headers = {
            'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203' #generate.cmd에서 찾아서 입력하세요
        }
        r = requests.get(gen_req_url, query_str_parms, headers=headers)
        gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
        form_data = {
            'code': r.content
        }
        r = requests.post(gen_req_url, form_data, headers=headers)
        df = pd.read_excel(BytesIO(r.content))
        df['일자'] = tdate
        df['시장구분']=index_name
        df=df['종목명']
        file_name = 'basic_'+ str(tdate) + '.xlsx'
        df.to_excel(path+file_name, index=False, index_label=None)
        print('KRX crawling completed :', tdate)
        return

    def get_historical_data_b(self,index_name,start, end):
        year_start = start//10000
        year_end = end//10000
        month_start = (start-year_start * 10000)//100
        month_end = (end - year_end * 10000)//100+1
        for year in range(year_start, year_end+1):
            for month in range(month_start, month_end):
                for day in range(1, 32):
                    tdate = year * 10000 + month * 100 + day * 1
                    if start <= tdate <=end:
                        krx_basic(index_name,tdate)

    def krx_c(self,stock_code,start,end):
        gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
        query_str_parms = {
            'locale': 'ko_KR',
            'tboxisuCd_finder_stkisu0_0': str(stock_code), #+'/'+'삼성전자',
            'isuCd': 'KR7'+str(stock_code)+'003',
            'isuCd2': 'KR7'+str(stock_code)+'003',
            #'codeNmisuCd_finder_stkisu0_0': '삼성전자',
            'param1isuCd_finder_stkisu0_0': 'ALL',
            'strtDd': str(start),
            'endDd': str(end),
            'adjStkPrc_check': 'Y',
            'adjStkPrc': '2',
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
            'name': 'fileDown',
            'url': 'dbms/MDC/STAT/standard/MDCSTAT01701'
        }
        headers = {
            'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203' #generate.cmd에서 찾아서 입력하세요
        }
        r = requests.get(gen_req_url, query_str_parms, headers=headers)
        gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
        form_data = {
            'code': r.content
        }
        r = requests.post(gen_req_url, form_data, headers=headers)
        df = pd.read_excel(BytesIO(r.content))
        file_name = 'basic_'+ str(start) + '.xlsx'
        df.to_excel(path+file_name, index=False, index_label=None)
        print('KRX crawling completed :', start)
        return

    def krx_d(self,index_name,tdate):
        gen_req_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
        query_str_parms = {
            'mktId': index_name,
            'trdDd': str(tdate),
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
            'name': 'fileDown',
            'url': 'dbms/MDC/STAT/standard/MDCSTAT01501'
        }
        headers = {
            'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203' #generate.cmd에서 찾아서 입력하세요
        }
        r = requests.get(gen_req_url, query_str_parms, headers=headers)
        gen_req_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
        form_data = {
            'code': r.content
        }
        r = requests.post(gen_req_url, form_data, headers=headers)
        df = pd.read_excel(BytesIO(r.content))
        df['일자'] = tdate
        file_name = 'basic_'+ str(tdate) + '.xlsx'
        df.to_excel(path+file_name, index=False, index_label=None)
        print('KRX crawling completed :', tdate)
        return

    def get_historical_data_d(self,index_name,start, end):
        year_start = start//10000
        year_end = end//10000
        month_start = (start-year_start * 10000)//100
        month_end = (end - year_end * 10000)//100+1
        for year in range(year_start, year_end+1):
            for month in range(month_start, month_end):
                for day in range(1, 32):
                    tdate = year * 10000 + month * 100 + day * 1
                    if start <= tdate <=end:
                        krx_basic(index_name,tdate)

# 필요한 추가적인 import나 유틸리티 함수는 필요에 따라 추가합니다.
