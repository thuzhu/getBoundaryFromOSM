# -*- coding:utf-8 -*-
# =========================        GetSubarea.py         =============================
#             An recursive function of structure analysis for subarea
#                        Part of GetOSMBoundary project
#
#                          Version: 1.0.1 (2018-03-01)
#                            Interpreter: Python 3.2
#                           Test platform: Windows 10
#
#                        Author: Zhu Deng, Master Student
#             (Department for Earth System Science, Tsinghua University)
#                           Website: http://zhudeng.top
#                    Contact Email: dengz16@mails.tsinghua.edu.cn
#
#                        Copyright: belongs to Dr.Bai's Lab
#             (Department for Earth System Science, Tsinghua University)
# ====================================================================================

import xml.etree.cElementTree as ET
import urllib2
import pypinyin
import os
import GetBoundary

# Constant value definition
URL = "http://www.openstreetmap.org/api/0.6/"

def getSubarea(subareaID, Path, parentInfo):
    objectID = subareaID
    objectInformation = [objectID, '', '', '']
    # Crawler object information, response in XML format
    attempts = 0
    success = False
    while attempts < 10 and not success:
        try:
            objectUrl = URL + "relation/" + objectID
            objectRequest = urllib2.Request(objectUrl)
            objectResponse = urllib2.urlopen(objectRequest)
            objectXML = objectResponse.read()
            success = True
        except:
            attempts += 1
            if attempts == 10:
                return
    # Parse the XML using ElementTree
    xmlTree = ET.fromstring(objectXML)

    ######################################
    # After analyzing the XML file, we found that the key information was stored in a children path
    # so we have to locate it first
    target = []
    for temp in xmlTree.findall('relation'):
        if (temp.get('id') == objectID):
            target = temp
    # extract [Attributes] (labeled as 'tag in node') of target
    name_ = 'noName'
    for label in target.findall('tag'):
        if (label.get('k') == 'name:en'):
            objectInformation[1] = label.get('v')
        if (label.get('k') == 'name:zh'):
            objectInformation[2] = label.get('v')
        if (label.get('k') == 'admin_level'):
            objectInformation[3] = label.get('v')
        if (label.get('k') == 'name'):
            name_ = label.get('v')

    if (objectInformation[2] == ''):
        if (isinstance(name_, unicode)):
            objectInformation[2] = name_
        else:
            objectInformation[2] = name_.decode("utf-8")
    if (objectInformation[1] == ''):
        objectInformation[1] = "".join(pypinyin.lazy_pinyin(objectInformation[2]))
    if (objectInformation[3] == ''):
        objectInformation[3] = "n"

    # record parent's information
    newParentInfo = parentInfo
    newParentInfo.append(objectInformation)

    # extract all [Boundary] (labeled as 'outer') ids of target object ###
    boundary = []
    boundary_inner = []
    # extract [Subareas] (labeled as 'subarea')
    subarea = []
    for temp in target.findall('member'):
        if (temp.get('role') == 'outer'):
            boundary.append(temp.get('ref'))
        if (temp.get('role') == 'inner'):
            boundary_inner.append(temp.get('ref'))
        if (temp.get('role') == 'subarea'):
            subarea.append(temp.get('ref'))

    if (subarea):
        for subAreaID in subarea:
            #print("in", newParentInfo)
            getSubarea(subAreaID, Path, newParentInfo)
            #print("out", newParentInfo)

    print("in", newParentInfo)

    if (boundary and os.path.exists(Path + "result/" + objectInformation[3] + "/" + objectInformation[1].replace("_", " ").replace(".", " ").replace("/", " ").replace("\'", " ").replace(",", " ").replace("-", " ").replace("(", "").replace(")", "") + '_' + objectInformation[0] + '.shp') == False):
        GetBoundary.getBoundary(boundary, Path, boundary_inner, parentInfo)

    parentInfo.pop()
