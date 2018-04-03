# -*- coding:utf-8 -*-
# =========================        GetBoundary.py         =============================
#                  Generate shpfile of boundary in specific path
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

import urllib2

URL = "http://www.openstreetmap.org/api/0.6/"
#
def getUrl(objectID):
    objectUrl = URL + "way/" + str(objectID) + "/full"
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            objectRequest = urllib2.Request(objectUrl)
            objectResponse = urllib2.urlopen(objectRequest)
            objectXML = objectResponse.read()
            success = True
        except:
            attempts += 1
            if attempts == 3:
                return ""
    return objectXML
