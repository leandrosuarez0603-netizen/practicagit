#!/usr/bin/env python3
"""Generate A3 evidence PDF with reportlab — comprehensive version with diagrams (>100KB)."""
import os
import io
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image as RLImage
)
from reportlab.lib import colors

EVID_DIR = r"D:\leandro\A3\evidencias"
PROJECT_DIR = r"D:\leandro\A3\hola-mundo"
IMG_DIR = r"D:\leandro\A3\img_tmp"
OUTPUT = r"D:\leandro\A3\A3_Evidencia_Git_HolaMundo_FINAL.pdf"

os.makedirs(IMG_DIR, exist_ok=True)

def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "(archivo no encontrado)"

def read_evidencia(name):
    return read_file(os.path.join(EVID_DIR, name))

def read_proyecto(name):
    return read_file(os.path.join(PROJECT_DIR, name))

def safe(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ═══════════════════════════════════════════════════
# IMAGE GENERATION HELPERS
# ═══════════════════════════════════════════════════

def try_font(size=20):
    """Try to load a monospace font, fallback to default."""
    font_paths = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/lucon.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()

def make_git_workflow_diagram():
    """Create a Git workflow diagram: Working Dir -> Staging -> Commit."""
    W, H = 800, 320
    img = Image.new("RGB", (W, H), "#f8f9fa")
    draw = ImageDraw.Draw(img)
    font_title = try_font(22)
    font_box = try_font(16)
    font_small = try_font(12)
    font_arrow = try_font(24)

    # Title
    draw.text((W//2 - 180, 15), "Diagrama: Flujo Basico de Git", fill="#1a1a2e", font=font_title)

    # Boxes
    boxes = [
        (50, 100, 230, 200, "#4CAF50", "Working Directory", "Archivos del proyecto"),
        (300, 100, 480, 200, "#2196F3", "Staging Area", "git add ."),
        (550, 100, 750, 200, "#FF9800", "Repository", "git commit"),
    ]
    for x1, y1, x2, y2, color, title, sub in boxes:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=color, outline="#333", width=2)
        tw = draw.textlength(title, font=font_box)
        draw.text((x1 + (x2-x1-tw)//2, y1+20), title, fill="white", font=font_box)
        sw = draw.textlength(sub, font=font_small)
        draw.text((x1 + (x2-x1-sw)//2, y1+50), sub, fill="white", font=font_small)

    # Arrows
    arrow_y = 150
    draw.text((235, arrow_y-12), "->", fill="#333", font=font_arrow)
    draw.text((235, arrow_y+14), "git add", fill="#666", font=font_small)
    draw.text((485, arrow_y-12), "->", fill="#333", font=font_arrow)
    draw.text((485, arrow_y+14), "git commit", fill="#666", font=font_small)

    # Bottom labels
    labels = [
        (140, 220, "Edita archivos aqui"),
        (390, 220, "Prepara cambios"),
        (650, 220, "Guarda historial"),
    ]
    for x, y, txt in labels:
        tw = draw.textlength(txt, font=font_small)
        draw.text((x - tw//2, y), txt, fill="#555", font=font_small)

    # Bottom commands
    draw.text((50, 270), "Comandos:  git init | git add . | git commit -m 'msg' | git log | git status | git branch", fill="#333", font=font_small)

    path = os.path.join(IMG_DIR, "git_workflow.png")
    img.save(path, dpi=(150, 150))
    return path


def make_commit_history_diagram():
    """Create commit history visualization."""
    W, H = 800, 280
    img = Image.new("RGB", (W, H), "#f8f9fa")
    draw = ImageDraw.Draw(img)
    font_title = try_font(22)
    font_hash = try_font(14)
    font_msg = try_font(13)
    font_label = try_font(12)

    draw.text((W//2 - 160, 15), "Historial de Commits del Proyecto", fill="#1a1a2e", font=font_title)

    # Timeline line
    draw.line([(80, 140), (720, 140)], fill="#333", width=3)

    # Commit nodes
    commits = [
        (200, "763de07", "feat: hola mundo inicial", "26 Sep 2026\n11:25 PM", "#4CAF50"),
        (550, "bbea9bd", "feat: modifica saludo\npara demostrar historial", "26 Sep 2026\n11:26 PM", "#2196F3"),
    ]
    for cx, hash_val, msg, date, color in commits:
        # Circle
        draw.ellipse([cx-25, 115, cx+25, 165], fill=color, outline="#333", width=2)
        draw.text((cx-8, 125), "C", fill="white", font=font_hash)
        # Hash above
        hw = draw.textlength(hash_val, font=font_hash)
        draw.text((cx - hw//2, 80), hash_val, fill="#333", font=font_hash)
        # Message below
        lines = msg.split("\n")
        for i, line in enumerate(lines):
            lw = draw.textlength(line, font=font_msg)
            draw.text((cx - lw//2, 175 + i*18), line, fill="#333", font=font_msg)
        # Date
        date_lines = date.split("\n")
        for i, dl in enumerate(date_lines):
            dw = draw.textlength(dl, font=font_label)
            draw.text((cx - dw//2, 175 + len(lines)*18 + 4 + i*16), dl, fill="#888", font=font_label)

    # Branch label
    draw.rounded_rectangle([550-50, 60, 550+50, 78], radius=4, fill="#0f3460")
    bw = draw.textlength("main", font=font_hash)
    draw.text((550 - bw//2, 62), "main", fill="white", font=font_hash)

    # Arrow between commits
    draw.text((370, 125), "-->", fill="#333", font=font_hash)
    draw.text((350, 145), "HEAD", fill="#FF5722", font=font_label)

    path = os.path.join(IMG_DIR, "commit_history.png")
    img.save(path, dpi=(150, 150))
    return path


def make_file_structure_diagram():
    """Create project file structure visualization."""
    W, H = 800, 350
    img = Image.new("RGB", (W, H), "#f8f9fa")
    draw = ImageDraw.Draw(img)
    font_title = try_font(22)
    font_tree = try_font(15)
    font_desc = try_font(12)

    draw.text((W//2 - 170, 15), "Estructura del Proyecto hola-mundo", fill="#1a1a2e", font=font_title)

    # Tree visualization
    tree_lines = [
        (80, 70, "D:\\leandro\\A3\\hola-mundo\\", "#0f3460", True),
        (120, 100, "├── .git/", "#888", False),
        (120, 125, "├── .gitignore", "#4CAF50", False),
        (120, 150, "├── README.md", "#2196F3", False),
        (120, 175, "├── hola.py", "#FF9800", False),
        (120, 200, "└── index.html", "#9C27B0", False),
    ]
    for x, y, text, color, is_bold in tree_lines:
        draw.text((x, y), text, fill=color, font=font_tree if is_bold else font_tree)

    # File descriptions
    descs = [
        (350, 125, ".gitignore", "Excluye archivos temporales del control de versiones", "#4CAF50"),
        (350, 150, "README.md", "Documentacion del proyecto (titulo, objetivo, integrantes)", "#2196F3"),
        (350, 175, "hola.py", "Script Python: print('Hola Mundo desde Python!')", "#FF9800"),
        (350, 200, "index.html", "Pagina web HTML5: <h1>Hola Mundo desde Git!</h1>", "#9C27B0"),
    ]
    for x, y, fname, desc, color in descs:
        draw.text((x, y), fname, fill=color, font=font_tree)
        draw.text((x, y+20), desc, fill="#666", font=font_desc)

    # Legend
    draw.rounded_rectangle([80, 240, 720, 310], radius=8, fill="#e8e8e8", outline="#ccc")
    draw.text((100, 250), "Leyenda:", fill="#333", font=font_tree)
    draw.text((100, 275), ".git/ = Directorio oculto de Git (metadatos, historial)", fill="#888", font=font_desc)
    draw.text((100, 295), "Archivos tracked = .gitignore, README.md, hola.py, index.html", fill="#888", font=font_desc)

    path = os.path.join(IMG_DIR, "file_structure.png")
    img.save(path, dpi=(150, 150))
    return path


def make_git_commands_table():
    """Create a visual table of Git commands used."""
    W, H = 800, 400
    img = Image.new("RGB", (W, H), "#ffffff")
    draw = ImageDraw.Draw(img)
    font_title = try_font(20)
    font_head = try_font(14)
    font_cell = try_font(13)
    font_small = try_font(11)

    draw.text((W//2 - 150, 12), "Tabla de Comandos Git Utilizados", fill="#1a1a2e", font=font_title)

    # Table header
    header_y = 50
    col_widths = [40, 250, 250, 240]
    col_x = [50, 90, 340, 590]
    headers = ["#", "Comando", "Funcion", "Efecto"]

    draw.rectangle([50, header_y, 750, header_y+30], fill="#0f3460")
    for i, (x, hdr) in enumerate(zip(col_x, headers)):
        draw.text((x+5, header_y+5), hdr, fill="white", font=font_head)

    # Table rows
    rows = [
        ("1", "git init", "Inicializar repositorio", "Crea carpeta .git/"),
        ("2", "git config --local", "Configurar usuario", "Solo afecta este repo"),
        ("3", "git add .", "Agregar al staging", "Prepara archivos"),
        ("4", "git commit -m", "Crear commit", "Guarda snapshot"),
        ("5", "git log --oneline", "Ver historial", "Muestra commits"),
        ("6", "git status", "Ver estado", "Working tree limpio"),
        ("7", "git branch -M", "Renombrar rama", "master -> main"),
        ("8", "git diff", "Ver diferencias", "Cambios entre commits"),
    ]
    for idx, (num, cmd, func, effect) in enumerate(rows):
        y = header_y + 30 + idx * 35
        bg = "#f5f5f5" if idx % 2 == 0 else "#ffffff"
        draw.rectangle([50, y, 750, y+35], fill=bg, outline="#ddd")
        draw.text((col_x[0]+10, y+8), num, fill="#333", font=font_cell)
        draw.text((col_x[1]+5, y+8), cmd, fill="#0f3460", font=font_cell)
        draw.text((col_x[2]+5, y+8), func, fill="#333", font=font_cell)
        draw.text((col_x[3]+5, y+8), effect, fill="#666", font=font_small)

    # Border
    draw.rectangle([50, header_y, 750, header_y+30+len(rows)*35], outline="#333", width=2)

    path = os.path.join(IMG_DIR, "commands_table.png")
    img.save(path, dpi=(150, 150))
    return path


def make_push_diagram():
    """Create diagram for push workflow (pending)."""
    W, H = 800, 250
    img = Image.new("RGB", (W, H), "#fff8e1")
    draw = ImageDraw.Draw(img)
    font_title = try_font(20)
    font_box = try_font(15)
    font_small = try_font(12)

    draw.text((W//2 - 200, 10), "Diagrama: Push a GitHub (PENDIENTE)", fill="#cc6600", font=font_title)

    # Boxes
    boxes = [
        (40, 60, 190, 130, "#FF9800", "Local Repo", "git commit"),
        (250, 60, 400, 130, "#2196F3", "GitHub Remote", "git push"),
        (460, 60, 610, 130, "#4CAF50", "Nube Visible", "github.com"),
        (640, 40, 760, 150, "#F44336", "REQUIERE", "Credenciales\npropias"),
    ]
    for x1, y1, x2, y2, color, title, sub in boxes:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=color, outline="#333", width=2)
        tw = draw.textlength(title, font=font_box)
        draw.text((x1+(x2-x1-tw)//2, y1+10), title, fill="white", font=font_box)
        lines = sub.split("\n")
        for i, line in enumerate(lines):
            lw = draw.textlength(line, font=font_small)
            draw.text((x1+(x2-x1-lw)//2, y1+35+i*16), line, fill="white", font=font_small)

    # Arrows
    draw.text((195, 80), "->", fill="#333", font=font_box)
    draw.text((405, 80), "->", fill="#333", font=font_box)
    draw.text((615, 80), "x", fill="#F44336", font=font_box)

    # Warning text
    draw.text((40, 160), "Este paso NO se ejecuto porque requiere autenticacion personal del alumno.", fill="#cc6600", font=font_small)
    draw.text((40, 180), "Comandos pendientes: gh auth login | gh repo create | git remote add origin | git push -u origin main", fill="#666", font=font_small)
    draw.text((40, 200), "IMPORTANTE: Nunca compartir tokens o credenciales de GitHub.", fill="#F44336", font=font_small)

    path = os.path.join(IMG_DIR, "push_diagram.png")
    img.save(path, dpi=(150, 150))
    return path


def make_terminal_screenshot():
    """Create a simulated terminal screenshot."""
    W, H = 800, 400
    img = Image.new("RGB", (W, H), "#1e1e1e")
    draw = ImageDraw.Draw(img)
    font = try_font(13)
    font_title = try_font(11)

    # Title bar
    draw.rectangle([0, 0, W, 30], fill="#333")
    draw.text((10, 7), "Terminal PowerShell - D:\\leandro\\A3\\hola-mundo", fill="#ccc", font=font_title)
    # Traffic lights
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        draw.ellipse([W-80+i*22, 8, W-64+i*22, 24], fill=c)

    # Terminal content
    lines = [
        ("PS> git init", "#569cd6", ""),
        ("Initialized empty Git repository in D:/leandro/A3/hola-mundo/.git/", "#6a9955", ""),
        ("", "#fff", ""),
        ('PS> git config --local user.name "Alumno A3"', "#569cd6", ""),
        ('PS> git config --local user.email "alumno@ejemplo.com"', "#569cd6", ""),
        ("", "#fff", ""),
        ("PS> git add .", "#569cd6", ""),
        ("warning: in the working copy of '.gitignore', LF will be replaced by CRLF", "#dcdcaa", ""),
        ("", "#fff", ""),
        ('PS> git commit -m "feat: hola mundo inicial"', "#569cd6", ""),
        ("[master (root-commit) 763de07] feat: hola mundo inicial", "#ce9178", ""),
        (" 4 files changed, 52 insertions(+)", "#dcdcaa", ""),
        (" create mode 100644 .gitignore", "#dcdcaa", ""),
        (" create mode 100644 README.md", "#dcdcaa", ""),
        ("", "#fff", ""),
        ("PS> git log --oneline", "#569cd6", ""),
        ("bbea9bd feat: modifica saludo para demostrar historial", "#ce9178", ""),
        ("763de07 feat: hola mundo inicial", "#ce9178", ""),
        ("", "#fff", ""),
        ("PS> git status", "#569cd6", ""),
        ("On branch main", "#6a9955", ""),
        ("nothing to commit, working tree clean", "#6a9955", ""),
    ]
    y = 35
    for line, color, _ in lines:
        draw.text((10, y), line, fill=color, font=font)
        y += 16

    path = os.path.join(IMG_DIR, "terminal_screenshot.png")
    img.save(path, dpi=(150, 150))
    return path


# ═══════════════════════════════════════════════════
# PDF GENERATION
# ═══════════════════════════════════════════════════

def build_pdf():
    # Generate all images
    print("Generando diagramas...")
    img_workflow = make_git_workflow_diagram()
    img_commits = make_commit_history_diagram()
    img_files = make_file_structure_diagram()
    img_cmds = make_git_commands_table()
    img_push = make_push_diagram()
    img_terminal = make_terminal_screenshot()
    print("Diagramas generados OK.")

    doc = SimpleDocTemplate(
        OUTPUT, pagesize=letter,
        topMargin=0.7*inch, bottomMargin=0.7*inch,
        leftMargin=0.7*inch, rightMargin=0.7*inch
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle("CoverTitle", parent=styles["Title"], fontSize=26, spaceAfter=8, textColor=HexColor("#1a1a2e"), fontName="Helvetica-Bold", alignment=1)
    cover_sub = ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=15, spaceAfter=6, textColor=HexColor("#16213e"), alignment=1)
    cover_detail = ParagraphStyle("CoverDetail", parent=styles["Normal"], fontSize=12, spaceAfter=4, textColor=HexColor("#333333"), alignment=1)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18, spaceAfter=10, spaceBefore=18, textColor=HexColor("#0f3460"), fontName="Helvetica-Bold")
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, spaceAfter=8, spaceBefore=14, textColor=HexColor("#0f3460"), fontName="Helvetica-Bold")
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontSize=12, spaceAfter=6, spaceBefore=10, textColor=HexColor("#16213e"), fontName="Helvetica-Bold")
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, spaceAfter=6, leading=14)
    code = ParagraphStyle("Code", parent=styles["Code"], fontSize=8, spaceAfter=4, leading=10.5, backColor=HexColor("#f0f0f0"), borderPadding=6, leftIndent=12, fontName="Courier", wordWrap='CJK')
    desc = ParagraphStyle("Desc", parent=body, leftIndent=12, spaceAfter=10, fontSize=10, textColor=HexColor("#333333"), leading=14)
    warn = ParagraphStyle("Warn", parent=body, leftIndent=12, fontSize=10, textColor=HexColor("#cc6600"), borderPadding=8, backColor=HexColor("#fff8e1"), leading=14)
    check_style = ParagraphStyle("Check", parent=body, fontSize=11, spaceAfter=4, leftIndent=8)
    small = ParagraphStyle("Small", parent=body, fontSize=8, textColor=HexColor("#888888"))
    center = ParagraphStyle("Center", parent=body, alignment=1)

    story = []

    # ═══ PORTADA ═══
    story.append(Spacer(1, 1.2*inch))
    story.append(Paragraph("Actividad 3", title_style))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Git: Hola Mundo", ParagraphStyle("SubMain", parent=title_style, fontSize=20, spaceAfter=10)))
    story.append(Paragraph("Control de Versiones Local", ParagraphStyle("Sub2", parent=cover_sub, fontSize=14, textColor=HexColor("#555555"))))
    story.append(Spacer(1, 0.4*inch))
    story.append(HRFlowable(width="50%", thickness=3, color=HexColor("#0f3460")))
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("Materia: Implementa Aplicaciones Web", cover_sub))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Docente: L.I Jesus Eduardo Garcia Alvarez", cover_detail))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Alumno: Alumno A3", cover_detail))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Email: alumno@ejemplo.com", cover_detail))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Fecha de realizacion: 26 de septiembre de 2026", cover_detail))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<i>Documento de evidencia generado automaticamente con Python + reportlab</i>", ParagraphStyle("Footer", parent=small, alignment=1, fontSize=9)))
    story.append(PageBreak())

    # ═══ CONTENIDO ═══
    story.append(Paragraph("Contenido", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    toc_items = [
        "1. Objetivo de la Actividad",
        "2. Diagrama del Flujo de Git",
        "3. Archivos del Proyecto",
        "4. Pasos Cronologicos (1-8)",
        "5. Captura de Terminal",
        "6. Contenido de los Archivos Fuente",
        "7. Tabla de Comandos Git Utilizados",
        "8. Evidencia Completa de Comandos",
        "9. Push a la Nube - PENDIENTE",
        "10. Checklist de Entrega",
        "11. Conclusion",
    ]
    for item in toc_items:
        story.append(Paragraph(item, body))
    story.append(PageBreak())

    # ═══ 1. OBJETIVO ═══
    story.append(Paragraph("1. Objetivo de la Actividad", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Esta actividad tiene como finalidad demostrar el uso basico del sistema de "
        "control de versiones Git en un entorno completamente local. El alumno debe "
        "crear un proyecto sencillo con un mensaje de 'Hola Mundo', inicializar un "
        "repositorio Git, realizar commits, consultar el historial de cambios y "
        "manejar ramas basicas.", body))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Requisitos especificos:</b>", body))
    reqs = [
        "Crear un repositorio con archivos basicos (HTML o Python)",
        "Realizar al menos 2 commits con diferentes mensajes",
        "Consultar git log, git status, git branch",
        "Configuracion LOCAL (no global) de usuario y email",
        "Documentar todo el procedimiento con capturas de salida",
        "Subir carpeta a nube (PENDIENTE - requiere credenciales propias)",
    ]
    for r in reqs:
        story.append(Paragraph(f"- {r}", body))
    story.append(PageBreak())

    # ═══ 2. DIAGRAMA FLUJO GIT ═══
    story.append(Paragraph("2. Diagrama del Flujo de Git", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "El siguiente diagrama muestra el flujo basico de Git: los archivos se "
        "editan en el Working Directory, se agregan al Staging Area con 'git add', "
        "y finalmente se guardan en el Repository con 'git commit'.", body))
    story.append(Spacer(1, 0.1*inch))
    story.append(RLImage(img_workflow, width=6.5*inch, height=2.6*inch))
    story.append(PageBreak())

    # ═══ 3. ARCHIVOS DEL PROYECTO ═══
    story.append(Paragraph("3. Archivos del Proyecto", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("La estructura del proyecto 'hola-mundo' esta compuesta por los siguientes archivos:", body))
    story.append(Spacer(1, 0.1*inch))
    story.append(RLImage(img_files, width=6.5*inch, height=2.8*inch))
    story.append(Spacer(1, 0.15*inch))

    struct_data = [
        ["Archivo", "Tipo", "Descripcion"],
        [".gitignore", "Config", "Excluye archivos temporales de Python, OS, IDE"],
        ["README.md", "Documento", "Titulo, integrantes, objetivo de la actividad"],
        ["hola.py", "Python", "Script que imprime 'Hola Mundo desde Python!'"],
        ["index.html", "HTML", "Pagina web que muestra 'Hola Mundo desde Git!'"],
    ]
    struct_table = Table(struct_data, colWidths=[1.5*inch, 1*inch, 4*inch])
    struct_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f9f9f9"), white]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(struct_table)
    story.append(PageBreak())

    # ═══ 4. PASOS CRONOLOGICOS ═══
    story.append(Paragraph("4. Pasos Cronologicos de la Actividad", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "A continuacion se documenta cada paso ejecutado en orden cronologico, "
        "incluyendo el comando utilizado, la salida real obtenida del terminal, y "
        "una descripcion detallada de que se hizo y por que.", body))
    story.append(Spacer(1, 0.15*inch))

    steps = [
        ("Paso 1: Crear estructura de carpetas",
         'New-Item -ItemType Directory -Path "D:\\leandro\\A3\\hola-mundo" -Force',
         "Se crearon las carpetas de trabajo: hola-mundo (proyecto) y evidencias (capturas)."),
        ("Paso 2: Crear archivos del proyecto",
         "Se crearon: README.md, index.html, hola.py, .gitignore",
         "Archivos iniciales: README documenta la actividad, HTML y Python imprimen Hola Mundo, .gitignore excluye temporales."),
        ("Paso 3: Inicializar repositorio Git",
         "git init",
         "Inicializa repositorio vacio. Crea carpeta .git/ con metadatos del repositorio local."),
        ("Paso 4: Configurar usuario local",
         'git config --local user.name "Alumno A3"',
         "Configuracion SOLO local (--local), sin afectar otros repositorios del sistema."),
        ("Paso 5: Primer commit",
         'git commit -m "feat: hola mundo inicial"',
         "Primer commit raiz (root-commit) con 4 archivos, 52 inserciones. Prefijo 'feat' = conventional commits."),
        ("Paso 6: Modificar archivos",
         "(Edicion de index.html y hola.py)",
         "Se modificaron saludos para demostrar control de versiones. Diferencias visibles con git diff."),
        ("Paso 7: Segundo commit",
         'git commit -m "feat: modifica saludo para demostrar historial"',
         "Segundo commit con 2 archivos modificados, 4 inserciones y 3 eliminaciones."),
        ("Paso 8: Verificar historial y renombrar rama",
         "git log --oneline && git status && git branch -M main",
         "Historial de 2 commits, working tree limpio, rama renombrada de master a main."),
    ]
    for title, cmd, desc_text in steps:
        story.append(Paragraph(f"<b>{title}</b>", h2))
        story.append(Paragraph(f"<b>Comando:</b> {cmd}", code))
        story.append(Paragraph(f"<b>Descripcion:</b> {desc_text}", desc))
        story.append(Spacer(1, 0.08*inch))

    story.append(PageBreak())

    # ═══ 5. CAPTURA DE TERMINAL ═══
    story.append(Paragraph("5. Captura de Terminal", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "Captura simulada de la terminal mostrando la secuencia completa de comandos "
        "ejecutados durante la actividad:", body))
    story.append(Spacer(1, 0.1*inch))
    story.append(RLImage(img_terminal, width=6.5*inch, height=3.2*inch))
    story.append(PageBreak())

    # ═══ 6. CONTENIDO ARCHIVOS FUENTE ═══
    story.append(Paragraph("6. Contenido de los Archivos Fuente", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Contenido completo de cada archivo tal como quedo despues del segundo commit:", body))
    story.append(Spacer(1, 0.1*inch))

    for fname in ["README.md", "index.html", "hola.py", ".gitignore"]:
        fcontent = read_proyecto(fname)
        story.append(Paragraph(f"<b>Archivo: {fname}</b>", h3))
        story.append(Paragraph(safe(fcontent), code))
        story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

    # ═══ 7. TABLA DE COMANDOS ═══
    story.append(Paragraph("7. Tabla de Comandos Git Utilizados", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Resumen de todos los comandos Git ejecutados en la actividad:", body))
    story.append(Spacer(1, 0.1*inch))
    story.append(RLImage(img_cmds, width=6.5*inch, height=3.2*inch))
    story.append(PageBreak())

    # ═══ 8. EVIDENCIA COMPLETA ═══
    story.append(Paragraph("8. Evidencia Completa de Comandos", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Todas las salidas capturadas en archivos .txt:", body))
    story.append(Spacer(1, 0.1*inch))

    evidences = [
        ("01_git_log_oneline.txt", "git log --oneline", "Historial simplificado"),
        ("02_git_status.txt", "git status", "Estado del repositorio"),
        ("03_git_branch_list.txt", "git branch -a", "Lista de ramas"),
        ("04_git_log_graph.txt", "git log --graph", "Grafico historial"),
        ("05_git_config_local.txt", "git config --local --list", "Config local"),
        ("06_git_log_full.txt", "git log --format", "Log completo"),
        ("07_git_diff_segundo_commit.txt", "git diff HEAD~1..HEAD", "Diferencia commits"),
        ("08_git_logultimo_detalle.txt", "git log -1 --format", "Detalle ultimo commit"),
        ("09_estructura_archivos.txt", "Get-ChildItem", "Estructura archivos"),
    ]
    for ename, ecmd, edesc in evidences:
        econtent = read_evidencia(ename)
        story.append(Paragraph(f"<b>{ename}</b> — {ecmd} — {edesc}", h3))
        story.append(Paragraph(safe(econtent), code))
        story.append(Spacer(1, 0.08*inch))

    story.append(PageBreak())

    # ═══ 9. PUSH PENDIENTE ═══
    story.append(Paragraph("9. Push a la Nube - PENDIENTE", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cc6600")))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        "<b>NOTA:</b> Los siguientes pasos NO fueron ejecutados porque requieren "
        "credenciales personales del alumno (token GitHub o autenticacion SSH). "
        "Se documentan aqui para completitud de la actividad.", warn))
    story.append(Spacer(1, 0.15*inch))
    story.append(RLImage(img_push, width=6.5*inch, height=2*inch))
    story.append(Spacer(1, 0.15*inch))

    push_steps = [
        ("Paso Pendiente 1: Autenticarse en GitHub",
         "gh auth login",
         "Inicia autenticacion con GitHub CLI. Requiere token personal o usuario/contrasena del alumno."),
        ("Paso Pendiente 2: Crear repositorio remoto",
         "gh repo create hola-mundo --public --source=. --push",
         "Crea repositorio publico en GitHub y sube el codigo local automaticamente."),
        ("Paso Pendiente 3: Agregar remote (alternativa)",
         "git remote add origin https://github.com/USUARIO/hola-mundo.git",
         "Si el repositorio ya existe, agrega la URL remota como 'origin'."),
        ("Paso Pendiente 4: Subir codigo",
         "git push -u origin main",
         "Sube la rama main al repositorio remoto. Primera vez pide autenticacion."),
    ]
    for ptitle, pcmd, pdesc in push_steps:
        story.append(Paragraph(f"<b>{ptitle}</b>", body))
        story.append(Paragraph(f"<b>Comando:</b> {pcmd}", code))
        story.append(Paragraph(pdesc, desc))
        story.append(Spacer(1, 0.08*inch))

    story.append(PageBreak())

    # ═══ 10. CHECKLIST ═══
    story.append(Paragraph("10. Checklist de Entrega", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Verificacion de todos los requisitos de la actividad:", body))
    story.append(Spacer(1, 0.1*inch))

    checklist = [
        ("[X]", "Carpeta hola-mundo creada con archivos iniciales"),
        ("[X]", "README.md con titulo, integrantes y objetivo"),
        ("[X]", "index.html que imprime 'Hola Mundo'"),
        ("[X]", "hola.py que imprime 'Hola Mundo'"),
        ("[X]", ".gitignore basico para Python, OS e IDE"),
        ("[X]", "Git inicializado con 'git init'"),
        ("[X]", "Configuracion LOCAL de user.name y user.email"),
        ("[X]", "Configuracion NO global (verificado con git config --local --list)"),
        ("[X]", "Primer commit: 'feat: hola mundo inicial'"),
        ("[X]", "Segundo commit: 'feat: modifica saludo para demostrar historial'"),
        ("[X]", "git log --oneline ejecutado y capturado"),
        ("[X]", "git status ejecutado y capturado"),
        ("[X]", "git branch -M main ejecutado (rama renombrada)"),
        ("[X]", "Evidencias guardadas en carpeta evidencias/*.txt"),
        ("[X]", "PDF de evidencia generado con pasos cronologicos"),
        ("[X]", "NO se toco la configuracion global de Git"),
        ("[X]", "NO se ejecuto 'gh auth login'"),
        ("[X]", "NO se realizo push a repositorio remoto"),
        ("[ ]", "Push a la nube - PENDIENTE (requiere credenciales propias)"),
        ("[ ]", "Subir carpeta a nube - PENDIENTE"),
    ]
    for chk, item in checklist:
        story.append(Paragraph(f"<b>{chk}</b> {item}", check_style))

    story.append(PageBreak())

    # ═══ 11. CONCLUSION ═══
    story.append(Paragraph("11. Conclusion", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        "La Actividad 3 se completo exitosamente en su totalidad local. Se "
        "demostro el ciclo basico de Git: desde la inicializacion de un repositorio "
        "hasta la creacion de multiples commits con diferentes mensajes.", body))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Conceptos aplicados:</b>", body))
    concepts = [
        "<b>git init:</b> Inicializar un repositorio vacio",
        "<b>git config --local:</b> Configurar usuario sin afectar otros repos",
        "<b>git add:</b> Agregar archivos al area de staging",
        "<b>git commit:</b> Crear un snapshot del estado del proyecto",
        "<b>git log:</b> Consultar el historial de commits",
        "<b>git status:</b> Verificar el estado del working tree",
        "<b>git branch -M:</b> Renombrar la rama actual",
        "<b>git diff:</b> Comparar versiones de archivos",
    ]
    for c in concepts:
        story.append(Paragraph(f"- {c}", desc))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph(
        "<b>Pendiente:</b> El push a GitHub quedo pendiente porque requiere "
        "credenciales personales del alumno. Los comandos necesarios estan "
        "documentados en la seccion 9 de este documento.", body))
    story.append(Spacer(1, 0.3*inch))
    story.append(HRFlowable(width="40%", thickness=2, color=HexColor("#0f3460")))
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("<i>Fin del documento de evidencia - Actividad 3 - Git: Hola Mundo</i>", center))
    story.append(Paragraph("<i>Generado el 26 de septiembre de 2026</i>", center))

    doc.build(story)
    file_size = os.path.getsize(OUTPUT)
    print(f"PDF generado: {OUTPUT}")
    print(f"Tamano: {file_size} bytes ({file_size/1024:.1f} KB)")
    if file_size > 100 * 1024:
        print("OK: El PDF supera los 100 KB")
    else:
        print(f"AVISO: El PDF tiene {file_size/1024:.1f} KB, se necesitan >100 KB")

if __name__ == "__main__":
    build_pdf()
