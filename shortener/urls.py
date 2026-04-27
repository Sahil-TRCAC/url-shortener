from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from core.views import redirect_to_original, dashboard_page

urlpatterns = [
    # Login page
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Google OAuth
    path('auth/', include('social_django.urls', namespace='social')),
    
    # API endpoints
    path('api/', include('core.urls')),
    
    # Dashboard
    path('dashboard/', dashboard_page, name='dashboard'),
    
    # Logout
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    
    # Root redirect to login
    path('', LoginView.as_view(template_name='login.html'), name='home'),
    
    # Redirect short URL (MUST BE LAST)
    path('<str:short_code>/', redirect_to_original, name='redirect'),
]