from cloud_scheduler import filters


class ForceFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):
        forced_clouds = filter_properties.get('force')
        return cloud_state['name'] in forced_clouds

    @staticmethod
    def get_mark(self):
        return 'force'