import psycopg2

def conectar():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="clinica_db", 
            user="postgres",           
            password="334003562Mn#"      
        )
        print("✅ Conexión exitosa a la base de datos")
        return conexion
    except Exception as e:
        print("❌ Error al conectar:", e)

# Probar la conexión
if __name__ == "__main__":
    conectar()