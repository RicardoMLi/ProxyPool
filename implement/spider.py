import re

from lxml import etree
from .utils import get_page,get_pagenum


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            if proxy is None:
                print('获取代理失败')
            else:
                print('成功获取到代理 ', proxy)
                proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        base_url = 'https://www.kuaidaili.com/free/inha/'
        urls = [base_url+str(page) for page in range(1,3)]

        for url in urls:
            print('Starting Crawling ' + url)
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                ip_infos = selector.xpath("//div[@id='list']/table/tbody/tr")
                if ip_infos:
                    for ip_info in ip_infos:
                        ip = ip_info.xpath("./td[@data-title='IP']/text()")[0] if ip_info.xpath("./td[@data-title='IP']/text()") else ''
                        port = ip_info.xpath("./td[@data-title='PORT']/text()")[0] if ip_info.xpath("./td[@data-title='PORT']/text()") else ''
                        if ip and port:
                            yield ':'.join([ip,port])
            else:
                print('Crawling failed ' + url)
                yield None

    def crawl_xicidaili(self):
        base_url = 'http://www.xicidaili.com/wt/'
        urls = [base_url+str(page) for page in range(1,3)]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJThhMTg5ZTUyMmI2OGIyMjBhZTdhNjg2MWIwMTBiMzIzBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUxOdDBEZ3M4UENjVU1zbVJvRE12bzduYmhDWWNja3UvM1hDSkhmWnF1SHM9BjsARg%3D%3D--03929568ba3d5cf2a08d38643438be6bb6f8e085; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1541994530; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1542006128',
            'Host': 'www.xicidaili.com',
            'Referer': 'http://www.xicidaili.com/wt/3',
            'Upgrade-Insecure-Requests': '1',
        }

        for url in urls:
            print('Starting Crawling ' + url)
            html = get_page(url,options=headers)
            if html:
                selector = etree.HTML(html)
                ip_infos = selector.xpath("//tr[@class='odd']|//tr[@class='']")
                if ip_infos:
                    for ip_info in ip_infos:
                        ip = ip_info.xpath("./td[2]/text()")[0] if ip_info.xpath("./td[2]/text()") else ''
                        # 剔除多余空格或换行
                        ip = re.findall(r'\d+\.\d+\.\d+\.\d+',ip)[0]
                        port = ip_info.xpath("./td[3]/text()")[0] if ip_info.xpath("./td[3]/text()") else ''
                        # 剔除多余空格或换行
                        port = re.findall(r'\d+', port)[0]
                        if ip and port:
                            yield ':'.join([ip,port])
            else:
                print('Crawling failed ' + url)
                yield None

    def crawl_89ip(self):
        for page in range(1,3):
            url = 'http://www.89ip.cn/index_{page}.html'.format(page=str(page))
            print('Starting Crawling ' + url)
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                ip_infos = selector.xpath("//table[@class='layui-table']/tbody/tr")
                if ip_infos:
                    for ip_info in ip_infos:
                        ip = ip_info.xpath("./td[1]/text()")[0] if ip_info.xpath("./td[1]/text()") else ''
                        # 剔除多余空格或换行
                        ip = re.findall(r'\d+\.\d+\.\d+\.\d+',ip)[0]
                        port = ip_info.xpath("./td[2]/text()")[0] if ip_info.xpath("./td[2]/text()") else ''
                        # 剔除多余空格或换行
                        port = re.findall(r'\d+',port)[0]
                        if ip and port:
                            yield ':'.join([ip,port])
            else:
                print('Crawling failed ' + url)
                yield None

    def crawl_ihuan(self):
        start_url = 'https://ip.ihuan.me/'
        pagenum_list = get_pagenum(start_url)

        for page_num in pagenum_list:
            url = start_url + page_num
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                ip_infos = selector.xpath("//table/tbody/tr")
                for ip_info in ip_infos:
                    ip = ip_info.xpath("./td[1]")[0] if ip_info.xpath("./td[1]") else ''
                    port = ip_info.xpath("./td[2]")[0] if ip_info.xpath("./td[2]") else ''
                    if ip and port:
                        yield ':'.join([ip,port])
            else:
                print('Crawling failed ' + url)
                yield None

    def crawl_66ip(self):
        for page in range(1,3):
            url = 'http://www.66ip.cn/{page}.html'.format(page=str(page))
            html = get_page(url)
            if html:
                selector = etree.HTML(html)
                ip_infos = selector.xpath("//div[@id='main']//table/tr")[1:]
                for ip_info in ip_infos:
                    ip = ip_info.xpath("./td[1]/text()")[0] if ip_info.xpath("./td[1]/text()") else ''
                    port = ip_info.xpath("./td[2]/text()")[0] if ip_info.xpath("./td[2]/text()") else ''
                    if ip and port:
                        yield ':'.join([ip,port])
            else:
                print('Crawling failed ' + url)
                yield None





