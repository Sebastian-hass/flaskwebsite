from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Carpeta temporal para guardar los archivos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/sobremi')
def sobremi():
    return render_template("sobremi1.html")

@app.route('/contacto')
def contacto():
    return render_template("contacto.html")

@app.route('/requisitos')
def requisitos():
    return render_template("requisitos.html")

@app.route('/enviar', methods=['POST'])
def enviar():
    form_data = request.form.to_dict()
    files = request.files

    campos_traducidos = {
        "name": "Nombre completo",
        "email": "Correo electrónico",
        "phone": "Número de teléfono",
        "age": "Edad",
        "antiguedad": "Antigüedad laboral",
        "seguro": "Tipo de seguro",
        "ips_doc": "Documento IPS",
        "iva_doc": "Documento IVA",
        "fpublico_doc": "Documento de Funcionario Público",
        "todos_doc": "Documento Todos",
        "estado_civil": "Estado civil",
        "en_pareja": "¿Está en pareja?",
        "cedula": "Número de cédula",
        "income": "Ingresos mensuales",
        "message": "Mensaje adicional"
    }

    # Construir el mensaje en HTML
    mensaje = "<h2>Nuevo formulario recibido</h2><ul>"
    for key, value in form_data.items():
        label = campos_traducidos.get(key, key)
        mensaje += f"<li><strong>{label}:</strong> {value}</li>"
    mensaje += "</ul>"

    # Crear el correo
    msg = EmailMessage()
    msg.set_content("Tu cliente ha enviado un formulario. Revisa el mensaje en HTML para más detalles.")
    msg.add_alternative(mensaje, subtype='html')
    msg['Subject'] = 'Formulario enviado desde la web'
    msg['From'] = os.getenv("GMAIL_USER")
    msg['To'] = 'jesusalonsoarias4@gmail.com'

    # Adjuntar archivos si existen
    for field in ['ips_doc', 'iva_doc', 'fpublico_doc', 'todos_doc']:
        if field in files:
            file = files[field]
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                with open(filepath, 'rb') as f:
                    file_data = f.read()
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=filename)

                # Eliminar archivo temporal después de adjuntarlo
                os.remove(filepath)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
            smtp.send_message(msg)
        return redirect(url_for('gracias'))
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}", 500

@app.route('/gracias')
def gracias():
    return render_template("gracias.html")

if __name__ == '__main__':
    app.run(port=8000)
