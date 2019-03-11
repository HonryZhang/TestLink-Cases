#!/usr/bin/python
# _*_ coding:utf-8 _*_

#author:Hongrui
#date: 2019/02/11

import os,sys
import testlink
import xlrd
import pdb
from Log_util import Logger
reload(sys)
sys.setdefaultencoding('utf-8')

log = Logger().console_log(os.path.basename(__file__))


#获取testlink中所有project的信息
def getProject_info():
    project_info = {}
    projects = tls.getProjects()
    for project in projects:
        project_info[project['name']] = project['id']

#    print project_info
    return project_info

#获取testlink中所有project的ID
def getProject_id():
    project_ids = []
    projects = tls.getProjects()
    for project in projects:
        project_ids.append(project['id'])

#    print project_ids
    return project_ids

#获取指定用例集ID下的用例集信息

def get_suites(suite_id):

    try:
        suites = tls.getTestSuiteByID(suite_id)
#        print suites
        log.info(u'指定的用例集名称为：' + suites['name'].encode('utf-8'))
        return suites
    except testlink.testlinkerrors.TLResponseError as e:
        log.warning(str(e).split('\n')[1].encode('utf-8'))
        log.warning(str(e).split('\n')[0].encode('utf-8'))
        sys.exit()


#根据指定的用例属性，将对应的编号保存到testlink
def format_info(cdata):
    types = {
        u'低':1,
        u'中':2,
        u'高':3,
        u'自动':2,
        u'手动':1
    }

    return types.get(cdata)


#将用例上传到testlink中
def upload_created_cases(project_id,father_id,test_file_name):
    upload_success = 0
    upload_fail = 0

    case_names = []
    for data in tls.getTestCasesForTestSuite(father_id, True, 'full'):
        case_names.append(data['name'])

    if project_id not in getProject_id():
        log.error(u'指定的项目不存在，请确认项目ID是否正确')
        sys.exit()

    if not get_suites(father_id):
        log.error(u'指定的用例集不存在，请确认ID是否正确')
        #print 'test suite not exist'
        sys.exit()

    log.info(u'开始读取Excel中的用例数据')
    test_cases = readExcel(os.path.join('testCase',test_file_name))
    log.info(u'读取数据完毕，开始解析数据')

    for test_case in test_cases:
        log.info(u'导入用例--%s'%test_case[0])
        if test_case[0] == '':
            log.error(u'用例名不能为空,请重新输入')
            sys.exit()
        if test_case[0] in case_names:
            log.error(u'用例集中已经存在相同的用例名，请重新检查')
            upload_fail += 1
            continue
        if test_case[1] == '':
            log.warning(u'用例<%s>的摘要信息为空，将其设置为无'%(test_case[0]))
            test_case[1] =u'无'
        if test_case[6] =='':
            log.warning(u'用例<%s>的重要性信息为空，将其设置为高'%(test_case[0]))
            test_case[6] = u'高'

        case_data = {
        'title':test_case[0],
        'summary':test_case[1],
        'preconditions':test_case[2],
        'step': zip(test_case[3].split('\n'),test_case[4].split('\n')),
        'automation':format_info(test_case[5]),
        'importance':format_info(test_case[6]),
        'authorlogin':test_case[7]
        }
        # print case_data['title'].encode('utf-8')
        # print case_data['summary'].encode('utf-8')
        # print case_data['preconditions'].encode('utf-8')
        # for i in range(len(case_data['step'])):
        #     print case_data['step'][i][0].encode('utf-8'),case_data['step'][i][1].encode('utf-8')
        # print case_data['authorlogin'].encode('utf-8')

        #将用例导入到testlink中

        if import_testlink_cases(project_id,father_id,case_data):
            upload_success += 1
        else:
            upload_fail += 1

    total = upload_fail + upload_success
    log.info(u'本次操作共提交%d条数据，成功导入%d条，失败%d条' % (total, upload_success, upload_fail))



#读取excel表信息
def readExcel(file_path):
    #将所有的用例保存到一个列表中
    case_list = []
    #打开并读取excel
    try:
        book = xlrd.open_workbook(file_path)
    except Exception as error:
        log.error(u'路径不存在或者打开excel失败:'+str(error))
        sys.exit()
    else:
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows
        log.info(u'指定Excel文档中总共有%d条用例'%(rows-1))
        for i in range(rows):
            if i!=0:
                case_list.append((sheet.row_values(i)))
    return case_list


#根据从excel中读取到的数据，转换成测试用例
def import_testlink_cases(project_id,suites_id,data):
#    print data['authorlogin']
    log.info(u'testlink当前登录用户为：'+data['authorlogin'])


    # if data['importance']not in [1,2,3]:
    #     log.warning('用户未设置用例<%s>的重要性，默认为3'%(data['title']))
    #     data['important']=3
    # if data['summary']=='':
    #     log.warning('用户未设置用例<%s>的摘要信息，默认为无'%(data['title']))
    #     data['summary']='无'

    for i in range(0,len(data['step'])):
        tls.appendStep(data['step'][i][0],data['step'][i][1],data['automation'])
    log.info(u'解析用例数据完毕，开始导入用例')
    try:
        tls.createTestCase(data['title'],suites_id,project_id,data['authorlogin'],data['summary'],preconditions = data['preconditions'],importance = data['importance'],execution_type = '2')

    except Exception as e:
        log.error(u'导入用例<%s>失败,'%(data['title'])+ u'失败原因：'+ str(e))
        return False
    else:
        log.info(u'导入用例<%s>成功'%(data['title']))
        return True



if __name__ == "__main__":
    url = 'http://10.255.101.237/lib/api/xmlrpc/v1/xmlrpc.php'

    key = '0cccaff364e5ccc988eb7d72561aa49a'
    #pdb.set_trace()
    tls = testlink.TestlinkAPIClient(url, key)
    project_info = getProject_info()
    for k,v in project_info.items():
        log.info('项目名称为：%s'%k + ',' + '对应的项目ID为：%s'%str(v))
        #print '项目名称为：%s'%k+','+'对应的项目ID为：%s'%str(v)
    #father_id = '4'
    project_id = raw_input('\n'+ u'请输入项目ID：')
    father_id = raw_input('\n'+ u'请输入测试用例集ID：')
    #project_id = '1'
    #file_name ='testCase_Example.xlsx'
    file_name = 'hongrui.xlsx'
    log.info(u'开始执行脚本')

    upload_created_cases(project_id,father_id,file_name)
