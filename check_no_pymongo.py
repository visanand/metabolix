# scripts/check_no_pymongo.py
import os

print("🔍 Checking for forbidden 'pymongo' imports...")

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, encoding="utf-8") as f:
                contents = f.read()
                if "pymongo" in contents:
                    print(f"❌ Forbidden pymongo usage found in {path}")
                    exit(1)

print("✅ No pymongo usage detected. All good.")
