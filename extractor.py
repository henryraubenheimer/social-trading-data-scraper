# from google import genai
# import json
# import pandas as pd

# # export GEMINI_API_KEY=AIzaSyAYABkXxJKZh8H7VCAw6Pm3CFftD6lSJvg

# with open('screenshots/screenshot_1.png', 'rb') as f:
#     image_bytes = f.read()

# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=[genai.types.Part.from_bytes(
#         data=image_bytes,
#         mime_type='image/jpeg',
#       ), "Output the data in this table in JSON format"]
# )

# df = pd.DataFrame(json.loads(response.text[7:-3]))
# df.to_csv('csvs/screenshot_1.csv', index=False)

import os
import json
import pandas as pd
from google import genai

def get_mime_type(filename):
    """Get MIME type based on file extension"""
    ext = os.path.splitext(filename)[1].lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff'
    }
    return mime_types.get(ext, 'image/jpeg')  # Default to jpeg

# Create csvs directory if it doesn't exist
os.makedirs('csvs', exist_ok=True)

# Get all image files from screenshots directory
screenshot_dir = 'screenshots'
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}

# Get list of image files and sort them for consistent processing order
image_files = [f for f in os.listdir(screenshot_dir) 
               if any(f.lower().endswith(ext) for ext in image_extensions)]
image_files.sort()

for filename in image_files:
    input_path = os.path.join(screenshot_dir, filename)
    
    # Create output filename (replace image extension with .csv)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join('csvs', f'{base_name}.csv')
    
    print(f"Processing {filename}...")
    
    try:
        with open(input_path, 'rb') as f:
            image_bytes = f.read()
        
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[genai.types.Part.from_bytes(
                data=image_bytes,
                mime_type=get_mime_type(filename),
            ), "Output the data in this table in JSON format"]
        )
        
        df = pd.DataFrame(json.loads(response.text[7:-3]))
        df.to_csv(output_path, index=False)
        
        print(f"Successfully processed {filename} -> {base_name}.csv")
        
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
        continue

print("Processing complete!")