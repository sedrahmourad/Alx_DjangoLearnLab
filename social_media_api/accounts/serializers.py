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
        
        # 2. Safely pop the M2M fields before creating the instance
        # Even if read_only, DRF can sometimes include it, causing a crash.
        followers_data = validated_data.pop('followers', None) # Safely remove followers if present
        
        # 3. Create the user instance without the M2M data
        # THIS IS WHERE THE 500 ERROR LIKELY HAPPENS IF followers IS STILL HERE
        user = User.objects.create(**validated_data)
        
        # 4. Hash and save the password
        user.set_password(password)
        user.save()
        
        # 5. Handle M2M fields (only if necessary, but this step confirms safety)
        if followers_data is not None:
             # Since you should not set followers on registration, this block is usually empty
             # For example, user.followers.set(followers_data) would go here
             pass

        # 6. Create and return the authentication token
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