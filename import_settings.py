import os
import dotenv

dotenv.load_dotenv(verbose=True)

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
dotenv.load_dotenv(dotenv_path)

gemini_api = os.getenv("GEMINI_API_KEY")
voicevox_exe = os.getenv("VOICEVOX_EXE")
voicevox_host = os.getenv("VOICEVOX_HOST")
voicevox_port = os.getenv("VOICEVOX_PORT")