
from cloud_scheduler import filters


class RamFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):
        ram_limit_mb = filter_properties['ram_mb']

        return cloud_state['ram_mb'] >= ram_limit_mb


    @staticmethod
    def get_mark(self):
        return 'ram_mb'
  