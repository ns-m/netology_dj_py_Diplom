from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view, name='main'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('add_to_cart/<product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/', views.show_cart_view, name='cart'),
    path('<section>/', views.show_section_view, name='section'),
    path('<section_slug>/<product_slug>/', views.show_product_view, name='product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
