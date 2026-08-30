from pathlib import Path
import re
from collections import defaultdict
from datetime import datetime

# =====================================================
# CONFIGURAÇÃO
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = PROJECT_ROOT / "game"

OUTPUT_DIR = Path(
    r"E:\RenPy\NotebookLM\Chronicles VN\Engenharia_Reversa\Dependencias"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# LOG
# =====================================================

LOG = []

def log(msg):

    print(msg)
    LOG.append(msg)

# =====================================================
# SALVAR
# =====================================================

def salvar(nome, linhas):

    caminho = OUTPUT_DIR / nome

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as f:

        for linha in linhas:
            f.write(f"{linha}\n")

    log(f"Arquivo salvo: {nome}")

# =====================================================
# INÍCIO
# =====================================================

log("=" * 60)
log("EXPORTADOR DE DEPENDÊNCIAS")
log("=" * 60)

log(f"Projeto: {PROJECT_ROOT}")
log(f"Game: {GAME_DIR}")
log(f"Saída: {OUTPUT_DIR}")

if not GAME_DIR.exists():

    log("ERRO: pasta game não encontrada!")

    salvar(
        "00_ERRO.txt",
        [
            "A pasta game não foi encontrada.",
            f"Esperado: {GAME_DIR}"
        ]
    )

    raise SystemExit()

# =====================================================
# COLEÇÕES
# =====================================================

labels = {}
screens = {}

label_refs = defaultdict(set)
screen_refs = defaultdict(set)

# =====================================================
# LISTA ARQUIVOS
# =====================================================

arquivos_rpy = list(
    GAME_DIR.rglob("*.rpy")
)

log(
    f"Arquivos .rpy encontrados: {len(arquivos_rpy)}"
)

if len(arquivos_rpy) == 0:

    salvar(
        "00_ERRO.txt",
        [
            "Nenhum arquivo .rpy encontrado.",
            f"Pasta analisada: {GAME_DIR}"
        ]
    )

    raise SystemExit()

# =====================================================
# PASSO 1
# MAPEIA LABELS E SCREENS
# =====================================================

for arquivo in arquivos_rpy:

    try:

        try:

            texto = arquivo.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            texto = arquivo.read_text(
                encoding="latin-1"
            )

        rel = str(
            arquivo.relative_to(
                PROJECT_ROOT
            )
        )

        encontrados = re.findall(
            r'^\s*label\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )

        for lbl in encontrados:

            labels[lbl] = rel

        encontrados = re.findall(
            r'^\s*screen\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )

        for scr in encontrados:

            screens[scr] = rel

    except Exception as e:

        log(
            f"ERRO lendo {arquivo}: {e}"
        )

log(
    f"Labels encontradas: {len(labels)}"
)

log(
    f"Screens encontradas: {len(screens)}"
)

# =====================================================
# PASSO 2
# REFERÊNCIAS
# =====================================================

for arquivo in arquivos_rpy:

    try:

        try:

            texto = arquivo.read_text(
                encoding="utf-8"
            )

        except UnicodeDecodeError:

            texto = arquivo.read_text(
                encoding="latin-1"
            )

        rel = str(
            arquivo.relative_to(
                PROJECT_ROOT
            )
        )

        # CALL

        for alvo in re.findall(
            r'\bcall\s+([A-Za-z0-9_]+)',
            texto
        ):

            label_refs[alvo].add(rel)

        # JUMP

        for alvo in re.findall(
            r'\bjump\s+([A-Za-z0-9_]+)',
            texto
        ):

            label_refs[alvo].add(rel)

        # CALL SCREEN

        for alvo in re.findall(
            r'call\s+screen\s+([A-Za-z0-9_]+)',
            texto
        ):

            screen_refs[alvo].add(rel)

        # SHOW SCREEN

        for alvo in re.findall(
            r'show\s+screen\s+([A-Za-z0-9_]+)',
            texto
        ):

            screen_refs[alvo].add(rel)

    except Exception as e:

        log(
            f"ERRO processando {arquivo}: {e}"
        )

# =====================================================
# EXPORTA LABELS
# =====================================================

linhas = []

for lbl in sorted(labels):

    linhas.append("=" * 60)
    linhas.append(f"LABEL: {lbl}")
    linhas.append("")
    linhas.append("Definida em:")
    linhas.append(labels[lbl])

    linhas.append("")
    linhas.append("Utilizada por:")

    refs = sorted(
        label_refs.get(lbl, [])
    )

    if refs:

        linhas.extend(refs)

    else:

        linhas.append(
            "[SEM REFERÊNCIAS]"
        )

    linhas.append("")

salvar(
    "17_Referencias_Labels.txt",
    linhas
)

# =====================================================
# EXPORTA SCREENS
# =====================================================

linhas = []

for scr in sorted(screens):

    linhas.append("=" * 60)
    linhas.append(f"SCREEN: {scr}")
    linhas.append("")
    linhas.append("Definida em:")
    linhas.append(screens[scr])

    linhas.append("")
    linhas.append("Utilizada por:")

    refs = sorted(
        screen_refs.get(scr, [])
    )

    if refs:

        linhas.extend(refs)

    else:

        linhas.append(
            "[SEM REFERÊNCIAS]"
        )

    linhas.append("")

salvar(
    "18_Referencias_Screens.txt",
    linhas
)

# =====================================================
# LABELS NÃO USADAS
# =====================================================

nao_usadas = []

for lbl in sorted(labels):

    if lbl not in label_refs:

        nao_usadas.append(
            f"{lbl} -> {labels[lbl]}"
        )

if not nao_usadas:

    nao_usadas.append(
        "Nenhuma label sem referência encontrada."
    )

salvar(
    "27_Labels_Nao_Utilizadas.txt",
    nao_usadas
)

# =====================================================
# DIAGNÓSTICO
# =====================================================

salvar(
    "99_Diagnostico.txt",
    [
        f"Data: {datetime.now()}",
        "",
        f"Projeto: {PROJECT_ROOT}",
        f"Game: {GAME_DIR}",
        "",
        f"Arquivos RPY: {len(arquivos_rpy)}",
        f"Labels: {len(labels)}",
        f"Screens: {len(screens)}",
        f"Referências Labels: {len(label_refs)}",
        f"Referências Screens: {len(screen_refs)}"
    ]
)

salvar(
    "98_Log.txt",
    LOG
)

log("Concluído.")
