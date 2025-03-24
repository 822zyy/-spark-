import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import os
import time
import logging
import random
import pandas as pd

# service =Service('./chromedriver.exe')
# options = webdriver.ChromeOptions()
# browser = webdriver.Chrome(service=service, options=options)
# browser.get('https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=Java&city=%E5%85%A8%E5%9B%BD')
# from spyder.widgets import browser
logging.basicConfig(filename='spider.log', level=logging.INFO)

class spider(object):
    def __init__(self,type,city,page):
        self.type = type        #类型（java、python…）
        self.city = city
        self.page = int(page)
        self.spiderUrl = 'https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=%s&city=%s&pn=%s'


    def startBrowser(self):
        service = Service('D:\djangoProject\基于spark的求职智能分析系统\spiders\chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.debugger_address='localhost:8222'       #端口开-保存用户数据（chrome --remote-debugging-port=8222）
        # print('3')
        browser = webdriver.Chrome(service=service, options=options)
        # print('4')
        return browser

    def main(self,page):
        # print(type(self.page))
        # print(type(page))
        if int(self.page) > page:
            return
        print(self.page)
        # print('2')
        browser = self.startBrowser()
        print('正在爬取的页码路径'+self.spiderUrl%(self.type,self.city,self.page))
        browser.get(self.spiderUrl%(self.type,self.city,str(self.page)))
        time.sleep(1)
        joblist = browser.find_elements(by=By.XPATH,value='//div[@id="jobList"]/div[@class="list__YibNq"]/div[@class="item__10RTO"]')
        print(joblist)
        print(len(joblist))
        for index,job in enumerate(joblist):
            try:
                # title职位
                title = job.find_element(by=By.XPATH, value='.//div[@class="p-top__1F7CL"]/a').text

                # company公司
                company = job.find_element(by=By.XPATH, value='.//div[@class="company-name__2-SjF"]/a').text

                # salary薪资
                salary = job.find_element(by=By.XPATH, value='.//div[@class="p-bom__JlNur"]/span').text
                salary = re.findall('\d+', salary)
                minsalary = int(salary[0]) * 1000
                maxsalary = int(salary[1]) * 1000
                # work_experience工作经验        education学历
                all = job.find_element(by=By.XPATH, value='.//div[@class="p-bom__JlNur"]').get_attribute(
                    'textContent').split('/')
                work_experience = all[0].split('k')[2].strip()
                education = all[1].strip()

                # com_tag公司tag       com_People公司人数
                try:
                    com_tag = job.find_element(by=By.XPATH,
                                               value='.//div[@class="company__2EsC8"]/div[@class="industry__1HBkr"]').text
                    com_People = re.findall('\d+', com_tag)
                except:
                    com_tag = '无'
                    com_People = [10]
                try:
                    com_People = '-'.join(com_People)
                except:
                    com_People = [0]

                # tag_List专业标签
                tag_List = job.find_elements(by=By.XPATH, value='.//div[@class="ir___QwEG"]/span')
                tagData = []
                for tag in tag_List:
                    tagData.append(tag.text)
                workTag = '/'.join(tagData)

                # welfare公司福利
                try:
                    welfare = job.find_element(by=By.XPATH,
                                               value='.//div[@class="item-bom__cTJhu"]/div[@class="il__3lk85"]').text.replace(
                        "“", "")
                    welfare = welfare.replace("”", "")
                except:
                    welfare = '无'

                imgSrc = job.find_element(by=By.XPATH, value='.//div[@class="com-logo__1QOwC"]/img').get_attribute(
                    "src")
                print(imgSrc)
                print(title, company, minsalary, maxsalary, work_experience, education, com_tag, com_People, workTag,
                      welfare)

                self.save_to_csv([self.type, self.city, title, company, minsalary, maxsalary, work_experience,
                                  education, com_tag, com_People, workTag, welfare, imgSrc])
                # break
            except:
                continue
        self.page += 1
        # time.sleep(3)
        time.sleep(random.uniform(2, 5))
        self.main(page)


    def save_to_csv(self,rowData):
        with open('./jobData.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)

    def init(self):
        if not os.path.exists('./jobData.csv'):
            with open('./jobData.csv', 'w', newline='', encoding='utf-8') as wf:
                writer = csv.writer(wf)
                writer.writerow(['type','city','title', 'company','minsalary','maxsalary','work_experience',
                                 'education','com_tag','com_People','workTag','welfare','imgSrc'])


if __name__ =="__main__":
    cityList = ['北京','上海','深圳','广州','杭州','成都','南京','武汉','西安','厦门','长沙','苏州','天津','重庆','郑州',
                '青岛','合肥','福州','济南','大连','珠海','无锡','佛山','东莞','宁波','常州','沈阳','石家庄','昆明','南昌','南宁'
                '哈尔滨','海口','中山','惠州','贵阳','长春','太原','嘉兴','泰安','昆山','烟台','兰州','泉州']

    typeList = ["大数据","Hadoop", "Hive", "Spark", "HBase", "大数据开发工程师", "运维工程师",
                "数据库管理员", "SQL", "数据分析师", "ETL工程师", "数据仓库", "数据采集", "数据处理",
                "云计算工程师", "爬虫工程师", "Java开发", "Python开发", "C++工程师", "前端开发",
                "后端开发", "全栈工程师", "机器学习工程师", "人工智能研究员", "深度学习", "自然语言处理",
                "计算机视觉", "嵌入式开发", "物联网工程师", "区块链开发", "智能合约", "DevOps工程师",
                "Kubernetes", "Docker", "Linux运维", "网络安全工程师", "渗透测试", "系统架构师",
                "解决方案架构师", "测试开发工程师", "自动化测试", "性能测试", "产品经理", "技术经理",
                "算法工程师", "推荐系统工程师", "音视频开发", "GIS开发", "Unity3D开发", "Unreal引擎开发",
                "移动端开发", "Android开发", "iOS开发", "Flutter开发", "React", "Vue.js", "Node.js",
                "Spring框架", "MyBatis", "微服务架构", "分布式系统", "消息队列", "Redis", "MongoDB",
                "Elasticsearch", "Neo4j", "TensorFlow", "PyTorch", "PaddlePaddle", "OpenCV",
                "FPGA开发", "数字电路设计", "芯片验证工程师", "5G通信", "网络协议开发", "云原生开发",
                "SRE工程师", "BI开发", "数据科学家", "量化工程师", "ERP开发", "CRM开发", "SAP实施",
                "工业互联网", "边缘计算", "服务网格", "Serverless", "量子计算", "RPA开发"]
    for city in cityList:
        for type in typeList:
            try:
                spiderObj = spider(type, city, '1')
                spiderObj.main(10)
                time.sleep(5)
            except Exception as e:
                print(f"爬取 {city} - {type} 时出错: {str(e)}")
                continue
        #     spiderObj =spider(type,city,'1')
        #     spiderObj.main(10)
        # # break

    # browser.quit()
    # spiderObj.init()