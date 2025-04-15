#API请求配置
class Config:
    API_BASE_URL = "http://apaas.sit.internal.virtueit.net:81"
    COMPANY_CREATE_ENDPOINT = "/v5/qzzservice/biz/enterprise/add"
    COMPANY_DIAGNOSIS_ENDPOINT = "/v5/qzzservice/biz/dtd/digitalQuestion/saveDigitalQuestionResult"
    REPORT_GENERATE_ENDPOINT = "/v5/qzzservice/biz/dtd/aiReport/submit"
    POLLING_ENDPOINT = "/v5/qzzservice/biz/dtd/aiReport/polling"
    HEADERS = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxOTA5NTI2MTY2Nzc1NzAxNTA1Iiwicm5TdHIiOiJVOVlQdEhEd0t6WWZBQUJNRjVsdXdSdllBUVN6RGYwVSIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjE3ODkxOTE4NzYxNDY0MDUzNzciLCJ1c2VySWQiOjE5MDk1MjYxNjY3NzU3MDE1MDV9.m4gmqfQp3IIrDB_x5xPWRVAbdTWFgEmBe5Jj7Upy6a0",
        "Cookie":"zxqy_token=true; zxqy_token_new=BearereyJhbGciOiJIUzI1NiJ9.QW1JcW1wMVVUU2lsUisvNmlmekxQL0RRSXA5VUJDSFd1UFJRdnQ1Ym5GVVoxSUZiS0p5TlVibkFkcjZ3SXVFNjNoaWNtb1Jnb0l6TVM4MlRWVWhkaWJ1d0dPZ0lKd2dXeVVFSFpBVXhWM01DeG1XRi9JMGhsU29pTjBxQlhKY21CSjRzbVprMjNFemZ0cjRKYVZXYmpRNlFpZkROamFJPQ.KO1Qql1qRdC29IYJnlgg0XaTv61vsgFYJn1d2CPi1yk; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxOTA5NTI2MTY2Nzc1NzAxNTA1Iiwicm5TdHIiOiJVOVlQdEhEd0t6WWZBQUJNRjVsdXdSdllBUVN6RGYwVSIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjE3ODkxOTE4NzYxNDY0MDUzNzciLCJ1c2VySWQiOjE5MDk1MjYxNjY3NzU3MDE1MDV9.m4gmqfQp3IIrDB_x5xPWRVAbdTWFgEmBe5Jj7Upy6a0",
        "ClientId": "e5cd7e4891bf95d1d19206ce24a7b32e"
    }
    
    # 注意：上面的认证信息需要从系统登录后获取最新的值
    # 如果遇到"认证失败，无法访问系统资源"错误，请更新上面的认证信息
    