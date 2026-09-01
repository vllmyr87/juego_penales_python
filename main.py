import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from game.app import PenaltyGame


if __name__ == "__main__":
    db_usuario = os.getenv("DB_USUARIO", "jugador_local")
    db_password = os.getenv("DB_PASWORD", "")

    if db_password:
        print(f"Conectando usuario: {db_usuario}")
    else:
        print(f"Conectando usuario: {db_usuario}")

    PenaltyGame().run()
