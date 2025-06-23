# 💸 Gestor de Gastos Inteligente con IA y OCR

Aplicación web desarrollada en Flask que permite registrar, analizar y clasificar automáticamente tus gastos personales mediante Inteligencia Artificial y tecnologías de OCR. Diseñada para ofrecer una experiencia de usuario fluida y un análisis financiero personalizado.

---

## 🧠 Características principales

- 📝 Registro de gastos manual o automático mediante imágenes y PDF.
- 📷 Integración con OCR (`Tesseract` + `pdfplumber`) para extraer texto de tickets y facturas.
- 🤖 Clasificación automática de gastos por categoría con IA entrenada en ejemplos reales.
- 🧾 Edición y confirmación de atributos extraídos antes de guardar el gasto.
- 📊 Panel de control con resúmenes financieros y comparaciones por mes.
- 💡 Reglas inteligentes que detectan hábitos de consumo y generan recomendaciones.
- 🧾 Compatible con imágenes escaneadas o PDFs digitales.

---

## 🚀 Tecnologías utilizadas

| Herramienta         | Uso                                         |
|---------------------|---------------------------------------------|
| **Python**          | Lenguaje principal                          |
| **Flask**           | Framework backend web                       |
| **mysql-connector** | Conexión y gestión de base de datos MySQL   |
| **Tesseract**       | Motor OCR para reconocimiento de texto      |
| **pdfplumber**      | Extracción de texto e imágenes de PDFs      |
| **Pillow**          | Procesamiento de imágenes                   |
| **Scikit-learn**    | Clasificación automática de gastos (IA)     |
| **joblib**          | Serialización de modelos de IA              |

---

## 🛠️ Instalación y ejecución local

```bash
# Clona el repositorio
git clone https://github.com/tu-usuario/gestor-gastos-ia.git
cd gestor-gastos-ia

# Crea entorno virtual
python -m venv venv
# Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la aplicación
flask run
```

---

## ⚙️ Requisitos adicionales

- **Tesseract OCR**  
  Descarga e instala desde: https://github.com/tesseract-ocr/tesseract  
  Asegúrate de agregar la ruta de instalación a tu variable de entorno `PATH` o configúrala en tu código.

- **MySQL Server**  
  Debes tener un servidor MySQL en ejecución y configurar las credenciales en el archivo de conexión.

---

## 📂 Estructura del proyecto

```
src/
├── app.py
├── database/
│   ├── __init__.py
│   └── helpeDB.py
├── IA/
│   ├── dataset/
│   ├── models/
│   └── utils/
│       ├── train_model.py
│       ├── image_processing.py
│       └── tools.py
├── routes/
│   └── main.py
└── templates/
    ├── base.html
    ├── home.html
    └── prueba3.html
```

---

## 🧪 Entrenamiento del modelo de IA

El modelo de clasificación se entrena con ejemplos reales de gastos. Puedes modificar o ampliar el dataset en `src/IA/dataset/`.  
Para reentrenar el modelo ejecuta:

```bash
python src/IA/utils/train_model.py
```

---

## ✨ Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o un pull request para sugerir mejoras o reportar errores.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

## 🙋‍♂️ Autor

Desarrollado por ignacioz21.
