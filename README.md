# Sistema de Monitoramento de Saúde Mental SRQ-20

Este projeto é um sistema web de monitoramento da saúde mental de trabalhadores utilizando o questionário SRQ-20 (Self-Reporting Questionnaire), composto por um backend Django com REST API e um frontend HTML/CSS/JavaScript.

## Tecnologias Utilizadas

### Backend

- Python 3.10+
- Django 4.2
- Django REST Framework
- SQLite (para desenvolvimento)
- JWT Authentication

### Frontend

- HTML5
- CSS3
- JavaScript (Vanilla)
- Chart.js (para visualização de dados)

## Funcionalidades

- Cadastro e login de usuários
- Aplicação do formulário SRQ-20 (20 perguntas com Sim/Não)
- Cálculo da pontuação total (0–20)
- Estratificação:
  - 0 ponto: Nenhum sofrimento
  - 1–7: Leve
  - 8–14: Moderado
  - 15–20: Grave
- Armazenamento das respostas no banco de dados
- Relatório individual com histórico de respostas
- Relatório geral (média da população, gráficos, percentuais)
- Sugestão de atividades conforme o nível
- Exportação em JSON/CSV
- Interface responsiva

## Instalação e Configuração

### Backend

1. Clone o repositório:

```bash
git clone <url_do_repositorio>
cd srq20_backend
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute as migrações:

```bash
python manage.py migrate
```

5. Popule o banco de dados com as perguntas do SRQ-20:

```bash
python manage.py populate_srq20
```

6. Crie um superusuário:

```bash
python manage.py createsuperuser
```

7. Execute o servidor:

```bash
python manage.py runserver
```

### Frontend

O frontend pode ser servido de várias maneiras:

#### Opção 1: Usando o servidor Python simples

1. Navegue até a pasta do frontend:

```bash
cd frontend
```

2. Execute o servidor Python:

```bash
python server.py
```

3. Acesse http://localhost:8080 no seu navegador

#### Opção 2: Usando extensões do VS Code ou outro servidor HTTP

Você pode usar extensões como "Live Server" no VS Code ou qualquer outro servidor HTTP simples para servir os arquivos do frontend.

## Estrutura do Projeto

### Backend

- `srq20_backend/`: Configurações do projeto Django
- `core/`: Aplicativo principal com modelos, views e serializadores
  - `models.py`: Modelos de dados (Usuario, Pergunta, Resposta, etc.)
  - `views.py`: Views da API REST
  - `serializers.py`: Serializadores para a API
  - `middleware.py`: Middleware para rastreamento de acesso
  - `management/commands/`: Comandos personalizados

### Frontend

- `frontend/`: Arquivos da interface
  - `index.html`: Página inicial
  - `login.html`: Página de login
  - `cadastro.html`: Página de cadastro
  - `srq20.html`: Página do questionário
  - `resultado.html`: Página de resultados
  - `historico.html`: Página de histórico
  - `metricas.html`: Página de métricas (admin)
  - `css/`: Arquivos CSS
  - `js/`: Arquivos JavaScript
  - `img/`: Imagens e recursos

## Endpoints da API

### Autenticação

- `POST /api/registro/` - Registrar um novo usuário
- `POST /api/token/` - Obter token JWT
- `POST /api/token/refresh/` - Renovar token JWT
- `POST /api/token/verify/` - Verificar token JWT

### Usuários

- `GET /api/usuarios/me/` - Obter informações do usuário logado
- `GET /api/usuarios/` - Listar usuários (admin)
- `POST /api/usuarios/` - Criar usuário (admin)
- `GET /api/usuarios/{id}/` - Detalhes do usuário (admin)
- `PUT /api/usuarios/{id}/` - Atualizar usuário (admin)
- `DELETE /api/usuarios/{id}/` - Excluir usuário (admin)

### Questionário SRQ-20

- `GET /api/srq20/` - Listar perguntas do SRQ-20
- `POST /api/srq20/` - Enviar respostas e receber avaliação

### Avaliações

- `GET /api/avaliacoes/` - Listar avaliações do usuário
- `GET /api/avaliacoes/{id}/` - Detalhes da avaliação
- `GET /api/avaliacoes/estatisticas/` - Estatísticas gerais (admin)
- `GET /api/avaliacoes/export/?formato=json` - Exportar dados (admin)
- `GET /api/avaliacoes/export/?formato=csv` - Exportar dados em CSV (admin)

### Perguntas

- `GET /api/perguntas/` - Listar perguntas
- `GET /api/perguntas/{id}/` - Detalhes da pergunta

### Respostas

- `GET /api/respostas/` - Listar respostas do usuário
- `POST /api/respostas/` - Criar resposta
- `GET /api/respostas/{id}/` - Detalhes da resposta
- `PUT /api/respostas/{id}/` - Atualizar resposta
- `DELETE /api/respostas/{id}/` - Excluir resposta

### Atividades Sugeridas

- `GET /api/atividades-sugeridas/` - Listar atividades sugeridas
- `GET /api/atividades-sugeridas/{id}/` - Detalhes da atividade sugerida
- `POST /api/atividades-sugeridas/` - Criar atividade sugerida (admin)
- `PUT /api/atividades-sugeridas/{id}/` - Atualizar atividade sugerida (admin)
- `DELETE /api/atividades-sugeridas/{id}/` - Excluir atividade sugerida (admin)

### Histórico de Acessos

- `GET /api/historico-acessos/` - Listar histórico de acessos (admin)
- `GET /api/historico-acessos/{id}/` - Detalhes do acesso (admin)

## Configuração CORS para Desenvolvimento

Para desenvolvimento local, o backend já está configurado para aceitar solicitações do frontend. Se você encontrar problemas de CORS, verifique se o backend está configurado para aceitar solicitações do endereço do seu frontend.

## Licença

Este projeto está licenciado sob a licença MIT.

## Contato

Para mais informações, entre em contato com [seu_email@example.com].
