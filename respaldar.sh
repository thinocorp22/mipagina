#!/bin/bash

echo "===================================="
echo "🚀 Iniciando proceso de respaldo..."
echo "===================================="

# 1. Comprobar si hay conexión a internet haciendo ping a GitHub
echo "Verificando conexión a la red..."
if ! ping -c 1 github.com &> /dev/null
then
    echo "❌ Error: No hay conexión a internet. Conéctate e intenta de nuevo."
    exit 1
fi
echo "✅ ¡Conexión exitosa!"

# 2. Agregar todos los cambios al área de preparación
echo "Preparando archivos..."
git add .

# 3. Pedir un mensaje de commit personalizado en la terminal
echo -v
read -p "📝 Escribe una breve descripción de tus cambios: " mensaje

# Si el usuario no escribe nada, poner uno por defecto
if [ -z "$mensaje" ]; then
    mensaje="Actualización automática del sitio"
fi

# 4. Realizar el commit con el mensaje del usuario
git commit -m "$mensaje"

# 5. Subir los cambios a GitHub
echo "Subiendo cambios a la nube (GitHub)..."
git push

echo "===================================="
echo "🎉 ¡Respaldo completado con éxito!"
echo "===================================="

