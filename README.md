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

![Captura de tela de 2023-04-18 00-33-30](https://user-images.githubusercontent.com/37959973/232665132-9077c415-d738-4ea0-ad1c-f519740a962e.png?text=imagem_do_projeto#vitrinedev)


# 1) Documantação da API

[Postman](https://documenter.getpostman.com/view/18852890/2s93RRvsgF)

A documentação da API (swagger) esta disponível na rota `/docs/`.

# 2) Funcionalidades

## 2.1) Tutors

- `Cadastrar`: Salvar tutor através de um `POST /tutor/`.

- `Buscar por id`: Busca Tutor por ID através de um `GET /tutor/{ID}/`, onde *{ID}* é o identificador do Tutor.
  - É necessário estar autenticado.

- `Buscar todos`: Busca paginada de tutores através de um `GET /tutor/`.
  - É necessário estar autenticado.

- `Atualizar`: Atualizar Tutor através de um `PATCH /tutor/{ID}/`, onde *ID* é o identificador do Tutor.
  - Apenas o próprio usuário Tutor pode atualizar seus dados.
  - É necessário estar autenticado.

- `Deletar`: Deletar Tutor através de um `DELETE /tutor/{ID}`, onde *{ID}* é o identificador do Tutor.
  - Apenas o próprio usuário Tutor pode se deletar.
  - É necessário estar autenticado.
  - O objeto não é deletado de verdade do banco de dados (`soft delete`)

## 2.2) Shelter

- `Cadastrar`: Salvar Shelter através de um `POST /shelter/`.

- `Buscar todos`: Busca paginada de shelters através de um `GET /shelter/`.
  - É necessário estar autenticado.

- `Buscar por id`: Busca Shelter por ID através de um `GET /shelter/{ID}/`, onde *{ID}* é o identificador do Shelter.
  - É necessário estar autenticado.

- `Atualizar`: Atualizar Shelter através de um `PATCH /shelter/{ID}/`, onde *ID* é o identificador do Shelter,
  os novos dados do abrigo devem ser enviados no corpo da requisição.
  - Apenas o próprio usuário Shelter pode atualizar seus dados.
  - É necessário estar autenticado.

- `Deletar`: Deletar Shelter através de um `DELETE /shelter/{ID}`, onde *{ID}* é o identificador do Shelter.
  - Apenas o próprio usuário Shelter pode se deletar.
  - É necessário estar autenticado.
  - O objeto não é deletado de verdade do banco de dados (`soft delete`)
  - Todos os `pets` associando as este abrigo também são deletados.

## 2.3) Pet
- `Cadastrar`: Salvar Pet através de um `POST /pet/` com as informações.
  - Apenas Shelters podem cadastrar Pets.

- `Buscar todos`: Busca paginada de pets através de um `GET /pets/`.
  - É necessário estar autenticado.

- `Buscar por id`: Busca Pet por ID através de um `GET /pet/{ID}/`, onde *{ID}* é o identificador do Pet.
  - É necessário estar autenticado.

- `Atualizar`: Atualizar Pet através de um `PATH /pet/{ID}/`, onde *ID* é o identificador do Pet.
  - Apenas o Abrigo que cadastrou o Pet pode atualiza-lo.

- `Deletar`: Deletar Pet através de um `DELETE /pet/{ID}`, onde *{ID}* é o identificador do Pet.
  - Apenas o Abrigo que cadastrou o Pet pode deleta-lo.
  - objeto não deletado de verdade do banco de dados (`soft delete`)
  <!-- - Pet relacionado a uma Adoption não pode ser deletado. -->

## 2.4 Adoption
- `Adotar`: Solicitar uma adoção de um Pet através de um `POST /adoption/`.
  - Apenas usuários do tipo tutor podem solicitar uma adoção.
  - É necessário estar autenticado
  - Apenas Pets não é adotados podem receber uma solicitação de adoção.

- `Buscar todos`: Busca paginada de adoções através de um `GET /adoption/`.
  - É necessário estar autenticado.
  <!-- - Busca somente adoções relacionadas ao usuário autenticado (Shelter ou Guardian). -->

<!-- - `Atualizar status`: Atualização de status através de um ` /api/adoptions/{ID}/status` com a informação *status*
  em um JSON no corpor da requisição. Os status possíveis são *ANALYSING*, *CONCLUDED* e *CANCELED*. Apenas usuários do tipo
  Shelter atualizar status.
  - Uma adoção só pode ter o status atualizado pelo Shelter relacionado na adoção.<br> -->

- `Deletar`: Deletar uma adoção através de um `DELETE /adoption/{ID}`, onde *{ID}* é o identificador da Adoção.
  - O objeto é deletado de verdade do banco de dados.(`hard delete`)
  - Uma adoção só pode ser deletada pelo Shelter relacionado na adoção.


# 3) Variaveis de ambiente

Foi usando o `python-decouple` portanto primeiro as variaveis são procuradas nas variaveis de ambiente. Se não forem achadas são lá elas são procuradas no arquivo `.env`.

Do ambiente de desenvolvimento basta definir o arquivo `.env`:

```
DEBUG=True
SECRET_KEY=Sua_chave_secreta_aqui!
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://adopet_user:123456@localhost:5432/adopet_user
DOC_API=True
```

# 4) Rodando o projeto via docker.

Você precisa primeiro copiar o docker compose de desenvolvimento para a raiz do projeto

```console
cp docker/docker-compose.dev.yml docker-compose.yml
```

Agora você pode subir a aplicação com

```console
make docker_build_and_up
```

A aplicação ficará disponivel em `http://localhost:8000/`

Todas as variaveis de ambiente usadas no conteiner são as definida no arquivo `.env` exceto o `DATABASE_URL` que é sobrescrito dentro do docker compose. Além disso foi utilizazndo `PYTHONBREAKPOINT=ipdb.set_trace` portanto é necessario usar o `pytest` com `-s` caso você queria usar `breakpoints`.

## 4.1) Outros comandos

* rodando os testes : `make docker_pytest`
* aplicando as migrações: `make docker_migrate`
* gerando as migrações: `make docker_makemigrations`
* criando o superusuario: `docker_create_admin`
* subindo os containers: `make docker_up`
* parando os containers: `make docker_down`
* gerando a imagem da aplicação: `make build`
* subindo o container do banco de dados: `make up_db`
