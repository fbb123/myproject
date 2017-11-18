from rest_framework import serializers
from .models import UserFav,UserLeavingMessage,UserAddress
from goods.serializers import GoodsSerializer

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserFav
        fields = ("user","goods","id")


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("goods","id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d %H:%M")
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")