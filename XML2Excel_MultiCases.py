#!/usr/bin/python
# _*_ coding:utf-8 _*_

#author:Hongrui
#date:2019/2/14

import sys,xlrd,json
from xlutils.copy import copy
#reload(sys)
#sys.setdefaultencoding('utf8')

import xmltodict,os,re

#去掉xml件中的部分html字符<p>,</p>,<br/>
def transfer_xml(xml_file):
    with open(xml_file,'r')as f:
        lines = f.readlines()
    with open(xml_file,'w')as f_w:
        pattern = re.compile(r'(<\d+)')
        for line in lines:
            if pattern.findall(line):
                for str in pattern.findall(line):
                    new_str = str.replace('<', '小于')
                    line = re.sub(pattern, new_str, line)
            if '<p>' or '</p>' in line:
                line = line.replace('<p>','').replace('</p>','')
            if '<br/>' in line:
                line = line.replace('<br/>','')
            if '<em>' or '</em>' in line:
                line = line.replace('<em>','').replace('</em>', '')
            if '<a href=' in line:
                line = line.replace('<a href=', '')
            if '</a>' in line:
                line = line.replace('</a>', '')
            if '<div' in line:
                line = line.replace('<div','div')
            if '<a class' in line:
                line = line.replace('<a class','class')
            if '</div>' in line:
                line = line.replace('</div>', '/div')
            # if '<span class=' in line:
            #     src = line.find('<span class=')
            #     dst = line.find('>')
            #     line = line.replace(line[src:dst+1], '')
            if '<span' in line:
                line = line.replace('<span', '')
            if '</span>' in line:
                line = line.replace('</span>', '')
            if '&jqlQuery=' in line:
                line = line.replace(line[line[0:line.find('&jqlQuery=')].rfind('<'):line[line.find('&jqlQuery='):].find('>')+line.find('&jqlQuery=') + 1], '')
            if '<bucket' in line:
                line = line.replace('<bucket','bucket')
            if '<索引池pool-name>' in line:
                line = line.replace('<索引池pool-name>','indexpool-name')
            if '<bucket id>_<对象名>' in line:
                line = line.replace('<bucket id>_<对象名>','bucket id_对象名')
            if '<del>'or '</del>' in line:
                line = line.replace('<del>','').replace('</del>','')
            if '&' in line:
                line = line.replace('&','or')
            if '<ip>' in line:
                line = line.replace('<ip>', 'ip')
            if '<\\' in line:
                line = line.replace('<\\', '')
            if '<DIR>' in line:
                line = line.replace('<DIR>','DIR')
            if '<网关' in line:
                line = line.replace('<网关','网关')
            if '<img' in line:
                line = line.replace('<img','img')
            if '<object_name>' in line:
                line = line.replace('<object_name>','object_name')
            if '<对象名>' in line:
                line = line.replace('<对象名>','对象名')
            if '<>' in line:
                line = line.replace('<>','大于小于符号')
            if '<ol>' or '</ol>' in line:
                line = line.replace('<ol>', '').replace('</ol>','')
            if '<li>' or '</li>' in line:
                line = line.replace('<li>', '').replace('</li>', '')
            f_w.write(line)
            #f_w.write(line.encode('utf-8'))
    new_file = xml_file
    return new_file

#将xml文件转换成json格式
def xml_2_json(file):
    #new_file = transfer_xml(xml_file)
    with open(file,'r')as xml:
        xml_string = xml.read()
    #xml.close()
    try:
        json_file = xmltodict.parse(xml_string)
        return json_file
    except Exception as e:
        print '\033[1;31m请检查用例对应的xml文件中是否包含\'<xxx\'或者\'<xxx>\'类似的字符串，如果存在，请将字符串前的\'<\'删除后再次执行.\033[0m'
        print 'Error:',e


#读取json文件，取出需要的数据，以元组的形式存放到datas列表中，方便后续扩展成多用例批量导入
def get_datas(xml_file):

    datas = []
    new_file = transfer_xml(xml_file)
    test = xml_2_json(new_file)
    #test = xml_2_json()
    #print json.dumps(test)
    total_cases = len(test['rss']['channel']['item'])
    print '\033[1;34m本次预计转换<%s>条用例，列表如下： \033[0m'%total_cases
    for i in range(len(test['rss']['channel']['item'])):
        case_name = test['rss']['channel']['item'][i]['title']
        case_name = ''.join(case_name.split())
        print case_name
        summary = test['rss']['channel']['item'][i]['summary']
        #print summary
        actions = []
        expected_results=[]
        steps_dict = test['rss']['channel']['item'][i]['customfields']['customfield'][1]
        #print steps_dict
        #if steps_dict.has_key('customfieldvalues'):
        if steps_dict.get('customfieldvalues'):
            steps = steps_dict['customfieldvalues']['steps']['step']
            # 如果用例只有一个步骤，则返回的是一个集合，不是列表，需要判断
            if isinstance(steps, dict):
                step_number = steps['index']
                action = steps['step']
                actions.append(step_number + '.' + action)
                expected_result = steps['result']
                expected_results.append(step_number + '.' + expected_result)
            elif isinstance(steps, list):
                for j in range(len(steps)):
                    ##print range(len(steps))
                    step_number = steps[j]['index']
                    action = ' '.join(steps[j]['step'].split())
                    actions.append(step_number + '.' + action)
                    expected_result = steps[j]['result']
                    if isinstance(expected_result, dict):
                        continue
                    if expected_result is None:
                        expected_result = ''
                        expected_results.append(expected_result)

                    else:
                        expected_result = ' '.join(expected_result.split())
                        expected_results.append(step_number + '.' + expected_result)
        else:
            #print u'\033[1;31m----Case:%s 居然没有用例步骤. Skip it!---- \033[0m' % (case_name)
            #total_cases -=1
            #continue
            actions = []
            expected_results=[]

        #print steps

        precondition = u'1.集群状态正常'+'\n'+u'2.UI登录正常'+u'3.已经创建好数据池和对象索引池'+u'4.已初始化对象存储'+u'5.已经创建至少1个数据池data_pool0和1个索引池index_pool0'

        execution_type =u'手动'
        importance = u'高'

        # actions = []
        # expected_results=[]
