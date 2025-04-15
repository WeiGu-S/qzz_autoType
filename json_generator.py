import random
import json
import data_random_generator

class ApiJsonGenerator:
    #生成企业Json
    def __init__(self):
        # 初始化数据
        self.data = {}

    # 生成企业信息Json
    @staticmethod
    def create_company_info_json(enterprise_name, province_code, city_code, district_code, location,address, first_industry_id, second_industry_id)-> dict:
        data = {
            "enterpriseName": enterprise_name,
            "contacts": "",
            "telephone": "",
            "provinceCode": province_code,
            "cityCode": city_code,
            "districtCode": district_code,
            "location": location,
            "address": address,
            "firstIndustryId": first_industry_id,
            "secondIndustryId": second_industry_id,
            "registeredCapital": random.randint(100, 10000),
            "establishmentTime": "",
            "employeesNum": random.randint(10, 1000),
            "enterpriseType": random.randint(1, 4),
            "enterpriseScale": random.randint(1, 4),
            "mainProducts": random.choice(["电子产品", "机械设备", "化工产品", "纺织品", "食品"]),
            "businessBenefits":"[{\"2021\":{\"totalAssets\":\"\",\"income\":\"\",\"profit\":\"\"}},{\"2022\":{\"totalAssets\":\"\",\"income\":\"\",\"profit\":\"\"}},{\"2023\":{\"totalAssets\":\"\",\"income\":\"\",\"profit\":\"\"}}]",
            "systemCertification": random.choice(["数据分类分级 (工业领域)", "数据安全防护体系", "两化融合管理体系", "质量管理体系", "环境管理体系", "能源管理体系", "职业健康安全管理体系", "信息安全管理体系", "数据管理能力成熟度评估模型 (DCMM)","无"]),
            "highTechEnterprise": random.randint(1, 4),
            "intelligentManufacturingDemonstrationFactory": random.randint(1, 4),
            "industrialInternetBenchmarkFactory": random.randint(1, 3),
            "specializedInnovativeLittleGiant": random.randint(1, 3),
            "applyResearchDevelopDesignSoftware": random.choice(["CAD","CAE","DBOM","CAM","数字孪生","其他","以上均无"]),
            "designSoftwareBrandModel":"",
            "applyProductionManufacturingSoftware":random.choice(["MES","APS","PLM","PDM","其他","以上均无"]),
            "manufacturingSoftwareBrandModel":"",
            "applyQualityManagementSoftware":random.choice(["QMS","LIMS","其他","以上均无"]),
            "qualitySoftwareBrandModel":"",
            "applyOperationsManagementSoftware":random.choice(["ERP","CRM","SRM","SCM","OA","BI","其他","以上均无"]),
            "operationsSoftwareBrandModel":"",
            "applyWarehouseLogisticsSoftware":random.choice(["WMS","其他","以上均无"]),
            "logisticsSoftwareBrandModel":"",
            "applyCloudService": random.choice(["公有云","私有云","混合云","无"]),
            "cloudServiceBrandModel":"",
            "networkUseSituation": random.choice(["宽带","专线","5G","无"]),
            "networkOperator":"",
            "digitalTransformFunds": random.randint(1, 5),
            "planCloudServiceSituation": random.choice(["设备上云","业务系统上云","资源上云（数据）","其他","以上均无"]),
            "intentionCloudBrandModel":"",
            "planApplySoftwareType":random.choice(["研发设计（CAD等）","生产管理（MES等）","运营管理（ERP等）","质量管理（QMS等）","仓储物流（WMS等）","其他","以上均无"]),
            "intentionSoftwareBrandModel":""
        } 
        return data

    #生成诊断结果Json
    def create_answer_result_json(company_id):
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
                            random.choice(["1844557809308536832", "1844558205435383808", "1844558225635151872", "1844558246426316800", "1844558268689682432"])
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
                            random.choice(["1844559593980694528", "1844559625031127040", "1844559641703485440", "1844559656928808960", "1844559712058740736"])
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
                            random.choice(["1844560165639163904", "1844560368551202816", "1844560386293108736", "1844560403942739968", "1844560424025067520", "1844560424025067525", "1844561303776137217", "1844561303776137218", "1844561303776137219", "1844561303776137220", "1844562916863512576", "1844562916863512577", "1844562916863512578", "1844562916863512579", "1844562916863512580"])
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
                            random.choice(["1844564007877480448", "1844564007877480449", "1844564007877480450", "1844564007877480451", "1844564007877480452"])
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
                            random.choice(["1844566961237921792", "1844566961237921793", "1844566961237921794", "1844566961237921795", "1844566961237921796"])
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
                            random.choice(["1844567243388751872", "1844567243388751873", "1844567243388751874", "1844567243388751875", "1844567243388751876"])
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
                            random.choice(["1844567897058447360", "1844567897058447361", "1844567897058447362", "1844567897058447363", "1844567897058447364", "1844567897058447365"])
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
                            random.choice(["1844570548034736128", "1844570548034736129", "1844570548034736130", "1844570548034736131", "1844570548034736132"])
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
                            random.choice(["1844571859526488064", "1844571859526488065", "1844571859526488066", "1844571859526488067", "1844571859526488068", "1844571859526488069"])
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
                            random.choice(["1844572513741443072", "1844572513741443073", "1844572513741443074", "1844572513741443075", "1844572513741443076"])
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
                            random.choice(["1844578556164837376", "1844578599512969216", "1844578619477856256"])
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
                            random.choice(["1844579044516040704", "1844579058487267328", "1844579077122560000"])
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
                            random.choice(["1844579462285496320", "1844579477376602112", "1844579491805007872"])
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
                            random.choice(["1844580125358821376", "1844580142404472832", "1844580156207927296"])
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
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 2,
                        "title": "企业在工艺设计场景上数字化应用情况",
                        "scenariosId": "1844281512367886317",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 3,
                        "title": "企业在营销管理场景上数字化应用情况",
                        "scenariosId": "1844297130567667718",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 4,
                        "title": "企业在售后服务场景上数字化应用情况",
                        "scenariosId": "1844298655008428019",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 5,
                        "title": "企业在计划排程场景上数字化应用情况",
                        "scenariosId": "1844297130567667720",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 6,
                        "title": "企业在生产管控场景上数字化应用情况",
                        "scenariosId": "1844298014265577421",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 7,
                        "title": "企业在质量管理场景上数字化应用情况",
                        "scenariosId": "1844300392054263822",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 8,
                        "title": "企业在设备管理场景上数字化应用情况",
                        "scenariosId": "1844321192011263823",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 9,
                        "title": "企业在安全生产场景上数字化应用情况",
                        "scenariosId": "1844299240533266424",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 10,
                        "title": "企业在能耗管理场景上数字化应用情况",
                        "scenariosId": "1844300392054263825",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 11,
                        "title": "企业在采购管理场景上数字化应用情况",
                        "scenariosId": "1844301970047897626",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 12,
                        "title": "企业在仓储物流场景上数字化应用情况",
                        "scenariosId": "1844281512367886327",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 13,
                        "title": "企业在财务管理场景上数字化应用情况",
                        "scenariosId": "1844303187348164628",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 14,
                        "title": "企业在人力资源场景上数字化应用情况",
                        "scenariosId": "1844300392054263829",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 15,
                        "title": "企业在协同办公场景上数字化应用情况",
                        "scenariosId": "1844298655008428030",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    },
                    {
                        "firstModuleName": "数字化经营",
                        "firstModuleKey": 4,
                        "order": 16,
                        "title": "企业在决策支持场景上数字化应用情况",
                        "scenariosId": "1844295437452972031",
                        "scenariosLevel": data_random_generator.RandomDataGenerator.get_scenario_level()
                    }
                ]
            }
        return data

    #生成诊断报告 Json
    def create_report_json(company_id: str, report_id: str) :
        # 随机生成报告调查数据
        rosterName = data_random_generator.RandomDataGenerator.get_name()
        rosterContacts = data_random_generator.RandomDataGenerator.get_contact()
        rosterAgency = data_random_generator.RandomDataGenerator.get_angency_name()
        sitesurveyDate = data_random_generator.RandomDataGenerator.get_date()
        sitesurvey = data_random_generator.RandomDataGenerator.get_research_description()
       
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
            "sitesurveyDate": sitesurveyDate,
            "sitesurvey": sitesurvey, 
            "sitesurveyIds": [],
            "siteSurveyPeopleList": [
                {
                    "rosterName": rosterName,
                    "rosterAgency": rosterAgency,
                    "rosterRole": "调查员",
                    "rosterContacts": rosterContacts
                }
            ]
        }
        # 构建返回的json数据
        return data
