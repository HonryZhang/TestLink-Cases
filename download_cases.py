#!/usr/bin/python
# _*_ coding:utf-8 _*_

#author:Hongrui
#date: 2019/02/11

import os,copy,sys
import testlink
import xlrd
reload(sys)
sys.setdefaultencoding('utf-8')

from xlutils.copy import copy
from Log_util import Logger

log = Logger().console_log(os.path.basename(__file__))

#从testlink上导出指定的用例集，将数据保持到datas列表中
#father_id为用例集的APIID
#列表元素包括：用例名，摘要，预置条件，操作步骤，期望结果，重要性以及测试方式
def download_case():
    log.info(u'开始下载用例')

    suits_name = get_suites(father_id)['name']
    log.info(u'指定的用例集名称为：' + suits_name.encode('utf-8'))

    datas = []
    for data in tls.getTestCasesForTestSuite(father_id,True,'full'):
        actions = []
        expected_results = []
        case_name = data['name']
        summary = data['summary'].replace('<p>','').replace('</p>','')
        preconditions = data['preconditions'].replace('<p>','').replace('</p>','')
        importance = data['importance']
        execution_type = data['execution_type']
        author = data['author_id']

        for i in range(len(data['steps'])):
            step_number = data['steps'][i]['step_number']
            actions.append(step_number+'.'+data['steps'][i]['actions'].replace('<p>','').replace('</p>',''))
            expected_result = data['steps'][i]['expected_results']
            if expected_result == '':
                expected_results.append(expected_result)
            else:
                expected_results.append(step_number+'.'+expected_result.replace('<p>','').replace('</p>',''))
        datas.append((case_name,preconditions,'\n'.join(actions),'\n'.join(expected_results),execution_type,author,importance,summary))

    log.info(u'下载数据完毕，开始执行格式转换')
    save_suites(os.path.join('testCase','download_template.xls'),datas,father_id)


#将datas中的数据解析并保持到excel中
def save_suites(file_path,datas,father_id):
    #获取当前用例集的名字
    suits_name = get_suites(father_id)['name']

    #读取excel模版
    book = xlrd.open_workbook(file_path,formatting_info=True)
    #复制读取的excel
    new_book = copy(book)

    #读取复制的excel的第一个sheet
    sheet = new_book.get_sheet(0)
    #默认第一行已经写好数据
    line_num = 1

#    print len(datas)
    #逐个读取datas列表的数据，并根据指定的行和列，写入到excel单元格中
    for i in range(0,len(datas)):
        case_name,preconditions,actions,expected_results,execution_type,author,importance,summary = datas[i]
        #print case_name,preconditions,actions,expected_results,execution_type,author,importance,summary

        sheet.write(line_num,0,u'%s'%case_name)
        sheet.write(line_num, 1, u'%s' % preconditions)
        sheet.write(line_num, 2, u'%s' % actions)
        sheet.write(line_num, 3, u'%s' % expected_results)
        sheet.write(line_num, 4, u'%s' % execution_type)
        sheet.write(line_num, 5, u'%s' % author)
        sheet.write(line_num, 6, u'%s' % importance)
        sheet.write(line_num, 7, u'%s' % summary)

        line_num += 1

    log.info(u'用例集_<%s>中总共有<%d>条用例'%(suits_name.encode('utf-8'),line_num-1))
    #设置导出的excel的保存目录
    report_path = os.path.abspath(os.path.join('download'))
#    print 'report_path is:',report_path
    if not os.path.exists(report_path):
        os.makedirs(report_path)


    # temp = os.path.abspath(os.path.join(report_path, suits_name))
    # print temp

    #将用例集下的所有用例保存为以用例集命名的xls文档中
    log.info(u'开始保存用例')
    try:
        new_book.save(os.path.abspath(os.path.join(report_path, suits_name+'.xls')))
    except Exception as e:
        log.error(u'保存用例失败',str(e))
        sys.exit()
    else:
        log.info(u'导出用例成功，存放地址为:'+ report_path)


def get_suites(suite_id):

    try:
        suites = tls.getTestSuiteByID(suite_id)
        return suites
    except testlink.testlinkerrors.TLResponseError as e:
#        print str(e).split('\n')[1]
        log.warning(str(e).split('\n')[1])
        log.warning(str(e).split('\n')[0])
        sys.exit()

if __name__=="__main__":
    url = 'http://10.255.101.237/testlink/lib/api/xmlrpc/v1/xmlrpc.php'

    #登陆testlink后点击上方个人账号进入个人中心，新页面点击 '生成新的秘钥'，使用该key替换掉upload_excel_data.py文件中的key值
    key = '57e7409a17606635ddf3619f99104247'
    tls = testlink.TestlinkAPIClient(url, key)
    #要下载的用例集的ID，可通过在testlink界面选取用例集，然后点击右键获取
    father_id = raw_input(u'请输入测试用例集ID：')
    #father_id = "4"
    log.info(u'开始执行脚本')
    download_case()