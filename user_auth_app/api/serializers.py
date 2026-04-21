from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        pw = self.validated_data['password']
        pw_repeated = self.validated_data['repeated_password']

        if pw != pw_repeated:
            raise serializers.ValidationError("Passwords do not match")
        
        if len(pw) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        
        if self.validated_data['email'] in User.objects.values_list('email', flat=True):
            raise serializers.ValidationError("Email is already in use")
        
        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        account.set_password(pw)
        account.save()
        return account