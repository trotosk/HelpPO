import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
from templates import get_general_template, get_code_template, get_criterios_Aceptacion_template
# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Asistente PO con Claude",
    page_icon="🤖",
    layout="wide"
)

# Título de la aplicación
st.title("🤖 Asistente PO con Claude de Anthropic")

# Inicializar el cliente de Anthropic
@st.cache_resource
def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    
    if not api_key:
        st.error("No se encontró la clave API de Anthropic. Por favor, configura la variable de entorno ANTHROPIC_API_KEY.")
        st.stop()
    
    return anthropic.Anthropic(api_key=api_key)

client = get_client()
def generate_response(template_type="PO Casos exito"):

# Definir templates para diferentes casos de uso
# Selección de template
    if template_seleccionado == "general":
        template = get_general_template()
    elif template_seleccionado == "PO Casos exito":
        template = get_criterios_Aceptacion_template()
    elif template_seleccionado == "code":
        template = get_code_template()

    return template
# Panel lateral para configuración
with st.sidebar:
    st.header("Configuración")
    
    # Selección de modelo
    modelo = st.selectbox(
        "Modelo de Claude",
        ["claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    )
    
    # Selección de template
    template_seleccionado = st.selectbox(
        "Tipo de consulta",
        ["PO Casos exito", "general", "code"]
    )
    

    # Parámetros de generación
    st.subheader("Parámetros")
    temperatura = st.slider("Temperatura", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.slider("Máximo de tokens", min_value=100, max_value=4096, value=1000, step=100)

# Inicializar el estado de sesión para el área de texto si no existe
if 'texto_usuario' not in st.session_state:
    st.session_state.texto_usuario = ""

# Función para borrar el contenido del área de texto
def borrar_texto():
    st.session_state.texto_usuario = ""

# Área principal para entrada y respuesta
st.subheader("Ingresa tu contenido")
input_text = st.text_area("", height=150, placeholder="Escribe aquí tu texto o consulta...",value=st.session_state.texto_usuario,key="texto_usuario")

# Historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Crear dos columnas de igual ancho
col1, col2 = st.columns([0.5, 2])

# Colocar un botón en cada columna
with col1:
    botonEnviar = st.button("Enviar")

with col2:
    botonBorrar = st.button("Borrar contenido", on_click=borrar_texto)

# Botón para enviar
if botonEnviar:
    if not input_text:
        st.warning("Por favor, ingresa un texto.")
    else:
        with st.spinner("Procesando..."):
            try:
                # Formatear el prompt según el template seleccionado
                prompt_template = generate_response(template_seleccionado)
                
                # Reemplazar variables en el template
                prompt = prompt_template.format(input=input_text)
                
                # Guardar mensaje del usuario
                st.session_state.messages.append({"role": "user", "content": input_text})
                
                # Llamar a la API de Anthropic
                response = client.messages.create(
                    model=modelo,
                    max_tokens=max_tokens,
                    temperature=temperatura,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Obtener respuesta
                respuesta = response.content[0].text
                
                # Guardar respuesta de Claude
                st.session_state.messages.append({"role": "assistant", "content": respuesta})

                
            except Exception as e:
                st.error(f"Error al comunicarse con la API de Anthropic: {str(e)}")

# Botón para borrar el contenido
#st.button("Borrar contenido", on_click=borrar_texto)

# Mostrar historial de conversación
st.subheader("Historial de conversación")
contenido = ""
for msg in reversed(st.session_state.messages):
    if msg["role"] == "user":
        st.info(msg["content"])
        st.success(contenido)
    else:
        contenido = msg["content"]
        

# Instrucciones de configuración en el footer
st.markdown("---")
