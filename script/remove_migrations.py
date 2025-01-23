import os
from pathlib import Path

PATH = Path(__name__).resolve().parent


def remove_all_migrations():
    for root, dirs, files in os.walk(PATH):
        for f in files:
            root_split = root.split("/")
            
            if root_split[-1] == "migrations" and root_split[-3] == "odoo":
                if f != "__init__.py":
                    print(os.path.join(root, f))
            
if __name__ == "__main__":
    remove_all_migrations()