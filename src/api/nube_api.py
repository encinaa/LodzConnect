"""AQUI ME DAIS VUESTRA API Q CONECTA CON LA NUBE"""

# Ejemplo cutron
class CloudStorageAPI:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
    
    def upload_file(self, file_path, destination_name, access_token=None):
        # Sube archivo a la nube
        pass
    
    def get_file_url(self, file_name):
        # Devuelve URL para acceder al archivo
        pass
    
    def list_files(self, access_token=None):
        # Lista archivos en la nube
        pass



"""import requests
import os

class CloudStorageAPI:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
    
    def upload_file(self, file_path, destination_name, access_token=None):
        #Sube un archivo a la nube
        
        try:
            # Preparar headers con autenticación
            headers = {}
            if access_token:
                headers['Authorization'] = f'Bearer {access_token}'
            elif self.api_key:
                headers['X-API-Key'] = self.api_key
            
            # Leer archivo
            with open(file_path, 'rb') as file:
                files = {'file': (destination_name, file)}
                
                response = requests.post(
                    f"{self.base_url}/upload",
                    files=files,
                    headers=headers,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'url': data.get('url'),
                    'file_id': data.get('file_id')
                }
            else:
                return {
                    'success': False,
                    'error': f"Error {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_file_url(self, file_name):
        #Obtiene URL para descargar archivo
        
        return f"{self.base_url}/files/{file_name}"
    
    def list_files(self, access_token=None):
        #Lista archivos en la nube
        
        try:
            headers = {}
            if access_token:
                headers['Authorization'] = f'Bearer {access_token}'
            
            response = requests.get(
                f"{self.base_url}/files",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}"""