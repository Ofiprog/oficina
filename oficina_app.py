import streamlit as st
from supabase import create_client, Client

# --- Supabase Setup (Mantén tu configuración) ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"  # Reemplaza con tu API Key
supabase: Client = create_client(url, key)

# --- Streamlit App ---
st.set_page_config(page_title="App Oficina - Clientes", layout="wide")

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

# --- Funciones para la interfaz de Streamlit ---

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

# --- Main App Logic ---

def main():
    st.title("Gestión de Clientes")
    mostrar_clientes()
    agregar_cliente()
    editar_cliente()
    eliminar_cliente()

if __name__ == "__main__":
    main()
