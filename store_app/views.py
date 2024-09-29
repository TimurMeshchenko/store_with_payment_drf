from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
import json

from store import settings
from store_app.models import Product
from store_app.serializers import ProductSerializer  

stripe.api_key = settings.STRIPE_SECRET_KEY

class CatalogView(APIView):
    template_name = "catalog.html"

    def get(self, request, *args, **kwargs):
        """
        GET method to render the catalog template with serialized data.
        """
        return render(request, self.template_name)


class BasketView(APIView):
    template_name = "basket.html"

    def get(self, request, *args, **kwargs):
        """
        GET method to render the backset template with serialized data.
        """
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        basket = json.loads(request.body)
        payment_intent = stripe.PaymentIntent.create(
            amount=self.calculate_order_amount(basket),
            currency='rub',
        )

        return Response({'clientSecret': payment_intent.client_secret})

    def calculate_order_amount(self, basket):
        total_price = 0

        for product in basket:
            product_object = get_object_or_404(Product, pk=product['id'])
            serializer = ProductSerializer(product_object)
            product_count = product['count'] if 'count' in product else 1
            total_price += float(serializer.data['price']) * product_count

        return int(total_price * 100)

@api_view(['GET'])
def get_products_page(request):
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 30))

    products_page_objects = Product.objects.all().order_by('id')[offset:offset + limit]    
    serializer = ProductSerializer(products_page_objects, many=True)
    context = {'products': serializer.data}
    products_html = render(request, 'product_template.html', context).content.decode()

    return Response({"products": products_html})

@api_view(['GET'])
def get_product(request):
    product_id = request.GET.get('product_id')
    product_object = get_object_or_404(Product, pk=product_id)
    serializer = ProductSerializer(product_object)

    return Response({"product": serializer.data})

@api_view(['GET'])
def get_products_by_search(request):
    product_name = request.GET.get('product_name')
    products_matched = Product.objects.filter(name__icontains=product_name)[:10]
    serializer = ProductSerializer(products_matched, many=True)

    return Response({"products": serializer.data})