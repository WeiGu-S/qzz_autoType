import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import os

class EnterpriseDataExporter:
    def __init__(self, api_url, auth_token, cookies):
        """
        初始化分页数据采集器
        :param api_url: 接口地址
        :param auth_token: Bearer Token
        :param cookies: Cookie字符串
        """
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": auth_token,
            "Content-Type": "application/json; charset=utf-8",
            "Cookie": cookies,  # 直接注入Cookie字符串[6](@ref)
            "Clientid":"e5cd7e4891bf95d1d19206ce24a7b32e"
        })
        
        # 配置自动重试（网络波动/服务端错误）
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
    
    def fetch_all_pages(self, payload = None, page_size=20, version = "new"):
        """
        分页获取全部数据
        :param filters: 筛选条件字典
        :param page_size: 每页数据量
        :return: 合并后的数据集
        """
        all_data = []
        page_num = 1
        if version == "new":
            while True:
                # 构造请求体（含分页参数）[8](@ref)
                payload = {
                    "pageNum": page_num,
                    "pageSize": page_size,
                    "digitalLevel": "",
                    "location": "",
                    "keyWord": ""
                }
                try:
                    # 发送POST请求（JSON格式）[7](@ref)
                    response = self.session.post(
                        self.api_url,
                        json=payload,
                        timeout=15
                    )
                    response.raise_for_status()  # 非2xx状态码触发异常
                    
                    data = response.json()
                    print(f"API响应数据结构: {data}")
                    
                    # 检查认证状态
                    if data.get('code') == 401:
                        raise requests.exceptions.RequestException(f"认证失败: {data.get('msg')}")
                    
                    # 校验数据结构[1](@ref)
                    if not isinstance(data.get("rows"), list):
                        raise ValueError(f"响应中缺少有效的rows字段，API返回: {data}")
                    
                    page_data = data["rows"]
                    all_data.extend(page_data)
                    print(f"✅ 第{page_num}页获取成功: {len(page_data)}条记录")
                    
                    # 终止条件：数据量不足page_size[2](@ref)
                    if len(page_data) < page_size:
                        print(f"⏹ 终止分页（第{page_num}页数据不足{page_size}条）")
                        break
                    
                    page_num += 1
                    time.sleep(0.3)  # 防止请求过载[4](@ref)
                    
                except requests.exceptions.RequestException as e:
                    print(f"❌ 第{page_num}页请求失败: {str(e)}")
                    break
            
            print(f"📊 总计获取 {len(all_data)} 条数据")
            return all_data
        elif version == "old":
            pageNum = 1
            while True:
                try:
                    # 发送POST请求（JSON格式）[7](@ref)
                    response = self.session.get(
                        url = self.api_url.format(pageNum = pageNum),
                        timeout=15
                    )
                    response.raise_for_status()  # 非2xx状态码触发异常
                    
                    data = response.json()
                    print(f"API响应数据结构: {data}")
                    # 检查认证状态
                    if data["results"].get('code') == 401:
                        raise requests.exceptions.RequestException(f"认证失败: {data['results'].get('msg')}")
                    # 校验数据结构[1](@ref)
                    if not isinstance(data.get("results"), dict):
                        raise ValueError(f"响应中缺少有效的results字段，API返回: {data}")
                    if "data" not in data["results"]:
                        raise ValueError(f"响应中缺少data字段，API返回: {data['results']}")
                    page_data = data["results"]["data"]
                    all_data.extend(page_data)
                    print(f"✅ 第{pageNum}页获取成功: {len(page_data)}条记录")
                    # 终止条件：数据量不足page_size[2](@ref)
                    if len(page_data) < 10:
                        print(f"⏹ 终止分页（第{pageNum}页数据不足 10 条）")
                        break
                    pageNum += 1
                    time.sleep(0.3)  # 防止请求过载[4](@ref)
                except requests.exceptions.RequestException as e:
                    print(f"❌ 第{pageNum}页请求失败: {str(e)}")
                    break
            
            print(f"📊 总计获取 {len(all_data)} 条数据")
            return all_data
        else:
            raise ValueError("不支持的版本类型")

    @staticmethod
    def export_to_excel(data, filename="enterprise_data.xlsx"):
        """导出数据到Excel"""
        if not data:
            raise ValueError("无有效数据可导出")
        
        df = pd.DataFrame(data)
        # 动态生成带时间戳的文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"{filename.split('.')[0]}_{timestamp}.xlsx"
        
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"💾 数据已导出至: {os.path.abspath(output_file)}")
        return output_file

