from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    Usuario,
    Pergunta,
    Resposta,
    Avaliacao,
    AtividadeSugerida,
    HistoricoAcesso,
)


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "genero",
                    "data_nascimento",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "criado_em", "atualizado_em")},
        ),
    )
    readonly_fields = ("criado_em", "atualizado_em")
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "genero",
        "is_staff",
    )
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ("ordem", "texto", "categoria")
    list_filter = ("categoria",)
    search_fields = ("texto", "categoria")
    ordering = ("ordem",)


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pergunta", "resposta", "data_resposta")
    list_filter = ("resposta", "data_resposta")
    search_fields = ("usuario__username", "pergunta__texto")
    date_hierarchy = "data_resposta"


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "pontuacao_total", "nivel_sofrimento", "data_avaliacao")
    list_filter = ("nivel_sofrimento", "data_avaliacao")
    search_fields = ("usuario__username",)
    date_hierarchy = "data_avaliacao"


@admin.register(AtividadeSugerida)
class AtividadeSugeridaAdmin(admin.ModelAdmin):
    list_display = ("nivel_sofrimento", "descricao")
    list_filter = ("nivel_sofrimento",)
    search_fields = ("descricao",)


@admin.register(HistoricoAcesso)
class HistoricoAcessoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "data_acesso", "ip")
    list_filter = ("data_acesso",)
    search_fields = ("usuario__username", "ip")
    date_hierarchy = "data_acesso"


admin.site.register(Usuario, CustomUserAdmin)
