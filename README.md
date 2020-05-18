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

1.download目录用于存放下载的用例集

2.logs目录用于存放执行记录

3.testCase用于存放下载用例的excel模板以及上传用例的excel模板

4.download_cases.py用于从用例集下载用例，下载后的文件名为用例集名称

5.upload_cases.py用于将模板excel中的所有用例上传到执行的用例集中

6.Log_util.py主要是日志设置模块

#### 上传用例(upload_cases.py)：


1.API对应的URL为：url = 'https://testlink.xsky.com/lib/api/xmlrpc/v1/xmlrpc.php'

2.API对应的key为：登陆testlink后点击上方个人账号进入个人中心，新页面点击 '生成新的秘钥'，使用该key替换掉main文件中的key值

3.father_id为目标用例集ID，可通过在testlink用例管理界面选取用例集，然后点击右键获取APIID

4.project_id为目标项目ID,可以根据日志显示ID进行选择

5.模板Excel中作者列必须与登陆用户名一致，否则上传时会引发鉴权或数据统计问题

6.模板Excel需放在testCase目录下，不建议修改模板Excel的文件名

7.为了直观的体现用例步骤和对应的期望结果，建议在步骤前加上编号。（尽管导入到testlink后会自带编号）

8.执行upload_cases.py

#### 将testlink上用例集中的用例导出成excel格式(download_single_test_suite.py）：


 1. API对应的URL为：url ='https://testlink.xsky.com/lib/api/xmlrpc/v1/xmlrpc.php'

 2. API对应的key为：登陆testlink后点击上方个人账号进入个人中心，新页面点击 '生成新的秘钥'，使用该key替换掉main文件中的key值

 3. father_id为目标用例集ID，可通过在testlink用例管理界面选取用例集，然后点击右键获取APIID

 4.执行download_single_test_suite.py
 
### 将testlink上的多个用例集中的用例导出成excel格式(download_multi_suites.py）


 1. API对应的URL为：url ='https://testlink.xsky.com/lib/api/xmlrpc/v1/xmlrpc.php'

 2. API对应的key为：登陆testlink后点击上方个人账号进入个人中心，新页面点击 '生成新的秘钥'，使用该key替换掉main文件中的key值

 3. father_id为目标用例集ID，可通过在testlink用例管理界面选取用例集，然后点击右键获取APIID

 4.执行download_multi_suites.py, 输入不同的用例集ID，ID之间用英文模式下的逗号分隔

#### 将Jira用例导入到testlink(XML2Excel.py）

1.目前只支持单独用例的导入

2.选取jira上的某个用例，导出为xml格式

3.选择将xml文件的<rss version="0.92">...</rss>,另存为本地的xml_test.xml.路径保持和脚本所在路径平行。支持修改文件名，同时要记住修改XML2Excel.py脚本中main方法的xml文件名

4.为了导入方便，执行XML2Excel.py时，需要输入testlink的登录用户名，保持和upload_cases.py的配置一致。脚本执行完成后，会生成以用户名命令的excel文件

5.打开upload_cases.py，修改main方法中的file_name为刚刚导出的excel文件

6.执行upload_cases.py上传用例

#### 将Jira单个用例逐个导入到testlink(XML2Excel_OneByONe.py）

1.每次只能导入一个用例，但是所有的用例都保持在一个excel文件中

2.一次批量导入多个单独的用例到testlink用例集中。如果用例是不同模块的，需要手动调整到对应的目录下

3.选取jira上的某个用例，导出为xml格式

4.选择将xml文件的<rss version="0.92">...</rss>,另存为本地的xml_test.xml.路径保持和脚本所在路径平行。支持修改文件名，同时要记住修改XML2Excel.py脚本中main方法的xml文件名

5.为了导入方便，执行XML2Excel.py时，需要输入testlink的登录用户名，保持和upload_cases.py的配置一致。脚本执行完成后，会生成以用户名命令的excel文件

6.打开upload_cases.py，修改main方法中的file_name为刚刚导出的excel文件

7.执行upload_cases.py上传用例

#### 将Jira多个用例导入到testlink(XML2Excel_MultiCases.py）

1.通过在jira上根据关键字查找到的所有用例，然后导出成xml 格式，再根据xml解析成excel格式，导入到testlink

2.选择将xml文件的<rss version="0.92">...</rss>,另存为本地的xml_test.xml.路径保持和脚本所在路径平行。支持修改文件名，同时要记住修改XML2Excel.py脚本中main方法的xml文件名

3.为了导入方便，执行XML2Excel.py时，需要输入testlink的登录用户名，保持和upload_cases.py的配置一致。脚本执行完成后，会生成以用户名命令的excel文件

4.如果用例步骤中，有带'< >'字符，则在解析该步骤的时候会报错：提示没有结束符。

5.如果用例步骤中，有带超链接 ' <a href=xxx a/ > '，该步骤在解析时也也会报错。需要收到修改步骤后提交。

6.打开upload_cases.py，修改main方法中的file_name为刚刚导出的excel文件

7.执行upload_cases.py上传用例

