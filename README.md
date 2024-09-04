# eStracta-Flask-Project


# Comandos para inicialização do projeto
Criação do venv:

```
python -m venv venv
```
Ativação do venv no windows bash / powershell:
```
# bash
source venv/scripts/activate
 
# powershell
.\venv\Scripts\activate
```
Ou no MacOS/Linux:
```
source venv/bin/activate
```
Instalação das requirements:
```
pip install -r requirements.txt
```

# Criando a database e a tabela 'empresas'
Rode os comando para criar o arquivo de database e migrations:
```
flask db init
```
```
flask db migrate
```
```
flask db upgrade
```

# Rode o programa com o comando:
```
python app.py
```


# Documentação da API
```
http://127.0.0.1:5000/docs
```

# Informações da API

<p>As rotas são protegidas por token de acesso, portanto para acessa-las é preciso fazer o cadastro e o login com um usuário existente</p>
<p>As senhas dos usuários são rasheadas no banco de dados</p>
