from supabase import create_client

# --- Supabase Setup ---
url: str = "https://yundfqluztuthknvmoco.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase = create_client(url, key)

# --- Funciones CRUD para la tabla "Movimientos" ---

def get_movimientos():
    """Obtiene todos los registros de la tabla 'Movimientos'."""
    try:
        data = supabase.table("Movimientos").select("*").execute()
        return data.data
    except Exception as e:
        return f"Error al obtener los movimientos: {e}"

def insert_movimiento(id_dias, id_tipomov, id_cliente, monto, tipo_cam, tot_ope, pesos, transfer):
    """Inserta un nuevo registro en la tabla 'Movimientos'."""
    try:
        supabase.table("Movimientos").insert({
            "Id_dias": id_dias,
            "Id_Tipomov": id_tipomov,
            "Id_cliente": id_cliente,
            "Monto": monto,
            "Tipo_cam": tipo_cam,
            "Tot_ope": tot_ope,
            "Pesos": pesos,
            "Transfer": transfer
        }).execute()
        return "Movimiento agregado correctamente."
    except Exception as e:
        return f"Error al agregar el movimiento: {e}"

def update_movimiento(id, id_dias, id_tipomov, id_cliente, monto, tipo_cam, tot_ope, pesos, transfer):
    """Actualiza un registro existente en la tabla 'Movimientos'."""
    try:
        supabase.table("Movimientos").update({
            "Id_dias": id_dias,
            "Id_Tipomov": id_tipomov,
            "Id_cliente": id_cliente,
            "Monto": monto,
            "Tipo_cam": tipo_cam,
            "Tot_ope": tot_ope,
            "Pesos": pesos,
            "Transfer": transfer
        }).eq("id", id).execute()
        return "Movimiento actualizado correctamente."
    except Exception as e:
        return f"Error al actualizar el movimiento: {e}"

def delete_movimiento(id):
    """Elimina un registro de la tabla 'Movimientos'."""
    try:
        supabase.table("Movimientos").delete().eq("id", id).execute()
        return "Movimiento eliminado correctamente."
    except Exception as e:
        return f"Error al eliminar el movimiento: {e}"