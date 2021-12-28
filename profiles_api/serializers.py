from rest_framework import serializers


#Works similar to Django form for post request
class HelloSerializer(serializers.Serializer):
    """ Serializers is a name field for testing API View"""
    name = serializers.CharField(max_length=20)

