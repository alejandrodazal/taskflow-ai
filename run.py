#!/usr/bin/env python3
"""
Punto de entrada para la aplicación TaskFlow Kanban
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        # Iniciar servidor web
        from kanban_app.web import create_app
        app = create_app()
        print("Iniciando servidor web TaskFlow Kanban...")
        print("Accede a http://127.0.0.1:5002")
        app.run(debug=True, port=5002)
    else:
        # Iniciar CLI
        from kanban_app.cli import cli
        cli()

if __name__ == '__main__':
    main()