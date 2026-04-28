import email
import email.utils
import os
from email.message import EmailMessage

def extract_mht_text(mht_file_path):
    with open(mht_file_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    
    text_parts = []
    
    def extract_parts(part):
        if part.get_content_type() == 'text/html' or part.get_content_type() == 'text/plain':
            charset = part.get_content_charset() or 'utf-8'
            payload = part.get_payload(decode=True)
            if payload:
                text = payload.decode(charset, errors='ignore')
                text_parts.append(text)
        elif part.is_multipart():
            for subpart in part.get_payload():
                extract_parts(subpart)
    
    extract_parts(msg)
    return '\n\n'.join(text_parts)

if __name__ == "__main__":
    mht_path = "/workspaces/AntiGravity_Bobov_App/legal/Входящие - marchyachts@gmail.com - Gmail.mht"
    if os.path.exists(mht_path):
        extracted_text = extract_mht_text(mht_path)
        output_path = "/workspaces/AntiGravity_Bobov_App/legal/extracted_correspondence.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"Extracted text saved to {output_path}")
    else:
        print("MHT file not found")