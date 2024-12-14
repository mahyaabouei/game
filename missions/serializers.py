from rest_framework import serializers
from .models import Missions

class MissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missions
        fields = '__all__'
