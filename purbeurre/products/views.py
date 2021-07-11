import logging
from django.shortcuts import get_object_or_404
from research.models import Product
from account.models import Profile
from django.views.generic.base import TemplateView

# Logger

logger = logging.getLogger(__name__)


class ProductView(TemplateView):

    template_name = "products/detail.html"

    def get_context_data(self, **kwargs):
        display_fav = 1
        product_id = kwargs['product_id']

        if self.request.user.is_authenticated:
            user_pk = self.request.user.id
            user_profile = Profile.objects.get(user_id=user_pk)
            favs = user_profile.favorite.all()
            for fav in favs:
                if product_id == fav.barcode:
                    display_fav = 0

        p = get_object_or_404(Product, pk=product_id)
        context = super().get_context_data(**kwargs)
        context = {"product": p, "display_fav": display_fav}
        return context

    def post(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        user_pk = request.user.id
        user_profile = get_object_or_404(Profile, user_id=user_pk)
        user_profile.favorite.add(product_id)
        user_profile.save()
        logger.info('New favorite', exc_info=True, extra={
                # Optionally pass a request and we'll grab any information we can
                'request': request,
            })
        return self.get(request, *args, **kwargs)
