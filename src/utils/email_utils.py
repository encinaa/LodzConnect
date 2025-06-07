import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv
import base64

load_dotenv()

def enviar_correo(destino, asunto, cuerpo, archivo_adjunto=None):
    """api_key = os.environ.get("SENDGRID_API_KEY")"""
    api_key = "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"
    if not api_key:
        raise ValueError("No se encontró la variable de entorno SENDGRID_API_KEY")
    
    print(f"API KEY usada: {api_key[:10]}...")
    message = Mail(
        from_email='uniconectaule@gmail.com',
        to_emails=destino,
        subject=asunto,
        html_content=cuerpo
    )
    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        raise RuntimeError(f"Error enviando correo: {e}")