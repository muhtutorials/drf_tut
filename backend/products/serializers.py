from rest_framework.reverse import reverse
from rest_framework import serializers

from api.serializers import UserSerializer
from .models import Product
from .validators import validate_title


class ProductSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source='user', read_only=True)
    url = serializers.SerializerMethodField()
    title = serializers.CharField(validators=[validate_title])
    body = serializers.CharField(source='description')

    class Meta:
        model = Product
        fields = ['title', 'body', 'price', 'owner', 'url', 'path']

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('product-detail', kwargs={'pk': obj.pk}, request=request)
