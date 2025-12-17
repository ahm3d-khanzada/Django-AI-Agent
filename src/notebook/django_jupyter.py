import os
import sys
import pathlib

CURRENT_FILE = pathlib.Path(__file__).resolve()
NOTEBOOK_DIR = CURRENT_FILE.parent
DJANGO_PROJECT_ROOT = NOTEBOOK_DIR.parent

DJANGO_SETTINGS_MODULE = "movies.settings"


def init(verbose=True):
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except ImportError:
        pass

    if verbose:
        print("Notebook dir :", NOTEBOOK_DIR)
        print("Django root  :", DJANGO_PROJECT_ROOT)

    if not DJANGO_PROJECT_ROOT.exists():
        raise FileNotFoundError(DJANGO_PROJECT_ROOT)

    os.chdir(DJANGO_PROJECT_ROOT)

    if str(DJANGO_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(DJANGO_PROJECT_ROOT))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

    import django
    django.setup()

    if verbose:
        print("Django ready in Jupyter")












































































# """
# django_jupyter.py

# Safe initialization of Django environment for Jupyter Notebooks.
# """

# import os
# import sys
# import pathlib


# # -----------------------------
# # Paths Configuration
# # -----------------------------
# CURRENT_FILE = pathlib.Path(__file__).resolve()  # Current file: django_jupyter.py
# NOTEBOOK_DIR = CURRENT_FILE.parent               # Notebook folder
# DJANGO_PROJECT_ROOT = NOTEBOOK_DIR.parent       # src/ folder (Django project root)

# # Django settings module
# DJANGO_SETTINGS_MODULE = "movies.settings"


# # -----------------------------
# # Django Initialization
# # -----------------------------
# def init(verbose: bool = True):
#     """
#     Initialize Django environment for Jupyter notebooks.

#     - Applies nest_asyncio for notebook compatibility
#     - Adds Django project root to sys.path
#     - Sets environment variables for Django settings
#     - Calls django.setup()
#     """
#     # ---------------------------------------
#     # Apply nest_asyncio for async support
#     # ---------------------------------------
#     try:
#         import nest_asyncio
#         nest_asyncio.apply()
#         if verbose:
#             print("✔ nest_asyncio applied (Jupyter compatible)")
#     except ImportError:
#         if verbose:
#             print("⚠ nest_asyncio not installed. Skipping async patch.")

#     # ---------------------------------------
#     # Debug / Info print
#     # ---------------------------------------
#     if verbose:
#         print(f"Notebook directory: {NOTEBOOK_DIR}")
#         print(f"Django project root: {DJANGO_PROJECT_ROOT}")

#     # ---------------------------------------
#     # Check Django project root exists
#     # ---------------------------------------
#     if not DJANGO_PROJECT_ROOT.exists():
#         raise FileNotFoundError(f"Django project root not found: {DJANGO_PROJECT_ROOT}")

#     # ---------------------------------------
#     # Change working directory to Django project root
#     # ---------------------------------------
#     os.chdir(DJANGO_PROJECT_ROOT)

#     # ---------------------------------------
#     # Add Django project root to Python path
#     # ---------------------------------------
#     if str(DJANGO_PROJECT_ROOT) not in sys.path:
#         sys.path.insert(0, str(DJANGO_PROJECT_ROOT))

#     # ---------------------------------------
#     # Set environment variables
#     # ---------------------------------------
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
#     os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

#     # ---------------------------------------
#     # Setup Django
#     # ---------------------------------------
#     import django
#     if not django.apps.apps.ready:  # Avoid double setup
#         django.setup()

#     if verbose:
#         print("✅ Django environment initialized successfully")
