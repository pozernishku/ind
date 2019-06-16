# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from ind.items import IndItem
from datetime import timedelta, date



class IndSpSpider(scrapy.Spider):
    name = 'ind_sp'
    allowed_domains = ['fcainfoweb.nic.in']

    def start_requests(self):
        start_date = date(2010, 1, 1)
        end_date = date(2019, 6, 12)

        for d in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
            yield FormRequest('https://fcainfoweb.nic.in/Reports/Report_Menu_Web.aspx',
                            formdata={'ctl00_MainContent_ToolkitScriptManager1_HiddenField': ';;AjaxControlToolkit, Version=4.1.51116.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:fd384f95-1b49-47cf-9b47-2fa2a921a36a:475a4ef5:addc6819:5546a2b:d2e10b12:effe2a26:37e2e5c9:5a682656:c7029a2:e9e598a9',
                                        '__EVENTTARGET': '',
                                        '__EVENTARGUMENT': '',
                                        '__LASTFOCUS': '',
                                        '__VIEWSTATE': 'tYJ56vp8X8UyHCeamrEv4o7RDW7C/l3Kdl4g3W1ALhz9Ahz4zDigylETwBVC9dos/DFd/s3ahAR+obWoaCqfv6Ql9mNx+OKJ6xiwc/qVnar/h4CyB1BQ1SwzdSfZ3phhpEJSDYul/pWcENl9kyWL09c2XEDn1yI+FIw+hXh3gZyEzaEUpW9QXNuSEbTWKIgunn4zSSk/LhKS4u6gETXQ/o6HUIs9/tRMVUgX1s3CLZF0RLW36tXoaY0MXAg/oxvAL2N2x8m9C6Obb2ByG3vt2kC8ObHzozbIy6N96ZreJwZfnDKOs5eqSvFlLZnKylMNK9ihVWGRuBh/1b1iNB68hTmW4eKY0D9dSjuRvaymMC6KrxGUQceagniCa+pxYDMoMAirFtq8yUCLYkDZ+knNjjSVZvK1OfoQvOwnOx/XAt0q+VReFGpPRVPoAGEnp2eLZAiAs1n6d+NpjmEjLosIRKLThhX6SjIeol/WjsRfV5NfWTa/twCd0cqUUebk0Urd3k/a7ZCG7J8NM/nZvKe6L7xrBEDzO/NoZpi1Xz6sg+bCK3FKlm7SiD8tQ4qdiOn8A340259STLaaNWrSX0Djvw==',
                                        '__VIEWSTATEGENERATOR': '37FEC614',
                                        '__VIEWSTATEENCRYPTED': '',
                                        '__EVENTVALIDATION': 'q8cKOEaIicLKkfeG8LgaQ5a1tZ1RCjKaOLamOWf8UVRWjFEiYWd5Ebg5i/P7f8N51nF/AHNoU6KEfMV8h2V3ysIYi4L4OnrIzQcX9m3EXwXs/gdr15H5eRNtFSPtiDfqLswhgAfe15FKO2ssGhq0RfIs3vxiJg1yotIHNipod1KgeNd/ZOjQDYfhVChB9FFqmFXqcNSzcRfLT7NGWeo6g/Vwjk8usxXUsRomnv1SgzboFkPyoDFASLt+73pfPMjUod8Us+ApcKynkBBamspwXX0kvqX7lwrFX6PD3Qe3mVpFyiAjYNjoULFIOyaILYf6CvuQL2GK8cOxgQ4lI1wQsuoOtWCexRbBZNc7fIkAaq3uraWN+xxDProE3NFTj0syK+N8p1H+rXxKy1rJfFFFLht8mV3nSFNNEFzmiH19BKq1MhqaCtFdFBDlGCGwfm+B',
                                        'ctl00$MainContent$Ddl_Rpt_type': 'Wholesale',
                                        'ctl00$MainContent$ddl_Language': 'English',
                                        'ctl00$MainContent$Rbl_Rpt_type': 'Price report',
                                        'ctl00$MainContent$Ddl_Rpt_Option0': 'Daily Prices',
                                        'ctl00$MainContent$Txt_FrmDate': d.strftime('%d/%m/%Y'),
                                        'ctl00$MainContent$btn_getdata1': 'Get Data'},
                            callback=self.parse,
                            dont_filter=True,
                            meta={'max_retry_times': 15,
                                  'download_timeout': 600,
                                  'Date': d.strftime('%d/%m/%Y')})

    def parse(self, response):
        regs = [('DELHI', 'Delhi'),
                ('AHMEDABAD', 'Ahmedabad'),
                ('MUMBAI', 'Mumbai'),
                ('JAIPUR', 'Jaipur'),
                ('KOLKATA', 'Kolkata'),
                ('HYDERABAD', 'Hyderabad'),
                ('BENGALURU', 'Bengalaru')]
        
        comms = ['INDAGM-rice',
                 'INDAGM-wheat',
                 'INDAGM-atta-wheat',
                 'INDAGM-gram-dal',
                 'INDAGM-tur-arhar-dal',
                 'INDAGM-urad-dal',
                 'INDAGM-moong-dal',
                 'INDAGM-masoor-dal',
                 'INDAGM-sugar',
                 'INDAGM-milk',
                 'INDAGM-ground-nut-oil',
                 'INDAGM-mustard-oil',
                 'INDAGM-vanas-pati',
                 'INDAGM-soya-oil',
                 'INDAGM-sunflower-oil',
                 'INDAGM-palm-oil',
                 'INDAGM-gur',
                 'INDAGM-tea-loose',
                 'INDAGM-salt-pack-iodised',
                 'INDAGM-potato',
                 'INDAGM-onion',
                 'INDAGM-tomato']

        # Data does not exist for this date
        if response.xpath('//*[contains(text(), "Sorry, Data does not exist for this date")]'):
            return None

        # Items by Region
        for reg in regs:
            amounts = response.xpath(f'//tr/td/font[contains(text(), "{reg[0]}")]/ancestor::td/following-sibling::td/text()').getall()
            for i, comm in enumerate(comms):
                if amounts[i] != 'NR':
                    yield IndItem(Date=response.meta.get('Date'),
                                  Price=amounts[i],
                                  UniqueId=comm + '-' + reg[1],
                                  Region=reg[1],
                                  CommodityID=comm)
        # IndiaAverage
        avg_amounts = response.xpath('//tr/td/b[contains(text(), "Modal Price")]/ancestor::td/following-sibling::td/b/i')
        for i, avg_amount in enumerate(avg_amounts):
            yield IndItem(Date=response.meta.get('Date'),
                          Price=avg_amount.xpath('text()').get(''),
                          UniqueId=comms[i] + '-' + 'IndiaAverage',
                          Region='IndiaAverage',
                          CommodityID=comms[i])