# 使用示例
if __name__ == "__main__":
    # 配置参数（使用您提供的值）
    # 新版
    # config = {
    #     "API_URL": "https://szpt.onepower.com.cn/qzz/v5/qzzservice/biz/enterprise/list",
    #     "AUTH_TOKEN": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiJzeXNfdXNlcjoxIiwicm5TdHIiOiJ1T1NhZ0E1cDlhRUtCQUdZd0QzT2hMdFY1S0x4RVlSUiIsImNsaWVudGlkIjoiZTVjZDdlNDg5MWJmOTVkMWQxOTIwNmNlMjRhN2IzMmUiLCJ0ZW5hbnRJZCI6IjAwMDAwMCIsInVzZXJJZCI6MX0.w53haOx94Wsdkro4Ikkl3ZQ_Hq_XFInZJmGNiqT_bKA",
    #     "COOKIES": "EGG_SESS=iCfKow4hT7hSCdNJEKLpXAxM7DjUQW_6aR4AKdqWnNzdKDrksuy1UThi0WNKzqrv-KH2yBgp1j9BYFnVgTH_rz-7tXNICjercbuwOIeE_rPnN6zDoLSCDIKkE6t29Pm4O5VrdRETda2-s6xHjgV6Y1d32SMQRbJG8o7GGbGssxC53vKp8BriAy64p8YDYL986faPOZgcIjjANKyAb-9uejmi0N4bZoUSuVBoMnMeFojmaa7Bmrtw9wta4VzEVVhfDi8ylrwwbjrofljveNLRFf-jZmoxD1HC_-rhR-Ar9XOia8XlvwE56DrTMXJaBQAhbdvFBJX0HThXYtxiiiObFpch451sUK9hIzp6ppQxEQCquaObzOs-nVxTMZiL2LmEfo5b0rbfGFrZ1-E8Vfn-T1O0yA8gYm8GqdR-qJqcLhDnOLv0iMCorj-sMuFYEdNJwb6FO2L9EIGzcmnrLtWoCKFQxjmwcAIiebZKGbmkhLR3VM8_tccvEcLrxjXcj6j03DzWpssCs0wdJLn6Fyu6rXtZuh1YHfWhU7PixEFa8tkEOqquvDHcs9ZIx7yQuLcYm7bd4KMUmfMF5HtHItrAoE1jgg3bsU7ITLjHpF14kAP8g7up0N29p7Dvj3Xuzu6jqVeHzOoL59qc_k2YeLQF51xsic9pyRI7-Z0QukI7CoFmpm8qS0_2YSQa-FwlmvOEkZx8cy9ialB0297CWTWUg8lpY_Is71nudxTb5goHpsX7dPAyGcVpbwbf1naTNLnfvjRVDNdX7Zx90OwhrA3xdNef98mi5kIkeG3EOSy0s0Ie1Lj0XIVCRt3kNv6G1mTscdfO160j8QLRAUZeUShSlo9-tppTvE7vobXWmBDyIzITQfgtcXoyCfGTHTmIcyapHREeGGI2SyrvyQjooEWrYvW591WPt1892UvF5tyWCxGH4lIwcVlgbyk69F4VOqrrVJNOpZFMs4c_3EIB4oX8KkTgXGL3MAWEW4X7nCx57i8Q87BU1vLp0Wa-FTruTNGzg_SSF7hR9v8b1ctQKGFW5XnCG0aX5nzGCr60J3rSUiM-xNFp-YqbZ5IzQBow83jWw9FAl-7VWsJ9IcQ3YDylzijV_PlFHv_RpxvHXF6wXhpBGdKF3xNxk5iltEJLRwC7Halwe7DXAF0I4rKDJMr4x__L8UI4MntuuyzjAIluMi-hy16nMm_rtJiUL8mWt3cmaCNLWtW5zZkyds7Q5f48XBeZWZoescFQU3aep8SNJErWrVZqRiGdU9Y_DbV1eiwxkWR7yqCmcRS41e2nPgoY7iFDki8sWCPggzj2ZmMgCJFaUGEHOAL98wFYzFDWfuSjtSbxChbAcfPI_FPPwgWhtLwkzt8KYbNeAUXUrcwjCpfAWfjzoBsH5MG6Scoa0BiGwLWqYGObmzS6St4VkBoGVgPqe24xuGzxH7ibPkPH7RrCDaIYvMm3a6ecNlHoVvnlqVkkRhmlJWXvxQyz8ccTrQ=="
    # }
    
    # 老版
    config = {
        "API_URL": "https://szpt.onepower.com.cn/qzd/app/api/v1/ncapp_BwX9VYw8BejyMdp5erXoN8/ncmod_SbTuBaD4KyxpcJcJqWyT77/?page={pageNum}&page_size=10&ordering=-createtime",
        "AUTH_TOKEN": "JWT 64987172fbe4255c57038fb722e0b3490d2a59e3a4c53800d39bc46f77f97148ad7d8a68cdd82087f829061af2ab438eebfd20dfb473efca345004c5c9f73dc6485ba526aa5e7843a8a93cd535f1e820b801d3980958f96099f44125152023e22f75c15b5b847cd71527de0d89b85458ce92867abf5c5791cd9bfb43d2b75a5c50d3c0830030b1570887a88f33cfa6a25dafe917a74a0eb57dd75b1a90c85e248dd02efc840e86c9d63b695dda59755d073dc864879f5d3784946593326eddd505ecea24c00659c51ff045dc107867245cf077c416391ea12708c3752a2193db145261a43b8c4483970c1c928f7937705769b34ef5af711b6e2a47dec33b3d0a4f06912f953b944d2255f6b1a05a30c92b68953075ca7e88d13c6bc52e50ae",
        "COOKIES":"projId=onecode_31006; Admin-Token-onecode_31006=64987172fbe4255c57038fb722e0b3490d2a59e3a4c53800d39bc46f77f97148ad7d8a68cdd82087f829061af2ab438eebfd20dfb473efca345004c5c9f73dc6485ba526aa5e7843a8a93cd535f1e820b801d3980958f96099f44125152023e22f75c15b5b847cd71527de0d89b85458ce92867abf5c5791cd9bfb43d2b75a5c50d3c0830030b1570887a88f33cfa6a25dafe917a74a0eb57dd75b1a90c85e248dd02efc840e86c9d63b695dda59755d073dc864879f5d3784946593326eddd505ecea24c00659c51ff045dc107867245cf077c416391ea12708c3752a2193db145261a43b8c4483970c1c928f7937705769b34ef5af711b6e2a47dec33b3d0a4f06912f953b944d2255f6b1a05a30c92b68953075ca7e88d13c6bc52e50ae; language-onecode_31006=zh; EGG_SESS=iCfKow4hT7hSCdNJEKLpXFhpdOle7W5o5CycErJSZf0N73QV4bpsK6xX2q7dbIk1m71onlSkpTbi_6_mVEn3wfCSf-kqjYbKfrN7-Hy_32nufHqCN6urM-sZ3rI48zP3VpRcoiFU3GWuZotzWSrt3xfONAvcF2-CzxseG_O5Bpr6xpN4KUtO9TcavAHtKvq7p98I5oqDhw3N5Yi9m1kXU-jyqM29EDmBbbUtpvgSjLvoXWGoS_Nj3VzxiL225wTJfPrV610oUoSBOOT5mfh9Cz1CNT9VZJSzO97fm2pCCJTYgyLIVo3FDZBt_CyRTjZG1STZoiUA5Ue7EYwFwr35thxWIIt5IgyHha-WgssrnS8X-D8XuIZVqrQXz_BehoBQzutlpQD76a-qL43krDB281CC7VAUIRovnV7wGB_0EGcuvkapalEOuTvzuy7HHZL84KRZdPv0yiEp8DEfNhjz_9SMCJj7Pk2CgkuFE9GGLKkLErstmNIktCh24VcW3QImhiJsQeZqZNBF2UWM2GFNhsx_xnS9RX2jjO8FfQ4M-I8PkaCP_2YgB6Ml6im9rikjTbNjZLi2NXv7T02SowzAiy0Rw0nKfg5-UmvON-yd7m-u-V5DbvWAP_nZ-onHNIpleH-QO2R5kPOLuWfNu7bAL5l39Fe87eBuAqjtW_VjFTViBXkg_XRNH2nIdZyVYPzuysdtN8fL0MZvKi3KRdUQJwITYj7Ql31uXxaflDemObg_kN8ijU8o4Bk12m_-2T3nt6-3h7tvAojLN0A4K8PJ3q1kyZpbQ4kJ5mzjhd6Q5gWTwCphmhZkuR7peL6EyvWqLR8pVBw2OD822ZzsYXG7AiXd0E6IzcOlN-66ft7asQ-OXF4zpr-2wBHIJkeCBasGQ4dABZj2r2zah5UFqt1aXwXBTm0ujkNiANLYT0uotG1PSnVxWybIC7jgz7b2JDK6NprhtbnsN1DOl8-CeYEK8ANKzF8YJS4YbhWfG8-EpU7VzHpxzIYucrSDJd_o3vS_iYnaRSJXwgdN8jGGCvS6kdAqZaEfe0xTRuR225pNEiZQMHtorylqCPBU87vNVWDJXDvRd-JSAXxk-pShqDvEf5rXCZEjTg-2yZ9LAmP3jJmfVj9ee6QsYlPo-X2sFbHiiypcXai7p3TdwigAyKkkLqRpMZpywpYgP8QBG6VPyxt6lQs8atPEwJZvPTeCA2NEElXPyA9K7gUXcMCABDfB5uJCeDcbRHomGb21uXBNZyclKOA5jR562gxbD94xMw-L6vKrRskhe6N273j2qQpCWHarIOgDCj-8M0gJZSmkmj4oaLPVyj70m2R9jklfeSKwnyg10PGqo0KCE5UMTQp0GnDrxKVJPj2yLoDKs6nHlqxAWUzmujB0H4XKwoB2gxp8BMu_-v2Ibt8PU8mfZEUvwEYatsOdQC7fejAC-TMqv5DUP2I59fRUJvr31L_-l_O3sFgL811Rx8IwWPuNaSpmKw=="
    }
    
    # 初始化采集器
    exporter = EnterpriseDataExporter(
        api_url=config["API_URL"],
        auth_token=config["AUTH_TOKEN"],
        cookies=config["COOKIES"]
    )

    # 执行采集（分页获取全部数据）
    all_data = exporter.fetch_all_pages(version="old")
    
    # 导出Excel
    exporter.export_to_excel(all_data, "enterprise_list")