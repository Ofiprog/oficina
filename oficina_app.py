import streamlit as st
from supabase import create_client, Client
from modules.cajas import get_cajas, insert_caja, update_caja, delete_caja
from modules.clientes import get_clientes, insert_cliente, update_cliente, delete_cliente
from modules.Tipomov import get_tipo_movimientos, insert_tipo_movimiento, update_tipo_movimiento, delete_tipo_movimiento
from modules.Dias import get_dias, insert_dia, update_dia, delete_dia


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
        # Ordenar la lista de clientes por el campo "Nombre"
        clientes_ordenados = sorted(clientes, key=lambda cliente: cliente["Nombre"])
        # Reorganizar las columnas
        clientes_reorganizados = []
        for cliente in clientes_ordenados:
            clientes_reorganizados.append({
                "id": cliente["id"],
                "Nombre": cliente["Nombre"],
                "created_at": cliente["created_at"]
            })
        
        st.table(clientes_reorganizados)
    else:
        st.write("No hay clientes registrados.")

def agregar_cliente():
    """Formulario para agregar un nuevo cliente."""
    st.subheader("Agregar Cliente")
    nombre = st.text_input("Nombre")

    if st.button("Agregar"):
        insert_cliente(nombre)
        nombre = ""
        st.rerun()
        

def editar_cliente():
    """Formulario para editar un cliente existente."""
    st.subheader("Editar Cliente")
    clientes = get_clientes()
    if clientes:
        clientes_con_nombre = [cliente for cliente in clientes if 'Nombre' in cliente]
        if clientes_con_nombre:
            # Se agrega la key="editar_cliente_selectbox"
            cliente_seleccionado = st.selectbox("Selecciona un cliente", clientes_con_nombre, format_func=lambda x: f"{x['Nombre']}", key="editar_cliente_selectbox")
            if cliente_seleccionado:
                nombre = st.text_input("Nombre", value=cliente_seleccionado["Nombre"])

                if st.button("Actualizar"):
                    update_cliente(cliente_seleccionado["id"], nombre)
                    st.rerun()
        else:
            st.write("No hay clientes con el campo 'Nombre' para editar.")
    else:
        st.write("No hay clientes para editar.")

def eliminar_cliente():
    """Formulario para eliminar un cliente existente."""
    st.subheader("Eliminar Cliente")
    clientes = get_clientes()
    if clientes:
        clientes_con_nombre = [cliente for cliente in clientes if 'Nombre' in cliente]
        if clientes_con_nombre:
            # Se agrega la key="eliminar_cliente_selectbox"
            cliente_seleccionado = st.selectbox("Selecciona un cliente", clientes_con_nombre, format_func=lambda x: f"{x['Nombre']}", key="eliminar_cliente_selectbox")
            if cliente_seleccionado:
                if st.button("Eliminar"):
                    delete_cliente(cliente_seleccionado["id"])
                    st.rerun()
        else:
            st.write("No hay clientes con el campo 'Nombre' para eliminar.")
    else:
        st.write("No hay clientes para eliminar.")


def pagina_datos_dias():
    st.title("📅 Datos - Días")
    
    # Obtener los días y las cajas
    dias = get_dias()
    cajas = get_cajas()
    cajas_dict = {caja["id"]: caja["Nombre"] for caja in cajas} if cajas else {}

    # Verificar si hay días registrados
    if dias is None or len(dias) == 0:
        st.write("No hay días registrados.")
        return

    # Reemplazar el ID de la caja con su nombre
    for dia in dias:
        dia["Id_caja"] = cajas_dict.get(dia["Id_caja"], "Caja no encontrada")
    
    # Mostrar los días en un dataframe
    st.subheader("Lista de Días")
    st.dataframe(dias)

    # Formulario para agregar un nuevo día
    st.subheader("Agregar Día")
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha")
    with col2:    
        id_caja_nombre = st.selectbox("Caja", list(cajas_dict.values())) if cajas_dict else None

    col1, col2, col3 = st.columns(3)
    with col1:
        sal_ini = st.number_input("Saldo Inicial", format="%.2f", step=None)
    with col2:
        tot_mov = st.number_input("Total de Movimientos", format="%.2f", step=None)
    with col3:   
        sal_fin = st.number_input("Saldo Final", format="%.2f", step=None)

    if st.button("Agregar Día"):
        if id_caja_nombre:
            id_caja = {v: k for k, v in cajas_dict.items()}[id_caja_nombre]
            fecha_str = fecha.isoformat()  # Convertir fecha a cadena en formato YYYY-MM-DD
            
            # Validar que no exista un registro duplicado
            if validar_dia_unico(fecha_str, id_caja):
                mensaje = insert_dia(fecha_str, id_caja, sal_ini, tot_mov, sal_fin)
                st.success(mensaje)
                st.rerun()
            else:
                st.error("Ya existe un registro con la misma fecha y la misma caja.")
        else:
            st.error("No hay cajas disponibles para seleccionar.")

    
   # Formulario para seleccionar un día por fecha y caja
