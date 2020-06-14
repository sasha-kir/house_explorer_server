from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from explorer_api import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
