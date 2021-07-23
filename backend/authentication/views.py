from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



# @csrf_exempt
# @api_view(['GET', 'POST'])
# def register(request):
#     body = json.loads(request.body)
#     if body['password'] == body['confirm']:
#         try:
#             user = User.objects.create_user(username=body['username'], email=body['email'], password=make_password(body['password']))
#             return Response("Success", status=202)
#         except IntegrityError:
#             return Response("User already exists", status=401)            
#     else:
#         return Response("Passwords don't match", status=401)