# -*- coding: utf-8 -*-

import datetime
import json

def isDate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def printp(data):
	print json.dumps(data, indent=2, sort_keys=True)


def dict_merge(x, y):
	if x and not y:
		return x.copy()

	if y and not x:
		return y.copy()

	if not x and not y:
		return {}

	if x and y:
		z = x.copy()
		z.update(y)
		return z