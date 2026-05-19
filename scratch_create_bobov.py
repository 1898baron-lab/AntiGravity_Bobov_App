import sys
import os
import time
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm_mcp.auth import load_cached_tokens
from notebooklm_mcp.api_client import NotebookLMClient

tokens = load_cached_tokens()
os.environ['NOTEBOOKLM_AUTHUSER'] = '0'
client = NotebookLMClient(cookies=tokens.cookies, csrf_token="", session_id="")

title = "⚖️ AntiGravity: Дело Бобова (Юридический ассистент)"
try:
    notebook_id = client.create_notebook(title).id
    print(f"Created notebook: {notebook_id}")
    
    files_to_upload = [
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\bobov_attack_dashboard.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Bobov_Dossier_v3_Debug.html",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Bobov_Legal_Attack_Complete_2026.html",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\chatgpt_insights.txt",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\claim_fz68_compensation_v1.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\complaint_125_upk_v1.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\complaint_draft_new.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\complaint_prosecutor_bobov.txt",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\complaint_prosecutor_final.txt",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\complaint_prosecutor_v2_158.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\court_practice_analysis.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\court_precedents_report.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\evidence_synthesis_12m.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\extracted_correspondence.txt",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\legal_framework.txt",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\notary_request_letter.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\report_for_father.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\ultimatum_notary_final.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\Legal_Tactics\CAREER_PATH_BOBOV.md",
        r"C:\ANTIGRAVITY\1\obsidian_brain\2_KNOWLEDGE\SYNTHESIS\BOBOV_LEGAL_ATTACK.md"
    ]
    
    for filepath in files_to_upload:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            filename = os.path.basename(filepath)
            source_id = client.add_text_source(notebook_id, text=content, title=filename)
            print(f"Uploaded {filename}: {source_id}")
            time.sleep(2)
        else:
            print(f"File not found: {filepath}")

except Exception as e:
    print(f"Error: {e}")
