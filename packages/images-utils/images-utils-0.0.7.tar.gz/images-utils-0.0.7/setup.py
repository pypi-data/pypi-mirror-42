import setuptools


# with open("README.md", "r") as fh:
# 	long_description = fh.read()
long_description = 'images-utils'


setuptools.setup(
	name = "images-utils",
	version="0.0.7",
	auth="Huang Xu Hui",
	author_email="13250270761@163.com",
	description="images-utils has recognition function",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/suckmybigdick/flask-wechat-utils",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"setuptools==20.7.0",
		"Pillow",
		"numpy",
		"imutils",
		"opencv-python"
	],
)
