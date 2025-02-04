from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_imei(request):
    #filter_query = self.get_filter_query(request.query_params)

    return Response('Test')
