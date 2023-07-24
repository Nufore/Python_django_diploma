from django_filters.rest_framework import backends


class CustomDFB(backends.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):

        free_delivery = True if request.query_params.get('filter[freeDelivery]') == 'true' else None
        available = True if request.query_params.get('filter[available]') == 'true' else None
        sort = request.query_params.get('sort') if request.query_params.get('sort') else ''
        sort_type = '-' if request.query_params.get('sortType') == 'dec' else ''

        filtered_data = {
            'name': request.query_params.get('filter[name]'),
            'min_price': request.query_params.get('filter[minPrice]'),
            'max_price': request.query_params.get('filter[maxPrice]'),
            'freeDelivery': free_delivery,
            'available': available,
            'currentPage': request.query_params.get('currentPage'),
            'tags': request.query_params.getlist('tags[]'),
            'sort': sort_type + sort,
        }
        return {
            # "data": request.query_params,
            "data": filtered_data,
            "queryset": queryset,
            "request": request,
        }
