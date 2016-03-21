
from cloud_scheduler import filters


class DiskFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):

        disk_limit_gb = filter_properties['disk_gb']
        
        return cloud_state['disk_gb'] >= disk_limit_gb

    @staticmethod
    def get_mark(self):
        return 'disk_gb'
    
    
