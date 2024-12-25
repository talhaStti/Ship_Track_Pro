
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('signup.urls')),
    path('supplier', include('Supplier.urls')),
    path('customer', include('Customer.urls')),
    path('oilTanker', include('OilTanker.urls')),
    path('shippingCompany', include('ShippingCompany.urls')),
    path('portAuthority', include('PortAuthority.urls')),
    path('customAuthority', include('CustomAuthority.urls')),
    path('notification', include('notification.urls')),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
