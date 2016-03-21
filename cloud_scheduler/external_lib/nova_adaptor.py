# '''
# Created on Nov 25, 2015
#
# @author: stack
# '''
# import novaclient.client as nvclient
# import cinderclient.v2.client as cdclient
#
# class NovaAdapter(object):
#     '''
#     classdocs
#     '''
#     __version = 2
#     __username = 'admin'
#     __api_key = None
#     __project_id = ''
#     __auth_url = []
#
#     def __init__(self):
#         '''
#         Constructor
#         '''
#         self.__project_id='demo'
#         self.__auth_url.append('http://192.168.1.125:5000/v2.0')
#         self.__api_key='admin'
#
#
#     def getLimit(self,nova_client,cinder_client):
#         limits = nova_client.limits.get().absolute
#         usage_limits = {}
#         for i in limits:
#             #usage_limits[i.name] = i.value
#             if i.name ==  "maxTotalInstances":
#                 usage_limits["instanceTotal"] = i.value
#             elif i.name == "totalInstancesUsed":
#                 usage_limits["instanceUsed"] = i.value
#             elif i.name == "maxTotalCores":
#                 usage_limits["coresTotal"] = i.value
#             elif i.name == "totalCoresUsed":
#                 usage_limits["coresUsed"] = i.value
#             elif i.name == "maxTotalRAMSize":
#                 usage_limits["ramTotal"] = i.value
#             elif i.name == "totalRAMUsed":
#                 usage_limits["ramUsed"] = i.value
#
#             cinderlimits = cinder_client.limits.get().absolute
#             for i in cinderlimits:
#                 #usage_limits[i.name] = i.value
#                 if i.name ==  "maxTotalVolumeGigabytes":
#                     usage_limits["volumeStorage"] = i.value
#                 elif i.name == "totalGigabytesUsed":
#                     usage_limits["totalGigabytesUsed"] = i.value
#                 elif i.name == "maxTotalVolumes":
#                     usage_limits["volumeTotal"] = i.value
#                 elif i.name == "totalVolumesUsed":
#                     usage_limits["volumeTotalUsed"] = i.value
#
#         return usage_limits
#
#     def getLimits(self):
#         limits={}
#         for url in self.__auth_url:
#             nova_client = nvclient.Client(self.__version, self.__username, self.__api_key, self.__project_id, url)
#             cinder_client = cdclient.Client(self.__username, self.__api_key, self.__project_id, url)
#             limit = self.getLimit(nova_client,cinder_client)
#             limits[url]=limit
#         return limits
#
#     def get_base_Usages(self):
#         Usages={}
#         for url in self.__auth_url:
#             nova_client = nvclient.Client(self.__version, self.__username, self.__api_key, self.__project_id, url)
#             usage = self.getUsage(nova_client)
#             Usages[url]=usage
#         return Usages
#
#
#     def getUsage(self,nova_client):
#         usage={}
#         servers = nova_client.servers.list()
#         usage["instance"]=0
#         usage["ram"] = 0
#         usage["vcpus"] = 0
#         usage["disk"] = 0
#         #to get every server's usage
#         for server in servers:
#             usage["instance"]+=1
#             usage["ram"] += nova_client.flavors.get(server.flavor["id"]).ram
#             usage["vcpus"] += nova_client.flavors.find(id=server.flavor["id"]).vcpus
#             usage["disk"] += nova_client.flavors.get(server.flavor["id"]).disk
#
#         return usage