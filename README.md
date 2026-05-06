# 🎮 AHORCADO PREMIUM - Con soporte para vocales acentuadas

Juego del Ahorcado desarrollado en Python con Tkinter que utiliza el diccionario **Spanish-BFF** de Hugging Face con más de **66,000 palabras reales del español**, incluyendo soporte completo para vocales con acento (Á, É, Í, Ó, Ú).

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)

## ✨ Características

- 🎨 **Interfaz gráfica moderna** con Tkinter
- 📚 **Diccionario Spanish-BFF** (>66,353 palabras reales)
- 🔤 **Soporte para vocales acentuadas** (Á, É, Í, Ó, Ú)
- 🔥 **Modo difícil** (solo 4 intentos)
- 📏 **Selector de longitud** (4 a 10 letras)
- 📊 **Estadísticas en tiempo real** (victorias, derrotas, rachas)
- 💾 **Caché local** del diccionario para carga rápida
- 🎨 **Dibujo interactivo** del ahorcado

## 🖥️ Capturas de pantalla

*(Incluye capturas de tu juego aquí)*

## 📦 Requisitos

- Python 3.7 o superior
- Pip (gestor de paquetes de Python)

### Dependencias principales

| Paquete | Versión | Uso |
|---------|---------|-----|
| `tkinter` | (incluido en Python) | Interfaz gráfica |
| `datasets` | ≥2.0.0 | Descarga del diccionario Spanish-BFF |
| `unicodedata` | (incluido) | Normalización de acentos |

## 🚀 Instalación y Ejecución

### Windows (Ejecución rápida)

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/ahorcado-premium.git
   cd ahorcado-premium
   ```

2. **Ejecuta el instalador de dependencias:**
   - Haz doble clic en `install_requirements.ps1` (PowerShell)
   - O ejecuta: `.\install_requirements.ps1`

3. **Inicia el juego:**
   - Haz doble clic en `ejecutar.bat`
   - O ejecuta: `python Ahorcado.py`

### Windows (Manual)

```bash
# Instalar dependencias
pip install datasets

# Ejecutar juego
python Ahorcado.py
```

### Linux / macOS

```bash
# Instalar dependencias
pip3 install datasets

# Ejecutar juego
python3 Ahorcado.py
```

## 🎮 Cómo Jugar

1. **Selecciona la longitud** de la palabra (4-10 letras)
2. **Activa el modo difícil** (opcional) para solo 4 intentos
3. **Ingresa letras** una por una en el campo de texto
4. **Adivina la palabra** antes de que se complete el dibujo del ahorcado
5. **Las vocales acentuadas** se muestran correctamente pero se escriben sin acento (ej: para 'ÁRBOL' escribe 'A')

### Controles

| Tecla/Acción | Función |
|--------------|---------|
| `Enter` | Enviar letra |
| `🎲 NUEVA PALABRA` | Reiniciar partida actual |
| `🔄 REINICIAR ESTADÍSTICAS` | Resetear puntuaciones |
| `❌ SALIR` | Cerrar el juego |

## 📁 Estructura del Proyecto

```
ahorcado-premium/
│
├── Ahorcado.py              # Código principal del juego
├── ejecutar.bat             # Script de inicio para Windows
├── ejecutar.ps1             # Script de inicio para PowerShell
├── install_requirements.ps1 # Instalador de dependencias
├── README.md                # Este archivo
│
├── diccionario_spanish_bff.json  # Caché del diccionario (se genera automáticamente)
│
└── LICENSE                  # Licencia MIT
```

## 🔧 Personalización

### Cambiar la fuente del diccionario

Por defecto, el juego descarga el dataset `MMG/SpanishBFF` de Hugging Face. Puedes modificarlo en la línea 205 de `Ahorcado.py`:

```python
dataset = load_dataset("MMG/SpanishBFF", split="train")
```

### Ajustar intentos en modo difícil

En la línea 145 del código:

```python
self.intentos_restantes = 4 if self.modo_dificil else 6
```

Cambia el `4` por el número que prefieras.

## 🐛 Solución de Problemas

### Error: "No module named 'datasets'"

**Solución:** Ejecuta el instalador de dependencias:
```bash
pip install datasets
```

### Error: El juego no carga el diccionario

**Solución:** 
1. Verifica tu conexión a Internet (primera ejecución)
2. Elimina el archivo `diccionario_spanish_bff.json` y reinicia
3. El juego usará automáticamente el diccionario de respaldo

### Las vocales acentuadas no se muestran correctamente

**Solución:** Asegúrate de que tu terminal/sistema soporte UTF-8. El juego maneja los acentos internamente.

## 📊 Estadísticas

El juego mantiene un seguimiento de:
- 🏆 Victorias totales
- 💀 Derrotas totales
- 📈 Racha actual de victorias
- 🏅 Racha máxima alcanzada

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Christian Lera**

- GitHub: [@christianlera](https://github.com/christianlera)

## 🙏 Agradecimientos

- [Hugging Face](https://huggingface.co/) por el dataset [Spanish-BFF](https://huggingface.co/datasets/MMG/SpanishBFF)
- Comunidad de Python por Tkinter y las librerías utilizadas

## 📞 Contacto

¿Preguntas o sugerencias? Abre un issue en el repositorio o contacta al autor.

---

⭐ **Si te gusta este proyecto, no olvides darle una estrella en GitHub** ⭐
