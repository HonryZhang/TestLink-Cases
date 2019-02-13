# TestLink_Test
### 环境依赖

|环境依赖|安装方法|
| -------|:-------------:|
|python2.7 or python3|	https://www.python.org/|
|xlrd库|	ubuntu: apt-get install -y python-pip <br> pip install xlrd <br> centos: yum install -y python-pip <br> pip install xlrd|
|testlink库|	pip install TestLink-API-Python-client|
|xlutils库|	pip install xlutils|

#### 使用方法

代码目录结构：

PMO-公开 > 从Testlink导入导出用例 > image2019-2-13 14:7:15.png 

1.download目录用于存放下载的用例集

2.logs目录用于存放执行记录

3.testCase用于存放下载用例的excel模板以及上传用例的excel模板

4.download_cases.py用于从用例集下载用例，下载后的文件名为用例集名称

5.upload_cases.py用于将模板excel中的所有用例上传到执行的用例集中

6.Log_util.py主要是日志设置模块

----------------------------------------------------------
#### 上传用例(upload_cases.py)：

1. API对应的URL为：url = 'http://10.255.101.237/testlink/lib/api/xmlrpc/v1/xmlrpc.php'

2. API对应的key为：登陆testlink后点击上方个人账号进入个人中心，新页面点击 '生成新的秘钥'，使用该key替换掉main文件中的key值

3. father_id为目标用例集ID，可通过在testlink用例管理界面选取用例集，然后点击右键获取APIID

4. project_id为目标项目ID,可以根据日志显示ID进行选择

5. 模板Excel中作者列必须与登陆用户名一致，否则上传时会引发鉴权或数据统计问题

6. 模板Excel需放在testCase目录下，不建议修改模板Excel的文件名

7.为了直观的体现用例步骤和对应的期望结果，建议在步骤前加上编号。（尽管导入到testlink后会自带编号）

8. 执行upload_cases.py

----------------------------------------------------------
#### 下载用例(download_cases.py）：

1. API对应的URL为：url = 'http://10.255.101.237/testlink/lib/api/xmlrpc/v1/xmlrpc.php'

2. API对应的key为：登陆testlink后点击上方个人账号进入个人中心，新页面点击 '生成新的秘钥'，使用该key替换掉main文件中的key值

3. father_id为目标用例集ID，可通过在testlink用例管理界面选取用例集，然后点击右键获取APIID

  4.执行download_cases.py
