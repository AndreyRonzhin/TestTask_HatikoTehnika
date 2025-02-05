from django.conf import settings
from requests import RequestException
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .permissions import CheckToken
from .service import IMEI, IMEICheckNet



@api_view(['POST'])
@permission_classes([CheckToken])
def check_imei(request):
    content = None
    imei_str = request.query_params.get('imei', None)

    if imei_str is None:
        raise ParseError({"details": "Не указан imei"}, code=400)

    try:
        imei = IMEI(imei_str)
    except ValueError as ex:
        raise ParseError({"details": str(ex)}, code=400)

    token = settings.TOKEN_API_SANDBOX

    check_net = IMEICheckNet(imei.imei, token, 12)

    try:
        response_check_net = check_net.post_check_imei()
    except RequestException as ex:
       raise ParseError({"details": str(ex)}, code=520)
    else:
        content = response_check_net.get('content')


    return Response(content, status=status.HTTP_201_CREATED)
