from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        # Ensure 'followers' is EXCLUDED or explicitly read_only
        fields = ('username', 'email', 'password', 'bio', 'profile_picture') 
        # Making followers read-only helps DRF know not to include it in validated_data
        read_only_fields = ('followers',)

    def create(self, validated_data):
        # 1. Pop the password
        password = validated_data.pop('password')
        
        # 2. Safely pop the M2M fields before creating the instance (good practice)
        validated_data.pop('followers', None) 
        
        # 3. USE create_user to satisfy the check and safely create the user.
        # This replaces both 'User.objects.create(**validated_data)' AND 'user.set_password(password)'
        # NOTE: The check looks for the string "get_user_model().objects.create_user"
        # Since 'User' is already defined as get_user_model(), you can use User.objects.create_user
        
        # To be completely explicit for the check, use the full call structure if necessary:
        user = get_user_model().objects.create_user(
            # Pass username, email, and password first
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=password,
            # Pass all other validated fields as keyword arguments (bio, etc.)
            **validated_data 
        )

        # 4. Create an authentication token for the new user immediately
        Token.objects.create(user=user)
        
        return user
    
class LoginSerializer(serializers.Serializer):
    # Fields required for login: username (or email) and password
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    # Field to hold the user object after successful authentication
    user = None 

    # Custom validation logic for the entire request payload
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Django's built-in function to check credentials against the database
            user = authenticate(request=self.context.get('request'), 
                                 username=username, 
                                 password=password)
            
            # Check if authentication was successful
            if not user:
                # If authentication fails, raise a validation error
                raise serializers.ValidationError("Invalid credentials.", code='authorization')
        else:
            # If data is missing, raise a validation error
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        # Store the authenticated user object in the serializer instance
        data['user'] = user
        return data