<h1 align = "center">:rocket: RestfulApi :facepunch:</h1>

---
> 模型部署

## Usage
```python
import jieba
from restful_api import Api

pred1 = lambda x, y: x + y
pred2 = lambda x, y: x - y

api = Api(['feat1', 'feat2'], '/post1', pred1)
api = Api(['feat1', 'feat2'], '/post2', pred2, app=api.app)
api = Api(['text'], '/post3', jieba.lcut, app=api.app)
api.app.run()
```

## Test
```python
import requests
json = {'feat1': 1, 'feat2': 10}
requests.post('http://127.0.0.1:5000/post1', json=json).json()
requests.post('http://127.0.0.1:5000/post2', json=json).json()

# {'Probability': 11,
#  'Fields': ['feat1', 'feat2'],
#  'Request': {'feat1': 1, 'feat2': 10}}
# {'Probability': -9,
#  'Fields': ['feat1', 'feat2'],
#  'Request': {'feat1': 1, 'feat2': 10}}
 
json = {'text': '小米家还不错的公司'}
requests.post('http://127.0.0.1:5000/post3', json=json).json()

# {'Probability': ['小米', '家', '还', '不错', '的', '公司'],
#  'Fields': ['text'],
#  'Request': {'text': '小米家还不错的公司'}}
```