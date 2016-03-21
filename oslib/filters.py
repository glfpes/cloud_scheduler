
from oslib import loadables


class BaseFilter(object):
    """Base class of all filter classes."""
    def _filter_one(self, obj, filter_properties):
        """Return True if it passes the filter, False otherwise.
        Override this in a subclass.
        """
        return True

    def filter_all(self, filter_obj_list, filter_properties):
        """Yield objects that pass the filter.

        Can be overridden in a subclass, if you need to base filtering
        decisions on all objects.  Otherwise, one can just override
        _filter_one() to filter a single object.
        """

        for obj in filter_obj_list:
            if self._filter_one(obj, filter_properties):
                yield obj

    # Set to true in a subclass if a filter only needs to be run once
    # for each request rather than for each instance
    run_filter_once_per_request = False

    def run_filter_for_index(self, index):
        """Return True if the filter needs to be run for the "index-th"
        instance in a request.  Only need to override this if a filter
        needs anything other than "first only" or "all" behaviour.
        """
        if self.run_filter_once_per_request and index > 0:
            return False
        else:
            return True


class BaseFilterHandler(loadables.BaseLoader):
    """Base class to handle loading filter classes.

    This class should be subclassed where one needs to use filters.
    """

    def get_filtered_objects(self, filters, objs, filter_properties, index=0):

        list_objs = list(objs)

        for filter_ in filters:
            if filter_.run_filter_for_index(index):
                # cls_name = filter_.__class__.__name__
                # start_count = len(list_objs)
                objs = filter_.filter_all(list_objs, filter_properties)

                if objs is None:
                    # LOG.debug("Filter %s says to stop filtering", cls_name)
                    return []
                list_objs = list(objs)

        return list_objs
