from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from froala_editor import views
from django.contrib import admin

admin.site.site_header = 'Admin Panel'
admin.site.index_title = 'Admin Dashboard'
admin.site.site_title = 'Admin Dashboard'

handler404 = 'app.views.error_404'
handler500 = 'app.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls')),
    path('froala_editor/', include('froala_editor.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
