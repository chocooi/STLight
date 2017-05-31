from django.contrib.auth.models import User, Group
from .models import StreetLight, Zone, Order
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class StreetLightSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StreetLight
        fields = ('posX','posY', 'id', 'code', 'code', 'luminous' )
        read_only_fields = ( 'posX', 'posY', 'luminous')

class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'zoneName' )

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('commendCode', 'commendNum' )
