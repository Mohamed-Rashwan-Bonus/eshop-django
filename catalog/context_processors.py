from .models import Category


def categories_nav(request):
    return {'nav_categories': Category.objects.all()}
