# -*- coding: utf-8 -*-
from __future__ import division # 使得除法获得小数
import os.path # 获取文件名
from sys import exc_info # 报错提示
from traceback import print_tb # 错误截取
from PDFlib.PDFlib import *
from GDAL.readShapefile import *
# 定制选项
# 创建 PDFlib 和 Shapefile 对象
# 填写生成的PDF名称
Thor = PDFlib()# 拔起树根然后出发吧!
# pathNameList = ['F:\\PYX\\data\\node.shp','F:\\PYX\\data\\road_1.shp']
pathNameList = ['D:\\GIS数据\\china\\China.shp']
shpList = []
for a in range(len(pathNameList)):
    shpList.append(Shapefile(pathNameList[a]))
# ...
documentName = "hello.pdf"
pageX = 1000 # 页面宽度
pageY = 1000 # 页面高度
###############################################################################################
"""画图函数
    Requires:
        类型,数据列表,X轴放缩,Y轴放缩
"""
def painter(typeName,data,scaleX,scaleY):
    if typeName == 'Point':
        Thor.setcolor("fill", "rgb", 0.0, 0.85, 0.85, 0.0)
        Thor.circle(data[0] * scaleX, data[1] * scaleY,5)
        Thor.fill()
    elif typeName == 'LineString':
        Thor.setcolor("stroke", "rgb", 0.0, 0.5, 0.5, 0.0)
        Thor.moveto(data[0][0] * scaleX, data[0][1] * scaleY)
        for a in range(1,len(data)): # 第一个已经设置过了
            Thor.lineto(data[a][0] * scaleX, data[a][1] * scaleY)
        Thor.stroke()
    elif typeName == 'Polygon': # 尚未对凹多边形进行处理 TODO
        polygon = data # 取出一个多边形
        outerBoundary = polygon[0] # 取出多边形的外边界
        pointsNumber = len(outerBoundary) # 边界点个数
        lastPoint = outerBoundary[pointsNumber - 1]# 最后一个点
        path = -1
        path = Thor.add_path_point(path, lastPoint[0] * scaleX,
                    lastPoint[1] * scaleY, 'move', 'name=base')
        for pos in outerBoundary:
            path = Thor.add_path_point(path, pos[0] * scaleX, pos[1] * scaleY, 'line', '')

        Thor.draw_path(path, lastPoint[0] * scaleX, lastPoint[1] * scaleY,
            "stroke linewidth=1 fill fillcolor=Turquoise "
            "linecap=projecting attachmentpoint=base ")# 起始点闭合 选择开始点
    elif typeName == 'MultiPoint':
        for point in data:
            Thor.setcolor("fill", "rgb", 0.0, 0.85, 0.85, 0.0)
            Thor.circle(point[0] * scaleX, point[1] * scaleY,5)
            Thor.fill()
    elif typeName == 'MultiLineString':
        for line in data:
            Thor.setcolor("stroke", "rgb", 0.0, 0.5, 0.5, 0.0)
            Thor.moveto(line[0][0] * scaleX, line[0][1] * scaleY)
            for a in range(1,len(line)): # 第一个已经设置过了
                Thor.lineto(line[a][0] * scaleX, line[a][1] * scaleY)
            Thor.stroke()
    elif typeName == 'MultiPolygon':# 尚未对凹多边形进行处理 TODO
        for polygon in data:
            outerBoundary = polygon[0] # 取出多边形的外边界
            pointsNumber = len(outerBoundary) # 边界点个数
            lastPoint = outerBoundary[pointsNumber - 1]# 最后一个点
            path = -1
            path = Thor.add_path_point(path, lastPoint[0] * scaleX,
                        lastPoint[1] * scaleY, 'move', 'name=base')
            for pos in outerBoundary:
                path = Thor.add_path_point(path, pos[0] * scaleX, pos[1] * scaleY, 'line', '')

            Thor.draw_path(path, lastPoint[0] * scaleX, lastPoint[1] * scaleY,
                "stroke linewidth=1 fill fillcolor=Turquoise "
                "linecap=projecting attachmentpoint=base ")# 起始点闭合 选择开始点

            # for b in range(1,len(polygon)): # 开始挖出内边界

    else:
        print 'what the fuck?'
