
from cloud_scheduler import cloud_scheduler_manager

#script, request_num = sys.argv

scheduler = cloud_scheduler_manager.CloudSchedulerManager()

requests = {

    # request v3
    'v3':
    {

        'instance_name': ['my_instance_0', 'my_instance_1', 'my_instance_2', 'my_instance_3', 'my_instance_4', ],

        'instance_num': 5,

        'flavor':
        {
            'type': 'small' ,
            'cpu': 1, 'ram_mb': 1024, 'disk_gb': 10,
        },

        'policy':
        {
            #'force': ['http://192.168.1.123:5000' ],
            #'force': ['cloud_2'],
            #'ignore': ['http://cloud_ignored_keystone'],
            'ignore': ['cloud_1', 'cloud_2', ],
            #'price': {'min' : 0 , 'max' : 100 },
            'ha': 3,
        },

    },

}

# static cloud_state used currently
# please go to cloud_state_manager.py
ret = scheduler.select_cloud(requests['v3'])
print ret

