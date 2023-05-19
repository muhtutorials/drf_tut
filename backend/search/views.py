from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from algoliasearch_django import raw_search

from products.models import Product
from products.serializers import ProductSerializer


class AlgoliaSearchListView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        params = {'facetFilters': []}
        if request.user.is_authenticated:
            user = request.user.username
            params['facetFilters'].append(f'user:{user}')
        query = request.GET.get('q')
        if not query:
            return Response('')
        if request.GET.get('tags'):
            tags = request.GET.get('tags').split(',')
            params['tagFilters'] = tags
        public = request.GET.get('public') != '0'
        if public:
            params['facetFilters'].append(f'public:{public}')
        results = raw_search(Product, query, params)
        return Response(results)


class SearchListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results
