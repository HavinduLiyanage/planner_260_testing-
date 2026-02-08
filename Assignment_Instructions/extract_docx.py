import xml.etree.ElementTree as ET
import sys

def extract_text_from_docx_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        text = []
        for elem in root.iter():
            if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
                if elem.text:
                    text.append(elem.text)
            elif elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
                text.append('\n')
                
        return "".join(text)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_docx.py <xml_path> <output_file>")
        sys.exit(1)
    
    xml_path = sys.argv[1]
    output_file = sys.argv[2]
    
    text = extract_text_from_docx_xml(xml_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Extracted text to {output_file}")
