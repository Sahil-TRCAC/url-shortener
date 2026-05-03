from django.contrib import admin
from django.urls import path, include
from core.views import redirect_to_original, dashboard_page, login_view, register_view, logout_view

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth (CUSTOM — not Django default)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Google OAuth
    path('auth/', include('social_django.urls', namespace='social')),

    # Dashboard
    path('dashboard/', dashboard_page, name='dashboard'),

    # API (clean separation)
    path('api/', include('core.urls')),

    # Home → login
    path('', login_view, name='home'),

    # Short URL redirect (ALWAYS LAST)
    path('<str:short_code>/', redirect_to_original, name='redirect'),
]