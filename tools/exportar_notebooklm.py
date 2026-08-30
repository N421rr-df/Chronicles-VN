### exportar_notebooklm.py

from pathlib import Path
from datetime import datetime
import re

# ==========================
# CONFIGURAÇÃO
# ==========================

PROJECT_ROOT = Path(__file__).parent.parent

GAME_DIR = PROJECT_ROOT / "game"

OUTPUT_FILE = Path(
    r"E:\RenPy\NotebookLM\Chronicles VN\Engenharia_Reversa\Codigo\Chronicles VN_Completo.txt"
)

IGNORAR_PASTAS = {
    "__pycache__",
    ".git",
    ".vscode",
    "cache",
    "saves"
}

SEPARADOR = "=" * 100

# ==========================
# FUNÇÕES
# ==========================

def tamanho_legivel(bytes_size):
    kb = bytes_size / 1024
    return f"{kb:.2f} KB"


def listar_rpy():
    arquivos = []

    for arquivo in GAME_DIR.rglob("*.rpy"):

        ignorar = False

        for parte in arquivo.parts:
            if parte in IGNORAR_PASTAS:
                ignorar = True
                break

        if not ignorar:
            arquivos.append(arquivo)

    return sorted(arquivos)


def ler_arquivo(caminho):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "latin-1",
        "cp1252"
    ]

    for enc in encodings:
        try:
            with open(caminho, "r", encoding=enc) as f:
                return f.read()
        except:
            pass

    return ""


# ==========================
# EXECUÇÃO
# ==========================

def main():

    arquivos = listar_rpy()

    total_linhas = 0
    total_bytes = 0

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as saida:

        # =====================================
        # CABEÇALHO
        # =====================================

        saida.write("CAPITANIA DAS BRUMAS\n")
        saida.write("EXPORTAÇÃO PARA NOTEBOOKLM\n")
        saida.write("\n")

        saida.write(
            f"Gerado em: "
            f"{datetime.now():%Y-%m-%d %H:%M:%S}\n"
        )

        saida.write(
            f"Projeto: {GAME_DIR.parent.name}\n\n"
        )

        # =====================================
        # ÍNDICE
        # =====================================

        saida.write(SEPARADOR + "\n")
        saida.write("ÍNDICE DE ARQUIVOS\n")
        saida.write(SEPARADOR + "\n\n")

        for arquivo in arquivos:

            relativo = arquivo.relative_to(GAME_DIR)

            caminho_renpy = (
                "game/" +
                str(relativo).replace("\\", "/")
            )

            saida.write(
                f"- {caminho_renpy}\n"
            )

        saida.write("\n\n")

        # =====================================
        # ARQUIVOS
        # =====================================

        for numero, arquivo in enumerate(
            arquivos,
            start=1
        ):

            relativo = arquivo.relative_to(
                GAME_DIR
            )

            caminho_renpy = (
                "game/" +
                str(relativo).replace("\\", "/")
            )

            conteudo = ler_arquivo(
                arquivo
            )

            linhas = len(
                conteudo.splitlines()
            )

            tamanho = arquivo.stat().st_size

            modificado = datetime.fromtimestamp(
                arquivo.stat().st_mtime
            )

            total_linhas += linhas
            total_bytes += tamanho

            print(
                f"[{numero}/{len(arquivos)}] "
                f"{caminho_renpy}"
            )

            saida.write("\n\n")
            saida.write(SEPARADOR + "\n")

            saida.write(
                f"### {caminho_renpy}\n"
            )

            saida.write(
                f"### LINHAS: {linhas}\n"
            )

            saida.write(
                f"### TAMANHO: "
                f"{tamanho_legivel(tamanho)}\n"
            )

            saida.write(
                f"### MODIFICADO: "
                f"{modificado:%Y-%m-%d %H:%M:%S}\n"
            )

            saida.write(SEPARADOR + "\n\n")

            saida.write(conteudo)

            if not conteudo.endswith("\n"):
                saida.write("\n")

        # =====================================
        # RESUMO FINAL
        # =====================================

        saida.write("\n\n")
        saida.write(SEPARADOR + "\n")
        saida.write("ESTATÍSTICAS DO PROJETO\n")
        saida.write(SEPARADOR + "\n\n")

        saida.write(
            f"Arquivos .rpy: "
            f"{len(arquivos)}\n"
        )

        saida.write(
            f"Linhas totais: "
            f"{total_linhas}\n"
        )

        saida.write(
            f"Tamanho total: "
            f"{tamanho_legivel(total_bytes)}\n"
        )

    print()
    print("Concluído.")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
