import ast
import datetime
import json
from numpy import loadtxt

from django.test import TestCase

# Create your tests here.


# def serialize_datetime(obj):
#     if isinstance(obj, datetime.datetime):
#         return obj.isoformat()
#     raise TypeError("Type not serializable")
#
#
# def returne_datetime(obj):
#     if isinstance(obj, datetime.datetime):
#         return obj.isoformat()
#     raise TypeError("Type not serializable")
#
# DATE_NOW = datetime.datetime.now()
# a = [[DATE_NOW], [25], ['AAA']]
# print(type(a))
# print(a)
# b = json.dumps(a, default=str)
# print(type(b))
# print(b)
# t = str(a)
# print('t', type(t))
# print('t', t)
# # tl = ast.literal_eval(t)
# tl = t.split("'")
# print('tl', tl)
#
#
# l = json.loads(b)
# print(type(l))
# print(l)
# ln = str(l[0][0])
# print('дата текстом ', ln)
# nl = datetime.datetime.strptime(ln, "%Y-%m-%d %H:%M:%S.%f")
# print(type(nl))
# print('nl ', nl)


a = "[[[12, \"11:00:00\", \"12:00:00\", 2], [14, \"15:30:00\", \"21:00:00\", 4]], [[13, \"11:00:00\", \"12:00:00\", 5], [15, \"15:30:00\", \"21:00:00\", 6]], []]"
b = json.loads(a)
print(b)
c = b[0][0][1]
print(type(c))
d = datetime.datetime.strptime(c, "%H:%M:%S").time()
print(d)
print(type(d))
