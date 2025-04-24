from rest_framework import generics, views, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, AveragePriceSerializer
from django.db.models import Q


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ActiveProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Product.objects.filter(name__icontains=query)


class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)


class ProductImageUploadView(views.APIView):
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.image = request.FILES.get('image')
        product.save()
        return Response({'status': 'image uploaded'})


class CategoryStatsView(views.APIView):
    def get(self, request):
        stats = Category.objects.annotate(product_count=Count('product'))
        data = [{"category": c.name, "products": c.product_count} for c in stats]
        return Response(data)


class ToggleProductActiveView(views.APIView):
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.is_active = not product.is_active
        product.save()
        return Response({'status': f'is_active toggled to {product.is_active}'})


class ProductFilterByPriceView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        min_price = self.request.query_params.get('min')
        max_price = self.request.query_params.get('max')
        queryset = Product.objects.all()
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )


class AveragePriceAPIView(APIView):
    def get(self, request):
        data = (
            Product.objects
            .values('category_id')
            .annotate(
                average_price=Avg('price'),
                total_products=Count('id')
            )
        )

        serialized_data = []
        for item in data:
            category = Category.objects.get(pk=item['category_id'])
            serializer = AveragePriceSerializer({
                'category': category,
                'average_price': item['average_price'],
                'total_products': item['total_products']
            })
            serialized_data.append(serializer.data)

        return Response(serialized_data, status=status.HTTP_200_OK)