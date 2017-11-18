from django.conf.urls import url, include
from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import GoodsDocumentView

router = ExtendedDefaultRouter()
goods = router.register(r'goods',
                        GoodsDocumentView,
                        base_name='goodsdocument')

urlpatterns = [
    url(r'^', include(router.urls)),
]