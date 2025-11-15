#!/usr/bin/env python3
"""Download test images for the 5 trained landmarks"""
import json
import requests
from pathlib import Path

# Load metadata
with open('data/metadata.json', 'r') as f:
    metadata = json.load(f)

# Create output directory
output_dir = Path('../TestImages/samples')
output_dir.mkdir(parents=True, exist_ok=True)

print("Downloading test images for each landmark...\n")

for landmark_name, images in metadata.items():
    # Download first 2 images for each landmark
    for i, img_info in enumerate(images[:2]):
        image_id = img_info['image_id']
        url = img_info['url']
        
        output_path = output_dir / f"{landmark_name}_{i+1}_{image_id}.jpg"
        
        if output_path.exists():
            print(f"✓ Already exists: {output_path.name}")
            continue
        
        try:
            print(f"Downloading {landmark_name} #{i+1}... ", end='', flush=True)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            output_path.write_bytes(response.content)
            print(f"✓ Saved to {output_path.name}")
        except Exception as e:
            print(f"✗ Failed: {str(e)}")

print(f"\n✓ Test images saved to: {output_dir.absolute()}")
print(f"\nLandmarks:")
for name in metadata.keys():
    print(f"  - {name}")
