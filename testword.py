from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

# 模型文件
MODULE_FILE='./static/upload/output.model'
# 上传的文件
UPLOAD_FILE='./static/upload/zhinput1.txt'
# 分词文件
PSEG_FILE='./static/upload/output.txt'

model=Word2Vec(LineSentence(PSEG_FILE),size=4,window=5,min_count=100)
model.save(MODULE_FILE)
