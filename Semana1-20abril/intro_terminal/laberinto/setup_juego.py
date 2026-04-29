from __future__ import annotations

import argparse
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


BASE_NAME = "Laberinto_Terminal"
LOCK_CODE = "DRAGON-404"


@dataclass(frozen=True)
class GameFile:
    path: str
    content: str
    executable: bool = False


def clean(text: str) -> str:
    return dedent(text).strip("\n") + "\n"


TREASURE_SCRIPT = clean(
    "\n".join(
        [
            "from textwrap import dedent",
            "",
            "print(",
            "    dedent(",
            '        r"""',
            "        ----------------------------------------",
            "        FELICIDADES. HAS ENCONTRADO EL TESORO.",
            "        ----------------------------------------",
            "",
            "               ___________",
            "              '._==_==_=_.',",
            "              .-\\:      /-.",
            "             | (|:.     |) |",
            "              '-|:.     |-'",
            "                \\::.    /",
            "                 '::. .'",
            "                   ) (",
            "                 _.' '._",
            "                `-------`",
            "",
            "        Lo has conseguido usando la terminal.",
            "",
            "        Comandos que has practicado:",
            "        - pwd",
            "        - ls",
            "        - cd",
            "        - cat",
            "        - find",
            "        - grep",
            "        - python o python3 con argumentos",
            "",
            "        Si quieres seguir, vuelve a la raiz del juego y abre:",
            "        RETOS_EXTRA.txt",
            '        """',
            "    ).strip()",
            ")",
        ]
    )
)


UNLOCKER_SCRIPT = clean(
    dedent(
        f"""
        #!/usr/bin/env python3
        from pathlib import Path
        import stat
        import sys

        LOCK_CODE = {LOCK_CODE!r}
        TREASURE_SCRIPT = {TREASURE_SCRIPT!r}


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
        """
    )
)


