
import xml.etree.ElementTree as ET
import os

docx_path = r'c:\Users\havin\OneDrive\Documents\Software Testing Assignment\knowledge base\temp_extracted\workshop_nine_docx\word\document.xml'

try:
    tree = ET.parse(docx_path)
    root = tree.getroot()
    
    # Namespaces in docx xml
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    text = []
    for elem in root.iter():
        if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
            if elem.text:
                text.append(elem.text)
        elif elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
            text.append('\n')
            
    full_text = "".join(text)
    print(full_text)
    
except Exception as e:
    print(f"Error: {e}")
