
class Config:
    API_BASE_URL = "http://apaas.sit.internal.virtueit.net:81"
    COMPANY_CREATE_ENDPOINT = "/v5/qzzservice/biz/enterprise/add"
    COMPANY_DIAGNOSIS_ENDPOINT = "/v5/qzzservice/biz/dtd/digitalQuestion/saveDigitalQuestionResult"
    REPORT_GENERATE_ENDPOINT = "/v5/qzzservice/biz/dtd/aiReport/submit"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "",
        "Cookie": "",
        "Clienid": ""
    }
    