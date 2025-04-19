import streamlit as st
import locale
from supabase import create_client, Client
from modules.cajas import get_cajas, insert_caja, update_caja, delete_caja
from modules.clientes import get_clientes, insert_cliente, update_cliente, delete_cliente
from modules.Tipomov import get_tipo_movimientos, insert_tipo_movimiento, update_tipo_movimiento, delete_tipo_movimiento
from modules.Dias import get_dias, insert_dia, update_dia, delete_dia
from modules.Movimientos import get_movimientos, insert_movimiento, update_movimiento, delete_movimiento

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

    # Formulario para eliminar un día existente
    st.subheader("Eliminar Día")
    if dias:
        # Crear una lista de opciones combinadas
        opciones = [
            {"id": dia["id"], "texto": f"{dia['Fecha']} - {cajas_dict.get(dia['Id_caja'], 'Caja no encontrada')}"}
            for dia in dias
        ]

        # Crear el selectbox con las opciones combinadas
        dia_seleccionado = st.selectbox(
            "Selecciona un día para eliminar (Fecha - Caja)",
            opciones,
            format_func=lambda x: x["texto"],  # Mostrar solo el texto combinado
            key="eliminar_dia_selectbox"
        )

        # Obtener el ID del día seleccionado
        if dia_seleccionado:
            dia_id = dia_seleccionado["id"]
            st.write(f"ID del día seleccionado para eliminar: {dia_id}")

            # Botón para eliminar el día
            if st.button("Eliminar Día"):
                mensaje = delete_dia(dia_id)
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

# --- Página para gestionar las cajas ---
def pagina_datos_cajas():
    st.title("📦 Datos - Cajas")
    
    # Mostrar todas las cajas
    st.subheader("Lista de Cajas")
    cajas = get_cajas()
    if cajas:
        st.dataframe(cajas)
    else:
        st.write("No hay cajas registradas.")

    # Formulario para agregar una nueva caja
    st.subheader("Agregar Caja")
    nombre = st.text_input("Nombre de la Caja")
    if st.button("Agregar Caja"):
        insert_caja(nombre)
        st.rerun()

    # Formulario para editar una caja existente
    st.subheader("Editar Caja")
    if cajas:
        caja_seleccionada = st.selectbox("Selecciona una caja para editar", cajas, format_func=lambda x: f"{x['Nombre']}")
        if caja_seleccionada:
            nuevo_nombre = st.text_input("Nuevo Nombre", value=caja_seleccionada["Nombre"])
            if st.button("Actualizar Caja"):
                update_caja(caja_seleccionada["id"], nuevo_nombre)
                st.rerun()

    # Formulario para eliminar una caja existente
    st.subheader("Eliminar Caja")
    if cajas:
        caja_seleccionada = st.selectbox("Selecciona una caja para eliminar", cajas, format_func=lambda x: f"{x['Nombre']}", key="eliminar_caja_selectbox")
        if st.button("Eliminar Caja"):
            delete_caja(caja_seleccionada["id"])
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
    

