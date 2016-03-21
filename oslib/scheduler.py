
from oslo_utils import importutils

CONF_cloud_state_manager = 'oslib.cloud_state_manager.CloudStateManager'


class BaseCloudScheduler(object):
    """The base class that all cloud scheduler should inherit from."""

    def __init__(self):
        self.cloud_state_manager = importutils.import_object(CONF_cloud_state_manager)

    def select_destinations(self, context, request_spec, filter_properties):
        """Must override select_destinations method.

        :return: A list of cloud name as keys
            that satisfies the request_spec and filter_properties.
        """
        msg = "Cloud scheduler must implement select_destinations"
        raise NotImplementedError(msg)