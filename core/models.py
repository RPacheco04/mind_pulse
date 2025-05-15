from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Usuario(AbstractUser):
    GENDER_CHOICES = (
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino"),
        ("Outro", "Outro"),
    )

    email = models.EmailField(unique=True, verbose_name=_("E-mail"))
    genero = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name=_("Gênero"),
    )
    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name=_("Data de nascimento")
    )
    criado_em = models.DateTimeField(default=timezone.now, verbose_name=_("Criado em"))
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name=_("Atualizado em"))

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.username


class Pergunta(models.Model):
    CATEGORIAS = (
        ("sintomas físicos", "Sintomas Físicos"),
        ("distúrbios psicoemocionais", "Distúrbios Psicoemocionais"),
        ("outros", "Outros"),
    )

    texto = models.TextField(verbose_name=_("Texto da pergunta"))
    categoria = models.CharField(
        max_length=100,
        choices=CATEGORIAS,
        default="outros",
        verbose_name=_("Categoria"),
    )
    ordem = models.IntegerField(verbose_name=_("Ordem"))

    class Meta:
        verbose_name = _("Pergunta")
        verbose_name_plural = _("Perguntas")
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.ordem}. {self.texto[:50]}..."


class Resposta(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="respostas",
        verbose_name=_("Usuário"),
    )
    pergunta = models.ForeignKey(
        Pergunta,
        on_delete=models.CASCADE,
        related_name="respostas",
        verbose_name=_("Pergunta"),
    )
    resposta = models.BooleanField(verbose_name=_("Resposta"))
    data_resposta = models.DateTimeField(
        default=timezone.now, verbose_name=_("Data da resposta")
    )

    class Meta:
        verbose_name = _("Resposta")
        verbose_name_plural = _("Respostas")

    def __str__(self):
        return f"{self.usuario.username} - {self.pergunta.ordem} - {'Sim' if self.resposta else 'Não'}"


class Avaliacao(models.Model):
    NIVEIS_SOFRIMENTO = (
        ("Nenhum", "Nenhum"),
        ("Leve", "Leve"),
        ("Moderado", "Moderado"),
        ("Grave", "Grave"),
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes",
        verbose_name=_("Usuário"),
    )
    pontuacao_total = models.PositiveSmallIntegerField(
        verbose_name=_("Pontuação total")
    )
    nivel_sofrimento = models.CharField(
        max_length=20, choices=NIVEIS_SOFRIMENTO, verbose_name=_("Nível de sofrimento")
    )
    data_avaliacao = models.DateTimeField(
        default=timezone.now, verbose_name=_("Data da avaliação")
    )

    class Meta:
        verbose_name = _("Avaliação")
        verbose_name_plural = _("Avaliações")
        ordering = ["-data_avaliacao"]

    def __str__(self):
        return f"{self.usuario.username} - {self.nivel_sofrimento} ({self.pontuacao_total} pontos)"

    @classmethod
    def calcular_nivel_sofrimento(cls, pontuacao):
        if pontuacao == 0:
            return "Nenhum"
        elif 1 <= pontuacao <= 7:
            return "Leve"
        elif 8 <= pontuacao <= 14:
            return "Moderado"
        else:  # 15-20
            return "Grave"


class AtividadeSugerida(models.Model):
    NIVEIS_SOFRIMENTO = (
        ("Leve", "Leve"),
        ("Moderado", "Moderado"),
        ("Grave", "Grave"),
    )

    nivel_sofrimento = models.CharField(
        max_length=20, choices=NIVEIS_SOFRIMENTO, verbose_name=_("Nível de sofrimento")
    )
    descricao = models.TextField(verbose_name=_("Descrição da atividade"))

    class Meta:
        verbose_name = _("Atividade Sugerida")
        verbose_name_plural = _("Atividades Sugeridas")

    def __str__(self):
        return f"{self.nivel_sofrimento} - {self.descricao[:50]}..."


class HistoricoAcesso(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="historico_acessos",
        verbose_name=_("Usuário"),
    )
    data_acesso = models.DateTimeField(
        default=timezone.now, verbose_name=_("Data de acesso")
    )
    ip = models.GenericIPAddressField(
        blank=True, null=True, verbose_name=_("Endereço IP")
    )

    class Meta:
        verbose_name = _("Histórico de Acesso")
        verbose_name_plural = _("Históricos de Acesso")
        ordering = ["-data_acesso"]

    def __str__(self):
        return f"{self.usuario.username} - {self.data_acesso.strftime('%d/%m/%Y %H:%M:%S')}"
