
from oslo_utils import importutils

im_cls = importutils.import_object('oslib.cloud_state_manager.CloudStateManager')

print im_cls