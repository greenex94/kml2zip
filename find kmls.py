import os
import shutil

# Get directory where the script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Output folder next to the script
OUTPUT_DIR = os.path.join(BASE_DIR, "collected_kml")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TARGET_NAME = "Field.kml"

copied_count = 0

for root, dirs, files in os.walk(BASE_DIR):
    if TARGET_NAME in files:
        source_path = os.path.join(root, TARGET_NAME)

        # Folder that contains Field.kml
        folder_name = os.path.basename(root.rstrip(os.sep))

        new_name = f"{folder_name}.kml"
        dest_path = os.path.join(OUTPUT_DIR, new_name)

        # Handle duplicate folder names
        counter = 1
        while os.path.exists(dest_path):
            new_name = f"{folder_name}_{counter}.kml"
            dest_path = os.path.join(OUTPUT_DIR, new_name)
            counter += 1

        shutil.copy2(source_path, dest_path)
        print(f"Copied: {source_path} -> {dest_path}")
        copied_count += 1

print(f"\nDone. {copied_count} files copied to: {OUTPUT_DIR}")
