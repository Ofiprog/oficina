import streamlit as st
from supabase import create_client,Client

url:str="https://yundfqluztuthknvmoco.supabase.co"
key:str="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl1bmRmcWx1enR1dGhrbnZtb2NvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDMzODcxNjAsImV4cCI6MjA1ODk2MzE2MH0.P20V-2gUuVuwmbh59kKzuM4kMjZco0x23ynic8RZhpc"
supabase: Client=create_client(url,key)

st.title("🎈 My new app")
st.write(
    " Probando !!!."
)
data=supabase.table("Usuarios").select("*").execute()
st.write(data)
