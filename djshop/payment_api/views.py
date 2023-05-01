from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view()
@permission_classes([AllowAny])
def get_response(request):
    if int(request.query_params['number']) % 2 == 0 and int(request.query_params['number'][-1]) != 0:
        return Response({'message': 'Successful payment',
                         'success': True})
    elif int(request.query_params['number']) % 2 == 1 or int(request.query_params['number'][-1]) == 0:
        return Response({'message': 'Failed payment',
                         'success': False})
