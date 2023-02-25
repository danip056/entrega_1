import sys
import os
sys.path.append(
    os.path.dirname(__file__)
)

from celery import shared_task
from compression import ZipManager, TarGzManager, TarBz2Manager, CompressionFormat
from bd_connection import Session
from models import Task
from api_models import Status
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
MAIL_USERNAME = "grupo8cloud@outlook.com"
MAIL_PASSWORD = "12345678A."
MAIL_FROM = "grupo8cloud@outlook.com"
MAIL_PORT = 587
MAIL_SERVER = "smtp.office365.com"
MAIL_FROM_NAME="Conversión exitosa"
MAIL_STARTTLS = True
MAIL_SSL_TLS = False
USE_CREDENTIALS = True
VALIDATE_CERTS = True


html_message = MIMEText("""<html>
  <head>
    <style>
      .container {
        max-width: 600px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
      }
      .header {
        background-color: #0078d4;
        padding: 20px;
        color: white;
        text-align: center;
      }
      .content {
        padding: 20px;
        background-color: #f0f0f0;
        text-align: center;
      }
      .button {
        background-color: #0078d4;
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin-bottom: 20px;
        cursor: pointer;
      }
      .button:hover {
        background-color: #005d9f;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>¡Conversion Exitosa!</h1>
      </div>
      <div class="content">
        <p>Apreciado cliente,</p>
        <p>Nos complace informarle de que la conversión de su archivo se ha completado y está listo para ser descargado desde nuestro sitio web</p>
        <p>Gracias por utilizar nuestro servicio. Si tiene alguna pregunta o duda, no dude en ponerse en contacto con nosotros.</p>
      </div>
    </div>
  </body>
</html>""" , "html")


def send_email(email_address):
    print(email_address)
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.starttls(context=context) 
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        message = MIMEMultipart("alternative")
        message["Subject"] = "Conversión completa"
        message["From"] = MAIL_FROM
        message["To"] = email_address
        message.attach(html_message)
        server.sendmail(MAIL_FROM, email_address, message.as_string())

    except Exception as e:
        print(e)
    finally:
        server.quit()

@shared_task(autoretry_for=(Exception,), max_retries=3 ,default_retry_delay=240, ignore_result=True)
def process_task(id_task):
    print("task id: {}".format(id_task))
    with Session() as session:
        task = session.query(Task).get(id_task)

        original_stored_file_name = task.original_stored_file_name
        try:
          original_file_ext = CompressionFormat(task.original_file_ext)
        except:
            original_file_ext = CompressionFormat.UNCOMPRESSED
        target_stored_file_name = task.target_stored_file_name
        target_file_ext = CompressionFormat(task.target_file_ext)

        with open(os.path.join(
            STORAGE_DIR,
            original_stored_file_name,
        ), "rb") as original_file:

            if original_file_ext == CompressionFormat.ZIP:
                files_dict = ZipManager.decompress(original_file)
            elif original_file_ext == CompressionFormat.TAR_GZ:
                files_dict = TarGzManager.decompress(original_file)
            elif original_file_ext == CompressionFormat.TAR_BZ2:
                files_dict = TarBz2Manager.decompress(original_file)
            else:
                files_dict = {original_stored_file_name: original_file.read()}

        if target_file_ext == CompressionFormat.ZIP:
            target_file = ZipManager.compress(files_dict)
        elif target_file_ext == CompressionFormat.TAR_GZ:
            target_file = TarGzManager.compress(files_dict)
        elif target_file_ext == CompressionFormat.TAR_BZ2:
            target_file = TarBz2Manager.compress(files_dict)
        else:
            target_file = list(files_dict.values())[0]

        with open(os.path.join(
            STORAGE_DIR,
            target_stored_file_name,),
            "wb") as new_file:
            new_file.write(target_file)
            
        task.status = Status.PROCESSED.value
        session.commit()
        
        email_address = task.user.email
        # send_email(email_address)

        return None

