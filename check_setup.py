"""
Script para verificar que todas las dependencias y servicios estén configurados correctamente
"""
import sys


def check_imports():
    """Verificar que todas las librerías necesarias estén instaladas"""
    print("🔍 Verificando importaciones...")
    
    required_modules = [
        ('django', 'Django'),
        ('pymongo', 'PyMongo'),
        ('langgraph', 'LangGraph'),
        ('langchain', 'LangChain'),
        ('langchain_google_vertexai', 'LangChain Google Vertex AI'),
        ('vertexai', 'Google Cloud Vertex AI'),
    ]
    
    missing = []
    for module, name in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Faltan las siguientes librerías: {', '.join(missing)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las librerías están instaladas\n")
    return True


def check_mongodb():
    """Verificar conexión a MongoDB"""
    print("🔍 Verificando conexión a MongoDB...")
    
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()
        print("  ✅ MongoDB está ejecutándose y accesible")
        print(f"  📊 Bases de datos disponibles: {client.list_database_names()}\n")
        return True
    except Exception as e:
        print(f"  ❌ Error al conectar a MongoDB: {e}")
        print("💡 Asegúrate de que MongoDB esté ejecutándose en localhost:27017\n")
        return False


def check_google_cloud():
    """Verificar configuración de Google Cloud"""
    print("🔍 Verificando configuración de Google Cloud...")
    
    try:
        import vertexai
        import os
        
        # Verificar si hay credenciales configuradas
        creds_env = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if creds_env:
            print(f"  ✅ Variable de entorno GOOGLE_APPLICATION_CREDENTIALS configurada")
            print(f"  📁 Archivo: {creds_env}")
        else:
            print("  ⚠️  Variable GOOGLE_APPLICATION_CREDENTIALS no configurada")
            print("  💡 Asegúrate de haber ejecutado: gcloud auth application-default login")
        
        # Leer el PROJECT_ID del archivo graph.py
        try:
            with open('chat/graph.py', 'r', encoding='utf-8') as f:
                content = f.read()
                if 'PROJECT_ID = "stone-poetry-473315-a9"' in content:
                    print("  ⚠️  Aún tienes el PROJECT_ID de ejemplo en graph.py")
                    print("  💡 Actualiza PROJECT_ID en chat/graph.py con tu ID de proyecto\n")
                    return False
                else:
                    print("  ✅ PROJECT_ID actualizado en graph.py\n")
        except FileNotFoundError:
            print("  ❌ No se encontró chat/graph.py\n")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        return False


def check_django():
    """Verificar configuración de Django"""
    print("🔍 Verificando configuración de Django...")
    
    try:
        import django
        import os
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mongochat.settings')
        django.setup()
        
        print(f"  ✅ Django {django.get_version()} configurado correctamente")
        
        # Verificar que las migraciones estén aplicadas
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', '--list', stdout=out)
        output = out.getvalue()
        
        if '[ ]' in output:
            print("  ⚠️  Hay migraciones pendientes")
            print("  💡 Ejecuta: python manage.py migrate\n")
            return False
        else:
            print("  ✅ Todas las migraciones aplicadas\n")
        
        return True
        
    except Exception as e:
        print(f"  ⚠️  No se pudo verificar Django completamente: {e}")
        print("  💡 Esto es normal si no has ejecutado 'python manage.py migrate' aún\n")
        return True


def main():
    print("=" * 60)
    print("  🚀 VERIFICACIÓN DE CONFIGURACIÓN DEL CHATBOT")
    print("=" * 60)
    print()
    
    checks = [
        check_imports(),
        check_mongodb(),
        check_google_cloud(),
        check_django(),
    ]
    
    print("=" * 60)
    if all(checks):
        print("✅ ¡TODO ESTÁ LISTO!")
        print("🎉 Puedes ejecutar: python manage.py runserver")
    else:
        print("⚠️  Hay algunos problemas que debes resolver")
        print("📖 Consulta el README.md para más información")
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Verificación cancelada")
        sys.exit(0)

