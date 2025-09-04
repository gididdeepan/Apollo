import os
import webbrowser
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cable_project.settings")

    # Open browser automatically (after a small delay)
    url = "http://127.0.0.1:8000"
    try:
        webbrowser.open_new(url)  # Opens in default browser
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
    execute_from_command_line([
        "manage.py",
        "runserver",
        "127.0.0.1:8000",
        "--noreload"
    ])

# import sys
# import os
# from django.core.management import execute_from_command_line

# if __name__ == "__main__":
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cable_project.settings")
#     execute_from_command_line(sys.argv)
