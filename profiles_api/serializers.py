from rest_framework import serializers
from profiles_api import models



#Works similar to Django form for post request
class HelloSerializer(serializers.Serializer):
    """ Serializers is a name field for testing API View"""
    name = serializers.CharField(max_length=20)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profiles object"""


    class Meta:
        model = models.UserProfile
        fields = ( #Fields which can be accessible to serializers
             'id','email','name','password'
        )

        #Making sure password is not visible during GET requests
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'style' : {
                    'input_type':'password'
                }
            }
         }


    def create(self, validated_data):
        """" Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name  = validated_data['name'],
            password= validated_data['password'],
        )

        return user