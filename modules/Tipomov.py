from supabase import create_client

# --- Supabase Setup ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase = create_client(url, key)

# --- Funciones CRUD para la tabla "Tipo_movimiento" ---

def get_tipo_movimientos():
    """Obtiene todos los registros de la tabla 'Tipo_movimiento'."""
    try:
        data = supabase.table("Tipo_movimiento").select("*").execute()
        return data.data
    except Exception as e:
        return f"Error al obtener los tipos de movimiento: {e}"

def insert_tipo_movimiento(nombre):
    """Inserta un nuevo registro en la tabla 'Tipo_movimiento'."""
    try:
        supabase.table("Tipo_movimiento").insert({"Nombre": nombre}).execute()
        return "Tipo de movimiento agregado correctamente."
    except Exception as e:
        return f"Error al agregar el tipo de movimiento: {e}"

def update_tipo_movimiento(id, nombre):
    """Actualiza un registro existente en la tabla 'Tipo_movimiento'."""
    try:
        supabase.table("Tipo_movimiento").update({"Nombre": nombre}).eq("Id", id).execute()
        return "Tipo de movimiento actualizado correctamente."
    except Exception as e:
        return f"Error al actualizar el tipo de movimiento: {e}"

def delete_tipo_movimiento(id):
    """Elimina un registro de la tabla 'Tipo_movimiento'."""
    try:
        supabase.table("Tipo_movimiento").delete().eq("Id", id).execute()
        return "Tipo de movimiento eliminado correctamente."
    except Exception as e:
        return f"Error al eliminar el tipo de movimiento: {e}"