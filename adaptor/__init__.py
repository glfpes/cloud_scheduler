# -*- coding: utf-8 -*-

from oslib import loadables

CONF_CLOUD_LIST = [

    # user name or password or auth_key ?


    # cloud 1
    {
        'name': 'cloud_1',
        'type': 'openstack',
        'end_point': 'xx.xx.xx.xx/xxxx/xxxxx',
        'user_name': 'xxxx',
        'password': 'xxxxxxx',
    },

    # cloud 2
    {
        'name': 'cloud_2',
        'type': 'aliyun',
        'access_key': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'access_secret': 'xxxxxxxxxxxxxxxxxxxxxxx',
        'region_id': 'xxxxxxxxxxxxxxxxx',
    },

]

CONF_TYPE_CLS_MAP = {

    'openstack': 'OpenStackAdaptor',
    'aliyun': 'AliYunAdaptor',

}


class BaseAdaptor(object):
    """
    所有adaptor的基类
    """

    def __init__(self, config):
        raise NotImplementedError

    def get_cloud_state(self, context):
        """
        :param context: 暂未定义的预留参数，传入{}即可
        :return: 云的状态
        这个函数必须被重写
        """
        raise NotImplementedError()

    def create_instance(self, build_spec, context):
        """
        :param build_spec: 要创建的instance的参数
        :param context: 暂未定义的预留参数，传入{}即可
        :return: 云API返回的错误信息
        创建instance，这个函数必须被重写。如果没有错误信息，返回空字符串
        """
        raise NotImplementedError


class AdaptorHandler(loadables.BaseLoader):

    def __init__(self):
        super(AdaptorHandler, self).__init__(BaseAdaptor)

        self.adaptor_cls_map = {cls.__name__: cls for cls in self.all_adaptors()}
        self.type_cls_map = CONF_TYPE_CLS_MAP

        # 给每朵云创建一个adaptor并加入self.adaptors列表
        self.adaptors = {}
        for cloud in self._get_cloud_list():
            self.adaptors[cloud.get('name')] = self.adaptor_cls_map.get(self.type_cls_map.get(cloud.get('type')))(cloud)

    def get_all_cloud_state(self, context):
        """
        :param context: 暂未定义的预留参数，传入{}即可
        :return: 所有云当前状态的字典 {云名称: 状态}

        """
        return {cloud: self.adaptors.get(cloud).get_cloud_state() for cloud in self.adaptors}

    def create_instance(self, build_spec, context):
        """
        :param build_spec: 要创建的instance的参数
        :param context: 暂未定义的预留参数，传入{}即可
        :return: 错误信息
        """
        for cloud in self.adaptors:
            return {cloud: self.adaptors.get(cloud).create_instance(build_spec, context)}

    def _get_cloud_list(self):
        """
        read db
        读数据库
        """
        # todo: use db or configure file 这里改为读取数据库的操作
        return CONF_CLOUD_LIST

    def all_adaptors(self):
        """
        返回当前目录下的所有adaptor类型
        """
        return AdaptorHandler.get_all_classes()