from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers


class HelloApiView(APIView):

    serializer_class = serializers.HelloSerializer

    """ Test API View"""
    def get(self,request,format = None):
        """ Returns a list of Api View features"""
        an_apiview = [
            'Uses HTTP methods as functions(get,post,put,patch,delete)',
            'Is similar to traditional Django View',
            'Gives you the most control over application logic',
            'Is manually mapped to URLs',
        ]

        return Response({
            'message' : 'Hello',
            'an_apiview' : an_apiview
        })

    def post(self,request):
        """ Create a hello message with our name"""
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f"Hello {name}"
            return Response({
                'message' : message
            })
        else: #Return HTTP Bad response
            return Response(
                serializer.errors, #Passing the errors to the users
                status = status.HTTP_400_BAD_REQUEST
            )

    def put(self,request, pk = None):
        """ Handle updating an object. PK is the key for an object to be updated"""
        return Response({
            'method' : 'Put request'
        })

    def patch(self,request,pk = None):
        """ Handle partial update of an update. More like update provided fields in the request"""
        return Response({
            'method' : 'Patch request'
        })

    def delete(self,request, pk=None):
        """Delete object in the database"""
        return Response({'method' : 'Delete Request'})