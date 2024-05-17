import pymysql
import requests


class TaoTian:
    url = "https://talent.taotian.com/position/search?_csrf=c5b59e41-a543-4baf-b58a-6b65a98f1217"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Cookie': 'XSRF-TOKEN=c5b59e41-a543-4baf-b58a-6b65a98f1217; SESSION=QjY2MkI0Qjg2NDA2NzY2Qjg2QURFQTk3NzYwNkM5Q0I=; cna=ME3QHXh/qlACAWAWwpOatA43; xlly_s=1; prefered-lang=zh; isg=BDAwbsUnIXqCbP1-hUHbfyF8Af6CeRTDh2KRaiqBjAvE5dGP0owYUeHTPfWF9cyb',
        'Referer': 'https://talent.taotian.com/off-campus/position-list?lang=zh'
    }

    def __init__(self):
        self.db = pymysql.connect(host="localhost", user="root", password="", db="py_spider")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    @classmethod
    def get_data(cls):
        for page in range(21, 26):
            json_data = {
                "channel": "group_official_site",
                "language": "zh",
                "batchId": "",
                "categories": "",
                "deptCodes": [],
                "key": "",
                "pageIndex": page,
                "pageSize": 10,
                "regions": "",
                "subCategories": ""
            }
            response = requests.post(url=cls.url, headers=cls.headers, json=json_data).json()
            print('Getting data:', page)
            work_list = response['content']['datas']
            yield work_list

    def create_table(self):
        sql = """
            create table if not exists taotian(
                id int primary key auto_increment,
                categories varchar(20),
                work_name varchar(50) not null,
                city varchar(50),
                description text
            );
        """
        try:
            self.cursor.execute(sql)
            print('Create table success')
        except Exception as e:
            print('Create table failed', e)

    def insert_data(self, *args):
        """
        :param args:
            id
            categories
            work_name
            city
            description
        """
        sql = """
            insert into taotian(categories, work_name, city, description) values (%s, %s, %s, %s);
        """
        try:
            self.cursor.execute(sql, args)
            self.db.commit()
            print('Insert data success')
        except Exception as e:
            print('Insert data failed', e)
            self.db.rollback()

    def main(self):
        self.create_table()
        all_generated_objs = self.get_data()
        for obj in all_generated_objs:
            for item in obj:
                categories = item['categories'][0] if item['categories'] else 'N/A'
                work_name = item['name']
                city = item['workLocations'][0]
                description = item['description']
                self.insert_data(categories, work_name, city, description)


taotian = TaoTian()
taotian.main()