def pagina_datos_movimientos():
    st.title("📊 Datos - Movimientos")
    
    # Obtener los movimientos, días, tipos de movimiento y clientes
    movimientos = get_movimientos()
    dias = get_dias()
    cajas = get_cajas()
    tipos_movimiento = get_tipo_movimientos()
    clientes = get_clientes()
    cajas_dict = {caja["id"]: caja["Nombre"] for caja in cajas} if cajas else {}

    # Crear diccionarios para facilitar la selección
    dias_dict = {dia["id"]: f"{dia['Fecha']} - {cajas_dict.get(dia['Id_caja'], 'Caja no encontrada')}" for dia in dias} if dias else {}
    tipos_mov_dict = {tipo["id"]: tipo["Nombre"] for tipo in tipos_movimiento} if tipos_movimiento else {}
    clientes_dict = {cliente["id"]: cliente["Nombre"] for cliente in clientes} if clientes else {}

    # Mostrar todos los movimientos
    st.subheader("Lista de Movimientos")
    if movimientos:
        for movimiento in movimientos:
            movimiento["Id_dias"] = dias_dict.get(movimiento["Id_dias"], "Día no encontrado")
            movimiento["Id_Tipomov"] = tipos_mov_dict.get(movimiento["Id_Tipomov"], "Tipo no encontrado")
            movimiento["Id_cliente"] = clientes_dict.get(movimiento["Id_cliente"], "Cliente no encontrado")
        st.dataframe(movimientos)
    else:
        st.write("No hay movimientos registrados.")

    # Formulario para agregar un nuevo movimiento
    st.subheader("Agregar Movimiento")
    col1, col2 = st.columns(2)
    with col1:
        id_dias_nombre = st.selectbox("Día", list(dias_dict.values())) if dias_dict else None
        id_tipomov_nombre = st.selectbox("Tipo de Movimiento", list(tipos_mov_dict.values())) if tipos_mov_dict else None
    with col2:
        id_cliente_nombre = st.selectbox("Cliente", list(clientes_dict.values())) if clientes_dict else None
        # Campo de entrada para el monto
        monto=st.number_input(
            "Monto",
            key="monto",  # Clave para almacenar el valor en st.session_state
            format="%.2f",
            on_change=actualizar_valor  # Función que se ejecuta al cambiar el valor
        )
    col1, col2 = st.columns(2)
    with col1:
        tipo_cam=st.number_input(
            "Tipo de Cambio",
            key="tipo_cam",  # Clave para almacenar el valor en st.session_state
            format="%.2f",
            on_change=actualizar_valor  # Función que se ejecuta al cambiar el valor
        )
        
        # Mostrar el resultado calculado
        #locale.format_string("$%.2f", monto, grouping=True)
        st.write(f"Resultado: {st.session_state.get('resultado', 0):.2f}")
        tot_ope = st.number_input("Total Operaciones", format="%.2f", step=None)
    with col2:
        pesos = st.number_input("Pesos", format="%.2f", step=None)
        transfer = st.number_input("Transferencia", format="%.2f", step=None)

    if st.button("Agregar Movimiento"):
        if id_dias_nombre and id_tipomov_nombre and id_cliente_nombre:
            id_dias = {v: k for k, v in dias_dict.items()}[id_dias_nombre]
            id_tipomov = {v: k for k, v in tipos_mov_dict.items()}[id_tipomov_nombre]
            id_cliente = {v: k for k, v in clientes_dict.items()}[id_cliente_nombre]
            mensaje = insert_movimiento(id_dias, id_tipomov, id_cliente, monto, tipo_cam, tot_ope, pesos, transfer)
            st.success(mensaje)
            st.rerun()
        else:
            st.error("Selecciona un día, un tipo de movimiento y un cliente.")

    # Formulario para editar un movimiento existente
    st.subheader("Editar Movimiento")
    if movimientos:
        movimiento_seleccionado = st.selectbox(
            "Selecciona un movimiento para editar",
            movimientos,
            format_func=lambda x: f"{x['Id_dias']} - {x['Id_Tipomov']} - {x['Id_cliente']}"
        )
        if movimiento_seleccionado:
            col1, col2 = st.columns(2)
            with col1:
                nuevo_id_dias_nombre = st.selectbox(
                    "Nuevo Día",
                    list(dias_dict.values()),
                    index=list(dias_dict.values()).index(dias_dict.get(movimiento_seleccionado["Id_dias"], ""))
                )
                nuevo_id_tipomov_nombre = st.selectbox(
                    "Nuevo Tipo de Movimiento",
                    list(tipos_mov_dict.values()),
                    index=list(tipos_mov_dict.values()).index(tipos_mov_dict.get(movimiento_seleccionado["Id_Tipomov"], ""))
                )
            with col2:
                nuevo_id_cliente_nombre = st.selectbox(
                    "Nuevo Cliente",
                    list(clientes_dict.values()),
                    index=list(clientes_dict.values()).index(clientes_dict.get(movimiento_seleccionado["Id_cliente"], ""))
                )
                nuevo_monto = st.number_input("Nuevo Monto", format="%.2f", value=movimiento_seleccionado["Monto"], step=None)
            col1, col2 = st.columns(2)
            with col1:
                nuevo_tipo_cam = st.number_input("Nuevo Tipo de Cambio", format="%.2f", value=movimiento_seleccionado["Tipo_cam"], step=None)
                nuevo_tot_ope = st.number_input("Nuevo Total Operaciones", format="%.2f", value=movimiento_seleccionado["Tot_ope"], step=None)
            with col2:
                nuevo_pesos = st.number_input("Nuevo Pesos", format="%.2f", value=movimiento_seleccionado["Pesos"], step=None)
                nuevo_transfer = st.number_input("Nuevo Transferencia", format="%.2f", value=movimiento_seleccionado["Transfer"], step=None)

            if st.button("Actualizar Movimiento"):
                nuevo_id_dias = {v: k for k, v in dias_dict.items()}[nuevo_id_dias_nombre]
                nuevo_id_tipomov = {v: k for k, v in tipos_mov_dict.items()}[nuevo_id_tipomov_nombre]
                nuevo_id_cliente = {v: k for k, v in clientes_dict.items()}[nuevo_id_cliente_nombre]
                mensaje = update_movimiento(
                    movimiento_seleccionado["id"],
                    nuevo_id_dias,
                    nuevo_id_tipomov,
                    nuevo_id_cliente,
                    nuevo_monto,
                    nuevo_tipo_cam,
                    nuevo_tot_ope,
                    nuevo_pesos,
                    nuevo_transfer
                )
                st.success(mensaje)
                st.rerun()

    # Formulario para eliminar un movimiento existente
    st.subheader("Eliminar Movimiento")
    if movimientos:
        movimiento_seleccionado = st.selectbox(
            "Selecciona un movimiento para eliminar",
            movimientos,
            format_func=lambda x: f"{x['Id_dias']} - {x['Id_Tipomov']} - {x['Id_cliente']}",
            key="eliminar_movimiento_selectbox"
        )
        if st.button("Eliminar Movimiento"):
            mensaje = delete_movimiento(movimiento_seleccionado["id"])
            st.success(mensaje)
            st.rerun()



