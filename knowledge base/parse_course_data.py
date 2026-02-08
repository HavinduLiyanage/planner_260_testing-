
import json
import re

file_path = r'c:\Users\havin\OneDrive\Documents\Software Testing Assignment\knowledge base\Software-Testing---CSI3105-2-2026-Feb-08_07-41-50-506\viewer\course-data.js'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # regex to find the start of the JSON object
    match = re.search(r'window\.COURSE_DATA\s*=\s*({.*})', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        # Parse JSON
        data = json.loads(json_str)
        
        with open('debug_assignments.txt', 'w', encoding='utf-8') as out_f:
            assignments = data.get('assignments')
            out_f.write(f"Type: {type(assignments)}\n")
            if isinstance(assignments, list):
                out_f.write(f"Length: {len(assignments)}\n")
                out_f.write(f"Content: {assignments}\n")
            else:
                out_f.write(f"Content: {assignments}\n")

        with open('course_structure.txt', 'w', encoding='utf-8') as out_f:
            out_f.write(f"Course Title: {data.get('title')}\n")
            
            modules = data.get('modules', [])
            for module in modules:
                module_name = module.get('name')
                out_f.write(f"\nModule: {module_name}\n")
                items = module.get('items', [])
                for item in items:
                    title = item.get('title')
                    out_f.write(f"  - Item: {title}\n")
                    
                    item_content = item.get('content', '')
                    if 'href=' in item_content:
                        links = re.findall(r'href="([^"]+)"', item_content)
                        for link in links:
                             if 'viewer/files' in link:
                                 out_f.write(f"      Link: {link}\n")

    else:
        print("Could not find JSON object in file.")

except Exception as e:
    print(f"Error: {e}")
