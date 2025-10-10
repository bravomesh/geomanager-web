from django.core.cache import cache
from .models import SiteTheme, Navbar

def theme_context(request):
    theme = cache.get('active_theme')
    if not theme:
        try:
            theme = SiteTheme.objects.get(is_active=True)
            cache.set('active_theme', theme, 60*60*24)  # Cache for 24 hours
        except SiteTheme.DoesNotExist:
            # Fallback to default colors
            theme = {
                'primary_color': '#034930',
                'secondary_color': '#198754',
                'accent_color': '#fbc02d',
                'primary_text_color': '#ffffff',
                'secondary_text_color': '#333333',
                'background_color': '#ffffff',
            }
    return {'theme': theme}

def navbar_context(request):
    navbar = Navbar.objects.live().first()
    return {'navbar': navbar}