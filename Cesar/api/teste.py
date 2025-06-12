from mysql.connector import connect
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
try:
    conn = connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("✅ Conexão bem-sucedida!")
except Exception as e:
    print(f"❌ Erro: {e}")