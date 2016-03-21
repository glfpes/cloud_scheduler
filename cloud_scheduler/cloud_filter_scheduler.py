
import random

from oslib import scheduler
from cloud_scheduler import filters


CONF_subset_size = 1
CONF_mark_cls_map =\
    {
        'cpu': 'CPUFilter',
        'disk_gb': 'DiskFilter',
        'ram_mb': 'RamFilter',
        'force': 'ForceFilter',
        'ignore': 'IgnoreFilter',
        'price': 'PriceFilter',
    }


class CloudFilterScheduler(scheduler.BaseCloudScheduler):
    """Scheduler that can be used for filtering and weighing."""
    def __init__(self):

        super(CloudFilterScheduler, self).__init__()
        self.filter_handler = filters.CloudFilterHandler()
        filter_classes = self.filter_handler.all_filters()

        self.filter_cls_map = {cls.__name__: cls for cls in filter_classes}
        self.filter_obj_map = {}

        self.mark_cls_map = CONF_mark_cls_map

        # TODO: weight
        #self.weight_handler =




    def select_destinations(self, context, request_spec, filter_properties):
        """Select a filtered cloud"""

        selected_clouds = self._schedule(context, request_spec, filter_properties)

        # todo: what if not enough clouds can meet the request

        return selected_clouds

    def _schedule(self, context, request_spec, filter_properties):
        """Returns a list of clouds that meet the required specs,
        ordered by their fitness.
        """

        clouds = self._get_all_cloud_states(None)
        selected_clouds = []
        num_instance = request_spec.get('num_instance', 1)

        # ha -- High Availability Request.
        #
        # if ha == 0, which means no ha request, then create each instance on
        # cloud randomly choiced from top m clouds given by filter
        # and weighed;
        #
        # if not, then instances created will be as far as possilbe on
        # various clouds. of course these clouds will come from filter
        # and weight.
        ha = request_spec.get('ha', 0)
        if not ha:

            for num in range(num_instance):
                clouds = self._get_filtered_clouds(clouds, filter_properties)

                if not clouds:
                    # no more clouds can meet the request
                    break

                weighed_clouds = self._get_weighed_clouds(clouds, filter_properties)

                # Choose a cloud randomly from top scheduler_cloud_subset_size cloud
                scheduler_cloud_subset_size = CONF_subset_size
                if scheduler_cloud_subset_size > len(selected_clouds):
                    scheduler_cloud_subset_size = len(selected_clouds)
                if scheduler_cloud_subset_size < 1:
                    scheduler_cloud_subset_size = 1

                chosen_cloud = random.choice(weighed_clouds[0:scheduler_cloud_subset_size])
                selected_clouds.append(chosen_cloud)
                chosen_cloud.consume_from_instance(request_spec['consumable_res'])

        else:

            while(num_instance > 0):

                clouds = self._get_filtered_clouds(clouds, filter_properties)
                if not clouds:
                    # no more clouds can meet the request
                    break

                group_size = min(ha, len(clouds), num_instance)
                num_instance -= group_size

                weighed_clouds = self._get_weighed_clouds(clouds, filter_properties)

                for cloud in weighed_clouds[0:group_size]:
                    cloud.consume_from_instance(request_spec['consumable_res'])

                selected_clouds.extend(weighed_clouds[0:group_size])

        return selected_clouds

    def _get_all_cloud_states(self, context):
        return self.cloud_state_manager.get_all_cloud_states()

    def _get_filtered_clouds(self, clouds, filter_properties):
        """Filter hosts and return only ones passing all filters."""

        # analyse filter_properties to get filter class names
        filter_class_names = []
        for mark in filter_properties.keys():
            if not self.mark_cls_map.get(mark):
                raise Exception('mark %s is not in mark_cls_map.' % mark)
            if filter_properties.get(mark):
                filter_class_names.append(self.mark_cls_map.get(mark))

        filters = self._choose_cloud_filters(filter_class_names)

        return self.filter_handler.get_filtered_objects(filters,clouds,filter_properties)

    def _get_weighed_clouds(self, clouds, weight_properties):
        """Weigh the clouds, NOT finished yet"""
        # TODO: finished this method
        return clouds

    def _choose_cloud_filters(self, filter_cls_names):
        """Since the caller may specify which filters to use we need
        to have an authoritative list of what is permissible. This
        function checks the filter names against a predefined set
        of acceptable filters.
        """
        if not isinstance(filter_cls_names, (list, tuple)):
            filter_cls_names = [filter_cls_names]

        good_filters = []
        bad_filters = []
        for filter_name in filter_cls_names:
            if filter_name not in self.filter_obj_map:
                if filter_name not in self.filter_cls_map:
                    bad_filters.append(filter_name)
                    continue
                filter_cls = self.filter_cls_map[filter_name]
                self.filter_obj_map[filter_name] = filter_cls()
            good_filters.append(self.filter_obj_map[filter_name])
        if bad_filters:
            msg = ", ".join(bad_filters)
            raise Exception('SchedulerHostFilterNotFound: filter_name = ', msg)
        return good_filters