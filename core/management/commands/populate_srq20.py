from django.core.management.base import BaseCommand
from core.models import Pergunta, AtividadeSugerida


class Command(BaseCommand):
    help = "Populates the database with SRQ-20 questions and suggested activities"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Populating SRQ-20 questions..."))

        # Dictionary with SRQ-20 questions
        srq20_questions = [
            {
                "ordem": 1,
                "texto": "Você tem dores de cabeça frequentes?",
                "categoria": "sintomas físicos",
            },
            {
                "ordem": 2,
                "texto": "Tem falta de apetite?",
                "categoria": "sintomas físicos",
            },
            {"ordem": 3, "texto": "Dorme mal?", "categoria": "sintomas físicos"},
            {
                "ordem": 4,
                "texto": "Assusta-se com facilidade?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 5,
                "texto": "Tem tremores nas mãos?",
                "categoria": "sintomas físicos",
            },
            {
                "ordem": 6,
                "texto": "Sente-se nervoso(a), tenso(a) ou preocupado(a)?",
                "categoria": "distúrbios psicoemocionais",
            },
            {"ordem": 7, "texto": "Tem má digestão?", "categoria": "sintomas físicos"},
            {
                "ordem": 8,
                "texto": "Tem dificuldade de pensar com clareza?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 9,
                "texto": "Tem se sentido triste ultimamente?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 10,
                "texto": "Tem chorado mais do que de costume?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 11,
                "texto": "Encontra dificuldade para realizar com satisfação suas atividades diárias?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 12,
                "texto": "Tem dificuldade para tomar decisões?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 13,
                "texto": "Tem dificuldade no serviço (seu trabalho é penoso, causa-lhe sofrimento)?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 14,
                "texto": "É incapaz de desempenhar um papel útil em sua vida?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 15,
                "texto": "Tem perdido o interesse pelas coisas?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 16,
                "texto": "Você se sente uma pessoa inútil, sem préstimo?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 17,
                "texto": "Tem tido a ideia de acabar com a vida?",
                "categoria": "distúrbios psicoemocionais",
            },
            {
                "ordem": 18,
                "texto": "Sente-se cansado(a) o tempo todo?",
                "categoria": "sintomas físicos",
            },
            {
                "ordem": 19,
                "texto": "Tem sensações desagradáveis no estômago?",
                "categoria": "sintomas físicos",
            },
            {
                "ordem": 20,
                "texto": "Você se cansa com facilidade?",
                "categoria": "sintomas físicos",
            },
        ]

        # Create questions
        for question_data in srq20_questions:
            Pergunta.objects.get_or_create(
                ordem=question_data["ordem"],
                defaults={
                    "texto": question_data["texto"],
                    "categoria": question_data["categoria"],
                },
            )

        # Dictionary with suggested activities
        activities = [
            {
                "nivel_sofrimento": "Leve",
                "descricao": "Praticar atividade física regularmente, pelo menos 30 minutos por dia, 3 vezes por semana",
            },
            {
                "nivel_sofrimento": "Leve",
                "descricao": "Buscar momentos de lazer e relaxamento, como passeios ao ar livre, leitura de livros ou hobbies",
            },
            {
                "nivel_sofrimento": "Leve",
                "descricao": "Manter uma rotina de sono saudável, dormindo entre 7 a 8 horas por noite",
            },
            {
                "nivel_sofrimento": "Moderado",
                "descricao": "Buscar apoio de amigos e familiares para conversas e compartilhamento de sentimentos",
            },
            {
                "nivel_sofrimento": "Moderado",
                "descricao": "Praticar técnicas de respiração e meditação diariamente para reduzir o estresse",
            },
            {
                "nivel_sofrimento": "Moderado",
                "descricao": "Considerar consulta com um profissional de saúde mental para orientação",
            },
            {
                "nivel_sofrimento": "Grave",
                "descricao": "Procurar atendimento psicológico ou psiquiátrico o mais breve possível",
            },
            {
                "nivel_sofrimento": "Grave",
                "descricao": "Não hesitar em buscar ajuda profissional especializada urgente",
            },
            {
                "nivel_sofrimento": "Grave",
                "descricao": "Em caso de pensamentos suicidas, entrar em contato imediatamente com o Centro de Valorização da Vida (CVV) pelo telefone 188",
            },
        ]

        # Create activities
        for activity_data in activities:
            AtividadeSugerida.objects.get_or_create(
                nivel_sofrimento=activity_data["nivel_sofrimento"],
                descricao=activity_data["descricao"],
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated SRQ-20 questions and activities!"
            )
        )
