import sys
sys.path.append('../')
from app.models import ArticleModel

with open('../data/article.txt', 'r', encoding='utf8')as f:
    for line in f:
        topic, title, content, count, url = line.split('\t')
        content += '...'
        a = ArticleModel(topic, title, content, url)
        a.add_record()