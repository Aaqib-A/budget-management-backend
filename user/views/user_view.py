from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
import logging

# for filter View
from rest_framework import generics
from django_filters import rest_framework as filters
from user.filters import UserFilter

from user.models import User
from user.serializers import UserCreateSerializer, UserModelSerializer

from rest_framework.permissions import IsAuthenticated
from utils.permission_class import AdminAllPermission, CustomerAllPermission
from utils.role_filter_utils import RoleBasedQuery

log = logging.getLogger('budget_log')

class UserView(generics.ListAPIView, APIView):
    permission_classes = [IsAuthenticated & 
            (AdminAllPermission | CustomerAllPermission)
        ]

    queryset = User.objects.all()

    serializer_class = UserCreateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def list(self, request):
        try:
            user = request.user
            utils = RoleBasedQuery(user)
            user_role_query = utils.user_query()

            queryset = User.objects.filter(user_role_query)
            filter_backends = self.filter_queryset(queryset)
            serializer = UserCreateSerializer(filter_backends,many=True)
            resp = Response(serializer.data, status=status.HTTP_200_OK)
            return resp
        except Exception as e:
            log.error("[{user} | GET | UserView Error] Error - {error}".format(user=request.user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp
    

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            password = data.get('password')
            if not password:
                raise ValidationError("'password' is required")



            user_serialized = UserCreateSerializer(data=data)
            if user_serialized.is_valid():
                user_serialized.save()

                user = User.objects.get(username = user_serialized.data["username"])
                user.set_password(data['password'])
                user.save()
            else:
                raise ValidationError(user_serialized.errors)

            user_ser = UserModelSerializer(user)
            resp = user_ser.data

            return Response(resp, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            log.error("[{user} | POST | UserView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | UserView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:

            user_id = request.GET.get('user_id')
            if not user_id:
                raise ValidationError("'user_id' is required")


            # if "role" in data.keys():
            #     data.pop("role")
            if "password" in data.keys() and user.role != 'admin':
                raise ValidationError("'password' can only be changed by 'super_admin'")

            old_user = User.objects.get(user_id = user_id)
            user_serialized = UserCreateSerializer(old_user, data=data, partial=True)
            if user_serialized.is_valid():
                user_serialized.save()
                
                if "password" in data.keys():
                    old_user.set_password(data['password'])
                    old_user.save()
            else:
                raise ValidationError(user_serialized.errors)

            user_ser = UserModelSerializer(old_user)
            resp = user_ser.data
            return Response(resp, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            log.error("[{user} | POST | UserView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | UserView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

