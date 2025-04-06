import streamlit as st
from supabase import create_client, Client

# --- Supabase Setup (Mantén tu configuración) ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase: Client = create_client(url, key)

# --- Funciones para interactuar con Supabase ---

def get_clientes():
    """Obtiene todos los clientes de la tabla 'Clientes'."""
    try:
        data = supabase.table("Clientes").select("*").execute()
        return data.data
    except Exception as e:
        st.error(f"Error al obtener clientes: {e}")
        return []

def insert_cliente(nombre):
    """Inserta un nuevo cliente en la tabla 'Clientes'."""
    try:
        response = supabase.table("Clientes").insert({"Nombre": nombre}).execute()
        st.success("Cliente agregado correctamente.")
        print("Respuesta de Supabase:", response)
    except Exception as e:
        st.error(f"Error al agregar cliente: Posible Duplicacion de Nombre: {e}")
        #print("Error:", e)

def update_cliente(id, nombre):
    """Actualiza un cliente existente en la tabla 'Clientes'."""
    try:
        supabase.table("Clientes").update({"Nombre": nombre}).eq("id", id).execute()
        st.success("Cliente actualizado correctamente.")
    except Exception as e:
        st.error(f"Error al actualizar cliente: {e}")

def delete_cliente(id):
    """Elimina un cliente de la tabla 'Clientes'."""
    try:
        supabase.table("Clientes").delete().eq("id", id).execute()
        st.success("Cliente eliminado correctamente.")
    except Exception as e:
        st.error(f"Error al eliminar cliente: {e}")