GAME_FILES: tuple[GameFile, ...] = (
    GameFile(
        "leeme.txt",
        clean(
            """
            ====================================
                 EL LABERINTO DE LA TERMINAL
            ====================================

            Tu mision es encontrar el tesoro del castillo.

            Para abrir la Caja_Fuerte del Sotano_Oscuro vas a necesitar:
            - una llave escondida en lo mas alto del castillo
            - un codigo secreto oculto entre libros y registros
            - ejecutar el comando correcto cuando llegues al candado

            Comandos recomendados para esta aventura:
            - pwd
            - ls
            - cd
            - cat
            - find
            - grep
            - python o python3

            Ruta sugerida:
            1. Entra en Sala_Principal
            2. Lee PISTA_1.txt
            3. Sigue las pistas sin usar explorador grafico

            Reglas del juego:
            - Mira donde estas antes de moverte
            - Lee los archivos de texto
            - Usa TAB para autocompletar
            - Si te pierdes, vuelve a usar pwd y ls
            """
        ),
    ),
    GameFile(
        "mapa_laberinto.txt",
        clean(
            """
            MAPA DEL LABERINTO

            - Sala_Principal/
            - Sotano_Oscuro/
            - Torre_Alta/
            - Taller_del_Guardia/

            Rumores del castillo:
            - El sotano guarda la caja.
            - La torre guarda la llave.
            - La biblioteca guarda el codigo.
            - El comando correcto abre el final.
            """
        ),
    ),
    GameFile(
        "RETOS_EXTRA.txt",
        clean(
            """
            RETOS EXTRA PARA SEGUIR PRACTICANDO

            Cuando termines la mision principal, prueba esto:

            1. Crea una carpeta llamada mochila dentro del laberinto.
               mkdir mochila

            2. Copia la llave del sotano a esa carpeta.
               cp Torre_Alta/Biblioteca/Archivo_Secreto/llave_sotano.txt mochila/

            3. Crea una bitacora y escribe una linea.
               touch mochila/bitacora.txt
               echo "He superado el laberinto" > mochila/bitacora.txt

            4. Renombra una pista secundaria.
               mv Sala_Principal/pista_confusa.txt Sala_Principal/pista_ordenada.txt

            5. Borra un archivo temporal del taller.
               rm Taller_del_Guardia/borrar_esto.tmp

            6. Busca todos los archivos .txt del juego.
               find . -name "*.txt"

            7. Busca el codigo sin abrir archivo por archivo.
               grep -R "CODIGO_COFRE" .
            """
        ),
    ),
    GameFile(
        "Sala_Principal/polvo.txt",
        clean(
            """
            Nada interesante por aqui.
            El polvo no abre cofres.
            """
        ),
    ),
    GameFile(
        "Sala_Principal/silla_rota.log",
        clean(
            """
            Registro del mayordomo:
            La silla se rompio cuando alguien intento alcanzar un libro sin usar
            la escalera.
            """
        ),
    ),
    GameFile(
        "Sala_Principal/pista_confusa.txt",
        clean(
            """
            Esta nota sirve mejor como practica para renombrar archivos.
            No contiene la pista principal.
            """
        ),
    ),
    GameFile(
        "Sala_Principal/PISTA_1.txt",
        clean(
            """
            PISTA 1

            El primer secreto esta donde hace frio y casi no entra luz.
            Baja al Sotano_Oscuro y escucha lo que dice la puerta.
            """
        ),
    ),
    GameFile(
        "Sotano_Oscuro/eco.txt",
        clean(
            """
            El eco repite:
            "La caja existe, pero sigue cerrada."
            """
        ),
    ),
    GameFile(
        "Sotano_Oscuro/PISTA_2.txt",
        clean(
            """
            PISTA 2

            La Caja_Fuerte esta cerrada.
            La llave no esta aqui.
            La guardaron en lo mas alto del castillo.

            Sube a Torre_Alta/Biblioteca.
            Si no encuentras la llave a simple vista, usa find.
            """
        ),
    ),
    GameFile(
        "Sotano_Oscuro/Caja_Fuerte/candado.txt",
        clean(
            f"""
            CANDADO DE LA CAJA FUERTE

            Inscripcion del metal:
            "La llave abre la cerradura."
            "El codigo abre el mecanismo."
            "El comando correcto abre el final."

            Ya deberias tener el codigo: {LOCK_CODE}

            Cuando estes en esta carpeta, escribe exactamente:
            python3 abrir_candado.py {LOCK_CODE}

            Si tu sistema usa python en vez de python3, prueba:
            python abrir_candado.py {LOCK_CODE}
            """
        ),
    ),
    GameFile(
        "Sotano_Oscuro/Caja_Fuerte/pista_final.txt",
        clean(
            """
            Si el candado se abre bien, el propio script te dira el siguiente
            comando exacto para llegar al tesoro.
            """
        ),
    ),
    GameFile(
        "Sotano_Oscuro/Caja_Fuerte/abrir_candado.py",
        UNLOCKER_SCRIPT,
        executable=True,
    ),
    GameFile(
        "Torre_Alta/escalera_caracol.txt",
        clean(
            """
            Cada escalon cruje.
            Quien sube por curiosidad encuentra respuestas.
            Quien sube sin leer, se pierde.
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/catalogo.txt",
        clean(
            """
            CATALOGO DE LA BIBLIOTECA

            - historia_del_reino.txt
            - bestiario.txt
            - poemas.txt
            - registro_arcano.txt
            - Archivo_Secreto/

            Si buscas algo concreto, no abras todo a mano.
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/historia_del_reino.txt",
        clean(
            """
            El castillo fue construido para ensenar paciencia, orden y una
            costumbre profesional: mirar primero y actuar despues.
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/bestiario.txt",
        clean(
            """
            BESTIARIO

            Dragon: guarda codigos y tesoros.
            Buho: observa desde lo alto.
            Ratones: roen pergaminos, pero nunca pistas importantes.
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/poemas.txt",
        clean(
            """
            Quien usa la terminal con calma,
            rara vez se pierde.
            Quien usa find con criterio,
            siempre vuelve con premio.
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/registro_arcano.txt",
        clean(
            f"""
            REGISTRO ARCANO

            Entrada 14:
            CODIGO_COFRE={LOCK_CODE}

            Nota del bibliotecario:
            Guarda bien este codigo. Lo necesitaras al volver a la Caja_Fuerte.
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/PISTA_3.txt",
        clean(
            """
            PISTA 3

            La llave no esta al aire libre.
            Se escondio dentro de Archivo_Secreto.

            Consejo:
            - usa ls para orientarte
            - usa find si quieres localizar la llave mas rapido
            - usa grep para descubrir el codigo del cofre
            """
        ),
    ),
    GameFile(
        "Torre_Alta/Biblioteca/Archivo_Secreto/llave_sotano.txt",
        clean(
            """
            LLAVE DEL SOTANO

            Bien hecho.
            Esta es la llave correcta para la Caja_Fuerte del Sotano_Oscuro.

            Antes de volver abajo te falta una cosa:
            el codigo secreto del cofre.

            Pista:
            Vuelve un nivel arriba, a la Biblioteca, y busca alli la palabra
            CODIGO_COFRE con grep -R.
            """
        ),
    ),
    GameFile(
        "Taller_del_Guardia/plantilla.txt",
        clean(
            """
            Plantilla de practica.
            Puedes copiarme o dejarme como estoy.
            """
        ),
    ),
    GameFile(
        "Taller_del_Guardia/borrar_esto.tmp",
        clean(
            """
            Archivo temporal del guardia.
            Sirve para practicar rm cuando termine la aventura.
            """
        ),
    ),
)


def write_game_file(base_dir: Path, game_file: GameFile) -> None:
    target = base_dir / game_file.path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(game_file.content, encoding="utf-8")
    if game_file.executable:
        target.chmod(target.stat().st_mode | stat.S_IXUSR)


def setup(base_dir: Path, force: bool = False) -> None:
    if base_dir.exists():
        if any(base_dir.iterdir()) and not force:
            raise FileExistsError(
                f"La carpeta '{base_dir}' ya existe y no esta vacia. "
                "Usa --force para recrearla."
            )
        if force:
            shutil.rmtree(base_dir)

    base_dir.mkdir(parents=True, exist_ok=True)
    for game_file in GAME_FILES:
        write_game_file(base_dir, game_file)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crea un laberinto de carpetas para practicar terminal."
    )
    parser.add_argument(
        "--base",
        default=BASE_NAME,
        help=(
            "Carpeta de salida del juego. Por defecto crea "
            f"'{BASE_NAME}' en el directorio actual."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Borra y recrea la carpeta si ya existe.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    base_dir = Path(args.base).expanduser().resolve()

    try:
        setup(base_dir, force=args.force)
    except FileExistsError as error:
        print(error, file=sys.stderr)
        return 1

    print("Juego configurado correctamente.")
    print(f"Se ha creado la carpeta '{base_dir.name}' en: {base_dir}")
    print()
    print("Para empezar:")
    print(f"  cd {base_dir}")
    print("  cat leeme.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
