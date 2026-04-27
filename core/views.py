from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ShortURL, ClickEvent
from .utils import generate_short_code

def logout_view(request):
    """Custom logout view"""
    logout(request)
    return redirect('/')

def get_client_ip(request):
    """Get visitor's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def detect_device(user_agent):
    """Detect if visitor is using mobile, tablet, or desktop"""
    user_agent = user_agent.lower()
    if 'mobile' in user_agent or 'android' in user_agent:
        return 'mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        return 'tablet'
    else:
        return 'desktop'

@login_required
def dashboard_page(request):
    """Show the main dashboard"""
    return render(request, 'dashboard.html', {'user': request.user})

@api_view(['POST'])
@login_required
def create_short_url(request):
    """Create a new short URL"""
    original_url = request.data.get('url')
    
    if not original_url:
        return Response({'error': 'URL is required'}, status=400)
    
    # Generate unique short code
    short_code = generate_short_code()
    
    # Create the short URL
    short_url = ShortURL.objects.create(
        user=request.user,
        original_url=original_url,
        short_code=short_code
    )
    
    return Response({
        'success': True,
        'short_code': short_code,
        'short_url': f"http://127.0.0.1:8000/{short_code}",
        'original_url': original_url
    })

def redirect_to_original(request, short_code):
    """Redirect visitor to original URL and track the click"""
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    
    # Track the click
    ClickEvent.objects.create(
        short_url=short_url,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        device_type=detect_device(request.META.get('HTTP_USER_AGENT', ''))
    )
    
    # Increment click count
    short_url.total_clicks += 1
    short_url.save()
    
    # Redirect to original URL
    return redirect(short_url.original_url)

@api_view(['GET'])
@login_required
def get_analytics(request, short_code):
    """Get analytics for a specific short URL"""
    short_url = get_object_or_404(ShortURL, short_code=short_code, user=request.user)
    
    # Get all clicks for this URL
    clicks = short_url.clickevent_set.all()
    
    # Prepare analytics data
    analytics = {
        'total_clicks': short_url.total_clicks,
        'original_url': short_url.original_url,
        'created_at': short_url.created_at.strftime("%Y-%m-%d %H:%M"),
        'devices': {},
        'recent_clicks': []
    }
    
    # Count devices
    for click in clicks:
        device = click.device_type
        analytics['devices'][device] = analytics['devices'].get(device, 0) + 1
    
    # Get recent 10 clicks
    for click in clicks[:10]:
        analytics['recent_clicks'].append({
            'time': click.clicked_at.strftime("%Y-%m-%d %H:%M"),
            'device': click.device_type,
            'ip': click.ip_address
        })
    
    return Response(analytics)

@api_view(['GET'])
@login_required
def dashboard_stats(request):
    """Get all URLs and stats for the dashboard"""
    user_urls = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    
    data = {
        'total_urls': user_urls.count(),
        'total_clicks': sum(url.total_clicks for url in user_urls),
        'urls': [
            {
                'short_code': url.short_code,
                'original_url': url.original_url[:100],
                'clicks': url.total_clicks,
                'created_at': url.created_at.strftime("%Y-%m-%d")
            }
            for url in user_urls
        ]
    }
    return Response(data)