"""
exercise 1
https://talent.taotian.com/position/search?_csrf=c5b59e41-a543-4baf-b58a-6b65a98f1217
https://talent.taotian.com/position/search?_csrf=c5b59e41-a543-4baf-b58a-6b65a98f1217

https://talent.taotian.com/position/search?_csrf=c5b59e41-a543-4baf-b58a-6b65a98f1217
https://talent.taotian.com/position/search?_csrf=c5b59e41-a543-4baf-b58a-6b65a98f1217


Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36

{
  "channel": "group_official_site",
  "language": "zh",
  "batchId": "",
  "categories": "",
  "deptCodes": [],
  "key": "",
  "pageIndex": 2,
  "pageSize": 10,
  "regions": "",
  "subCategories": ""
}

{
    "success": true,
    "errorMsg": null,
    "errorCode": null,
    "content": {
        "datas": [
            {
                "trackId": "SSP1699307939376pdhuFPibWl8746",
                "positionUrl": "/off-campus/position-detail?positionId=1053307&track_id=SSP1699307939376pdhuFPibWl8746",
                "bucket": "DEFAULT",
                "id": 1053307,
                "name": "技术线-Java开发工程师-价格平台",
                "status": null,
                "categories": [
                    "技术类-开发"
                ],
                "publishTime": 1699256630000,
                "graduationTime": null,
                "modifyTime": 1699256630000,
                "workLocations": [
                    "杭州"
                ],
                "interviewLocations": null,
                "regionEnNameMap": {},
                "technologyNameIdMap": {},
                "tags": null,
                "requirement": "1、有Java开发经验，熟悉Spring、MyBatis等技术框架\n2、熟悉常见的NoSQL技术，比如HBase、MongoDB、Redis等\n3、具有一定的业务理解能力，能够发现业务需求、系统架构设计中存在的问题，并给出有效的解决方案\n4、具有营销领域和大数据领域从业经验优先\n5、具有较强的协调沟通能力",
                "description": "1、负责淘系全域营销产品或模块的技术架构设计、研发和持续优化工作\n2、应对电商业务和海量数据带来的高并发、高可用和高负载的挑战，保持系统的高稳定性\n3、协助业务方梳理业务需求和解决方案，共同推动方案落地",
                "experience": {
                    "from": 1,
                    "to": null
                },
                "degree": "bachelor",
                "department": "阿里集团",
                "project": null,
                "positionType": null,
                "code": "GP1053307",
                "categoryName": null,
                "categoryType": null,
                "batchName": null,
                "batchId": null,
                "batchWillingCount": null,
                "channels": null,
                "operations": [],
                "isTongyi": false,
                "useInternal": null,
                "isLingYang": null
            },
            {
                "trackId": "SSP1699307939376GKLjhigDqF9682",
                "positionUrl": "/off-campus/position-detail?positionId=1029804&track_id=SSP1699307939376GKLjhigDqF9682",
                "bucket": "DEFAULT",
                "id": 1029804,
                "name": "技术线-高级Java开发工程师-内容创作",
                "status": null,
                "categories": [
                    "技术类-开发"
                ],
                "publishTime": 1699254976000,
                "graduationTime": null,
                "modifyTime": 1699254976000,
                "workLocations": [
                    "北京",
                    "杭州"
                ],
                "interviewLocations": null,
                "regionEnNameMap": {},
                "technologyNameIdMap": {},
                "tags": null,
                "requirement": "1、Java基础扎实，熟悉IO、多线程、集合等基础框架，熟悉分布式、缓存、消息、搜索等中间件。\n2、掌握常用设计模式和面向对象设计原则，具备分布式、高并发、高可用、大数据的系统设计能力。\n3、热爱技术研发，具有快速学习能力；注重代码质量，有良好的软件工程知识和编码规范意识。\n4、业务理解能力强，善于思考和沟通，有责任心和团队精神。\n5、加分项：有大数据研发技能，或擅长用数据分析问题。",
                "description": "1. 参与内容创作平台、内容运营平台的架构设计和代码实现，支撑手淘内容化重点战役。\n2. 深入理解内容业务，分析和发现运营及创作者痛点，通过优秀的技术方案和产品体系，提升内容经营效率。\n3. 持续改进和优化系统架构，保障日常稳定性，提升产品体验，支撑内容业务的高速发展。",
                "experience": {
                    "from": 1,
                    "to": null
                },
                "degree": "bachelor",
                "department": "阿里集团",
                "project": null,
                "positionType": null,
                "code": "GP1029804",
                "categoryName": null,
                "categoryType": null,
                "batchName": null,
                "batchId": null,
                "batchWillingCount": null,
                "channels": null,
                "operations": [],
                "isTongyi": false,
                "useInternal": null,
                "isLingYang": null
            },
            {
                "trackId": "SSP1699307939376HGMzButURu1850",
                "positionUrl": "/off-campus/position-detail?positionId=1044302&track_id=SSP1699307939376HGMzButURu1850",
                "bucket": "DEFAULT",
                "id": 1044302,
                "name": "技术线-AIGC算法工程师-杭州/北京",
                "status": null,
                "categories": [
                    "技术类-算法"
                ],
                "publishTime": 1699251049000,
                "graduationTime": null,
                "modifyTime": 1699251049000,
                "workLocations": [
                    "杭州"
                ],
                "interviewLocations": null,

"""