#!/usr/bin/env python3
from pathlib import Path
import stat
import sys

LOCK_CODE = 'DRAGON-404'
TREASURE_SCRIPT = 'from textwrap import dedent\n\nprint(\n    dedent(\n        r"""\n        ----------------------------------------\n        FELICIDADES. HAS ENCONTRADO EL TESORO.\n        ----------------------------------------\n\n               ___________\n              \'._==_==_=_.\',\n              .-\\:      /-.\n             | (|:.     |) |\n              \'-|:.     |-\'\n                \\::.    /\n                 \'::. .\'\n                   ) (\n                 _.\' \'._\n                `-------`\n\n        Lo has conseguido usando la terminal.\n\n        Comandos que has practicado:\n        - pwd\n        - ls\n        - cd\n        - cat\n        - find\n        - grep\n        - python o python3 con argumentos\n\n        Si quieres seguir, vuelve a la raiz del juego y abre:\n        RETOS_EXTRA.txt\n        """\n    ).strip()\n)\n'


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python3 abrir_candado.py DRAGON-404")
        return 1

    codigo = sys.argv[1].strip()
    if codigo != LOCK_CODE:
        print("Codigo incorrecto. El candado sigue cerrado.")
        print("Pista: vuelve a la biblioteca y busca CODIGO_COFRE con grep -R.")
        return 1

    tesoro_dir = Path(".tesoro")
    tesoro_dir.mkdir(exist_ok=True)
    tesoro_path = tesoro_dir / "tesoro.py"
    tesoro_path.write_text(TREASURE_SCRIPT, encoding="utf-8")
    tesoro_path.chmod(tesoro_path.stat().st_mode | stat.S_IXUSR)

    print("Candado abierto correctamente.")
    print("Se ha revelado .tesoro/tesoro.py")
    print("Comando exacto para continuar:")
    print("  python3 .tesoro/tesoro.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
