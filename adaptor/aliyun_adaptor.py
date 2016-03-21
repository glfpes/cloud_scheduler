# -*- coding: utf-8 -*-
# Aliyun adaptor -- tianye

import json

from adaptor import BaseAdaptor

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
#from aliyunsdkecs.request.v20140526 import DescribeZonesRequest

# from aliyunsdkecs.request.v20140526 import StartInstanceRequest
# from aliyunsdkecs.request.v20140526 import StopInstanceRequest
# from aliyunsdkecs.request.v20140526 import RebootInstanceRequest
# from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
# from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
# from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest

class AliYunAdaptor(BaseAdaptor):
    ## 构造函数
    # @param AccessKey 字符串 AccessKey是访问阿里云API的凭证，此处传入AccessKey的ID
    # @param AccessSecret 字符串 AccessKey的口令
    # @param RegionId 字符串 区域ID
    def __int__(self, config):
        self.name = config.get('name')
        self.__clt = client.AcsClient(config.get('access_key'),
                                      config.get('access_secret'),
                                      config.get('region_id'))

    def create_instance(self, build_spec, context):
        self.createInstance(build_spec)

    def get_cloud_state(self, context):
        query_result = self.query()
        ret = {'name': self.name}

        raise Exception('Not finished yet')

        return ret




    ## 创建单个实例
    # @param build_spec 字典 {{'instance_name', instance_name}, {'instance_type', instance_type}, {'SecurityGroupId', SecurityGroupId}, {'image_id', image_id}}
    # @return 布尔 实例创建成功返回True，否则False
    def __createSingleInstance(self, build_spec):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')
        request.set_InstanceName(build_spec['instance_name'])
        request.set_InstanceType(build_spec['instance_type'])
        request.set_SecurityGroupId(build_spec['SecurityGroupId'])
        request.set_ImageId(build_spec['image_id'])
        result = self.__clt.do_action(request)
        return 'Code' not in json.loads(result)

    ## 创建实例
    # @param build_spec 字典 {{'instance_name', [String, ...]}, {'instance_type', String}, {'SecurityGroupId', String}, {'image_id', String}}
    # @return 列表 实例创建成功则对应列表项为True，否则False
    def createInstance(self, build_spec):
        instance_name = build_spec['instance_name']
        result = []
        for name in instance_name:
            build_spec['instance_name'] = name
            result.append(self.__createSingleInstance(build_spec))
        return result

    ## 查询调度所需信息
    # @return 字典 {{'InstanceTypes', [{{'InstanceTypeId', String}, {'CpuCoreCount', Integer}, {'MemorySize', Double}, {'InstanceTypeFamily', String}}, ...]}, {'Regions', [{{'RegionId', String}, {'LocalName', String}}, ...]}}
    def query(self):
        query_result = {}

        instance_type_resquest = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        instance_type_resquest.set_accept_format('json')
        result = json.loads(self.__clt.do_action(instance_type_resquest))
        query_result['InstanceTypes'] = result['InstanceTypes']

        region_request = DescribeRegionsRequest.DescribeRegionsRequest()
        region_request.set_accept_format('json')
        result = json.loads(self.__clt.do_action(region_request))
        query_result['Regions'] = result['Regions']

        # zone_request = DescribeZonesRequest.DescribeZonesRequest()
        # zone_request.set_accept_format('json')
        # self.__clt.do_action(zone_request)

        return query_result
    # def startInstance(self):
    #     request = StartInstanceRequest.StartInstanceRequest()
    #     return self.__clt.do_action(request)
    #
    # def stopInstance(self):
    #     request = StopInstanceRequest.StopInstanceRequest()
    #     return self.__clt.do_action(request)
    #
    # def rebootInstance(self):
    #     request = RebootInstanceRequest.RebootInstanceRequest()
    #     return self.__clt.do_action(request)
    #
    # def describeInstanceStatus(self):
    #     request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    #     return self.__clt.do_action(request)
    #
    # def describeInstances(self):
    #     request = DescribeInstancesRequest.DescribeInstancesRequest()
    #     return self.__clt.do_action(request)
    #
    # def deleteInstance(self):
    #     request = DeleteInstanceRequest.DeleteInstanceRequest()
    #     return self.__clt.do_action(request)