import subprocess
from pathlib import Path
import platform
import sys

from scripts.utils import echo, color
from scripts.core import config_manager as cfg
from scripts.core.constants import OUTPUT_DIR

is_windows = platform.system() == "Windows"
is_zombdec = bool(cfg.get_zomboid_decompiler())
is_pwb = bool(cfg.get_pywikibot())

def run_batch_file(batch_path: str, name: str = None, args: list[str] = None):
    if not is_windows:
        echo.error("Batch files can only be run on Windows.")
        return
    
    if not name:
        name = Path(batch_path).name
    echo.info(f"Running {name}...")

    command = [batch_path]
    if args:
        command += args

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        echo.error(f"There was a problem running {name}")
        echo.write(result.stderr, style_func=color.error)

def run_python_file(script_path: str, name: str = None):
    if not name:
        name = Path(script_path).name
    echo.info(f"Running {name}...")

    result = subprocess.run(
        [sys.executable, script_path],
        shell=True,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        echo.error(f"There was a problem running {name}")
        print(result.stderr)


def run_zomboid_decompiler():
    print(color.style("ZomboidDecompiler", color.BLUE))
    if not is_windows:
        print("This process can only be run on Windows. Please manually run the Zomboid Decompiler:\nhttps://github.com/demiurgeQuantified/ZomboidDecompiler")
        return True
    
    if not is_zombdec:
        print("ZomboidDecompiler has not been set up yet. Ensure you have downloaded the ZomboidDecompiler:\nhttps://github.com/demiurgeQuantified/ZomboidDecompiler")
        choice = input("Enter the path to the ZomboidDecompiler batch (.bat) file:\n> ").strip()

        if not choice:
            print("No path detected. Returning to previous menu.")
            return True

        cfg.set_zomboid_decompiler(choice)
    
    game_path = Path(cfg.get_game_directory())
    output_path = Path(OUTPUT_DIR) / "ZomboidDecompiler"
    
    run_batch_file(cfg.get_zomboid_decompiler(),args=[str(game_path), str(output_path)])

    echo.success(f"ZomboidDecompiler process completed. Decompiled files should be found in \"{output_path}\"")

    return False
    

def run_pywikibot():
    if not is_pwb:
        print("Pywikibot has not been set up yet. Ensure you have downloaded and set up pywikibot:\nhttps://www.mediawiki.org/wiki/Manual:Pywikibot/Installation")
        choice = input("Enter the path to the entry point python (.py) file:\n> ").strip()

        if not choice:
            print("No path detected. Returning to previous menu.")
            return True

        cfg.set_pywikibot(choice)
    
    run_python_file(cfg.get_pywikibot())

    echo.success("Pywikibot process completed.")

    return False


def choose_process(run_directly: bool = False):
    post_zombdec = ""
    post_pwb = ""
    if not is_windows:
        post_zombdec += color.error(" [Windows Only]")
    if not is_zombdec:
        post_zombdec += color.warning(" [Setup]")
    if not is_pwb:
        post_pwb += color.warning(" [Setup]")

    options = [
        "1: ZomboidDecompiler - Runs ZomboidDecompiler." + post_zombdec,
        "2: pywikibot - Runs pywikibot." + post_pwb
    ]
    options.append("Q: Quit" if run_directly else "B: Back")

    while True:
        print("\nWhich process do you want to run?")
        choice = input("\n".join(options) + "\n> ").strip().lower()

        if choice in ('q', 'b'):
            break

        try:
            if int(choice) in range(1, 3):
                break
        except ValueError:
            pass
        print("Invalid choice.")
    
    return choice

def main(run_directly: bool = False):
    while True:
        choice = choose_process(run_directly)

        if choice == '1':
            do_repeat = run_zomboid_decompiler()
            if not do_repeat:
                break
        
        elif choice == '2':
            do_repeat = run_pywikibot()
            if not do_repeat:
                break
        elif choice in ('q', 'b'):
            break


if __name__ == "__main__":
    main(run_directly=True)