import jieba
from restful_api import Api

pred1 = lambda x, y: x + y
pred2 = lambda x, y: x - y

api = Api(['feat1', 'feat2'], '/post1', pred1)
api = Api(['feat1', 'feat2'], '/post2', pred2, app=api.app)
api = Api(['text'], '/post3', jieba.lcut, app=api.app)
api.app.run()