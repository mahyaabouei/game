from authentication.models import User
from rest_framework import serializers
from .models import Otp, TradingCodes , PrivatePerson , UserProfile , Accounts , Addresses , JobInfo 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            mobile=validated_data['mobile'],
            name=validated_data('name' , ''),
        )
        return user
    
class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'


class TradingCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingCodes
        fields = '__all__'

class PrivatePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivatePerson
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

