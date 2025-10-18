"""
Utility module for handling different file formats
"""
import os

def read_file(file_path):
    """
    Read content from various file formats
    Supports .txt, .pdf, .docx
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.txt':
        return _read_txt(file_path)
    elif ext.lower() == '.pdf':
        return _read_pdf(file_path)
    elif ext.lower() == '.docx':
        return _read_docx(file_path)
    else:
        # Default to text reading for unknown formats
        return _read_txt(file_path)

def _read_txt(file_path):
    """Read text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def _read_pdf(file_path):
    """Read PDF file"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except ImportError:
        print("PyPDF2 not installed. Please install with: pip install PyPDF2")
        return ""
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def _read_docx(file_path):
    """Read DOCX file"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        print("python-docx not installed. Please install with: pip install python-docx")
        return ""
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

def save_results(results, output_path):
    """Save results to a file"""
    import pandas as pd
    
    df = pd.DataFrame(results)
    _, ext = os.path.splitext(output_path)
    
    if ext.lower() == '.csv':
        df.to_csv(output_path, index=False)
    elif ext.lower() == '.xlsx':
        df.to_excel(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)
    
    print(f"Results saved to {output_path}")