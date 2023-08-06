#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-3-4'
"""

from collections import OrderedDict

from vibora import Vibora, Request
from vibora.responses import JsonResponse


class Api(object):

    def __init__(self, fields, routing, predict, app=Vibora()):
        self.fields = fields
        self.app = app
        self.predict = predict
        self.app.route(routing, methods=['POST'])(self.home)

    async def home(self, request: Request):
        request = await request.stream.read()
        input = OrderedDict()
        output = OrderedDict()

        try:
            request = eval(request)
        except Exception as e:
            output['Request error'] = str(e)

        try:
            for field in self.fields:
                input[field] = request.get(field)
            output['Probability'] = self.predict(*input.values())
        except Exception as e:
            output['Predict error'] = str(e)
            output['Probability'] = 0
        finally:
            output['Fields'] = self.fields
            output['Request'] = request

        return JsonResponse(output)


if __name__ == '__main__':
    import jieba

    pred1 = lambda x, y: x + y
    pred2 = lambda x, y: x - y

    api = Api(['feat1', 'feat2'], '/post1', pred1)
    api = Api(['feat1', 'feat2'], '/post2', pred2, app=api.app)
    api = Api(['text'], '/post3', jieba.lcut, app=api.app)
    api.app.run()
