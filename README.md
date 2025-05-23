# Happy Kitty Slot Machine

## Descrição

Happy Kitty Slot Machine é uma aplicação web simples de jogo de loteria (máquina caça-níquel) desenvolvida em Flask e PostgreSQL. Os jogadores autenticam-se com CPF e podem girar três rolos em busca de figuras iguais para ganhar pontos.

## Tecnologias Utilizadas

* **Backend**: Python 3.9, Flask, Flask-Login, Flask-Migrate, Flask-SQLAlchemy
* **Banco de Dados**: PostgreSQL
* **Front-end**: HTML5, CSS3, JavaScript (vanilla) e PH Icons (para símbolos)
* **Ferramentas**: Git, Alembic, Gunicorn
* **Deploy**: Render

## Funcionalidades

* Autenticação de usuário via CPF
* Controle de pontuação e número de jogadas restantes
* Custo por jogada configurável (padrão: 100 pontos)
* Quadro de probabilidade e recompensa:

  * 1 diamante = +50 pontos
  * 2 diamantes = +100 pontos
  * 3 diamantes = +150 pontos
  * 1 sino = -50 pontos
  * 2 sinos = -100 pontos
  * 3 sinos = -150 pontos
  * 3 coroas = jackpot
* Sistema de animação dos rolos e celebração com confetes
* APIs REST para cadastro/atualização de jogadores e execução do spin

## Instalação e Configuração Local

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/HappyKittySlotMachine.git
   cd HappyKittySlotMachine
   ```

2. **Crie e ative o ambiente virtual**:

   ```bash
   python3.9 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente**:

   * Crie um arquivo `.env` na raiz do projeto com as chaves abaixo:

     ```env
     SECRET_KEY=seu-secret-key
     DATABASE_URL=postgresql://user:password@host:porta/dbname
     COST_PER_PLAY=100
     MAX_ATTEMPTS=10
     ```

5. **Inicialize o banco de dados**:

   ```bash
   flask db upgrade
   ```

6. **Execute a aplicação**:

   ```bash
   flask run
   ```

   Acesse em `http://localhost:5000`.
7. Cadastre um jogador no banco de dados (para teste usar o 12345678900)

## Modificando Probabilidades

O jogo sorteia figuras no arquivo `app/services.py`:

```python
FIGURES = ['1','2','3','4','5','6','7']
results = [random.choice(FIGURES) for _ in range(3)]
```

* Para alterar probabilidades de uma figura, basta duplicar seu valor na lista. Exemplo: dobrar chance do diamante (`'3'`):

  ```python
  FIGURES = ['1','2','3','3','4','5','6','7']
  ```
* Para usar pesos diferentes, substitua por `random.choices`:

  ```python
  symbols = ['1','2','3','4','5','6','7']
  weights = [10,10,20,10,10,10,10]
  results = random.choices(symbols, weights=weights, k=3)
  ```

## Deploy no Render

1. **Envie o código ao GitHub**.
2. **Crie um novo Web Service** em Render:

   * Ambiente: Python 3
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn run:app --workers 4 --bind 0.0.0.0:$PORT`
   * **Root Directory**: `/`
3. **Procfile** (já incluído):

   ```text
   web: gunicorn run:app --workers 4 --bind 0.0.0.0:$PORT
   ```
4. **Defina variáveis de ambiente** no painel do Render:

   * SECRET\_KEY
   * DATABASE\_URL
   * COST\_PER\_PLAY
   * MAX\_ATTEMPTS
5. **Migrations**:

   * Para contas gratuitas que não suportam post-deploy scripts, acesse o Shell do serviço e execute:

     ```bash
     flask db upgrade
     ```

## Estrutura do Projeto

```
├── app/
│   ├── static/
│   │   ├── css/styles.css
│   │   └── js/slot.js
│   ├── templates/
│   │   ├── index.html
│   │   └── login.html
│   ├── auth_page.py
│   ├── auth_api.py
│   ├── data_api.py
│   ├── models.py
│   ├── services.py
│   └── extensions.py
├── migrations/
├── run.py
├── config.py
├── requirements.txt
├── .env
├── Procfile
└── README.md
```

## Endpoints da API

* **POST** `/api/auth/login` – Login e criação de usuário
* **POST** `/api/players` – Adicionar ou atualizar jogador e recursos
* **POST** `/spin` – Executa o spin (motor do jogo)

## Logs

* Os logs da aplicação são gerados na pasta `logs/`. Ajuste o nível de log no `config.py` conforme necessário.

## Contribuindo

1. Fork este repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m "feat: descrição da funcionalidade"`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a [MIT License](LICENSE).