# # 如果用例只有一个步骤，则返回的是一个集合，不是列表，需要判断
#         if isinstance(steps, dict):
#             step_number = steps['index']
#             action = steps['step']
#             actions.append(step_number + '.' + action)
#             expected_result = steps['result']
#             expected_results.append(step_number + '.' + expected_result)
#         elif isinstance(steps, list):
#             for j in range(len(steps)):
#                 ##print range(len(steps))
#                 step_number = steps[j]['index']
#                 action = ' '.join(steps[j]['step'].split())
#                 actions.append(step_number + '.' + action)
#                 expected_result = steps[j]['result']
#                 if isinstance(expected_result, dict):
#                     continue
#                 if expected_result is None:
#                     expected_result = ''
#                     expected_results.append(expected_result)
#
#                 else:
#                     expected_result = ' '.join(expected_result.split())
#                     expected_results.append(step_number + '.' + expected_result)
#
    #将获取到的数据按元组形式存放到列表
        datas.append((case_name,summary,precondition,'\n'.join(actions),'\n'.join(expected_results),execution_type,importance))
    print '\033[1;34m本次实际转换<%s>条用例，请查看打印日志. \033[0m' % total_cases
    xml_to_xls(os.path.join('testCase', 'download_template.xls'), datas)


#读取datas列表中的元素，并按照列表对应的行列关系存入值
def xml_to_xls(file_path,datas):
    # 读取excel模版
    #book = xlrd.open_workbook(file_path, formatting_info=True)
    book = xlrd.open_workbook(file_path,formatting_info=True)
    # 复制读取的excel
    new_book = copy(book)

    # 读取复制的excel的第一个sheet
    sheet = new_book.get_sheet(0)
    # 默认第一行已经写好数据
    line_num = 1

    # print len(datas)
    # 逐个读取datas列表的数据，并根据指定的行和列，写入到excel单元格中
    # 目前只支持单个用例的转换，导入
    for i in range(0, len(datas)):
        case_name, summary, preconditions, actions, expected_results, execution_type, importance=datas[i]

        sheet.write(line_num, 0, u'%s' % case_name)
        sheet.write(line_num, 1, u'%s' % summary)
        sheet.write(line_num, 2, u'%s' % preconditions)
        sheet.write(line_num, 3, u'%s' % actions)
        sheet.write(line_num, 4, u'%s' % expected_results)
        sheet.write(line_num, 5, u'%s' % execution_type)
        sheet.write(line_num, 6, u'%s' % importance)
        sheet.write(line_num, 7, u'%s' % author)

        line_num += 1

    #log.info(u'用例集_<%s>中总共有<%d>条用例' % (suits_name.encode('utf-8'), line_num - 1))
    # 设置导出的excel的保存目录
    report_path = os.path.abspath(os.path.join('testCase'))
    #    print 'report_path is:',report_path
    if not os.path.exists(report_path):
        os.makedirs(report_path)

    # 将用例集下的所有用例保存为以login username命名的xls文档中
    #log.info(u'开始保存用例')
    try:
        new_book.save(os.path.abspath(os.path.join(report_path, author+'-null.xls')))
    except Exception as e:
        #log.error(u'保存用例失败', str(e))
        print e
        sys.exit()

    else:
        print '\033[1;32m转换用例成功,存放地址为:\033[0m'+os.path.join(report_path, author+'.xls')
        #print '\033[1;34m 本次实际转换%s条用例，请查看打印日志. \033[0m' % total_cases
        #log.info(u'导出用例成功，存放地址为:' + report_path)


if __name__=='__main__':
    xml_file = '/Users/xsky/Downloads/test_xml.xml'

    print '\033[5;31m用例转换前，请根据测试产品和测试集的实际情况，修改precondition字段的值（第128行)\033[0m'

    while True:
        response = raw_input('是否继续,默认为Y：(Y/N)-->')
        if response in ['Y','yes','y','']:
            author = 'hongrui'
            #author = raw_input('Testlink Login UserName:')
            get_datas(xml_file)
            break
        elif response in ['N','no','n','q']:
            print'\033[5;32m谢谢使用，请修改预置条件后再执行.\033[0m'
            sys.exit()
        else:
            print'\033[5;31m输入错误，请重新输入.\033[0m'
            continue