# Función que se ejecutará cuando cambie el valor del número
def actualizar_valor():
    st.session_state.resultado = st.session_state.monto * st.session_state.tipo_cam



# Campo de entrada para el tipo de cambio





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
    <style>
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none; 
        margin: 0; 
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
                if st.button("Cajas", key="cajas_button", type="secondary", help="Gestiona las cajas"):
                    st.session_state.pagina_actual = "Datos-cajas"
                if st.button("Tipos de Movimiento", key="tip_mov_button", type="secondary", help="Gestiona los tipos de movimiento"):
                    st.session_state.pagina_actual = "Datos-Tipos de Movimiento"
                if st.button("Días", key="dias_button", type="secondary", help="Gestiona los días"):
                    st.session_state.pagina_actual = "Datos-Días"    
                if st.button("Reportes", key="reportes_button", type="secondary", help="Gestiona los reportes"):
                    st.session_state.pagina_actual = "Datos-Reportes"
                if st.button("Movimientos", key="movimientos_button", type="secondary", help="Gestiona los movimientos"):
                    st.session_state.pagina_actual = "Datos-Movimientos"
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
        elif st.session_state.pagina_actual == "Datos-Movimientos":
            pagina_datos_movimientos()
        elif st.session_state.pagina_actual == "Configuración":
            pagina_configuracion()

if __name__ == "__main__":
    main()
