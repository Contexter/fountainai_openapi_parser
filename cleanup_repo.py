import os
import shutil
from datetime import datetime

# Define directories and files to clean
backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(backup_dir, exist_ok=True)

# Define paths to back up and remove
paths_to_clean = [
    "__pycache__",
    ".pytest_cache",
    "auto_fix_openapi_spec.py",
    "extend_tests.py",
    "extend_tests_for_coverage.py",
    "finalize_tests_for_coverage.py",
    "setup_tests.py",
    "update_openapi_spec.py",
]

# Create .gitignore file
def create_gitignore():
    gitignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environment directories
venv/
.env/

# Test results
.pytest_cache/
*.pytest_cache

# Ignore compiled test files
tests/__pycache__/
openapi_parser/__pycache__/

# Ignore temporary or local config files
.DS_Store
*.log
*.tmp
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    print(".gitignore file created.")

# Backup and remove specified paths
def backup_and_remove():
    for path in paths_to_clean:
        if os.path.exists(path):
            dest_path = os.path.join(backup_dir, path)
            try:
                if os.path.isdir(path):
                    shutil.move(path, dest_path)
                else:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(path, dest_path)
                print(f"Backed up and removed {path}.")
            except Exception as e:
                print(f"Error backing up {path}: {e}")

# Display backup contents
def display_backup_contents():
    print("\nBackup contents:")
    for root, dirs, files in os.walk(backup_dir):
        level = root.replace(backup_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 2 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

# Run the cleanup process
if __name__ == "__main__":
    print("Starting repository cleanup...")
    create_gitignore()
    backup_and_remove()
    display_backup_contents()
    print(f"\nRepository cleaned. A backup has been created in '{backup_dir}'. Review the backup before committing.")

