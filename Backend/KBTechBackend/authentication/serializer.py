from rest_framework import serializers
from .models import User, Sessions

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
class SessionSerializer(serializers.Serializer):
    class Meta:
        model = Sessions
        fields = '__all__'