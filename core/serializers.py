from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Pergunta, Resposta, Avaliacao, AtividadeSugerida, HistoricoAcesso

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "genero",
            "data_nascimento",
        )
        read_only_fields = ("id",)


class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
            "genero",
            "data_nascimento",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não conferem"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = Usuario.objects.create_user(**validated_data)
        return user


class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = ("id", "texto", "categoria", "ordem")
        read_only_fields = ("id",)


class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = ("id", "usuario", "pergunta", "resposta", "data_resposta")
        read_only_fields = ("id", "data_resposta")


class RespostaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = ("id", "pergunta", "resposta")
        read_only_fields = ("id",)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["usuario"] = request.user
        return super().create(validated_data)


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = (
            "id",
            "usuario",
            "pontuacao_total",
            "nivel_sofrimento",
            "data_avaliacao",
        )
        read_only_fields = ("id", "nivel_sofrimento", "data_avaliacao")

    def create(self, validated_data):
        pontuacao = validated_data.get("pontuacao_total")
        nivel_sofrimento = Avaliacao.calcular_nivel_sofrimento(pontuacao)
        validated_data["nivel_sofrimento"] = nivel_sofrimento
        return super().create(validated_data)


class AtividadeSugeridaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeSugerida
        fields = ("id", "nivel_sofrimento", "descricao")
        read_only_fields = ("id",)


class HistoricoAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoAcesso
        fields = ("id", "usuario", "data_acesso", "ip")
        read_only_fields = ("id", "data_acesso")
