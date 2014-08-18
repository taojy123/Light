
#!/usr/bin/env python
import os
import sys
import webbrowser
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lighting.settings")



if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv.append("runserver")
        sys.argv.append("0.0.0.0:8000")
    else:
        webbrowser.open_new_tab('http://127.0.0.1:8000')
    print sys.argv
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
