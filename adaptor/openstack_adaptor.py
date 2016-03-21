# -*- coding: utf-8 -*-


import novaclient.client as nvclient
import cinderclient.v2.client as cdclient

from adaptor import BaseAdaptor

class OpenStackAdaptor(BaseAdaptor):


    _version = 2
    _api_key = None
    _project_id = ''

    def __int__(self, config):
        # 每个adaptor保存对应云的名称，用户名密码，endpoint等
        self.name = config.get('name')
        self._user_name = config.get('user_name')
        self._password = config.get('password')
        self._end_point = config.get('end_point')

        self.nova_client = nvclient.Client(self._version, self._user_name, self._api_key, self._project_id, self._end_point)
        self.cinder_client = cdclient.Client(self._user_name, self._api_key, self._project_id, self._end_point)

    def create_instance(self, build_spec, context):
        raise Exception('Not finished yet')

    def get_cloud_state(self, context):

        ret = {'name': self.name}


        limit = self.get_limit(self.nova_client, self.cinder_client)

        ret['cpu'] = limit['coresTotal'] - limit['coresUsed']
        ret['ram'] = limit['ramTotal'] - limit['ramUsed']

        return ret

    def get_limit(self,nova_client,cinder_client):
        limits = nova_client.limits.get().absolute
        usage_limits = {}
        for i in limits:
            # usage_limits[i.name] = i.value
            if i.name ==  "maxTotalInstances":
                usage_limits["instanceTotal"] = i.value
            elif i.name == "totalInstancesUsed":
                usage_limits["instanceUsed"] = i.value
            elif i.name == "maxTotalCores":
                usage_limits["coresTotal"] = i.value
            elif i.name == "totalCoresUsed":
                usage_limits["coresUsed"] = i.value
            elif i.name == "maxTotalRAMSize":
                usage_limits["ramTotal"] = i.value
            elif i.name == "totalRAMUsed":
                usage_limits["ramUsed"] = i.value

            cinderlimits = cinder_client.limits.get().absolute
            for i in cinderlimits:
                # usage_limits[i.name] = i.value
                if i.name ==  "maxTotalVolumeGigabytes":
                    usage_limits["volumeStorage"] = i.value
                elif i.name == "totalGigabytesUsed":
                    usage_limits["totalGigabytesUsed"] = i.value
                elif i.name == "maxTotalVolumes":
                    usage_limits["volumeTotal"] = i.value
                elif i.name == "totalVolumesUsed":
                    usage_limits["volumeTotalUsed"] = i.value

        return usage_limits

    def get_base_usages(self):
        usages={}
        for url in self._end_point:
            nova_client = nvclient.Client(self._version, self._user_name, self._api_key, self._project_id, url)
            usage = self.get_usage(nova_client)
            usages[url]=usage
        return usages

    def get_usage(self,nova_client):
        usage={}
        servers = nova_client.servers.list()
        usage["instance"]=0
        usage["ram"] = 0
        usage["vcpus"] = 0
        usage["disk"] = 0
        # to get every server's usage
        for server in servers:
            usage["instance"]+=1
            usage["ram"] += nova_client.flavors.get(server.flavor["id"]).ram
            usage["vcpus"] += nova_client.flavors.find(id=server.flavor["id"]).vcpus
            usage["disk"] += nova_client.flavors.get(server.flavor["id"]).disk

        return usage
