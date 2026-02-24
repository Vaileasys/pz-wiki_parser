import subprocess
from pathlib import Path
import platform
import sys
import os

from scripts.utils import echo, color
from scripts.core import config_manager as cfg
from scripts.core.constants import OUTPUT_DIR

is_windows = platform.system() == "Windows"
is_pwb = bool(cfg.get_pywikibot())

def run_batch_file(batch_path: str, name: str = None, args: list[str] = None):
    if not is_windows:
        echo.error("Batch files can only be run on Windows.")
        return
    
    if not name:
        name = Path(batch_path).name
    echo.info(f"Running {name}, please wait...")

    command = [batch_path]
    if args:
        command += args

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    echo.info(result.stdout)
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

    echo.info(result.stdout)
    if result.stderr:
        echo.error(f"There was a problem running {name}")
        echo.error(result.stderr)


def run_zomboid_decompiler():
    print(color.style("ZomboidDecompiler", color.BLUE))
    
    # Determine the executable based on OS
    if is_windows:
        executable_name = 'ZomboidDecompiler.bat'
    else:
        executable_name = 'ZomboidDecompiler'
    
    decompiler_path = os.path.join('resources', 'ZomboidDecompiler', 'bin', executable_name)
    game_path = Path(cfg.get_game_directory())
    output_path = Path(OUTPUT_DIR) / "ZomboidDecompiler"
    
    # Run the command
    if is_windows:
        run_batch_file(decompiler_path, args=[str(game_path), str(output_path)])
    else:
        # Ensure the executable has execute permissions on Linux
        import stat
        current_permissions = os.stat(decompiler_path).st_mode
        os.chmod(decompiler_path, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        
        command = [decompiler_path, str(game_path), str(output_path)]
        echo.info(f"Running {executable_name}, please wait...")
        result = subprocess.run(command, capture_output=True, text=True)
        
        echo.info(result.stdout)
        if result.stderr:
            echo.error(f"There was a problem running {executable_name}")
            echo.write(result.stderr, style_func=color.error)

    echo.success(f"ZomboidDecompiler process completed. Decompiled files should be found in \"{output_path}\"")

    return False
    

def run_pywikibot():
    if not is_pwb:
        echo.error("Pywikibot has not been set up yet. Ensure you have downloaded and set up pywikibot:\nhttps://www.mediawiki.org/wiki/Manual:Pywikibot/Installation")
        choice = input("Enter the path to the entry point python (.py) file:\n> ").strip()

        if not choice:
            echo.error("No path detected. Returning to previous menu.")
            return True

        cfg.set_pywikibot(choice)
    
    run_python_file(cfg.get_pywikibot())

    echo.success("Pywikibot process completed.")

    return False


def choose_process(run_directly: bool = False):
    post_pwb = ""
    if not is_pwb:
        post_pwb += color.warning(" [Setup]")

    options = [
        "1: ZomboidDecompiler - Runs ZomboidDecompiler.",
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