st.subheader("Seleccionar Día para Editar")
dias = get_dias()
cajas = get_cajas()
cajas_dict = {caja["id"]: caja["Nombre"] for caja in cajas} if cajas else {}
if dias:
    # Crear una lista de opciones combinadas
    opciones = [
        {"id": dia["id"], "texto": f"{dia['Fecha']} - {cajas_dict.get(dia['Id_caja'], 'Caja no encontrada')}"}
        for dia in dias
    ]

    # Crear el selectbox con las opciones combinadas
    dia_seleccionado = st.selectbox(
        "Selecciona un día (Fecha - Caja)",
        opciones,
        format_func=lambda x: x["texto"]  # Mostrar solo el texto combinado
    )

    # Obtener el ID del día seleccionado
    if dia_seleccionado:
        dia_id = dia_seleccionado["id"]
        st.write(f"ID del día seleccionado: {dia_id}")

        # Aquí puedes realizar las operaciones con el ID seleccionado
        # Por ejemplo, cargar los datos del día para edición
        dia_para_editar = next((dia for dia in dias if dia["id"] == dia_id), None)
        if dia_para_editar:
            col1, col2, col3 = st.columns(3)
            with col1:
                nuevo_sal_ini = st.number_input(
                    "Nuevo Saldo Inicial",
                    format="%.2f",
                    value=dia_para_editar["Sal_Ini"],
                    step=None
                )
            with col2:
                nuevo_tot_mov = st.number_input(
                    "Nuevo Total de Movimientos",
                    format="%.2f",
                    value=dia_para_editar["Tot_mov"],
                    step=None
                )
            with col3:
                nuevo_sal_fin = st.number_input(
                    "Nuevo Saldo Final",
                    format="%.2f",
                    value=dia_para_editar["Sal_Fin"],
                    step=None
                )

            # Botón para actualizar el día
            if st.button("Actualizar Día"):
                mensaje = update_dia(
                    dia_id,
                    
                    nuevo_sal_ini,
                    nuevo_tot_mov,
                    nuevo_sal_fin
                )
                st.success(mensaje)
                st.rerun()

def pagina_datos_tip_mov():
    st.title("📦 Datos - Tipos de Movimiento")
    
    # Mostrar todos los tipos de movimiento
    st.subheader("Lista de Tipos de Movimiento")
    tipos_movimiento = get_tipo_movimientos()
    if tipos_movimiento:
        st.dataframe(tipos_movimiento)
    else:
        st.write("No hay tipos de movimiento registrados.")

    # Formulario para agregar un nuevo tipo de movimiento
    st.subheader("Agregar Tipo de Movimiento")
    nombre = st.text_input("Nombre del Tipo de Movimiento")
    if st.button("Agregar Tipo"):
        insert_tipo_movimiento(nombre)
        st.rerun()

    # Formulario para editar un tipo de movimiento existente
    st.subheader("Editar Tipo de Movimiento")
    if tipos_movimiento:
        tipo_seleccionado = st.selectbox("Selecciona un tipo para editar", tipos_movimiento, format_func=lambda x: f"{x['Nombre']}")
        if tipo_seleccionado:
            nuevo_nombre = st.text_input("Nuevo Nombre", value=tipo_seleccionado["Nombre"])
            if st.button("Actualizar Tipo"):
                update_tipo_movimiento(tipo_seleccionado["id"], nuevo_nombre)
                st.rerun()

    # Formulario para eliminar un tipo de movimiento existente
    st.subheader("Eliminar Tipo de Movimiento")
    if tipos_movimiento:
        tipo_seleccionado = st.selectbox("Selecciona un tipo para eliminar", tipos_movimiento, format_func=lambda x: f"{x['Nombre']}", key="eliminar_tipo_selectbox")
        if st.button("Eliminar Tipo"):
            delete_tipo_movimiento(tipo_seleccionado["id"])
            st.rerun()




def validar_dia_unico(fecha, id_caja):
    """Valida que no exista un registro con la misma fecha y la misma caja."""
    dias1 = get_dias()  # Obtiene todos los registros de la tabla 'Dias'
    for dia in dias1:
        if dia["Fecha"] == fecha and dia["Id_caja"] == id_caja:
            return False  # Ya existe un registro con la misma fecha y caja
    return True  # No existe un registro duplicado

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
    
    <style>
    .stNumberInput > div {
        width: 250px; /* Ajusta el ancho del campo */
    }
    </style>
    <style> button.step-up {display: none;} button.step-down {display: none;} </style>
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
                if st.button("Cajas", key="cajas_button", type="secondary", help="Gestiona las cajas"):
                    st.session_state.pagina_actual = "Datos-cajas"
                if st.button("Tipos de Movimiento", key="tip_mov_button", type="secondary", help="Gestiona los tipos de movimiento"):
                    st.session_state.pagina_actual = "Datos-Tipos de Movimiento"
                if st.button("Días", key="dias_button", type="secondary", help="Gestiona los días"):
                    st.session_state.pagina_actual = "Datos-Días"    
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
        elif st.session_state.pagina_actual == "Datos-cajas":
            pagina_datos_cajas()
        elif st.session_state.pagina_actual == "Datos-Tipos de Movimiento":
            pagina_datos_tip_mov()
        elif st.session_state.pagina_actual == "Datos-Días":
            pagina_datos_dias()    
        elif st.session_state.pagina_actual == "Productos":
            pagina_productos()
        elif st.session_state.pagina_actual == "Configuración":
            pagina_configuracion()

if __name__ == "__main__":
    main()
