import re


detect_mobile_reg = re.compile(
    r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|"
    r"ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|"
    r"p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows ce|xda|xiino",
    re.I | re.M)


class MobileMiddleware:
    """Для перенаправления пользователя на мобильную версию сайта."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.mobile = False
        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT']
            if detect_mobile_reg.search(user_agent):
                request.mobile = True
        response = self.get_response(request)
        return response
