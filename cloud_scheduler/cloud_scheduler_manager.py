
from cloud_scheduler import cloud_filter_scheduler


class CloudSchedulerManager(object):
    """Chooses a cloud and one of its host to run instances on."""

    def __init__(self):
        self.filter_scheduler = cloud_filter_scheduler.CloudFilterScheduler()


    def select_cloud(self, request):
        """Returns cloud(s) best suited for this request.
        The result should be a list of cloud.
        """

        # resolve request

        filter_properties = {}
        request_spec = {}


        request_spec['num_instance'] = request.get('instance_num', 1)
        request_policy = request.get('policy', {})
        request_flavor = request.get('flavor', {})

        request_spec['ha'] = request_policy.get('ha')

        for key in request.get('flavor'):
            filter_properties[key] = request_flavor.get(key, '')
        del filter_properties['type'] # flavor type should't be in 'filter_properties'

        # deep copy
        request_spec['consumable_res'] = {}
        for key in filter_properties:
            request_spec['consumable_res'][key] = filter_properties[key]

        filter_properties['force'] = request_policy.get('force', [])
        filter_properties['ignore'] = request_policy.get('ignore', [])
        filter_properties['price'] = request_policy.get('price', {})

        # build_spec will be returned with cloud list scheduled in it
        build_spec = {}
        build_spec['instance_name'] = request.get('instance_name')
        build_spec['num_instance'] = request.get('num_instance', 1)
        build_spec['flavor'] = request.get('flavor')

        # TODO: context might be used in the future
        context = {}

        selected_clouds = self.filter_scheduler.select_destinations(context, request_spec, filter_properties)

        cloud_list = dict(cloud_list = [cloud.get('name', '') for cloud in selected_clouds])
        build_spec.update(cloud_list)
        return build_spec
