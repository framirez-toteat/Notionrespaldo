"""
patch_videos.py — Reemplaza links de video locales con iframes de Google Drive.

USO:
1. Sube los videos a Google Drive y copia el ID de cada archivo (el ID está en la URL
   al abrir el video: drive.google.com/file/d/ESTE_ES_EL_ID/view)
2. Edita el diccionario DRIVE_MAP abajo con { "nombre_archivo.mp4": "ID_DE_DRIVE", ... }
3. Ejecuta: python patch_videos.py
"""

import os
import re

# ─── COMPLETA ESTE DICCIONARIO CON LOS IDS DE DRIVE ─────────────────────────
DRIVE_MAP = {
    # Raspberry
    "20260312_104524.mp4": "",

    # Mercado Pago Point
    "20250902_123229.mp4": "",
    "20250902_123757.mp4": "",
    "20250902_124709.mp4": "",

    # Getnet
    "A960_2025-06-18_16-19-10.mp4": "",
    "A960_2025-06-18_17-51-01.mp4": "",
    "POS_INTEGRADO.mp4": "",

    # Flujo Capacitación
    "Jerarquia_de_Ingredientes.mp4": "",
    "Ingredientes.mp4": "",
    "Jerarquia_de_SubRecetasPreelaborados_y_Porcionamiento.mp4": "",
    "Porcionamiento.mp4": "",
    "Jerarquia_de_Bodegas.mp4": "",

    # Proyectos Lorena
    "https___sync.facturante.com_Reseller_archiveresources_-_My_Workspace_2025-11-27_09-41-45.mp4": "",
    "Toteat_DTE_Admin_-_Google_Chrome_2026-01-30_08-43-05.mp4": "",
    "Toteat_DTE_Admin_-_Google_Chrome_2026-01-30_08-53-38.mp4": "",
    "Toteat_Restaurant_Manager_v.968_-_Google_Chrome_2026-02-03_17-19-19.mp4": "",

    # Tareas / Redelcom
    "Video_de_WhatsApp_2024-06-11RDC_CAlc.mp4": "",
    "Video_de_WhatsApp_Con_integracin.mp4": "",

    # Transbank
    "Transbank_Ejemplo_PDV.mov": "",
    "Transbank_Ejemplo_Totem.mov": "",

    # SAC / Formación - Onboarding
    "Grabacion_de_pantalla_2025-04-23_a_la(s)_19.18.56.mov": "",
    "Grabacion_de_pantalla_2025-04-23_a_la(s)_21.54.43.mov": "",
    "Grabacion_de_pantalla_2025-04-23_a_la(s)_22.00.00.mov": "",
    "Grabacion_de_pantalla_2025-04-26_a_la(s)_18.46.20.mov": "",
    "Grabacion_de_pantalla_2025-04-27_a_la(s)_20.41.49.mov": "",
    "Grabacion_de_pantalla_2025-04-27_a_la(s)_21.05.38.mov": "",
    "Grabacion_de_pantalla_2025-04-27_a_la(s)_21.41.44.mov": "",
    "Grabacion_de_pantalla_2025-04-27_a_la(s)_22.37.20.mov": "",
    "Grabacion_de_pantalla_2025-04-27_a_la(s)_22.50.05.mov": "",
    "Grabacin_de_pantalla_2025-10-28_a_la(s)_15.54.50_(1).mov": "",
    # SAC / Manuales - Intercom
    "Grabacion_de_pantalla_2025-10-02_a_la(s)_12.11.23.mov": "",
}
# ─────────────────────────────────────────────────────────────────────────────

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")

# Regex: <a href="carpeta/archivo.mp4">cualquier texto</a>
# o <a href="archivo.mp4">cualquier texto</a>
VIDEO_RE = re.compile(
    r'<a\s+href="(?:[^"]*/)?(([^"/]+\.(?:mp4|mov)))">([^<]*)</a>',
    re.IGNORECASE
)

def drive_embed(file_id, filename):
    return (
        f'<iframe src="https://drive.google.com/file/d/{file_id}/preview" '
        f'width="640" height="360" allow="autoplay" '
        f'style="border:none;max-width:100%;display:block;margin:0 auto" '
        f'title="{filename}"></iframe>'
    )

patched_files = 0
patched_links = 0
missing_ids = set()

for root, _, files in os.walk(CONTENT_DIR):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        path = os.path.join(root, fname)
        with open(path, encoding="utf-8", errors="ignore") as f:
            html = f.read()

        def replacer(m):
            global patched_links
            full_ref = m.group(1)   # e.g. "Getnet/A960_....mp4" or "A960_....mp4"
            filename = m.group(2)   # just the filename
            text     = m.group(3)
            file_id  = DRIVE_MAP.get(filename, "")
            if not file_id:
                missing_ids.add(filename)
                return m.group(0)   # sin cambios
            patched_links += 1
            return drive_embed(file_id, text or filename)

        new_html = VIDEO_RE.sub(replacer, html)
        if new_html != html:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_html)
            patched_files += 1
            print(f"  ✓ {os.path.relpath(path, CONTENT_DIR)}")

print(f"\nArchivos modificados : {patched_files}")
print(f"Links reemplazados   : {patched_links}")
if missing_ids:
    print(f"\nFaltan IDs para ({len(missing_ids)}):")
    for n in sorted(missing_ids):
        print(f"  - {n}")
