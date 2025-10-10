from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token # Used to retrieve the token
from rest_framework.permissions import AllowAny # Used for public endpoints
from .serializers import RegisterSerializer, LoginSerializer

# --- 1. Registration View ---

class RegisterView(generics.CreateAPIView):
    # Only the registration serializer is needed
    serializer_class = RegisterSerializer
    # Allow ANY user (even unauthenticated ones) to access this view
    permission_classes = (AllowAny,) 

    # We override the default CreateAPIView's post method for custom response
    def post(self, request, *args, **kwargs):
        # Pass the request data to the serializer for validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # The serializer's create method is called, which saves the user and generates the token
        user = serializer.save()

        # Retrieve the token that was automatically created in the serializer's create()
        token, created = Token.objects.get_or_create(user=user)

        # Build the successful response payload
        response_data = {
            # The token key is what the client needs for all future requests!
            'token': token.key,
            # Return some basic user details for immediate client use
            'user': {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
            }
        }
        
        # Return HTTP 201 CREATED status
        return Response(response_data, status=status.HTTP_201_CREATED)


# --- 2. Login/Token Retrieval View ---

class LoginView(generics.GenericAPIView):
    # Only the login serializer is needed
    serializer_class = LoginSerializer
    # Allow ANY user to access this view, as they are logging in
    permission_classes = (AllowAny,) 

    def post(self, request):
        # 1. Pass the request data to the serializer for validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Get the authenticated user object stored by the serializer's validate() method
        user = serializer.validated_data['user']

        # 3. Retrieve or create the token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)

        # 4. Build the successful response payload
        response_data = {
            # Return the token key (This is the secure ID)
            'token': token.key,
            # Return basic user details
            'user': {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
            }
        }
        
        # Return HTTP 200 OK status
        return Response(response_data, status=status.HTTP_200_OK)