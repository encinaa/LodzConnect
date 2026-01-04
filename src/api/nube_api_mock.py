import time
import random
from datetime import datetime
from pathlib import Path
import shutil
import os
import zipfile


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


    def upload_and_extract_zip(self, zip_path: str):
        """
        Simula la subida de un ZIP y su descompresión dentro de mock_storage.
        Extrae los archivos del ZIP manteniendo su estructura.
        """
        if not zipfile.is_zipfile(zip_path):
            return {"success": False, "error": "El archivo no es un ZIP válido."}

        extracted_files = []

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extract_dir = os.path.join(self.base_path, os.path.splitext(os.path.basename(zip_path))[0])
                os.makedirs(extract_dir, exist_ok=True)
                zip_ref.extractall(extract_dir)

                for root, _, files in os.walk(extract_dir):
                    for file_name in files:
                        relative_path = os.path.relpath(os.path.join(root, file_name), self.base_path)
                        extracted_files.append(relative_path)

            return {
                "success": True,
                "uploaded_count": len(extracted_files),
                "files": extracted_files
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_file(self, blob_name: str):
        """
        Simula la eliminación de un archivo o carpeta dentro de mock_storage.
        Si el blob_name representa una carpeta (por ejemplo, contenido descomprimido), la borra entera.
        """
        try:
            local_path = self._get_local_path(blob_name)
            if os.path.isdir(local_path):
                shutil.rmtree(local_path)
                return {"success": True, "deleted_folder": blob_name}
            elif os.path.isfile(local_path):
                os.remove(local_path)
                return {"success": True, "deleted_file": blob_name}
            else:
                return {"success": False, "error": "Archivo o carpeta no encontrada"}
        except Exception as e:
            return {"success": False, "error": str(e)}