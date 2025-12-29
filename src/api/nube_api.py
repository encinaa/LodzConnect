# src/api/nube_api.py
from azure.storage.blob import BlobClient
from urllib.parse import urlparse, parse_qs, urlencode


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
