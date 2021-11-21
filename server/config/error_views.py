from django.shortcuts import render


def custom_404_error(request, exception):
    """Отображение 404 ошибки."""
    return render(request, "main/error_page.html", {
        'error_title': 'Page Not Found',
        'error_message': '404',
    })
