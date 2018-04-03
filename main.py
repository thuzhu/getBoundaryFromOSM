# -*- coding:utf-8 -*-
# =========================  Get OpenStreetMap Boundary  =============================
#   Scrape administrative divisions boundary data from http://www.openstreetmap.org/
#                     Components: GetSubarea.py, GetBoundary.py
#                 Packages: os, xml, urllib2, pypinyin, json, arcpy
#
#                           Version: 1.0.1 (2018-03-01)
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

# ====================================================================================
#                       --- UDF: modify the objectID below ---
#  the id could be found in the url, such as:
#      (Guangdong Province) https://www.openstreetmap.org/relation/911844
#  so the id is 911894.
#  * It should be noticed that the type must be RELATION
objectID = '912940'     # relationID
name = 'Beijing'          # name of corresponding country or region
Path = "D:/Project/" + name + "/"       # output path
#=====================================================================================

import os
import GetSubarea

if (os.path.exists(Path) == False):
    os.makedirs(Path)

parentInfo = []

GetSubarea.getSubarea(objectID, Path, parentInfo)
