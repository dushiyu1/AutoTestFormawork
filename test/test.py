import json
import os

import allure
import pytest

from API.api import API


def get_test_cases():
    current_script = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.path.dirname(current_script)
    test_case_dir = os.path.join(current_dir, "DATA")
    if not os.path.exists(test_case_dir):
        raise FileNotFoundError("测试文件不存在，请确保根目录下存在DATA文件夹")
    test_cases = []
    for file in os.listdir(test_case_dir):
        if file.endswith(".json"):
            json_file_path = os.path.join(test_case_dir, file)
            with open(json_file_path, 'r', encoding='utf-8') as config_file:
                data = config_file.read()
                test_case = json.loads(data)
                test_cases.append((file, test_case))
    return test_cases


@allure.epic("SAP接口测试")
@allure.feature("OpenCall接口")
class Test_API:

    @classmethod
    @pytest.mark.parametrize("file_name,test_case",get_test_cases())
    @allure.title("测试用例 {file_name}")
    @allure.story("POST请求校验")
    def test_api(self,file_name,test_case):
        allure.dynamic.description(f"执行{file_name},校验接口返回结果")
        allure.attach(
            json.dumps(test_case,ensure_ascii=False,indent=2),
            name="测试用例参数",
            attachment_type=allure.attachment_type.JSON
        )
        try:
            res = API.do_api_test(test_case)
            with allure.step("校验状态码"):
                assert res.status_code == 200,f"状态码错误，预期200，实际{res.status_code}"
            with allure.step("校验业务返回结果"):
                actual_data = json.loads(res.text)
                expected_data = test_case['excepted']
                assert actual_data == expected_data,f"校验失败，预期{expected_data},实际{actual_data}"
            allure.attach(
                json.dumps(res.json(),ensure_ascii=False,indent=2),
                name="接口响应结果",
                attachment_type=allure.attachment_type.JSON
            )

        except AssertionError as e:
            allure.attach(str(e),name="失败原因",attachment_type=allure.attachment_type.TEXT)
            raise Exception(f"用例{file_name}校验失败：{str(e)}")
        except Exception as e:
            allure.attach(str(e),name="执行异常",attachment_type=allure.attachment_type.TEXT)
            raise Exception(f"用例{file_name}执行失败：{str(e)}")
