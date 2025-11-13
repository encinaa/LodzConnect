# src/api/nube_api_mock.py
import time
import random
from datetime import datetime

class CloudStorageAPIMock:
    """Simulador de la API de nube para testing"""
    
    def __init__(self, base_url="https://mock-api.ejemplo.com", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.uploaded_files = []  # Para trackear archivos "subidos"
    
    def upload_file(self, file_path, destination_name, access_token=None):
        """
        Simula la subida de archivos a la nube
        """
        print(f"🔧 [MOCK] Subiendo archivo: {destination_name}")
        
        # Simular delay de red
        time.sleep(1)
        
        # Simular éxito/error aleatorio (90% éxito)
        if random.random() < 0.9:
            file_id = f"mock_file_{int(time.time())}_{random.randint(1000,9999)}"
            mock_url = f"{self.base_url}/files/{file_id}"
            
            # Guardar en "historial" de subidas
            self.uploaded_files.append({
                'original_name': destination_name,
                'mock_url': mock_url,
                'timestamp': datetime.now(),
                'file_path': file_path
            })
            
            return {
                'success': True,
                'url': mock_url,
                'file_id': file_id,
                'message': '✅ Archivo subido exitosamente (MOCK)'
            }
        else:
            return {
                'success': False,
                'error': '❌ Error simulado en subida a nube (MOCK)'
            }
    
    def get_file_url(self, file_name):
        """Devuelve URL mock"""
        return f"{self.base_url}/files/mock_{file_name}"
    
    def list_files(self, access_token=None):
        """Lista archivos mock"""
        return {
            'success': True,
            'files': self.uploaded_files,
            'message': '📁 Lista de archivos mock'
        }
    
    def get_upload_stats(self):
        """Estadísticas para debugging"""
        return {
            'total_uploads': len(self.uploaded_files),
            'last_upload': self.uploaded_files[-1] if self.uploaded_files else None,
            'all_uploads': self.uploaded_files
        }