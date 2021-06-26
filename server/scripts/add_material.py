import sys
sys.path.append('../')
from app.models import MaterialModel

with open('../data/material.txt', 'r', encoding='utf8')as f:
    for line in f:
        topic, title, content, url = line.split('\t')
        content += '...'
        m = MaterialModel(topic, title, content, url)
        m.add_record()