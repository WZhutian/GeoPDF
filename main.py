# -*- coding: utf-8 -*-
from sys import exc_info
from traceback import print_tb
from PDFlib.PDFlib import *

# 创建 PDFlib 和 Shapefile 对象
Thor = PDFlib()

try:
    # 设置异常处理,检查返回项
    Thor.set_option("errorpolicy=return")
    # 文档开始(设置图层默认打开) 添加新页面
    if Thor.begin_document("hello.pdf", "openmode=layers") == -1:
        raise Exception("Error: " + Thor.get_errmsg())
    Thor.begin_page_ext(595, 842, "")
    # 搜索字体
    font = Thor.load_font(u"宋体","unicode", "")
    if font == -1:
        raise PDFlibException("Error: " + Thor.get_errmsg())

    # 定义图层
    layerRGB = Thor.define_layer(u"文字", "");
    Thor.begin_layer(layerRGB);
    # 添加文字
    Thor.set_text_pos(50, 700)
    Thor.setfont(font, 24)
    Thor.show(u"Hello world!搜索")
    # 图层结束
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
