import time
import random
from datetime import datetime
from pathlib import Path
import shutil


class CloudStorageAPIMock:
    """
    Simulador de la API de nube para testing.
    No sube nada real: copia el archivo a una carpeta local y
    devuelve una URL "falsa".
    """

    def __init__(
        self,
        base_url: str = "https://mock-api.ejemplo.com",
        api_key: str = None,
        carpeta_destino: str = "mock_uploads",
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.carpeta_destino = Path(carpeta_destino)
        self.carpeta_destino.mkdir(parents=True, exist_ok=True)
        self.uploaded_files = []

    def upload_file(self, file_path: str, destination_name: str, access_token=None) -> dict:
        print(f"🔧 [MOCK] Subiendo archivo: {destination_name}")
        time.sleep(0.5)

        if random.random() < 0.9:
            file_id = f"mock_file_{int(time.time())}_{random.randint(1000, 9999)}"
            mock_url = f"{self.base_url}/files/{file_id}"

            origen = Path(file_path)
            destino = self.carpeta_destino / destination_name
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(origen, destino)

            registro = {
                "original_name": destination_name,
                "mock_url": mock_url,
                "timestamp": datetime.now(),
                "file_path": str(destino),
                "file_id": file_id,
            }
            self.uploaded_files.append(registro)

            return {
                "success": True,
                "url": mock_url,
                "file_id": file_id,
                "message": "✅ Archivo subido exitosamente (MOCK)",
            }
        else:
            return {"success": False, "error": "❌ Error simulado en subida a nube (MOCK)"}

    def get_file_url(self, file_name: str) -> str:
        return f"{self.base_url}/files/mock_{file_name}"

    def list_files(self, access_token=None) -> dict:
        return {
            "success": True,
            "files": self.uploaded_files,
            "message": "📁 Lista de archivos mock",
        }

    def get_upload_stats(self) -> dict:
        return {
            "total_uploads": len(self.uploaded_files),
            "last_upload": self.uploaded_files[-1] if self.uploaded_files else None,
            "all_uploads": self.uploaded_files,
        }
