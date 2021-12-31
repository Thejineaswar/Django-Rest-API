from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Allow user to edit their own profile """

    def has_object_permission(self, request, view, obj):
        """ Check if the user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS: #Safe methods normally covers method which doesnt make changes
                                                          # to the data which is present in the database
            return True

        return obj.id == request.user.id #Checking if the object to which the changes are made, belong to the user

class UpdateOwnStatus(permissions.BasePermission):
    """ Allow users to update own status """

    def has_object_permission(self, request, view, obj):
        """ Check if the user is trying to update the status """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id == request.user.id # Why do we include user_profile?