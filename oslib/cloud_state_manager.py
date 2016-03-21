# from cloud_scheduler.external_lib import nova_adaptor

class CloudState(dict):

    def consume_from_instance(self, instance_property):

        # a sample of instance_property
        #
        # instance_property = {
        #     'cpu': 10,
        #     'ram_mb': 8192,
        #     'disk_gb': 2000,
        # }

        for key in instance_property:
            self[key] -= instance_property[key]


class CloudStateManager(object):

    # def __init__(self):
    #
    #     raise Exception('Not finished yet')
    #
    #     self.cloud_list = []
    #     self.adaptor = nova_adaptor.NovaAdapter()
    #     state_list = self.adaptor.getLimits()
    #
    #     for (name, state)  in state_list.iteritems():
    #         self.cloud_list.append(CloudState(
    #             name = name,
    #             cpu = state['coresTotal'] - state['coresUsed'],
    #             ram_mb = state['ramTotal'] - state['ramUsed'],
    #
    #         ))


    # def get_all_cloud_states(self):
    #
    #     return self.cloud_list


    def get_all_cloud_states(self):

        return [

            # cloud 1
            CloudState(
                {
                    'name': 'cloud_1',
                    'cpu': 2,
                    'ram_mb': 2048,
                    'disk_gb': 10,
                    'price': 10,
                }
            ),

            # cloud 2
            CloudState(
                {
                    'name': 'cloud_2',
                    'cpu': 1,
                    'ram_mb': 2048,
                    'disk_gb': 10,
                    'price': 10,
                }
            ),

            # cloud 3
            CloudState(
                {
                    'name': 'cloud_3',
                    'cpu': 4,
                    'ram_mb': 2048,
                    'disk_gb': 10,
                    'price': 10,
                }
            ),

            # cloud 4
            CloudState(
                {
                    'name': 'cloud_4',
                    'cpu': 8,
                    'ram_mb': 10240,
                    'disk_gb': 200,
                    'price': 10,
                }
            ),

            # cloud 5
            CloudState(
                {
                    'name': 'cloud_5',
                    'cpu': 32,
                    'ram_mb': 81920,
                    'disk_gb': 1000,
                    'price': 10,
                }
            ),

        ]