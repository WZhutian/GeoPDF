# -*- coding:utf-8 -*-
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import json
class Shapefile(object):
    def __init__(self,path):
        #支持中文路径,使属性表字段支持中文
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","YES")
        gdal.SetConfigOption("SHAPE_ENCODING","")
        # #注册所有的驱动
        ogr.RegisterAll()
        #数据格式的驱动
        driver = ogr.GetDriverByName('ESRI Shapefile')
        self.ds = driver.Open(path)
        if self.ds is None:
            print u'文件打开失败'
            sys.exit(1)
        self.layer = self.ds.GetLayerByIndex() #获取图层
        self.geometrys = [] # 预先保存两个数组,只需要遍历一次要素
        self.attributes = []

    """获取要素的地理信息 以及获取要素的属性信息
    0.循环函数,只执行一次,保存到全局变量中
    1.Returns:
        返回一个字典{type:'类型',coordinates:[要素]}
        具体类型如下:
            Point 点:[x,y],[x,y]
            MultiPoint 多点: TODO
            LineString 线:[ [x,y],[x,y],[x,y] ]
            MultiLineString 多线: TODO
            Polygon 面:[ [[x,y],[x,y],[x,y]],[面要素2], ... ]
            MultiPolygon 多面:[ [[[x,y],[x,y],[x,y]]],[[[x,y],[x,y],[x,y]]], .... ]
    2.Returns:
        [['a','b','c'],[],[]]属性值列表
    """
    def _getFeaturesInfo(self):
        defn = self.layer.GetLayerDefn()
        fieldCount = defn.GetFieldCount() # 属性键的个数
        featureCount = self.layer.GetFeatureCount() #要素个数

        for a in range(featureCount):
            feature = self.layer.GetNextFeature() # 获取第一个要素
            fieldListTemp = []
            for index in range(fieldCount):
                if feature.IsFieldSet(index):
                    fieldListTemp.append(feature.GetFieldAsString(index))
            self.attributes.append(fieldListTemp)
            # 获取要素中的几何体
            geometry = feature.GetGeometryRef()
            # print geometry.ExportToJson()
            self.geometrys.append(json.loads(geometry.ExportToJson()))
            feature.Destroy()

    def getGeometryInfo(self):
        if len(self.geometrys)==0:
            self._getFeaturesInfo()
        return self.geometrys

    def getAttributeInfo(self):
        if len(self.attributes)==0:
            self._getFeaturesInfo()
        return self.attributes

    """获取属性表信息
    Returns:
        [属性键列表]
    """
    def getTableInfo(self):
        listOut = []
        defn = self.layer.GetLayerDefn()
        fieldCount = defn.GetFieldCount()
        for index in range(fieldCount):
            field = defn.GetFieldDefn(index)
            listOut.append(field.GetNameRef())
            # print '%s: %s(%d.%d)' % (oField.GetNameRef(),oField.GetFieldTypeName(oField.GetType()),oField.GetWidth(),oField.GetPrecision())
        return listOut

    """ 获取画幅信息
    Returns:
        [投影坐标系信息,(左,右,下,上)经纬度元组,要素类型]
    PS:要素类型:点1,线2,面3
    """
    def getMapInfo(self):
        return [self.layer.GetSpatialRef(),self.layer.GetExtent(),self.layer.GetGeomType()]
    # 清除工作
    def delete(self):
        self.ds.Destroy()

#执行测试区域
if __name__=='__main__':
    # shp = Shapefile('D:\\GIS数据\\china\\China.shp')
    shp = Shapefile('F:\\PYX\\data\\road_1.shp')
    # shp = Shapefile('F:\\PYX\\data\\node.shp')
    # shp.getFeaturesInfo()
    # print type(shp.getMapInfo()[0].ExportToWkt())
    # print dir(shp.getMapInfo()[0])
    # shp.getAttributeInfo()
    # print str(shp.getTableInfo()).decode('string_escape') #一种方法
    # print shp.getGeometryInfo()

    # print shp.getAttributeInfo()

    shp.delete()
