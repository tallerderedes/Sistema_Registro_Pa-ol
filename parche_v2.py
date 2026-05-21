"""
Ejecutar con: py -3.11 parche_v2.py
Agrega los archivos y cambios que faltan en la v2
"""
import os, sqlite3

BASE = os.path.dirname(os.path.abspath(__file__))
TPL  = os.path.join(BASE, "templates")

# ── 1. importar_herramientas.html ─────────────────────────────────────────────
with open(os.path.join(TPL, "importar_herramientas.html"), "w", encoding="utf-8") as f:
    f.write("""\
{% extends "base.html" %}
{% block content %}
<h2>Importar Herramientas desde Excel</h2>
{% if msg %}
<div class="alert {% if 'Error' in msg %}alert-danger{% else %}alert-success{% endif %}">{{ msg }}</div>
{% endif %}
<div class="form-card">
  <p style="margin-bottom:16px;color:#555;font-size:.9rem">
    El archivo Excel debe tener estas columnas en orden:<br><br>
    <strong>nombre | descripcion | cantidad | estado</strong><br><br>
    Estado: <em>Bueno</em>, <em>Regular</em> o <em>Danado</em><br>
    La primera fila es el encabezado (se omite).
  </p>
  <a href="/plantillas/herramientas" class="btn btn-excel" style="margin-bottom:20px;display:inline-block">
    Descargar plantilla Excel
  </a>
  <form method="POST" enctype="multipart/form-data">
    <label>Seleccionar archivo Excel (.xlsx)</label>
    <input type="file" name="archivo" accept=".xlsx" required>
    <div class="form-actions">
      <button class="btn btn-success" type="submit">Importar</button>
      <a href="/herramientas" class="btn btn-secondary">Cancelar</a>
    </div>
  </form>
</div>
{% endblock %}
""")
print("[OK] templates/importar_herramientas.html")

# ── 2. importar_usuarios.html ─────────────────────────────────────────────────
with open(os.path.join(TPL, "importar_usuarios.html"), "w", encoding="utf-8") as f:
    f.write("""\
{% extends "base.html" %}
{% block content %}
<h2>Importar Usuarios desde Excel</h2>
{% if msg %}
<div class="alert {% if 'Error' in msg %}alert-danger{% else %}alert-success{% endif %}">{{ msg }}</div>
{% endif %}
<div class="form-card">
  <p style="margin-bottom:16px;color:#555;font-size:.9rem">
    El archivo Excel debe tener estas columnas en orden:<br><br>
    <strong>nombre | curso | division | turno | tipo</strong><br><br>
    Turno: <em>Manana</em> o <em>Tarde</em> &mdash; Tipo: <em>Alumno</em> o <em>Docente</em><br>
    La primera fila es el encabezado (se omite).
  </p>
  <a href="/plantillas/usuarios" class="btn btn-excel" style="margin-bottom:20px;display:inline-block">
    Descargar plantilla Excel
  </a>
  <form method="POST" enctype="multipart/form-data">
    <label>Seleccionar archivo Excel (.xlsx)</label>
    <input type="file" name="archivo" accept=".xlsx" required>
    <div class="form-actions">
      <button class="btn btn-success" type="submit">Importar</button>
      <a href="/usuarios" class="btn btn-secondary">Cancelar</a>
    </div>
  </form>
</div>
{% endblock %}
""")
print("[OK] templates/importar_usuarios.html")

# ── 3. Agregar columna destino a la BD si no existe ───────────────────────────
try:
    conn = sqlite3.connect(os.path.join(BASE, "paniol_cet22.db"))
    conn.execute("ALTER TABLE prestamos ADD COLUMN destino TEXT")
    conn.commit()
    conn.close()
    print("[OK] Columna 'destino' agregada a la base de datos")
except Exception as e:
    if "duplicate column" in str(e).lower():
        print("[OK] Columna 'destino' ya existia")
    else:
        print(f"[INFO] Base de datos: {e}")

# ── 4. Actualizar herramientas.html con boton importar ────────────────────────
with open(os.path.join(TPL, "herramientas.html"), "w", encoding="utf-8") as f:
    f.write("""\
{% extends "base.html" %}
{% block content %}
<h2>Herramientas</h2>
<div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap">
  <a href="/herramientas/nueva" class="btn btn-success">Nueva Herramienta</a>
  <a href="/herramientas/importar" class="btn btn-excel">Importar desde Excel</a>
</div>
<table>
  <thead>
    <tr><th>#</th><th>Nombre</th><th>Descripcion</th><th>Cantidad</th><th>Estado</th><th>Acciones</th></tr>
  </thead>
  <tbody>
    {% for h in herramientas %}
    <tr>
      <td>{{ h.id }}</td><td>{{ h.nombre }}</td>
      <td>{{ h.descripcion or "—" }}</td><td>{{ h.cantidad }}</td>
      <td><span class="badge {% if h.estado=='Bueno' %}badge-bueno{% elif h.estado=='Regular' %}badge-regular{% else %}badge-danado{% endif %}">{{ h.estado }}</span></td>
      <td>
        <a href="/herramientas/editar/{{ h.id }}" class="btn btn-info">Editar</a>
        <a href="/herramientas/eliminar/{{ h.id }}" class="btn btn-danger" onclick="return confirm('Eliminar?')">Borrar</a>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
""")
print("[OK] templates/herramientas.html actualizado")

