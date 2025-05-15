from django.utils import timezone
from .models import HistoricoAcesso


class HistoricoAcessoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Register access if user is authenticated and the request is not from admin
        if (
            request.user.is_authenticated
            and not request.path.startswith("/admin/")
            and not request.path.startswith("/static/")
            and not request.path.startswith("/media/")
        ):

            # Get IP address
            ip = self.get_client_ip(request)

            # Register access
            HistoricoAcesso.objects.create(usuario=request.user, ip=ip)

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip
