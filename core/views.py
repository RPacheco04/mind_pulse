from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Sum, Max, Min
from django.conf import settings
import json
import csv
import io

from .models import Pergunta, Resposta, Avaliacao, AtividadeSugerida, HistoricoAcesso
from .serializers import (
    UsuarioSerializer,
    UsuarioRegistroSerializer,
    PerguntaSerializer,
    RespostaSerializer,
    RespostaCreateSerializer,
    AvaliacaoSerializer,
    AtividadeSugeridaSerializer,
    HistoricoAcessoSerializer,
)

Usuario = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return UsuarioRegistroSerializer
        return self.serializer_class

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RegistroAPIView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    permission_classes = [permissions.AllowAny]


class PerguntaViewSet(viewsets.ModelViewSet):
    queryset = Pergunta.objects.all().order_by("ordem")
    serializer_class = PerguntaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["categoria"]


class RespostaViewSet(viewsets.ModelViewSet):
    queryset = Resposta.objects.all()
    serializer_class = RespostaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["usuario", "pergunta", "data_resposta"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RespostaCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Resposta.objects.all()
        return Resposta.objects.filter(usuario=user)


class SRQ20ViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Retorna todas as perguntas do SRQ-20"""
        perguntas = Pergunta.objects.all().order_by("ordem")
        serializer = PerguntaSerializer(perguntas, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Recebe as respostas do questionário e calcula a avaliação"""
        respostas_data = request.data.get("respostas", [])
        user = request.user

        # Salvar respostas
        for resposta_data in respostas_data:
            pergunta_id = resposta_data.get("pergunta")
            resposta_valor = resposta_data.get("resposta")

            try:
                pergunta = Pergunta.objects.get(id=pergunta_id)
                Resposta.objects.create(
                    usuario=user, pergunta=pergunta, resposta=resposta_valor
                )
            except Pergunta.DoesNotExist:
                return Response(
                    {"error": f"Pergunta com ID {pergunta_id} não existe"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Calcular pontuação
        pontuacao_total = sum(
            1 for resposta in respostas_data if resposta.get("resposta") is True
        )
        nivel_sofrimento = Avaliacao.calcular_nivel_sofrimento(pontuacao_total)

        # Criar avaliação
        avaliacao = Avaliacao.objects.create(
            usuario=user,
            pontuacao_total=pontuacao_total,
            nivel_sofrimento=nivel_sofrimento,
        )

        # Buscar atividades sugeridas
        atividades = []
        if nivel_sofrimento != "Nenhum":
            atividades = AtividadeSugerida.objects.filter(
                nivel_sofrimento=nivel_sofrimento
            )
            atividades = AtividadeSugeridaSerializer(atividades, many=True).data

        # Registrar acesso
        ip = request.META.get("REMOTE_ADDR", "")
        HistoricoAcesso.objects.create(usuario=user, ip=ip)

        return Response(
            {
                "avaliacao": AvaliacaoSerializer(avaliacao).data,
                "atividades_sugeridas": atividades,
            }
        )


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["usuario", "nivel_sofrimento", "data_avaliacao"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Avaliacao.objects.all()
        return Avaliacao.objects.filter(usuario=user)

    @action(detail=False, methods=["get"])
    def estatisticas(self, request):
        """Retorna estatísticas gerais das avaliações"""
        if not request.user.is_staff:
            return Response(
                {"error": "Você não tem permissão para acessar essas estatísticas."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Estatísticas gerais
        total_avaliacoes = Avaliacao.objects.count()
        media_pontuacao = Avaliacao.objects.aggregate(media=Avg("pontuacao_total"))[
            "media"
        ]

        # Contagem por nível de sofrimento
        distribuicao_niveis = (
            Avaliacao.objects.values("nivel_sofrimento")
            .annotate(total=Count("id"))
            .order_by("nivel_sofrimento")
        )

        # Estatísticas por gênero
        por_genero = (
            Avaliacao.objects.values("usuario__genero")
            .annotate(media=Avg("pontuacao_total"), total=Count("id"))
            .order_by("usuario__genero")
        )

        return Response(
            {
                "total_avaliacoes": total_avaliacoes,
                "media_pontuacao": media_pontuacao,
                "distribuicao_niveis": distribuicao_niveis,
                "por_genero": por_genero,
            }
        )

    @action(detail=False, methods=["get"])
    def export(self, request):
        """Exporta dados das avaliações em formato JSON"""
        if not request.user.is_staff:
            return Response(
                {"error": "Você não tem permissão para exportar esses dados."},
                status=status.HTTP_403_FORBIDDEN,
            )

        formato = request.query_params.get("formato", "json").lower()
        avaliacoes = Avaliacao.objects.all().select_related("usuario")

        if formato == "json":
            data = []
            for avaliacao in avaliacoes:
                data.append(
                    {
                        "id": avaliacao.id,
                        "usuario": avaliacao.usuario.username,
                        "pontuacao": avaliacao.pontuacao_total,
                        "nivel": avaliacao.nivel_sofrimento,
                        "data": avaliacao.data_avaliacao.isoformat(),
                        "genero": avaliacao.usuario.genero,
                    }
                )
            return Response(data)

        elif formato == "csv":
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            writer.writerow(
                ["ID", "Usuário", "Pontuação", "Nível de Sofrimento", "Data", "Gênero"]
            )

            for avaliacao in avaliacoes:
                writer.writerow(
                    [
                        avaliacao.id,
                        avaliacao.usuario.username,
                        avaliacao.pontuacao_total,
                        avaliacao.nivel_sofrimento,
                        avaliacao.data_avaliacao,
                        avaliacao.usuario.genero,
                    ]
                )

            buffer.seek(0)
            response_content = buffer.getvalue()

            return Response(response_content)

        return Response(
            {"error": 'Formato não suportado. Use "json" ou "csv".'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AtividadeSugeridaViewSet(viewsets.ModelViewSet):
    queryset = AtividadeSugerida.objects.all()
    serializer_class = AtividadeSugeridaSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["nivel_sofrimento"]


class HistoricoAcessoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricoAcesso.objects.all()
    serializer_class = HistoricoAcessoSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["usuario", "data_acesso"]
