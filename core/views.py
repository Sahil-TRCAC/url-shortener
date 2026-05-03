from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ShortURL, ClickEvent
from .utils import generate_short_code


# ========================
# AUTH VIEWS
# ========================

def register_view(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            print(username, email, password)  # debug

            if not username or not email or not password:
                messages.error(request, "All fields required")
                return redirect("register")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("dashboard")

        except Exception as e:
            print("ERROR:", e)  # 🔥 THIS WILL SHOW REAL ERROR
            return redirect("register")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")


# ========================
# DASHBOARD
# ========================

@login_required
def dashboard_page(request):
    return render(request, "dashboard.html", {"user": request.user})


# ========================
# UTIL FUNCTIONS
# ========================

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def detect_device(user_agent):
    user_agent = user_agent.lower()
    if "mobile" in user_agent or "android" in user_agent:
        return "mobile"
    elif "tablet" in user_agent or "ipad" in user_agent:
        return "tablet"
    return "desktop"


# ========================
# URL SHORTENER
# ========================

@api_view(["POST"])
@login_required
def create_short_url(request):
    original_url = request.data.get("url")

    if not original_url:
        return Response({"error": "URL is required"}, status=400)

    short_code = generate_short_code()

    short_url = ShortURL.objects.create(
        user=request.user,
        original_url=original_url,
        short_code=short_code
    )

    return Response({
        "success": True,
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:8000/{short_code}",
        "original_url": original_url
    })


def redirect_to_original(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)

    ClickEvent.objects.create(
        short_url=short_url,
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        device_type=detect_device(request.META.get("HTTP_USER_AGENT", ""))
    )

    short_url.total_clicks += 1
    short_url.save()

    return redirect(short_url.original_url)


# ========================
# ANALYTICS
# ========================

@api_view(["GET"])
@login_required
def get_analytics(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code, user=request.user)

    clicks = short_url.clickevent_set.all()

    analytics = {
        "total_clicks": short_url.total_clicks,
        "original_url": short_url.original_url,
        "created_at": short_url.created_at.strftime("%Y-%m-%d %H:%M"),
        "devices": {},
        "recent_clicks": []
    }

    for click in clicks:
        device = click.device_type
        analytics["devices"][device] = analytics["devices"].get(device, 0) + 1

    for click in clicks[:10]:
        analytics["recent_clicks"].append({
            "time": click.clicked_at.strftime("%Y-%m-%d %H:%M"),
            "device": click.device_type,
            "ip": click.ip_address
        })

    return Response(analytics)


@api_view(["GET"])
@login_required
def dashboard_stats(request):
    user_urls = ShortURL.objects.filter(user=request.user).order_by("-created_at")

    data = {
        "total_urls": user_urls.count(),
        "total_clicks": sum(url.total_clicks for url in user_urls),
        "urls": [
            {
                "short_code": url.short_code,
                "original_url": url.original_url[:100],
                "clicks": url.total_clicks,
                "created_at": url.created_at.strftime("%Y-%m-%d")
            }
            for url in user_urls
        ]
    }

    return Response(data)