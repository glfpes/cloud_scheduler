from cloud_scheduler import filters


class CPUFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):
        cpu_limit = filter_properties['cpu']
        
        return  cloud_state['cpu'] >= cpu_limit

    @staticmethod
    def get_mark(self):
        return 'cpu'