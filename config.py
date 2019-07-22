#coding:utf8
# Flask配置项，调试模式
DEBUG = True
# Flask配置项，设置请求内容的大小限制，即限制了上传文件的大小
MAX_CONTENT_LENGTH = 500 * 1024 * 1024
# 本应用的配置项，设置上传文件存放的目录
UPLOAD_FOLDER = './static/upload'
# 本应用的配置项，设置允许上传的文件类型
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg'])
# 模型文件
MODULE_FILE='./static/upload/output.model'
# 上传的文件
UPLOAD_FILE='./static/upload/zhinput1.txt'
# 分词文件
PSEG_FILE='./static/upload/output.txt'
# 向量文件
VECTOR_FILE='./static/upload/output.vector'
# 词性分类结果文件
classficationPath="./static/download/classfication.csv"
# 下载文件
DOWNLOAD_FOLDER="./static/download"