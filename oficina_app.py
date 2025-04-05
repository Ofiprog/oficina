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
if "datos_submenu_open" not in st.session_state:
    st.session_state.datos_submenu_open = False

# --- Funciones para interactuar con Supabase ---

def get_clientes():
    """Obtiene todos los clientes de la tabla 'clientes'."""
    try:
        data = supabase.table("clientes").select("*").execute()
        return data.data
    except Exception as e:
        st.error(f"Error al obtener clientes: {e}")
        return []

def insert_cliente(nombre):
    """Inserta un nuevo cliente en la tabla 'clientes'."""
    try:
        supabase.table("clientes").insert({"nombre": nombre}).execute()
        st.success("Cliente agregado correctamente.")
    except Exception as e:
        st.error(f"Error al agregar cliente: {e}")

def update_cliente(id, nombre):
    """Actualiza un cliente existente en la tabla 'clientes'."""
    try:
        supabase.table("clientes").update({"nombre": nombre}).eq("id", id).execute()
        st.success("Cliente actualizado correctamente.")
    except Exception as e:
        st.error(f"Error al actualizar cliente: {e}")

def delete_cliente(id):
    """Elimina un cliente de la tabla 'clientes'."""
    try:
        supabase.table("clientes").delete().eq("id", id).execute()
        st.success("Cliente eliminado correctamente.")
    except Exception as e:
        st.error(f"Error al eliminar cliente: {e}")

# --- Funciones para las Páginas ---
def pagina_dash():
    st.title("🏠 DashBoard")
    st.write("¡Bienvenido a la página de inicio de tu negocio!")

def pagina_datos_clientes():
    st.title("👥 Datos - Clientes")
    # --- CRUD de Clientes ---
    mostrar_clientes()
    agregar_cliente()
    editar_cliente()
    eliminar_cliente()

def mostrar_clientes():
    """Muestra la lista de clientes en una tabla."""
    clientes = get_clientes()
    if clientes:
        st.table(clientes)
    else:
        st.write("No hay clientes registrados.")

def agregar_cliente():
    """Formulario para agregar un nuevo cliente."""
    st.subheader("Agregar Cliente")
    nombre = st.text_input("Nombre")

    if st.button("Agregar"):
        insert_cliente(nombre)
        st.rerun()

def editar_cliente():
    """Formulario para editar un cliente existente."""
    st.subheader("Editar Cliente")
    clientes = get_clientes()
    if clientes:
        cliente_seleccionado = st.selectbox("Selecciona un cliente", clientes, format_func=lambda x: f"{x['nombre']}")
        if cliente_seleccionado:
            nombre = st.text_input("Nombre", value=cliente_seleccionado["nombre"])

            if st.button("Actualizar"):
                update_cliente(cliente_seleccionado["id"], nombre)
                st.rerun()
    else:
        st.write("No hay clientes para editar.")

def eliminar_cliente():
    """Formulario para eliminar un cliente existente."""
    st.subheader("Eliminar Cliente")
    clientes = get_clientes()
    if clientes:
        cliente_seleccionado = st.selectbox("Selecciona un cliente", clientes, format_func=lambda x: f"{x['nombre']}")
        if cliente_seleccionado:
            if st.button("Eliminar"):
                delete_cliente(cliente_seleccionado["id"])
                st.rerun()
    else:
        st.write("No hay clientes para eliminar.")

def pagina_datos_ventas():
    st.title("📈 Datos - Ventas")
    st.write("Aquí podrás gestionar las ventas.")

def pagina_datos_reportes():
    st.title("📊 Datos - Reportes")
    st.write("Aquí podrás ver los reportes.")

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
    .submenu-button {
        background-color: #007acc !important;
        margin-left: 10px !important;
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
                st.session_state.datos_submenu_open = False
            
            datos_button = st.button("Datos")
            if datos_button:
                st.session_state.datos_submenu_open = not st.session_state.datos_submenu_open

            if st.session_state.datos_submenu_open:
                if st.button("Clientes", key="clientes_button",  type="secondary",  help="Gestiona los clientes",):
                    st.session_state.pagina_actual = "Datos-Clientes"
                if st.button("Ventas", key="ventas_button", type="secondary", help="Gestiona las ventas"):
                    st.session_state.pagina_actual = "Datos-Ventas"
                if st.button("Reportes", key="reportes_button", type="secondary", help="Gestiona los reportes"):
                    st.session_state.pagina_actual = "Datos-Reportes"

            if st.button("Productos"):
                st.session_state.pagina_actual = "Productos"
                st.session_state.datos_submenu_open = False
            if st.button("Configuración"):
                st.session_state.pagina_actual = "Configuración"
                st.session_state.datos_submenu_open = False
            if st.button("Cerrar Sesión"):
                logout()

        # --- Page Content ---
        if st.session_state.pagina_actual == "Dashboard":
            pagina_dash()
        elif st.session_state.pagina_actual == "Datos":
            pagina_datos()
        elif st.session_state.pagina_actual == "Datos-Clientes":
            pagina_datos_clientes()
        elif st.session_state.pagina_actual == "Datos-Ventas":
            pagina_datos_ventas()
        elif st.session_state.pagina_actual == "Datos-Reportes":
            pagina_datos_reportes()
        elif st.session_state.pagina_actual == "Productos":
            pagina_productos()
        elif st.session_state.pagina_actual == "Configuración":
            pagina_configuracion()

if __name__ == "__main__":
    main()