################################################################################################
try:
    # 设置异常处理,检查返回项
    Thor.set_option("errorpolicy=return")
    # 文档开始(设置图层默认打开 , 设置PDF版本) 添加新页面
    if Thor.begin_document(documentName, "openmode=layers compatibility=1.7ext3") == -1:
        raise Exception("Error: " + Thor.get_errmsg())
#########################
#Step1 遍历一遍 shpList ,获取最大区间 (假设只按照经纬度来进行度量 TODO)
    maxRangeList = [1000,-1000,1000,-1000]
    for a in range(len(shpList)):
        maxRangeList[0] = min(maxRangeList[0], shpList[a].getMapInfo()[1][0])
        maxRangeList[1] = max(maxRangeList[1], shpList[a].getMapInfo()[1][1])
        maxRangeList[2] = min(maxRangeList[2], shpList[a].getMapInfo()[1][2])
        maxRangeList[3] = max(maxRangeList[3], shpList[a].getMapInfo()[1][3])
#Step2 设置PDF的空间位置信息 (作用于PDF的地理空间位置工具)
    # 设置wkt信息 (这里默认使用第一个shp的wkt信息 TODO)
    georefsystem = "worldsystem={type=geographic wkt="
    georefsystem += shpList[0].getMapInfo()[0].ExportToWkt()
    # 单位展示
    georefsystem += "} linearunit=M areaunit=SQM angularunit=degree"

    pageoptlist = "" # 地理数据选项列表
    pageoptlist += "viewports={{ georeference={"
    pageoptlist += georefsystem + " "
    # 设置四角位置的顺序
    pageoptlist += "mappoints={0 0  1 0  1 1  0 1} "
    # """
    # /*
    #  * The following can be used as a workaround for a problem with the
    #  * Avenza PDF Maps app on Android; otherwise the (almost) default
    #  * bounds values can be skipped:
    #  *
    #  * pageoptlist += "bounds={0.000001 0 0 1 1 1 1 0} "
    #  */
    # """
    pageoptlist += "worldpoints={"
    # 按照下左,下右,上右,上左的顺序填写
    pageoptlist += str(maxRangeList[2]) + " " + str(maxRangeList[0]) + " "
    pageoptlist += str(maxRangeList[2]) + " " + str(maxRangeList[1]) + " "
    pageoptlist += str(maxRangeList[3]) + " " + str(maxRangeList[1]) + " "
    pageoptlist += str(maxRangeList[3]) + " " +  str(maxRangeList[0]) + " "
    pageoptlist += "} } "
    # 设置显示地理坐标位置的范围信息
    pageoptlist += "boundingbox={0 0 "
    pageoptlist += str(pageX) + " " + str(pageY)
    pageoptlist += "} } }"

    Thor.begin_page_ext(pageX, pageY, pageoptlist)
#Step3 设置坐标原点以及缩放倍数
    scaleX = pageX / abs(maxRangeList[1] - maxRangeList[0])
    scaleY = pageY / abs(maxRangeList[3] - maxRangeList[2])
    Thor.translate(-maxRangeList[0] * scaleX, -maxRangeList[2] * scaleY) # 需要反方向移动,故设为负
#Step4 画图像
    for a in range(len(shpList)):
        geometryList = shpList[a].getGeometryInfo()
        # 图层, 以文件名作为图层名 (测试中文文件名 TODO)
        fileName = os.path.basename(pathNameList[a])
        layer = Thor.define_layer(fileName, "")
        Thor.begin_layer(layer)
        # 遍历要素 画图
        for b in range(len(geometryList)):
            painter(geometryList[b]['type'], geometryList[b]['coordinates'], scaleX, scaleY)
        Thor.end_layer()
###########################
    # 页面结束 文档结束
    Thor.end_page_ext("")
    Thor.end_document("")
# 错误处理
except PDFlibException:
    print("PDFlib exception occurred:\n[%d] %s: %s" %
	((Thor.get_errnum()), Thor.get_apiname(),  Thor.get_errmsg()))
    print_tb(exc_info()[2])

except Exception:
    print("Exception occurred: %s" % (exc_info()[0]))
    print_tb(exc_info()[2])

finally:
    Thor.delete()
    #这里添加shapefile对象的删除处理
    for a in shpList:
        a.delete()
