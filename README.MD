# Adopet API

Desafio backend 6 da alura.

| :placard: Vitrine.Dev |     |
| -------------  | --- |
| :sparkles: Nome        | `Apopet Api`
| :label: Tecnologias | `Django Rest Framework`, `Python`, `Postgres`, `Pytest`
| :rocket: URL         |
| :fire: Desafio     | https://www.alura.com.br/challenges/back-end


## Documantação da API

[Postman](https://documenter.getpostman.com/view/18852890/2s93RRvsgF)


## Variaveis de ambiente

Foi usando o `python-decouple` portanto primeiro as variaveis são procuradas nas variaveis de ambiente. Se não forem achadas são lá elas são procuradas no arquivo `.env`.

Do ambiente de desenvolvimento basta definir o arquivo `.env`:

```
DEBUG=True
SECRET_KEY=Sua_chave_secreta_aqui!
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://adopet_user:123456@localhost:5432/adopet_user

```


## Rodando o projeto via docker.

Você precisa primeiro compiar o docker compose de desenvolvimento para a raiz do projeto

```
cp docker/docker-compose.dev.yml docker-compose.yml
```

Agora você pode subir a aplicação com

```
make docker_build_and_up
```

A aplicação estará disponivel em `http://localhost:8000/`

Todas as variaveis de ambiente são as definida no arquivo `.env` exceto o `DATABASE_URL`que é sobrescrito dentro do docker compose.

### Outros comando

* rodando os testes : `make docker_pytest`
* aplicando as migrações: `make docker_migrate`
* gerando as migrações: `make docker_makemigrations`
* criando o superusuario: `docker_create_admin`
* subindo os containers: `make docker_up`
* parando os containers: `make docker_down`
* gerando a imagem da aplicação: `make build`
* subindo o container do banco de dados: `make up_db`

```
make docker_pytest
```
