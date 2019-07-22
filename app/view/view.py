import flask
from flask import request,Blueprint,render_template,Response,flash, redirect, url_for
from config import *
from app import api
import _thread
import os
from app.utilities.utilities import logger

@api.route("/searchindex")
def showSearch():
	return render_template("search.html")
@api.route("/trainindex")
def showTrain():
	return render_template("train.html")

import glob
@api.route("/downloadindex")
def showDownload():
	filenames=[]
	for filename in glob.glob(DOWNLOAD_FOLDER+"/*.[c,t][s,x][v,t]"):
		filenames.append(filename.rsplit('/',1)[1])
	return render_template("download.html",filenames=filenames)


from gensim.models import Word2Vec
@api.route("/searchResult", methods=["POST"])
def searchSimilarWord():
	inputword = request.form['inputword']
	en_wiki_model = Word2Vec.load(MODULE_FILE)
	res = en_wiki_model.wv.most_similar(inputword)
	str=[]
	for i in res:
		str.append(i[0])
	return render_template("search.html",results=str)

@api.route("/trainModule", methods=["POST","GET"])
def trainModule():
	print('start trainModule')
	_thread.start_new_thread(TrainModel, ("",""))
	return render_template('train.html')
	
@api.route("/")
def index():
	return redirect(url_for('robot.showSearch'))

	

# 检查文件类型是否合法
def allowed_file(filename):
    # 判断文件的扩展名是否在配置项ALLOWED_EXTENSIONS中
	# rsplit('.',1),以'.'为分隔符，从右往左分割一次
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


from werkzeug import secure_filename
@api.route("/Upload", methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		file=request.files['file']
		if file and allowed_file(file.filename):
			filename=secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER,UPLOAD_FILE.rsplit(r'/',1)[1]))
			_thread.start_new_thread(cutWords, ("",""))
			flash("上传成功")
			_thread.start_new_thread(classifyWords, ("",""))
			return render_template('train.html')
		else:
			flash("上传失败")
			return render_template('train.html')
	else:
		return render_template('train.html')

		

from flask import send_from_directory
@api.route("/download",methods=["POST","GET"])
@api.route("/download/<file>",methods=["POST","GET"])
def downloadFile(file=''):
	if file == '':
		return """
		<h1>暂未实现</h1>
		<form role="form" class="form-inline" action="/downloadindex" method="GET">
		<input type="submit" class="btn btn-primary" value="返回" />
		</form>
		"""
	else:
		return send_from_directory(classficationPath.rsplit('/',1)[0],file, as_attachment=True)
#生成器方式浏览文件内容
#	def generate():
#		with open("./static/upload/output.txt","rb",) as f:
#			line = f.readline()
#			yield line
#			while line:
#				line=f.readline()
#				yield line
#	return Response(generate(), mimetype='text')

#在浏览器中浏览文件
#	return send_from_directory(app.config['UPLOAD_FOLDER'],"output.txt")
		
	
import jieba
import jieba.analyse
import jieba.posseg as pseg
import codecs,sys
import multiprocessing
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def TrainModel(arg1,arg2):
	print('start trainModule thread')
	model=Word2Vec(LineSentence(PSEG_FILE),size=400,window=5,min_count=5)
	model.save(MODULE_FILE)
	model.wv.save_word2vec_format(VECTOR_FILE,binary=False)
	if os.path.exists(MODULE_FILE):
		print('训练成功')
	else:
		print('训练失败')


def cutWords(arg1,arg2):
	logger.info('cutwords start')
	#分词
	f=codecs.open(UPLOAD_FILE,'rb')
	target = codecs.open(PSEG_FILE,'w',encoding='utf-8')
	line_num=1
	line = f.readline()
	while line:
		line_seg = ''.join(jieba.cut(line))
		target.writelines(line_seg)
		line = f.readline()
	f.close()
	target.close()
	logger.info('cutwords finished')
	#建模
	#model=Word2Vec(LineSentence(PSEG_FILE),size=400,window=5,min_count=5)
	#model.save(MODULE_FILE)
	#model.wv.save_word2vec_format(VECTOR_FILE,binary=False)


def wordsInDic(dictSrc,dictRt):
	#词性分类
	category={
    'n':'名词',
    't':'时间词',
    's':'处所词',
    'b':'区别词',
    'z':'状态词',
    'a':'形容词',
    'v':'动词',
    'r':'代词',
    'm':'数词',
    'q':'量词',
    'd':'副词',
    'p':'介词',
    'c':'连词'
	}
	for word,flag in dictSrc:
		gkey=''
		for key in category:
			if key in flag:
				gkey=key
				break
		cnCategory=""
		if gkey in category:
			cnCategory=category[gkey]
		if cnCategory in dictRt and len(cnCategory)!=0:
			dictRt[cnCategory].add(word)
		elif len(cnCategory)!=0:
			dictRt[cnCategory]={word}

import jieba.posseg as pseg
import codecs,sys
import csv


#@api.route("/classifyWords", methods=['GET','POST'])
def classifyWords(arg1,arg2):
	logger.info('classifyWords start')
	dictRt={}
	with open(UPLOAD_FILE,"rb") as f:
		index=0
		for line in f:
			print(++index)
			dictSrc=pseg.cut(line)
			wordsInDic(dictSrc,dictRt)
	print("read finished")
	with open(classficationPath,'a+') as f:
		csv_write = csv.writer(f)
		#写入
		for item in dictRt.items():
			data_row = []
			data_row.append(item[0])
			content=""
			for str in item[1]:
				content+=str
				content+=","
			data_row.append(content)
			data_row.append(len(item[1]))
			csv_write.writerow(data_row)
	logger.info('classifyWords finished')
	