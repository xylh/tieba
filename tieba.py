
# -*- coding:utf-8 -*-
from lxml import etree
import urllib2
import urllib


class Tieba_Spider(object):
    def __init__(self):
        self.base_url = 'http://tieba.baidu.com/f?'#url路径
        #反爬头部
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        #xpath 匹配
        self.frist = '//a[@class="j_th_tit "]/@href'
        self.second= '//img[@class="BDE_Image"]/@src'
    # 发送请求
    def send_request(self, url):
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request)
        data = response.read()

        return data
        # 保存本地文件

    def write_file(self, data, image_name):
        print image_name
        file_path = 'images/' + image_name
        with open(file_path, 'w') as f:
            f.write(data)
    def analy(self,data,path):
        #转换类型
        file_data=etree.HTML(data)
        #解析
        res=file_data.xpath(path)
        return res
    # 调度方法 start_work
    def start_work(self):
        # 贴吧的名字
        tieba_name = raw_input('请输入抓取的贴吧名字:')
        # 开始的页数
        start_page = int(raw_input('请输入开始页数:'))
        # 结束的页数
        end_page = int(raw_input('请输入结束页数:'))

        # 开启循环
        for page in range(start_page, end_page + 1):
            pn = (page - 1) * 50
            # 发送请求
            params = {
                'kw': tieba_name,
                'pn': pn
            }

            # 网址的转译 url拼接
            params_str = urllib.urlencode(params)
            new_url = self.base_url + params_str
            data = self.send_request(new_url)

            # 第二层
            #  获取每一个子链接,发送请求
            reque=self.analy(data,self.frist)
            for i in reque:

                child_url= 'http://tieba.baidu.com'+i
                second_data=self.send_request(child_url)
             # 第三层
                image_list=self.analy(second_data,self.second)
                for li in image_list:
                    mes=self.send_request(li)
                    #文件名
                    image_name=li[-20:]
                    self.write_file(mes,image_name)



if __name__ == '__main__':
    tool = Tieba_Spider()
    tool.start_work()
