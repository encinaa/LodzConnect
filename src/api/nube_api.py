# src/api/nube_api.py
from azure.storage.blob import BlobClient
from urllib.parse import urlparse, parse_qs, urlencode
import zipfile
import os


class CloudStorageAPI:
    """
    API real contra Azure Blob Storage usando una URL SAS de contenedor.
    - La URL SAS completa se pasa en el constructor (sas_url).
    - A partir de esa URL se construyen las URLs de cada blob.
    """

    def __init__(self, sas_url: str):
        # URL SAS completa del contenedor, por ejemplo:
        # https://lodzconnect.blob.core.windows.net/files?sp=...&sig=...
        self.sas_url = sas_url

        parsed = urlparse(sas_url)
        # Parte base sin query (hasta /files)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        # Parámetros de la query (SAS tokens)
        self.query_params = parse_qs(parsed.query, keep_blank_values=True)

    def _build_blob_url(self, blob_name: str) -> str:
        """
        Construye la URL SAS de un blob concreto dentro del contenedor.
        """
        query = urlencode(self.query_params, doseq=True)
        # Ojo con las dobles barras, por eso strip("/")
        return f"{self.base_url.rstrip('/')}/{blob_name}?{query}"

    def upload_file(self, file_path: str, destination_name: str, access_token=None):
        """
        Sube un archivo a Azure Blob Storage.
        - file_path: ruta local del archivo
        - destination_name: nombre con el que se guardará en el contenedor
        """
        try:
            blob_url = self._build_blob_url(destination_name)
            blob_client = BlobClient.from_blob_url(blob_url)

            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            return {
                "success": True,
                "url": blob_url,
                "file_id": destination_name
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_file_url(self, file_name: str) -> str:
        """
        Devuelve la URL SAS de un blob ya existente.
        """
        return self._build_blob_url(file_name)

    def list_files(self, access_token=None):
        """
        Opcional: no la usamos ahora. Podrías implementarla con ContainerClient si quisieras.
        De momento devolvemos un mensaje informativo.
        """
        return {
            "success": False,
            "error": "list_files no implementado para Azure en esta práctica"
        }

    def delete_file(self, blob_name: str):
            """
            Elimina un archivo (blob) del contenedor en Azure Blob Storage.
            - blob_name: nombre exacto del archivo dentro del contenedor (por ejemplo 'backup_2025.zip')
            """
            try:
                blob_url = self._build_blob_url(blob_name)
                blob_client = BlobClient.from_blob_url(blob_url)
                blob_client.delete_blob()
                return {
                    "success": True, "deleted": blob_name
                }
            except Exception as e:
                return {"success": False, "error": str(e)
                }
            
    #MIRARLO SUBE LOS ZIP PERO NO LOS DESCOMPRIME
    def upload_and_extract_zip(self, zip_path: str, access_token: str = None):
        """
        Descomprime un archivo ZIP local y sube todos sus contenidos a Azure Blob Storage,
        manteniendo la estructura de carpetas interna.
        """
        import tempfile, shutil, zipfile, os
        from azure.storage.blob import BlobClient

        if not zipfile.is_zipfile(zip_path):
            return {"success": False, "error": "El archivo no es un ZIP válido."}

        uploaded_files = []
        temp_dir = None

        try:
            # 1️⃣ Crear carpeta temporal segura para extraer
            temp_dir = tempfile.mkdtemp(prefix="extract_zip_")
            print(f"📦 Extrayendo ZIP en: {temp_dir}")

            # 2️⃣ Extraer todos los archivos del ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # 3️⃣ Recorrer todos los archivos reales dentro del directorio extraído
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    local_file_path = os.path.join(root, file_name)

                    # Crear ruta relativa al directorio base del ZIP (para mantener estructura)
                    relative_path = os.path.relpath(local_file_path, temp_dir)
                    blob_name = relative_path.replace("\\", "/")  # usar rutas compatibles con Azure

                    print(f"☁️ Subiendo: {blob_name}")

                    # Crear cliente del blob
                    blob_url = self._build_blob_url(blob_name)
                    blob_client = BlobClient.from_blob_url(blob_url)

                    # Subir archivo descomprimido
                    with open(local_file_path, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True)

                    uploaded_files.append(blob_name)

            # 4️⃣ Limpiar el directorio temporal
            shutil.rmtree(temp_dir, ignore_errors=True)

            print(f"✅ Subida completa: {len(uploaded_files)} archivos")
            return {
                "success": True,
                "uploaded_count": len(uploaded_files),
                "files": uploaded_files,
                "url": self.base_url
            }

        except Exception as e:
            if temp_dir:
                shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"❌ Error descomprimiendo/subiendo ZIP: {e}")
            return {"success": False, "error": str(e)}
        