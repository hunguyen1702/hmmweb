import numpy as np
from urlparse import urlparse, parse_qs
from django.conf import settings
from sklearn.externals import joblib
import os


def is_query_request(request):
    if urlparse(request).query:
        return True
    return False


def get_uri_sequence(url):
    request = urlparse(url)
    uri_sequence = request.path.split('/')
    return uri_sequence


def transform_uri_sequence(uri_sequence):
    uri_labels = joblib.load(os.path.join(settings.MODEL_PATH, 'labelset/uri_labelset.pkl'))
    vector = []
    for i in uri_sequence:
        try:
            label = uri_labels.index(i)
        except ValueError:
            label = len(uri_labels) ** 2
        vector.append(label)
    return np.array(vector, dtype='int64')


def get_attr_sequence(url):
    request = urlparse(url)
    queries = request.query.split('&')
    attr_sequence = [entry.split('=')[0] for entry in queries]
    return attr_sequence


def tranform_attr_sequence(attr_sequence):
    attr_labels = joblib.load(os.path.join(settings.MODEL_PATH, 'labelset/attr_labelset.pkl'))
    vector = []
    for i in attr_sequence:
        try:
            label = attr_labels.index(i)
        except ValueError:
            label = len(attr_labels) ** 2
        vector.append(label)
    return np.array(vector, dtype='int64')


def get_value_sequence(url):
    request = urlparse(url)
    value_sequence = parse_qs(request.query)
    for i in value_sequence.keys():
        value_sequence[i] = value_sequence[i][0]
    return value_sequence


def tranform_value_sequence(value_sequence):
    vector = []
    for i in list(value_sequence):
        # i = i.decode('iso-8859-1')
        if i.isalpha():
            vector.append(0)
        elif i.isdigit():
            vector.append(99)
        else:
            vector.append(9999)
    return np.array(vector, dtype='int64')


def tranform_value_list(value_sequence):
    for i in value_sequence.keys():
        value_sequence[i] = tranform_value_sequence(value_sequence[i])
    return value_sequence


def score(sequence, model_file):
    model = joblib.load(model_file)
    return 2 ** model.score(np.column_stack([sequence]))


def is_anomalous(uri):
    v = get_uri_sequence(uri)
    v = transform_uri_sequence(v)
    model_dict = joblib.load(os.path.join(settings.MODEL_PATH, 'hmm_model_dict.pkl'))
    uri_score = score(v, os.path.join(settings.MODEL_PATH, model_dict['uri']['model_file']))
    if uri_score < model_dict['uri']['threshold']:
        return True
        #     score uri
    if is_query_request(uri):
        #         score query attribute
        v = get_attr_sequence(uri)
        v = tranform_attr_sequence(v)
        attr_score = score(v, os.path.join(settings.MODEL_PATH, model_dict['attribute']['model_file']))
        if attr_score < model_dict['attribute']['threshold']:
            return True
            #         score query attribute
            #         score query value by attribute
        v = get_value_sequence(uri)
        pv = False
        for key in v.keys():
            if key == 'id':
                if len(v[key]) > 1:
                    pv = True
                    break
                continue
            v[key] = tranform_value_sequence(v[key])
            value_score = score(v[key], os.path.join(settings.MODEL_PATH, 'value_model', model_dict[key]['model_file']))
            if value_score < model_dict[key]['threshold']:
                pv = True
                break
        return pv
        #         score query value by attribute
    else:
        return False
