#API请求配置
class Config:
    API_BASE_URL = "http://apaas.sit.internal.virtueit.net:81"
    COMPANY_CREATE_ENDPOINT = "/v5/qzzservice/biz/enterprise/add"
    COMPANY_DIAGNOSIS_ENDPOINT = "/v5/qzzservice/biz/dtd/digitalQuestion/saveDigitalQuestionResult"
    REPORT_GENERATE_ENDPOINT = "/v5/qzzservice/biz/dtd/aiReport/submit"
    HEADERS = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxOTA5NTI2MTY2Nzc1NzAxNTA1Iiwicm5TdHIiOiI0d09kRzBaT1dkY0w5NFRHemI0YnpDeUhBUWZrN1J5eCIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjE3ODkxOTE4NzYxNDY0MDUzNzciLCJ1c2VySWQiOjE5MDk1MjYxNjY3NzU3MDE1MDV9.rcLct7_6Vcia-_32odh3HjSIGcMF0QT9L5CQ7Os1qNA",
        "Cookie": "zxqy_token=true; zxqy_token_new=BearereyJhbGciOiJIUzI1NiJ9.QW1JcW1wMVVUU2lsUisvNmlmekxQL0RRSXA5VUJDSFd1UFJRdnQ1Ym5GVVoxSUZiS0p5TlVibkFkcjZ3SXVFNjNoaWNtb1Jnb0l6TVM4MlRWVWhkaWJ1d0dPZ0lKd2dXeVVFSFpBVXhWM01DeG1XRi9JMGhsU29pTjBxQlg1SWdBcDB0bXBrMzNFa3R4bEJ1MWtqU2JBUFVwQjZYUWEwPQ.1f4V5rbUU8Q7tTmfKRBEFZ2-OACc_xF7Xt5K2SfHV3c; Authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxOTA5NTI2MTY2Nzc1NzAxNTA1Iiwicm5TdHIiOiI0d09kRzBaT1dkY0w5NFRHemI0YnpDeUhBUWZrN1J5eCIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjE3ODkxOTE4NzYxNDY0MDUzNzciLCJ1c2VySWQiOjE5MDk1MjYxNjY3NzU3MDE1MDV9.rcLct7_6Vcia-_32odh3HjSIGcMF0QT9L5CQ7Os1qNA",
        "ClienId": "e5cd7e4891bf95d1d19206ce24a7b32e"
    }
    
    # 注意：上面的认证信息需要从系统登录后获取最新的值
    # 如果遇到"认证失败，无法访问系统资源"错误，请更新上面的认证信息
    