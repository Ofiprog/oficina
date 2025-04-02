import streamlit as st
from supabase import create_client,Client

# --- Supabase Setup ---
url:str="https://yundfqluztuthknvmoco.supabase.co"
key:str="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase: Client=create_client(url,key)

# --- Streamlit App ---
st.title("🔐 Aplicación de Login")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- Login Form ---
if not st.session_state.logged_in:
    st.subheader("Iniciar Sesión")
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        try:
            # Authenticate with Supabase
            data = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            if data.user:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"¡Bienvenido, {email}!")
                st.rerun() #rerun to show the logged in content
            else:
                st.error("Credenciales incorrectas.")
        except Exception as e:
            st.error(f"Error al iniciar sesión: {e}")

# --- Content for Logged-in Users ---
if st.session_state.logged_in:
    st.subheader(f"Bienvenido, {st.session_state.user_email}!")
    st.write("¡Has iniciado sesión correctamente!")

    if st.button("Cerrar Sesión"):
        try:
            supabase.auth.sign_out()
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.success("Sesión cerrada correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al cerrar sesión: {e}")

    # --- Example: Displaying Data from Supabase ---
    st.subheader("Datos de Usuarios (Ejemplo)")
    try:
        data = supabase.table("Usuarios").select("*").execute()
        st.write(data)
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
else:
    st.write("Por favor, inicia sesión para ver el contenido.")



data=supabase.table("Usuarios").select("*").execute()
st.write(data)
