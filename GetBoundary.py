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

import json
import xml.etree.cElementTree as ET
import arcpy
import os
import GetUrl

# Lines in GeoJson format
lineTemplate = '{"displayFieldName":"","fieldAliases":{"FID":"FID","Id":"Id"},"geometryType":"esriGeometryPolyline","spatialReference":{"wkid":4326,"latestWkid":4326},"fields":[' \
               '{"name":"FID","type":"esriFieldTypeOID","alias":"FID"},' \
               '{"name":"Id","type":"esriFieldTypeInteger","alias":"Id"},' \
               '{"name":"relationID","type":"esriFieldTypeString","alias":"relationID","length":50},' \
               '{"name":"wayID","type":"esriFieldTypeString","alias":"wayID","length":50},' \
               '{"name":"name","type":"esriFieldTypeString","alias":"name","length":50},' \
               '{"name":"name_zh","type":"esriFieldTypeString","alias":"name_zh","length":50}],' \
               '"features":[{"attributes":{"FID":0,"Id":0,"name":"first"},"geometry":{"paths":[[]]}}]}'

#
def getBoundaryLine(boundary, Path, objectName, extra=""):
    boundarys = json.loads(lineTemplate)
    boundarys['features'] = []
    i = 0
    for wayID in boundary:

        wayXML = GetUrl.getUrl(wayID)
        if (wayXML == ""): continue
        wayTree = ET.fromstring(wayXML)
        wayNode = []
        nodes = {}

        # Initial boundarys list
        boundarys['features'].append({})
        boundarys['features'][i]['attributes'] = ({})
        boundarys['features'][i]['attributes']['FID'] = str(i)
        boundarys['features'][i]['attributes']['wayID'] = str(wayID)
        boundarys['features'][i]['geometry'] = ({})
        boundarys['features'][i]['geometry']['paths'] = []

        # Get lon & lat of all nodes
        for node in wayTree.findall('node'):
            nodes[node.get('id')] = [float(node.get('lon')), float(node.get('lat'))]

        # Get the order of nodes in way
        for nd in wayTree.find('way').findall('nd'):
            wayNode.append(nodes[nd.get('ref')])

        boundarys['features'][i]['geometry']['paths'].append(wayNode)

        i = i + 1

    # write boundary in Json
    jsObj = json.dumps(boundarys)
    fileObject = open(Path + objectName + extra + '.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()

    if (os.path.exists(Path + objectName + extra + '.shp') == False):
        arcpy.JSONToFeatures_conversion(in_json_file=objectName + extra + '.json',
                                        out_features=objectName + extra + '.shp')
    if (os.path.exists(Path + objectName + extra + '_polygon.shp') == False):
        print(Path + objectName + extra + '_polygon.shp')
        arcpy.FeatureToPolygon_management(in_features=objectName + extra + '.shp',
                                          out_feature_class=objectName + extra + '_polygon.shp')

#
def getBoundary(boundary, Path, boundary_inner, parentInfo):
    objectInformation = parentInfo[len(parentInfo)-1]
    objectID = objectInformation[0]
    objectName = objectInformation[1].replace("_", " ").replace(".", " ").replace("/", " ").replace("\'", " ").replace(",", " ").replace("-", " ").replace("(", "").replace(")", "") + "_" + objectID
    adminLevel = objectInformation[3]

    arcpy.env.workspace = Path

    resultPath = "result/"
    if (adminLevel != ''):
        resultPath = resultPath + adminLevel + "/"
    if (os.path.exists(Path + resultPath) == False):
        os.makedirs(Path + resultPath)

    if (boundary_inner!=[]):
        getBoundaryLine(boundary, Path, objectName, "outer")
        getBoundaryLine(boundary_inner, Path, objectName, "inner")
        # clip the boundary with the inner boundary
        if (os.path.exists(Path + resultPath + objectName + '.shp') == False):
            arcpy.Erase_analysis(in_features = objectName + 'outer_polygon.shp',
                                 erase_features = objectName + 'inner_polygon.shp',
                                 out_feature_class = resultPath + objectName + '.shp')
    else:
        getBoundaryLine(boundary, Path, objectName)
        if (os.path.exists(Path + resultPath + objectName + '.shp') == False):
            arcpy.CopyFeatures_management(in_features = objectName + '_polygon.shp',
                                          out_feature_class = resultPath + objectName + '.shp')

    arcpy.env.workspace = Path + resultPath
    for info in parentInfo:
        arcpy.CalculateField_management(in_table=objectName + '.shp', field="Id", expression=str(objectID))
        arcpy.AddField_management(in_table=objectName + '.shp', field_name="L"+info[3]+"_ID", field_type="TEXT")
        arcpy.CalculateField_management(in_table=objectName + '.shp', field="L"+info[3]+"_ID",
                                        expression=str('"' + info[0].encode('utf8') + '"'))
        arcpy.AddField_management(in_table=objectName + '.shp', field_name="L"+info[3]+"_name", field_type="TEXT")
        arcpy.CalculateField_management(in_table=objectName + '.shp', field="L"+info[3]+"_name",
                                        expression=str('"' + info[1].encode('utf8') + '"'))
        arcpy.AddField_management(in_table=objectName + '.shp', field_name="L"+info[3]+"_nameZh", field_type="TEXT")
        arcpy.CalculateField_management(in_table=objectName + '.shp', field="L"+info[3]+"_nameZh",
                                        expression=str('"' + info[2].encode('utf8') + '"'))

