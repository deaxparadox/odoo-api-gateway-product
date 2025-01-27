from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.models import (
    AttributesModel,
    AttributeValuesModel,
    AttributesCustom
)
from product.serializers.attr_value_serializer import (
    AttributeValueSerializer,
    AttributeValueUpdateSerializer,
    AVCreateSerializer
)
from notifications.models import NotificationModel
from helpers.message import message_collector
from helpers.permissions import OnlyVendor

class AttributeValueView(APIView):
    permission_classes = [IsAuthenticated, OnlyVendor]
    
    def get(self, request, attr_id: int):
        """
        Just return the response of all attribute value from 
        specific category.
        """
        res_messages = []
        try:
            queryset = AttributesModel.objects.get(id=attr_id)
            serializer = AttributeValueSerializer(queryset.values.all(), many=True)
            return Response(
                {"Message": serializer.data},
                status=status.HTTP_200_OK
            )
        except AttributesModel.DoesNotExist as e:
            res_messages.append(str(e))
            return Response(
                {
                    "Error": res_messages
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            res_messages.append(str(e))
            return Response(
                {
                    "Error": res_messages
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def post(self, request, attr_id):
        """
        Create a new instance of attribute value.
        
        Step:
        - check for validated data.
        - requried attribute_id, because attribute_id is used in path.
        - check of attribute name existence.
        - create new attribute value
        """
        res_messages = []
        try:
            serializer = AVCreateSerializer(data=request.data)
            if serializer.is_valid():
                # Since attribute_id is a ForiegnKey with on_delete
                # set to null, therefore creating new will be not raise error,
                # it will have a default value of null.
                # 
                # Tte AttributeValue must exist for the given attribute_id in the path.
                # 
                # Check for similar AttributeValues existence,
                # using the name fields, if name exist, then return
                # 302 found repsonse, else create a new attribute value.
                post_value_name = serializer.validated_data.get('name')
                filter_values = AttributeValuesModel.objects.filter(name=post_value_name)
                print([str(q) for q in filter_values])  
                if len(filter_values) > 0:
                    for q in filter_values:
                        if q.name == post_value_name:
                            res_messages.append("Following value already exists with attribute id %d" % q.attribute_id.id)
                            return Response(
                                {"Message": res_messages},
                                status=status.HTTP_302_FOUND
                            )
                instance = serializer.save()
                instance.attribute_id = AttributesModel.objects.get(id=attr_id)
                instance.save()
                notify = NotificationModel(
                    title="Attribute value created successfully",
                    body="Attribute value %s with id %s created successfully" % (instance.name, instance.id)
                )
                notify.save()
                notify.vendor_user.add(request.user.client_vendor)
                res_messages.append("Successfully created attribute value")
                return Response({"Message": res_messages}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AttributeValuesModel.DoesNotExist as e:
            # If the given attribute ID doesnot exists,
            # delete new attribute value instance.
            res_messages.append(str(e))
            instance.delete()
            return Response(
                {
                    "Error": res_messages
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except AttributesModel.DoesNotExist as e:
            # If the given attribute ID doesnot exists,
            # delete new attribute value instance.
            res_messages.append(str(e))
            instance.delete()
            return Response(
                {
                    "Error": res_messages
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            res_messages.append(str(e))
            return Response(
                {
                    "Error": res_messages
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        
    
class AVUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, OnlyVendor]
    
    def put(self, request, attr_id, value_id):
        """
        Update the instance of attribute value
        
        Step:
        - required attribute_id and its related valid_id, both should match.
        - check for data validation.
        - attribute_id must be included in request data, and should match path string attr_id
        - attribute_id field cannot be updated
        - sequence field cannot be updated
        """
        res_messages = message_collector()
        try:
            serializer = AttributeValueUpdateSerializer(data=request.data)
            if serializer.is_valid():
                # fetching attribute_id throught attribute value_id
                instance_value = AttributeValuesModel.objects.get(id=value_id)
                instance_attr = instance_value.attribute_id
                # path attr_id should be instance attribute value_id
                if instance_attr.id != attr_id:
                    res_messages("Invalid attribute id and valud id")
                    return Response(
                        {"Message": res_messages()},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                instance = serializer.update(instance_value, serializer.validated_data)
                res_messages("Successfully update attribute value %d" % instance.id)
                notify = NotificationModel(
                    title="Attribute value update successfully",
                    body="Attribute value %s with id %s updated successfully" % (instance.name, instance.id)
                )
                notify.save()
                notify.vendor_user.add(request.user.client_vendor)
                return Response({"Message": res_messages()})
        except AttributeValuesModel.DoesNotExist as e:
            res_messages(str(e))
            return Response(
                {"message": res_messages()},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            res_messages(str(e))
            return Response({"Message": res_messages()}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, attr_id, value_id):
        """
        Delete the value using id.
        
        Step:
        - Search for value instance.
        - value attribute id must match given attr_id in path.
        - delete
        """
        rmc = message_collector()
        try:
            instance_value = AttributeValuesModel.objects.get(id=value_id)
            if instance_value.attribute_id is None or instance_value.attribute_id.id != attr_id:
                rmc("Invalid attributed_id and valid_id")
                return Response({"Message": rmc()}, status=status.HTTP_400_BAD_REQUEST)
            # create a notification before deleting the instance
            notify = NotificationModel(
                title="Attribute value deleted successfully",
                body="Attribute value %s with id %s delted successfully" % (instance_value.name, instance_value.id)
            )
            notify.save()
            notify.vendor_user.add(request.user.client_vendor)
            # delete the instance
            instance_value.delete()
            rmc("Successfully delete the value")
            
            return Response({"Message": rmc()}, status=status.HTTP_204_NO_CONTENT)
        except AttributeValuesModel.DoesNotExist as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            rmc(str(e))
            return Response(
                {"Error": rmc()},
                status=status.HTTP_400_BAD_REQUEST
            )
    