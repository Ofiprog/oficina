from supabase import create_client

# --- Supabase Setup ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase = create_client(url, key)

# --- Funciones para interactuar con la tabla "Cajas" ---
def get_cajas():
    """Obtiene todas las cajas de la tabla 'Cajas'."""
    try:
        data = supabase.table("Cajas").select("*").execute()
        return data.data
    except Exception as e:
        return f"Error al obtener cajas: {e}"

def insert_caja(nombre):
    """Inserta una nueva caja en la tabla 'Cajas'."""
    try:
        supabase.table("Cajas").insert({"Nombre": nombre}).execute()
        return "Caja agregada correctamente."
    except Exception as e:
        return f"Error al agregar caja: {e}"

def update_caja(id, nombre):
    """Actualiza una caja existente en la tabla 'Cajas'."""
    try:
        supabase.table("Cajas").update({"Nombre": nombre}).eq("id", id).execute()
        return "Caja actualizada correctamente."
    except Exception as e:
        return f"Error al actualizar caja: {e}"

def delete_caja(id):
    """Elimina una caja de la tabla 'Cajas'."""
    try:
        supabase.table("Cajas").delete().eq("id", id).execute()
        return "Caja eliminada correctamente."
    except Exception as e:
        return f"Error al eliminar caja: {e}"