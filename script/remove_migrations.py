import os
from pathlib import Path

PATH = Path(__name__).resolve().parent


def remove_all_migrations():
    for root, dirs, files in os.walk(PATH):
        for f in files:
            root_split = root.split("/")
            
            if root_split[-1] == "migrations" and root_split[-3] == "odoo":
                if f != "__init__.py":
                    try:
                        os.remove(os.path.join(root, f))
                        print("{:^20} : {:^20} : {:<20} -> Removed".format("Migration", root_split[-2], f))
                    except Exception as e:
                        print("{:^20} : {:^20} : {:<20} -> {}".format("Migration", root_split[-2], f, str(e)))
if __name__ == "__main__":
    remove_all_migrations()