from supabase import create_client

# --- Supabase Setup ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase = create_client(url, key)

# --- Funciones CRUD para la tabla "Dias" ---

def get_dias():
    """Obtiene todos los registros de la tabla 'Dias'."""
    try:
        data = supabase.table("Dias").select("*").execute()
        return data.data
    except Exception as e:
        return f"Error al obtener los días: {e}"

def insert_dia(fecha, id_caja, sal_ini, tot_mov, sal_fin):
    """Inserta un nuevo registro en la tabla 'Dias'."""
    try:
        supabase.table("Dias").insert({
            "Fecha": fecha,
            "Id_caja": id_caja,
            "Sal_ini": sal_ini,
            "Tot_mov": tot_mov,
            "Sal_Fin": sal_fin
        }).execute()
        return "Día agregado correctamente."
    except Exception as e:
        return f"Error al agregar el día: {e}"

def update_dia(id, fecha, id_caja, sal_ini, tot_mov, sal_fin):
    """Actualiza un registro existente en la tabla 'Dias'."""
    try:
        supabase.table("Dias").update({
            "Fecha": fecha,
            "Id_caja": id_caja,
            "Sal_ini": sal_ini,
            "Tot_mov": tot_mov,
            "Sal_Fin": sal_fin
        }).eq("id", id).execute()
        return "Día actualizado correctamente."
    except Exception as e:
        return f"Error al actualizar el día: {e}"

def delete_dia(id):
    """Elimina un registro de la tabla 'Dias'."""
    try:
        supabase.table("Dias").delete().eq("id", id).execute()
        return "Día eliminado correctamente."
    except Exception as e:
        return f"Error al eliminar el día: {e}"