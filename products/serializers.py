from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    label = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'description',
            'category', 'category_id', 'image',
            'is_active', 'discount_percent', 'discounted_price',
            'label'
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя не может быть пустым.")
        if len(value) < 3:
            raise serializers.ValidationError("Имя должно быть не короче 3 символов.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return value

    def validate_discount_percent(self, value):
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Скидка должна быть от 0 до 100.")
        return value

    def get_label(self, obj):
        if obj.discount_percent and obj.discount_percent > 0:
            return "On Sale"
        return "Regular"


class AveragePriceSerializer(serializers.Serializer):
    category = CategorySerializer()
    average_price = serializers.FloatField()
    total_products = serializers.IntegerField()
