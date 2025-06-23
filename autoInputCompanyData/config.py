#API请求配置
class Config:
    # API_BASE_URL = "https://szpt.onepower.com.cn/qzz"
    API_BASE_URL = "http://apaas.sit.internal.virtueit.net:81"
    COMPANY_CREATE_ENDPOINT = "/v5/qzzservice/biz/enterprise/add"
    COMPANY_DIAGNOSIS_ENDPOINT = "/v5/qzzservice/biz/dtd/digitalQuestion/saveDigitalQuestionResult"
    REPORT_GENERATE_ENDPOINT = "/v5/qzzservice/biz/dtd/aiReport/submit"
    POLLING_ENDPOINT = "/v5/qzzservice/biz/dtd/aiReport/polling"
    HEADERS = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxOTA5NTI2MTY2Nzc1NzAxNTA1Iiwicm5TdHIiOiJvbDhCeXl6eDdBaGN4TEdRVXhZRVdWbDUxT1NZYTc5cSIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjE3ODkxOTE4NzYxNDY0MDUzNzciLCJ1c2VySWQiOjE5MDk1MjYxNjY3NzU3MDE1MDV9.wMo5kMiWQ1gY9g039wYj552RJJGtUlPVwF6JlPl_ZRs",
        "Cookie": "zxqy_token=true; zxqy_token_new=BearereyJhbGciOiJIUzI1NiJ9.QW1JcW1wMVVUU2lsUisvNmlmekxQL0RRSXA5VUJDSFd1UFJRdnQ1Ym5GVVoxSUZiS0p5TlVibkFkcjZ3SXVFNjNoaWNtb1Jnb0l6TVM4MlRWVWhkaWJ1d0dPZ0lKd2dXeVVFSFpBVXhWM01DeG1XRi9JMGhsU29pTjB1RldwSWpDcHNrbjVrMDNEd1NyWEk3UzRvaUs3alZROUZSQVlJPQ.jvpxrM0Zemc9lulR5y1OQlvveEhxgTmnBLYCO203UqA; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxOTA5NTI2MTY2Nzc1NzAxNTA1Iiwicm5TdHIiOiJvbDhCeXl6eDdBaGN4TEdRVXhZRVdWbDUxT1NZYTc5cSIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjE3ODkxOTE4NzYxNDY0MDUzNzciLCJ1c2VySWQiOjE5MDk1MjYxNjY3NzU3MDE1MDV9.wMo5kMiWQ1gY9g039wYj552RJJGtUlPVwF6JlPl_ZRs",
        "ClientId": "e5cd7e4891bf95d1d19206ce24a7b32e"
    }
    
    # 注意：上面的认证信息需要从系统登录后获取最新的值
    # 如果遇到"认证失败，无法访问系统资源"错误，请更新上面的认证信息
    