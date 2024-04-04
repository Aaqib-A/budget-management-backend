# REST Essentials
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

# for filter View
from rest_framework import generics
from django_filters import rest_framework as filters
from transaction.filters import TransactionFilter

# Extra imports
from django.db import transaction
from django.db.models import Q
import logging

# Custom Defined Imports
from transaction.models import Transaction
from transaction.serializers import TransactionModelSerializer
from category.models import Category
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permission_class import AdminAllPermission, CustomerAllPermission, CustomerReadPermission
from utils.role_filter_utils import RoleBasedQuery
from utils.input_helper import RequestInputHelper


log = logging.getLogger('budget_log')

class TransactionView(generics.ListAPIView, APIView):
    permission_classes = [IsAuthenticated & 
            ( AdminAllPermission | CustomerAllPermission )
        ]

    serializer_class = TransactionModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def list(self, request):
        try:
            user = request.user
            utils = RoleBasedQuery(user)
            transaction_role_query = utils.transaction_query()

            queryset = Transaction.objects.filter(transaction_role_query)
            filter_backends = self.filter_queryset(queryset)
            serializer = TransactionModelSerializer(filter_backends,many=True)
            resp = Response(serializer.data, status=status.HTTP_200_OK)
            return resp
        except Exception as e:
            log.error("[{user} | GET | TransactionView Error] Error - {error}".format(user=request.user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            # handle input
            input_helper = RequestInputHelper(data=data, user=user)
            data = input_helper.return_data()

            # Check if Category belongs to same user
            utils = RoleBasedQuery(user)
            category_role_query = utils.category_query()
            Category.objects.get(category_role_query & Q(category_id=data["category"]))

            
            transaction_serialized = TransactionModelSerializer(data=data)
            if transaction_serialized.is_valid():
                transaction_serialized.save()
                resp = transaction_serialized.data
            else:
                raise ValidationError(transaction_serialized.errors)

            return Response(resp, status=status.HTTP_201_CREATED)
            
        except Category.DoesNotExist as e:
            log.error("[{user} | POST | TransactionView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except ValidationError as e:
            log.error("[{user} | POST | TransactionView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | TransactionView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        try:

            utils = RoleBasedQuery(user)
            transaction_role_query = utils.transaction_query()

            transaction_id = request.GET.get('transaction_id')
            if not transaction_id:
                raise ValidationError("'transaction_id' is required")
            
            # handle input
            input_helper = RequestInputHelper(data=data, user=user)
            input_helper.created_modified_by_patch()
            data = input_helper.return_data()

            # Check if Category belongs to same user
            category_role_query = utils.category_query()
            Category.objects.get(category_role_query & Q(category_id=data["category"]))

            old_transaction = Transaction.objects.get(transaction_role_query & Q(transaction_id = transaction_id))
            transaction_serialized = TransactionModelSerializer(old_transaction, data=data, partial=True)
            with transaction.atomic():
                if transaction_serialized.is_valid():
                    transaction_serialized.save()
                else:
                    raise ValidationError(transaction_serialized.errors)

            resp = transaction_serialized.data
            return Response(resp, status=status.HTTP_200_OK)
            
        except (Transaction.DoesNotExist, Category.DoesNotExist) as e:
            log.error("[{user} | POST | TransactionView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            log.error("[{user} | POST | TransactionView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | TransactionView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:

            utils = RoleBasedQuery(user)
            transaction_role_query = utils.transaction_query()

            transaction_id = request.GET.get('transaction_id')
            if not transaction_id:
                raise ValidationError("'transaction_id' is required")

            deleted_transaction = Transaction.objects.get(transaction_role_query & Q(transaction_id = transaction_id))
            deleted_transaction.delete()


            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Transaction.DoesNotExist as e:
            log.error("[{user} | POST | TransactionView Error] Error - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_400_BAD_REQUEST)
            return resp
        except (ValidationError) as e:
            log.error("[{user} | POST | TransactionView Error] Error - {error}".format(user=user,error=e))
            resp = Response (e, status=status.HTTP_400_BAD_REQUEST)
            return resp
        except Exception as e:
            log.exception("[{user} | POST | TransactionView Exception] Exception - {error}".format(user=user,error=e))
            resp = Response (str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return resp