# coding : UTF-8

# 通过setuptools模块导入所需要的函数
from setuptools import setup,find_packages

setup(
	name = "liang-test",
	version = "0.2",
	author = "liangjingfu",
	url = "http://www.cnblogs.com/liangjingfu/",
	packages = find_packages("src"), 	# src就是模块的保存目录
	package_dir = {"":"src"},			# 告诉setuptools 包都在src下

	# 配置其他的文件的打包处理
	package_data = {
		"":["*.txt","*.info","*.properties"],
		"":["data/*.*"],
	},
	exclude = ["*.test","*.test.*","test.*","test"]
)
