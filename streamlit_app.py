import streamlit as st
from supabase import create_client, Client

# --- Supabase Setup (Mantén tu configuración) ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase: Client = create_client(url, key)

# --- Streamlit App ---
st.set_page_config(page_title="App Oficina", layout="wide")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

# --- Funciones para las Páginas ---
def pagina_dash():
    st.title("🏠 DashBoard")
    st.write("¡Bienvenido a la página de inicio de tu negocio!")

def pagina_datos():
    st.title("👥 Gestión de Datos")
    st.write("Aquí podrás gestionar los Datos de tu aplicación.")
    

def pagina_productos():
    st.title("📦 Gestión de Productos")
    st.write("Aquí podrás gestionar los productos de tu negocio.")

def pagina_configuracion():
    st.title("⚙️ Configuración")
    st.write("Aquí podrás configurar las opciones de tu aplicación.")

# --- Login Form ---
def login_form():
    st.subheader("Iniciar Sesión")
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        try:
            data = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if data.user:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"¡Bienvenido, {email}!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")
        except Exception as e:
            st.error(f"Error al iniciar sesión: {e}")

# --- Logout ---
def logout():
    try:
        supabase.auth.sign_out()
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.success("Sesión cerrada correctamente.")
        st.rerun()
    except Exception as e:
        st.error(f"Error al cerrar sesión: {e}")

# --- CSS Personalizado para los Botones del Sidebar ---
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #0099ff; /* Color de fondo */
        color: white; /* Color del texto */
        border: none; /* Sin borde */
        border-radius: 5px; /* Bordes redondeados */
        padding: 10px 20px; /* Espaciado interno */
        text-align: center; /* Centrar texto */
        text-decoration: none; /* Sin subrayado */
        display: inline-block; /* Mostrar en línea */
        font-size: 16px; /* Tamaño de fuente */
        margin: 4px 2px; /* Margen */
        cursor: pointer; /* Cursor de mano */
        transition-duration: 0.4s; /* Transición suave */
    }
    div.stButton > button:hover {
        background-color: #007acc; /* Color de fondo al pasar el mouse */
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); /* Sombra al pasar el mouse */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Main App Logic ---
def main():
    if not st.session_state.logged_in:
        login_form()
    else:
        # --- Sidebar ---
        with st.sidebar:
            st.title("Menú")
            if st.button("Dashboard"):
                st.session_state.pagina_actual = "Dashboard"
            if st.button("Datos"):
                st.session_state.pagina_actual = "Datos"
            if st.button("Productos"):
                st.session_state.pagina_actual = "Productos"
            if st.button("Configuración"):
                st.session_state.pagina_actual = "Configuración"
            if st.button("Cerrar Sesión"):
                logout()

        # --- Page Content ---
        if st.session_state.pagina_actual == "Dashboard":
            pagina_dash()
        elif st.session_state.pagina_actual == "Datos":
            pagina_datos()
        elif st.session_state.pagina_actual == "Productos":
            pagina_productos()
        elif st.session_state.pagina_actual == "Configuración":
            pagina_configuracion()

if __name__ == "__main__":
    main()



