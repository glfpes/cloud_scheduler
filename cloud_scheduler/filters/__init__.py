

from oslib import filters

class BaseCloudFilter(filters.BaseFilter):
    """Base class for cloud filters."""

    @staticmethod
    def get_mark(self):
        raise NotImplementedError()

    def _filter_one(self, obj, filter_properties):
        """Return True if the object passes the filter, otherwise False."""
        return self.cloud_passes(obj, filter_properties)

    def cloud_passes(self, cloud_state, filter_properties):
        """Return True if the cloudState passes the filter, otherwise False.
        Override this in a subclass.
        """
        raise NotImplementedError()


class CloudFilterHandler(filters.BaseFilterHandler):
    def __init__(self):
        super(CloudFilterHandler, self).__init__(BaseCloudFilter)

    def all_filters(self):
        """Return a list of filter classes found in this directory.

        This method is used as the default for available scheduler filters
        and should return a list of all filter classes available.
        """
        return CloudFilterHandler().get_all_classes()
