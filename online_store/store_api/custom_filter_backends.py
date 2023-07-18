from django_filters.rest_framework import backends


class CustomDFB(backends.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        if request.query_params.get('filter[freeDelivery]') == 'true':
            free_delivery = True
        else:
            free_delivery = None

        if request.query_params.get('filter[available]') == 'true':
            available = True
        else:
            available = None

        filtered_data = {
            'name': request.query_params.get('filter[name]'),
            'min_price': request.query_params.get('filter[minPrice]'),
            'max_price': request.query_params.get('filter[maxPrice]'),
            'freeDelivery': free_delivery,
            'available': available,
            'currentPage': request.query_params.get('currentPage'),
            'tags': request.query_params.getlist('tags[]')
        }
        print('DATA: ', request.query_params)
        print('filtered_data: ', filtered_data)
        return {
            # "data": request.query_params,
            "data": filtered_data,
            "queryset": queryset,
            "request": request,
        }
