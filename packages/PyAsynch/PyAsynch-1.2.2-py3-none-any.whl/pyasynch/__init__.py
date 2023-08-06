import re


def serialize_address(endpoint_id, cluster_id, app_id):
    return 'pyasynch://{0}/{1}/{2}'.format(endpoint_id, cluster_id, app_id)


def deserialize_address(s: str):
    matched = re.match('^pyasynch\:\/\/(?P<endpoint_id>\S+)\/(?P<cluster_id>\S+)\/(?P<app_id>\S+)$', s)
    dic = matched.groupdict()
    return dic['endpoint_id'], dic['cluster_id'], dic['app_id']