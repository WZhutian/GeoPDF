# -*- coding: utf-8 -*-
from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *
from GDAL.readShapefile import *
# 定制选项
# 创建 PDFlib 和 Shapefile 对象
# 填写生成的PDF名称
Thor = PDFlib()
Shp_List = []
Shp_List.append(Shapefile('F:\\PYX\\data\\node.shp'))
Shp_List.append(Shapefile('F:\\PYX\\data\\road_1.shp'))
documentName = "hello.pdf"

try:
    # 设置异常处理,检查返回项
    Thor.set_option("errorpolicy=return")
    # 文档开始(设置图层默认打开) 添加新页面
    if Thor.begin_document(documentName, "openmode=layers") == -1:
        raise Exception("Error: " + Thor.get_errmsg())
    Thor.begin_page_ext(595, 842, "")
    #缩放
    Thor.translate(100,100)
    Thor.scale(0.5,0.5)
    # 画线
    Thor.setcolor("stroke", "rgb", 0.0, 0.5, 0.5, 0.0)
    Thor.moveto(0, 0)
    Thor.lineto(200, 600)
    Thor.stroke()

    # 画点(圆)
    Thor.setcolor("fill", "rgb", 0.0, 0.85, 0.85, 0.0)
    Thor.circle(100,500,10)
    Thor.fill()

    # 画面(凸多边形)
    path = -1
    path = Thor.add_path_point(path,0,0,'line','name=base')
    path = Thor.add_path_point(path,100,0,'line','')
    path = Thor.add_path_point(path,200,-25,'line','')
    path = Thor.add_path_point(path,0,-25,'line','')
    path = Thor.add_path_point(path,0,0,'line','')

    Thor.draw_path(path, 200, 600,
        "stroke linewidth=3 fill fillcolor=Turquoise "
        "linecap=projecting attachmentpoint=base ")# 起始点闭合 选择开始点

    # 画面(凹多边形) TODO

    # 添加属性 TODO

    # 添加交互 TODO

    # 搜索字体
    font = Thor.load_font(u"宋体","unicode", "")
    if font == -1:
        raise PDFlibException("Error: " + Thor.get_errmsg())
    # 添加文字
    Thor.set_text_pos(50, 700)
    Thor.setfont(font, 24)
    Thor.show(u"Hello world!搜索")

    # 图层
    layer0 = Thor.define_layer(u"文字", "");
    Thor.begin_layer(layer0);
    Thor.end_layer();

    # 页面结束 文档结束
    Thor.end_page_ext("")
    Thor.end_document("")

# 错误处理 --------固定不动
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
    for a in Shp_List:
        a.delete()
