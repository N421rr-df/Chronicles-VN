from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent

GAME_DIR = PROJECT_ROOT / "game"

OUTPUT_DIR = Path(
    r"E:\RenPy\NotebookLM\Chronicles VN\Engenharia_Reversa\Codigo"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

labels = set()
variaveis = set()
personagens = set()
screens = set()
imagens = set()
audios = set()

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
        re.findall(
            r'define\s+([A-Za-z0-9_]+)\s*=\s*Character\s*\(\s*[\'"]([^\'"]+)',
            texto
        )
    )

    screens.update(
        re.findall(
            r'^\s*screen\s+([A-Za-z0-9_]+)',
            texto,
            re.MULTILINE
        )
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
            r'audio\.([A-Za-z0-9_]+)',
            texto
        )
    )

def salvar(nome, dados):

    caminho = OUTPUT_DIR / nome

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as f:

        for item in sorted(dados):
            f.write(f"{item}\n")

salvar("Labels.txt", labels)
salvar("Variaveis.txt", variaveis)
salvar(
    "Personagens.txt",
    [f"{cod} = {nome}"
     for cod, nome in personagens]
)
salvar("Screens.txt", screens)
salvar("Imagens.txt", imagens)
salvar("Audios.txt", audios)

with open(
    OUTPUT_DIR / "Estatisticas.txt",
    "w",
    encoding="utf-8"
) as f:

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
        f"Imagens: {len(imagens)}\n"
    )

    f.write(
        f"Áudios: {len(audios)}\n"
    )

print("Exportação concluída.")
