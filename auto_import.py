import os


def auto_import(module):
    try:
        exec(f"import {module}")
        return f"import {module}"
    except ImportError:
        print(f"Automatically installing {module}...\n")
        try:
            os.system(f'python -m pip install {module}')
            print(f"Successfully installed {module}.")
        except ImportError:
            try:
                os.system(f'python -m pip3 install {module}')
                print(f"Successfully installed {module}.\n")
            except ImportError:
                print(f"ERROR: Failed to installed {module}.")
        return f"import {module}"
