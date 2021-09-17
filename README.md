# Pokemon-app

Back-end Technical Test.

## Description

App to save pokemon from an evolution chain

## Installation

```bash
docker-compose build
```

## Run

```bash
docker-compose up
```

## Usage

1. Command that receives as its only parameter an ID, representing
   the Evolution Chain

```bash
#docker-compose run app sh -c "python manage.py evolution_chains <id>" --rm
docker-compose run app sh -c "python manage.py evolution_chains 100" --rm
```

2. Expose a Web Service which only parameter is the “name” of a Pokemon
   search.

```bash
http://localhost:8000/api/pokemon/<name>
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
