from cloud_scheduler import filters


class PriceFilter(filters.BaseCloudFilter):
    def cloud_passes(self, cloud_state, filter_properties):
        bool_min = True
        bool_max = True
        min_price = filter_properties['price'].get('min', 'not_exist')
        if min_price != 'not_exist':
            bool_min = min_price <= cloud_state['price']
        max_price = filter_properties['price'].get('max', 'not_exist')
        if max_price != 'not_exist':
            bool_max = max_price >= cloud_state['price']

        return bool_min and bool_max

    @staticmethod
    def get_mark(self):
        return 'price'