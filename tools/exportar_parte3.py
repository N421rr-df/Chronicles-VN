from pathlib import Path
import re

# ==================================================
# CONFIGURAÇÃO
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = PROJECT_ROOT / "game"

OUTPUT_DIR = Path(
    r"E:\RenPy\NotebookLM\Chronicles VN\Engenharia_Reversa\Parte3"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==================================================
# LOG
# ==================================================

print("=" * 60)
print("EXPORTADOR PARTE 3")
print("=" * 60)
print("Projeto:", PROJECT_ROOT)
print("Game:", GAME_DIR)
print("Saída:", OUTPUT_DIR)
print()

# ==================================================
# COLEÇÕES
# ==================================================

classes = set()
funcoes = set()
imports = set()
personagens = set()
imagens = set()
audios = set()
variaveis = set()
labels = set()
screens = set()

# ==================================================
# AUXILIAR
# ==================================================

def salvar(nome, dados):

    caminho = OUTPUT_DIR / nome

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as f:

        for item in sorted(dados):
            f.write(f"{item}\n")

    print(f"Gerado: {nome}")

# ==================================================
# PROCURA ARQUIVOS
# ==================================================

arquivos_rpy = list(
    GAME_DIR.rglob("*.rpy")
)

print(
    f"Arquivos .rpy encontrados: {len(arquivos_rpy)}"
)

if len(arquivos_rpy) == 0:

    print("Nenhum arquivo .rpy encontrado.")
    raise SystemExit()

# ==================================================
# ANALISA
# ==================================================

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

        labels.update(
            re.findall(
                r'^\s*label\s+([A-Za-z0-9_]+)',
                texto,
                re.MULTILINE
            )
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

        personagens.update(
            [
                f"{cod} = {nome}"
                for cod, nome in re.findall(
                    r'define\s+([A-Za-z0-9_]+)\s*=\s*Character\s*\(\s*[\'"]([^\'"]+)',
                    texto
                )
            ]
        )

        imagens.update(
            re.findall(
                r'^\s*image\s+(.+?)\s*=',
                texto,
                re.MULTILINE
            )
        )

        audios.update(
            re.findall(
                r'define\s+audio\.([A-Za-z0-9_]+)',
                texto
            )
        )

        variaveis.update(
            re.findall(
                r'^\s*(?:define|default)\s+([A-Za-z0-9_\.]+)',
                texto,
                re.MULTILINE
            )
        )

    except Exception as erro:

        print(
            f"Erro em {arquivo}: {erro}"
        )

# ==================================================
# EXPORTA
# ==================================================

salvar(
    "30_Classes.txt",
    classes
)

salvar(
    "31_Funcoes.txt",
    funcoes
)

salvar(
    "32_Imports.txt",
    imports
)

salvar(
    "33_Personagens.txt",
    personagens
)

salvar(
    "34_Imagens_Declaradas.txt",
    imagens
)

salvar(
    "35_Audios_Declarados.txt",
    audios
)

salvar(
    "36_Variaveis.txt",
    variaveis
)

salvar(
    "37_Labels.txt",
    labels
)

salvar(
    "38_Screens.txt",
    screens
)

# ==================================================
# FRAMEWORKS
# ==================================================

frameworks = []

for pasta in GAME_DIR.iterdir():

    if not pasta.is_dir():
        continue

    nome = pasta.name.lower()

    palavras = [
        "nqtr",
        "quest",
        "inventory",
        "phone",
        "calendar",
        "time",
        "map",
        "gallery"
    ]

    for palavra in palavras:

        if palavra in nome:

            frameworks.append(
                pasta.name
            )

            break

salvar(
    "39_Frameworks_Detectados.txt",
    frameworks
)

# ==================================================
# MANUAL
# ==================================================

manual = []

manual.append(
    "MANUAL AUTOMÁTICO DO PROJETO"
)

manual.append("")
manual.append(
    f"Arquivos RPY: {len(arquivos_rpy)}"
)

manual.append(
    f"Labels: {len(labels)}"
)

manual.append(
    f"Screens: {len(screens)}"
)

manual.append(
    f"Classes: {len(classes)}"
)

manual.append(
    f"Funções: {len(funcoes)}"
)

manual.append(
    f"Personagens: {len(personagens)}"
)

manual.append(
    f"Variáveis: {len(variaveis)}"
)

manual.append(
    f"Imagens: {len(imagens)}"
)

manual.append(
    f"Áudios: {len(audios)}"
)

manual.append("")
manual.append(
    "Frameworks Detectados:"
)

for item in frameworks:

    manual.append(
        f"- {item}"
    )

with open(
    OUTPUT_DIR / "40_Manual_Projeto.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(manual)
    )

print()
print("PARTE 3 CONCLUÍDA")
