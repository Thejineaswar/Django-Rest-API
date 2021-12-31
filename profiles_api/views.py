from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


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


class HelloViewSet(viewsets.ViewSet):
    """ Test API Services"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """ Return a hello message"""
        a_viewset = [
            'Uses actions commonly used during API',
            'Automatically maps to URLs using routers',
            'Provides more functionality with less code'
        ]
        return Response({
            'message' : 'Hello',
            'a_viewset' : a_viewset
        })

    def create(self,request):
        """ Create a new hello message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name= serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({
                'message' : message
            })
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self,request,pk = None):
        """ Handle getting an object by its ID"""
        return Response({
            'http-method' : 'GET'
        })

    def update(self,request,pk = None):
        """ Handles updating an object """
        return Response({
            'http-method' : 'PUT'
        })

    def partial_update(self,request,pk = None):
        """ Handling update on part of the object"""
        return Response({
            'http-method': 'PATCH'
        })

    def destroy(self,request, pk=None):
        """ Handle removing an object """
        return Response({
            'http-method' : 'DELETE'
        })

class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,) #Dont forget to include "," in tuple
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields =('name','email',)


class UserLoginApiView(ObtainAuthToken):
    """ Handle creating user authentication tokens """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # have to add this across so it is visible on django's
                                                            # browsable api page. This would help for better visuals

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Handles creating, reading and updating profile feed items """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus ,
        IsAuthenticated # Can only make feed when logged in
    )

    def perform_create(self, serializer):
        """ Sets the user to profile to logged in user """
        serializer.save(user_profile = self.request.user)