# ── 5. Actualizar usuarios.html con boton importar ────────────────────────────
with open(os.path.join(TPL, "usuarios.html"), "w", encoding="utf-8") as f:
    f.write("""\
{% extends "base.html" %}
{% block content %}
<h2>Usuarios</h2>
<div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap">
  <a href="/usuarios/nuevo" class="btn btn-success">Nuevo Usuario</a>
  <a href="/usuarios/importar" class="btn btn-excel">Importar desde Excel</a>
</div>
<table>
  <thead>
    <tr><th>#</th><th>Nombre</th><th>Tipo</th><th>Curso</th><th>Turno</th><th>Acciones</th></tr>
  </thead>
  <tbody>
    {% for u in usuarios %}
    <tr>
      <td>{{ u.id }}</td><td>{{ u.nombre }}</td><td>{{ u.tipo }}</td>
      <td>{{ u.curso }} {{ u.division }}</td>
      <td><span class="badge {% if u.turno=='Manana' %}badge-manana{% else %}badge-tarde{% endif %}">{{ u.turno }}</span></td>
      <td>
        <a href="/usuarios/editar/{{ u.id }}" class="btn btn-info">Editar</a>
        <a href="/usuarios/eliminar/{{ u.id }}" class="btn btn-danger" onclick="return confirm('Eliminar?')">Borrar</a>
      </td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
""")
print("[OK] templates/usuarios.html actualizado")

# ── 6. Actualizar prestamo_form.html con selector de curso/taller ─────────────
with open(os.path.join(TPL, "prestamo_form.html"), "w", encoding="utf-8") as f:
    f.write("""\
{% extends "base.html" %}
{% block content %}
<h2>Nuevo Prestamo</h2>
<div class="form-card">
  <form method="POST">
    <label>Herramienta *</label>
    <select name="herramienta_id" required>
      <option value="">-- Seleccionar --</option>
      {% for h in herramientas %}
      <option value="{{ h.id }}">{{ h.nombre }} ({{ h.cantidad }} disp.) &mdash; {{ h.estado }}</option>
      {% endfor %}
    </select>

    <label>Usuario *</label>
    <select name="usuario_id" required>
      <option value="">-- Seleccionar --</option>
      {% for u in usuarios %}
      <option value="{{ u.id }}">{{ u.nombre }} &mdash; {{ u.tipo }} ({{ u.turno }})</option>
      {% endfor %}
    </select>

    <label>Sector *</label>
    <select name="sector" id="sector" required onchange="mostrarDestino()">
      <option value="">-- Seleccionar --</option>
      <option value="Taller">Taller</option>
      <option value="Aula">Aula</option>
    </select>

    <div id="div_taller" style="display:none;margin-top:12px">
      <label>Taller *</label>
      <select name="destino_taller" id="destino_taller">
        <option value="">-- Seleccionar taller --</option>
        {% for t in talleres %}
        <option value="{{ t }}">{{ t }}</option>
        {% endfor %}
      </select>
    </div>

    <div id="div_curso" style="display:none;margin-top:12px">
      <label>Curso *</label>
      <select name="destino_curso" id="destino_curso">
        <option value="">-- Seleccionar curso --</option>
        {% for c in cursos %}
        <option value="{{ c }}">{{ c }}</option>
        {% endfor %}
      </select>
    </div>

    <label>Observaciones</label>
    <textarea name="observaciones" rows="3" placeholder="Opcional..."></textarea>

    <div class="form-actions">
      <button class="btn btn-success" type="submit">Registrar Prestamo</button>
      <a href="/" class="btn btn-secondary">Cancelar</a>
    </div>
  </form>
</div>
<script>
function mostrarDestino() {
  var s = document.getElementById("sector").value;
  document.getElementById("div_taller").style.display = s === "Taller" ? "block" : "none";
  document.getElementById("div_curso").style.display  = s === "Aula"   ? "block" : "none";
  document.getElementById("destino_taller").required  = s === "Taller";
  document.getElementById("destino_curso").required   = s === "Aula";
}
</script>
{% endblock %}
""")
print("[OK] templates/prestamo_form.html actualizado")

print("\n================================================")
print("  PARCHE v2 APLICADO CORRECTAMENTE")
print("  Reinicia el servidor: py -3.11 app.py")
print("================================================\n")