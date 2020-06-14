# House Explorer Backend 🐍

A server on Flask for my [**house-explorer**](https://github.com/sasha-kir/house-explorer) React app.

Built using Python 3.7 and PostgreSQL.

## Install and run

1. Clone project locally

1. Install poetry

    ```sh
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
    ```

1. Configure poetry to create local venv

    ```sh
    poetry config virtualenvs.in-project true
    ```

1. Create poetry venv and source if needed

    ```sh
    poetry shell
    source .venv/bin/activate
    ```

1. Install dependencies

    ```sh
    poetry install
    ```

1. Create and source .env file

    ```sh
    source .env
    ```

    File should look something like this

    ```sh
    export FLASK_APP=explorer_api
    export FLASK_ENV="development"
    export JWT_KEY={KEY}
    export DATABASE_URL="postgresql://user:pass@localhost:5432/house_explorer"
    export DADATA_KEY={KEY}
    ```

1. Run tests

    ```
    pytest
    ```

1. Run server locally

    ```
    flask run
    ```
