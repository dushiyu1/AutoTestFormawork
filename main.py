import pytest

if  __name__ == "__main__":
    pytest.main(["-v","-s", #详细输出
                 "./test/test.py", #测试文件
                 "--alluredir=./allure-results", #测试报告
                 "--clean-alluredir" #每次运行清空测试报告
                 ])

    #自动打开报告
    import subprocess
    subprocess.call(["allure","serve","./allure-results"])