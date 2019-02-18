#!/usr/bin/python
# _*_ coding:utf-8 _*_

from xml.etree import ElementTree as ET

import json
xml_file = '/Users/xsky/Downloads/xml_test.xml'
#root1 = ET.parse(xml_file)
# f = open('test.json','a')
# for ee in root1.getiterator('steps'):
#     tempDict = ee.attrib
#     for childnode in ee.getchildren():
#         tempDict[childnode.tag]=childnode.text
#
#     tempJson = json.dumps(tempDict)
#     print tempJson
#     test_json = json.loads(tempJson)
#     #print test_json['title']
#     f.write(tempJson+'\n')
# f.close()


    #获取xml文件
import xmltodict
xml_file = open(xml_file, 'r')
    #读取xml文件内容
xml_str = xml_file.read()
    #将读取的xml内容转为json
json = xmltodict.parse(xml_str)
print json