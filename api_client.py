from inspect import Parameter
import requests
import logging
from typing import Optional, Dict
from config import Config

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        Config.validate()
        self.base_url = Config.API_BASE_URL.rstrip('/')
        self.session = requests.Session()
        
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {str(e)}", exc_info=True)
            return None

    def create_company(self, data: Dict) -> Optional[str]:
        endpoint = Config.COMPANY_CREATE_ENDPOINT
        response = self._request('POST', endpoint, json=data)
        return response.get('data') if response else None

    def start_diagnosis(self, company_id: str) -> Optional[str]:
        endpoint = Config.COMPANY_DIAGNOSIS_ENDPOINT
        data = {
            "enterpriseId": company_id,
            "digitalScoringQuestionList": [
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 1,
                    "title": "企业网络建设连接情况",
                    "questionId": "1844279046318460901",
                    "optionIds": [
                        random.choice(["1844555686395121664", "1844556078206029824", "1844557198219415552", "1844557465157505024", "1844557626575294464"])
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 2,
                    "title": "企业的生产设备数字化率",
                    "questionId": "1844279856171454402",
                    "optionIds": [
                        "1844558205435383808"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 3,
                    "title": "企业的生产设备联网率",
                    "questionId": "1844280428161273803",
                    "optionIds": [
                        "1844559625031127040"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 4,
                    "title": "企业实现数据自动采集的业务环节覆盖范围",
                    "questionId": "1844281512367886304",
                    "optionIds": [
                        "1844560424025067520"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 5,
                    "title": "企业使用本地或云化部署的信息化服务，实现业务的数字化管理情况",
                    "questionId": "1844295437452972005",
                    "optionIds": [
                        "1844564007877480450"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 6,
                    "title": "企业在保障网络安全方面采取的举措",
                    "questionId": "1844296377652350906",
                    "optionIds": [
                        "1844566961237921794"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化基础",
                    "firstModuleKey": 1,
                    "order": 7,
                    "title": "企业在保障数据安全方面采取的举措",
                    "questionId": "1844297130567667707",
                    "optionIds": [
                        "1844567243388751875"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化管理",
                    "firstModuleKey": 2,
                    "order": 1,
                    "title": "企业对数字化的认识与执行水平情况",
                    "questionId": "1844298014265577408",
                    "optionIds": [
                        "1844567897058447362"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化管理",
                    "firstModuleKey": 2,
                    "order": 2,
                    "title": "企业数字化管理制度的建立情况",
                    "questionId": "1844298655008428009",
                    "optionIds": [
                        "1844570548034736129"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化管理",
                    "firstModuleKey": 2,
                    "order": 3,
                    "title": "企业在数字化人才建设方面采取的措施",
                    "questionId": "1844299240533266410",
                    "optionIds": [
                        "1844571859526488066"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化管理",
                    "firstModuleKey": 2,
                    "order": 4,
                    "title": "企业近三年平均数字化投入总额占营业额的平均比例（企业成立不满三年按照实际成立时长计算年均投入）",
                    "questionId": "1844299717354328011",
                    "optionIds": [
                        "1844572513741443073"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化成效",
                    "firstModuleKey": 3,
                    "order": 1,
                    "title": "企业数字化改造后每百元营业收入中综合能源消费量相比于改造前的变化情况",
                    "questionId": "1844300392054263812",
                    "optionIds": [
                        "1844578599512969216"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化成效",
                    "firstModuleKey": 3,
                    "order": 2,
                    "title": "企业数字化改造后月均产品合格率相比于改造前的变化情况",
                    "questionId": "1844301970047897613",
                    "optionIds": [
                        "1844579058487267328"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化成效",
                    "firstModuleKey": 3,
                    "order": 3,
                    "title": "企业上年度人均营业收入相比于前年变化情况",
                    "questionId": "1844302134414282714",
                    "optionIds": [
                        "1844579477376602112"
                    ],
                    "blank": {}
                },
                {
                    "firstModuleName": "数字化成效",
                    "firstModuleKey": 3,
                    "order": 4,
                    "title": "企业上年度每百元营业收入中的成本相比于前年变化情况",
                    "questionId": "1844303187348164615",
                    "optionIds": [
                        "1844580142404472832"
                    ],
                    "blank": {}
                }
            ],
            "digitalScenariosList": [
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 1,
                    "title": "企业在产品设计场景上数字化应用情况",
                    "scenariosId": "1844295437452972016",
                    "scenariosLevel": 2
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 2,
                    "title": "企业在工艺设计场景上数字化应用情况",
                    "scenariosId": "1844281512367886317",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 3,
                    "title": "企业在营销管理场景上数字化应用情况",
                    "scenariosId": "1844297130567667718",
                    "scenariosLevel": 2
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 4,
                    "title": "企业在售后服务场景上数字化应用情况",
                    "scenariosId": "1844298655008428019",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 5,
                    "title": "企业在计划排程场景上数字化应用情况",
                    "scenariosId": "1844297130567667720",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 6,
                    "title": "企业在生产管控场景上数字化应用情况",
                    "scenariosId": "1844298014265577421",
                    "scenariosLevel": 2
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 7,
                    "title": "企业在质量管理场景上数字化应用情况",
                    "scenariosId": "1844300392054263822",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 8,
                    "title": "企业在设备管理场景上数字化应用情况",
                    "scenariosId": "1844321192011263823",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 9,
                    "title": "企业在安全生产场景上数字化应用情况",
                    "scenariosId": "1844299240533266424",
                    "scenariosLevel": 4
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 10,
                    "title": "企业在能耗管理场景上数字化应用情况",
                    "scenariosId": "1844300392054263825",
                    "scenariosLevel": 1
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 11,
                    "title": "企业在采购管理场景上数字化应用情况",
                    "scenariosId": "1844301970047897626",
                    "scenariosLevel": 2
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 12,
                    "title": "企业在仓储物流场景上数字化应用情况",
                    "scenariosId": "1844281512367886327",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 13,
                    "title": "企业在财务管理场景上数字化应用情况",
                    "scenariosId": "1844303187348164628",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 14,
                    "title": "企业在人力资源场景上数字化应用情况",
                    "scenariosId": "1844300392054263829",
                    "scenariosLevel": 2
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 15,
                    "title": "企业在协同办公场景上数字化应用情况",
                    "scenariosId": "1844298655008428030",
                    "scenariosLevel": 3
                },
                {
                    "firstModuleName": "数字化经营",
                    "firstModuleKey": 4,
                    "order": 16,
                    "title": "企业在决策支持场景上数字化应用情况",
                    "scenariosId": "1844295437452972031",
                    "scenariosLevel": 3
                }
            ]
        }
        response = self._request('POST', endpoint,params=data)
        return response.get('data') if response else None

    def generate_report(self, company_id: str, report_id: str) -> bool:
        endpoint = Config.REPORT_GENERATE_ENDPOINT
        data = {
            "enterpriseId": company_id,
            "recordId": report_id,
            "reportName": "中小企业数字化转型咨询诊断报告",
            "logoIds": [],
            "mainproducts": "",
            "mainproductsIds": [],
            "processflow": "",
            "processflowIds": [],
            "intelligentdevice": "",
            "intelligentdeviceIds": [],
            "industrialsoftware": "",
            "industrialsoftwareIds": [],
            "sitesurveyDate": "2025-04-09\n00:00:00",
            "sitesurvey": "ok",
            "sitesurveyIds": [],
            "siteSurveyPeopleList": [
                {
                    "rosterName": "doawAOtell6GVPL0D012Bw==",
                    "rosterAgency": "张三的机构",
                    "rosterRole": "张三的角色",
                    "rosterContacts": "Djx5rzQzhrz4ZXDauh8NOg=="
                }
            ],
        }
        response = self._request('POST', endpoint, params=data)
        return response.get('msg') if response else False