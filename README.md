# Adopet API

![](https://img.shields.io/github/last-commit/HenriqueCCdA/adopet-api?style=plasti&ccolor=blue)
![](https://img.shields.io/badge/Autor-Henrique%20C%20C%20de%20Andrade-blue)
[![codecov](https://codecov.io/gh/HenriqueCCdA/adopet-api/branch/main/graph/badge.svg?token=ciUVhvgHSW)](https://codecov.io/gh/HenriqueCCdA/adopet-api)
[![Python application](https://github.com/HenriqueCCdA/adopet-api/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/HenriqueCCdA/adopet-api/actions/workflows/CI.yml)

Desafio backend 6 da alura.

| :placard: Vitrine.Dev |     |
| -------------  | --- |
| :sparkles: Nome        | `Apopet Api`
| :label: Tecnologias | `Django Rest Framework`, `Python`, `Postgres`, `Pytest`, `Docker`, `swagger`
| :rocket: URL         |
| :fire: Desafio     | https://www.alura.com.br/challenges/back-end


## Documantação da API

[Postman](https://documenter.getpostman.com/view/18852890/2s93RRvsgF)

A documentação da API (swagger) esta disponível na rota `/docs/`. Portanto localmente `http://localhost:8000/docs/`.


## Variaveis de ambiente

Foi usando o `python-decouple` portanto primeiro as variaveis são procuradas nas variaveis de ambiente. Se não forem achadas são lá elas são procuradas no arquivo `.env`.

Do ambiente de desenvolvimento basta definir o arquivo `.env`:

```
DEBUG=True
SECRET_KEY=Sua_chave_secreta_aqui!
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://adopet_user:123456@localhost:5432/adopet_user
DOC_API=True
```

## Rodando o projeto via docker.

Você precisa primeiro cmpiar o docker compose de desenvolvimento para a raiz do projeto

```console
cp docker/docker-compose.dev.yml docker-compose.yml
```

Agora você pode subir a aplicação com

```console
make docker_build_and_up
```

A aplicação ficará disponivel em `http://localhost:8000/`

Todas as variaveis de ambiente usadas no conteiner são as definida no arquivo `.env` exceto o `DATABASE_URL` que é sobrescrito dentro do docker compose. Além disso foi utilizazndo `PYTHONBREAKPOINT=ipdb.set_trace` portanto é necessario usar o `pytest` com `-s` caso você queria usar `breakpoints`.

### Outros comandos

* rodando os testes : `make docker_pytest`
* aplicando as migrações: `make docker_migrate`
* gerando as migrações: `make docker_makemigrations`
* criando o superusuario: `docker_create_admin`
* subindo os containers: `make docker_up`
* parando os containers: `make docker_down`
* gerando a imagem da aplicação: `make build`
* subindo o container do banco de dados: `make up_db`
