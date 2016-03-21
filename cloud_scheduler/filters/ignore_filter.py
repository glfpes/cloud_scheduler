from cloud_scheduler import filters


class IgnoreFilter(filters.BaseCloudFilter):

    def cloud_passes(self, cloud_state, filter_properties):
        ignored_clouds = filter_properties.get('ignore')
        return cloud_state['name'] not in ignored_clouds

    @staticmethod
    def get_mark(self):
        return 'ignore'
