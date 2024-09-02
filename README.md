# eStracta-Flask-Project


# Comandos para inicialização do projeto
Criação do venv:

```
python -m venv venv
```
Ativação do venv no windows:
```
source venv/scripts/activate
```
Ou no MacOS/Linux:
```
source venv/bin/activate
```
Instalação das requirements:
```
pip install -r requirements.txt
```

# Criando e populando a DataBase
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
flask run
```