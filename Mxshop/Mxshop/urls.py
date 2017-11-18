"""Mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls #使用drf提供的文档
# from django.contrib import admin
from django.views.static import serve
from Mxshop.settings import MEDIA_ROOT
import xadmin
from django.views.generic import TemplateView
from goods.views import GoodsListViewSet,CategoryViewset,BannerViewset,IndexCategoryViewset
from users.views import SmsCodeViewset,UserViewset
from user_operation.views import UserFavViewset,LeavingMessageViewset,AddressViewset
from trade.views import ShopCartViewset,OrderViewset,AlipayView
router = DefaultRouter()
router.register(r'goods',GoodsListViewSet,base_name='goods')
router.register(r'categories',CategoryViewset,base_name='categories')
router.register(r'codes',SmsCodeViewset,base_name='codes')
router.register(r'users',UserViewset,base_name='users')
router.register(r'userfavs',UserFavViewset,base_name='userfavs')
router.register(r'messages',LeavingMessageViewset,base_name='messages')
router.register(r'address',AddressViewset,base_name='address')
router.register(r'shopcarts',ShopCartViewset,base_name='shopcarts')
router.register(r'orders',OrderViewset,base_name='orders')
router.register(r'banners',BannerViewset,base_name='banners')
router.register(r'indexgoods',IndexCategoryViewset,base_name='indexgoods')

from search_indexes import urls as search_index_urls
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'docs/',include_docs_urls(title = "慕学生鲜")),
    #drf自带的token认证方式
    # url(r'^api-token-auth/', views.obtain_auth_token),
    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),
    #支付宝支付结果通知接口
    url(r'^alipay/return',AlipayView.as_view(),name="alipay"),
    url(r'^index/',TemplateView.as_view(template_name="index.html"),name="index"),
    # Search URLs
    url(r'^search/', include(search_index_urls)),
]
