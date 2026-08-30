from pathlib import Path
import re

# ==================================================
# CONFIGURAÇÃO
# ==================================================

PROJECT_ROOT = Path(__file__).parent.parent

GAME_DIR = PROJECT_ROOT / "game"

OUTPUT_DIR = Path(
    r"E:\RenPy\NotebookLM\Chronicles VN\Engenharia_Reversa"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==================================================
# EXTENSÕES
# ==================================================

IMG_EXT = {
    ".png", ".jpg", ".jpeg",
    ".webp", ".gif", ".bmp"
}

AUDIO_EXT = {
    ".ogg", ".mp3",
    ".wav", ".opus",
    ".flac"
}

VIDEO_EXT = {
    ".webm", ".mp4",
    ".avi", ".mov",
    ".mkv"
}

FONT_EXT = {
    ".ttf", ".otf",
    ".woff", ".woff2"
}

# ==================================================
# COLEÇÕES
# ==================================================

labels = set()
variaveis = set()
personagens = set()
screens = set()
classes = set()
funcoes = set()
imports = set()
calls = set()
jumps = set()

imagens = []
audios = []
videos = []
fontes = []

todos_arquivos = []

# ==================================================
# AUXILIARES
# ==================================================

def salvar(nome, dados):

    caminho = OUTPUT_DIR / nome

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as f:

        if isinstance(dados, list):
            for item in dados:
                f.write(f"{item}\n")
        else:
            for item in sorted(dados):
                f.write(f"{item}\n")

# ==================================================
# ESTRUTURA
# ==================================================

estrutura = []

for item in PROJECT_ROOT.rglob("*"):

    try:

        relativo = item.relative_to(
            PROJECT_ROOT
        )

        estrutura.append(
            str(relativo)
        )

        if item.is_file():

            todos_arquivos.append(
                str(relativo)
            )

            ext = item.suffix.lower()

            if ext in IMG_EXT:
                imagens.append(
                    str(relativo)
                )

            elif ext in AUDIO_EXT:
                audios.append(
                    str(relativo)
                )

            elif ext in VIDEO_EXT:
                videos.append(
                    str(relativo)
                )

            elif ext in FONT_EXT:
                fontes.append(
                    str(relativo)
                )

    except:
        pass

# ==================================================
# ANALISA RPY
# ==================================================

for arquivo in GAME_DIR.rglob("*.rpy"):

    try:

        texto = arquivo.read_text(
            encoding="utf-8"
        )

    except:

        try:

            texto = arquivo.read_text(
                encoding="latin-1"
            )

        except:

            continue

    labels.update(
        re.findall(
            r'^\s*label\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )
    )

    variaveis.update(
        re.findall(
            r'^\s*(?:default|define)\s+([A-Za-z0-9_\.]+)',
            texto,
            re.MULTILINE
        )
    )

    personagens.update(
        [
            f"{cod} = {nome}"
            for cod, nome in re.findall(
                r'define\s+([A-Za-z0-9_]+)\s*=\s*Character\s*\(\s*[\'"]([^\'"]+)',
                texto
            )
        ]
    )

    screens.update(
        re.findall(
            r'^\s*screen\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )
    )

    classes.update(
        re.findall(
            r'^\s*class\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )
    )

    funcoes.update(
        re.findall(
            r'^\s*def\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )
    )

    imports.update(
        re.findall(
            r'^\s*(?:import|from)\s+(.+)',
            texto,
            re.MULTILINE
        )
    )

    calls.update(
        re.findall(
            r'\bcall\s+([A-Za-z0-9_]+)',
            texto
        )
    )

    jumps.update(
        re.findall(
            r'\bjump\s+([A-Za-z0-9_]+)',
            texto
        )
    )

# ==================================================
# EXPORTAÇÃO
# ==================================================

salvar(
    "01_Estrutura_Projeto.txt",
    estrutura
)

salvar(
    "02_Arquivos.txt",
    todos_arquivos
)

salvar(
    "03_Labels.txt",
    labels
)

salvar(
    "04_Variaveis.txt",
    variaveis
)

salvar(
    "05_Personagens.txt",
    personagens
)

salvar(
    "06_Screens.txt",
    screens
)

salvar(
    "07_Classes.txt",
    classes
)

salvar(
    "08_Funcoes.txt",
    funcoes
)

salvar(
    "09_Imports.txt",
    imports
)

salvar(
    "10_Calls.txt",
    calls
)

salvar(
    "11_Jumps.txt",
    jumps
)

salvar(
    "12_Imagens.txt",
    imagens
)

salvar(
    "13_Audios.txt",
    audios
)

salvar(
    "14_Videos.txt",
    videos
)

salvar(
    "15_Fontes.txt",
    fontes
)

with open(
    OUTPUT_DIR / "16_Estatisticas.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        f"Arquivos: {len(todos_arquivos)}\n"
    )

    f.write(
        f"Labels: {len(labels)}\n"
    )

    f.write(
        f"Variáveis: {len(variaveis)}\n"
    )

    f.write(
        f"Personagens: {len(personagens)}\n"
    )

    f.write(
        f"Screens: {len(screens)}\n"
    )

    f.write(
        f"Classes: {len(classes)}\n"
    )

    f.write(
        f"Funções: {len(funcoes)}\n"
    )

    f.write(
        f"Imagens: {len(imagens)}\n"
    )

    f.write(
        f"Áudios: {len(audios)}\n"
    )

    f.write(
        f"Vídeos: {len(videos)}\n"
    )

    f.write(
        f"Fontes: {len(fontes)}\n"
    )

print("Engenharia Reversa concluída.")
