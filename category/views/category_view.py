# REST Essentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

# for filter View
from rest_framework import generics
from django_filters import rest_framework as filters
from category.filters import CategoryFilter

# Extra imports
from django.db import transaction
from django.db.models import Q
import logging

# Custom Defined Imports
from category.models import Category
from category.serializers import CategoryModelSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permission_class import AdminAllPermission, CustomerAllPermission, CustomerReadPermission
from utils.role_filter_utils import RoleBasedQuery
from utils.input_helper import RequestInputHelper


log = logging.getLogger('budget_log')

class CategoryView(generics.ListAPIView, APIView):
    permission_classes = [IsAuthenticated & 
            ( AdminAllPermission | CustomerAllPermission )
        ]

    serializer_class = CategoryModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter

    def list(self, request):
        try:
            user = request.user
            utils = RoleBasedQuery(user)
            category_role_query = utils.category_query()

            queryset = Category.objects.filter(category_role_query)
            filter_backends = self.filter_queryset(queryset)
            serializer = CategoryModelSerializer(filter_backends,many=True)
            resp = Response(serializer.data, status=status.HTTP_200_OK)
            return resp
        except Exception as e:
            log.error("[{user} | GET | CategoryView Error] Error - {error}".format(user=request.user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            # handle input
            input_helper = RequestInputHelper(data=data, user=user)
            input_helper.created_modified_by_post()
            input_helper.category_post_user()
            data = input_helper.return_data()

            category_serialized = CategoryModelSerializer(data=data)
            if category_serialized.is_valid():
                category_serialized.save()
                resp = category_serialized.data
            else:
                raise ValidationError(category_serialized.errors)

            return Response(resp, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            log.error("[{user} | POST | CategoryView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | CategoryView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        try:

            utils = RoleBasedQuery(user)
            category_role_query = utils.category_query()

            category_id = request.GET.get('category_id')
            if not category_id:
                raise ValidationError("'category_id' is required")
            
            # handle input
            input_helper = RequestInputHelper(data=data, user=user)
            input_helper.created_modified_by_patch()
            input_helper.category_patch_user()
            data = input_helper.return_data()

            old_category = Category.objects.get(category_role_query & Q(category_id = category_id))
            category_serialized = CategoryModelSerializer(old_category, data=data, partial=True)
            with transaction.atomic():
                if category_serialized.is_valid():
                    category_serialized.save()
                else:
                    raise ValidationError(category_serialized.errors)

            resp = category_serialized.data
            return Response(resp, status=status.HTTP_200_OK)
            
        except Category.DoesNotExist as e:
            log.error("[{user} | POST | CategoryView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            log.error("[{user} | POST | CategoryView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | CategoryView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:

            utils = RoleBasedQuery(user)
            category_role_query = utils.category_query()

            category_id = request.GET.get('category_id')
            if not category_id:
                raise ValidationError("'category_id' is required")

            deleted_category = Category.objects.get(category_role_query & Q(category_id = category_id))
            deleted_category.delete()


            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Category.DoesNotExist as e:
            log.error("[{user} | POST | CategoryView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            log.error("[{user} | POST | CategoryView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | CategoryView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp