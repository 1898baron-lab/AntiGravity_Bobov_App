import re
import json
import asyncio
import os

class MastodontVerifier:
    """
    Verification Layer for Mastodont AI Factory.
    Enforces Rosatom/GOST engineering standards by auditing agent responses.
    """
    
    def __init__(self, ntd_db_path="scripts/ntd_database.json"):
        self.ntd_db_path = ntd_db_path
        self.ntd_data = self._load_ntd_db()

    def _load_ntd_db(self):
        try:
            with open(self.ntd_db_path, "r", encoding="utf-8") as f:
                return json.load(f).get("gost_database", [])
        except Exception:
            return []

    async def verify(self, response_text: str) -> dict:
        """
        Runs a 3-layer audit on the provided text.
        """
        report = {
            "status": "unverified",
            "confidence": 0,
            "findings": [],
            "missing_ntd": True
        }
        
        # Layer 1: Structure Audit
        has_structure = self._check_structure(response_text)
        if has_structure:
            report["findings"].append("Structure: OK (Logical blocks detected)")
            report["confidence"] += 20
        
        # Layer 2: NTD Audit (GOST/SP Search)
        found_ntd = self._audit_ntd(response_text)
        if found_ntd:
            report["findings"].append(f"NTD Audit: SUCCESS (Found: {', '.join(found_ntd)})")
            report["confidence"] += 60
            report["missing_ntd"] = False
            report["status"] = "verified"
        else:
            report["findings"].append("NTD Audit: FAILED (No valid GOST/SP references found)")
            
        # Layer 3: Engineering Keywords Audit
        keywords_score = self._audit_keywords(response_text)
        report["confidence"] += keywords_score
        
        # Final Confidence Normalization (cap at 100)
        report["confidence"] = min(report["confidence"], 100)
        
        return report

    def _check_structure(self, text):
        # Checks for headings or numbered lists
        return bool(re.search(r'#{1,3}\s|\d\.\s', text))

    def _audit_ntd(self, text):
        found = []
        # Basic regex for GOST and SP
        ntd_patterns = [r'ГОСТ\s\d+\.?\d*-?\d*', r'СП\s\d+\.\d+\.\d+']
        for pattern in ntd_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for m in matches:
                if m.upper() not in found:
                    found.append(m.upper())
        return found

    def _audit_keywords(self, text):
        score = 0
        technical_keywords = ["допуск", "сталь", "расчет", "чертеж", "материал", "КМД"]
        for kw in technical_keywords:
            if kw.lower() in text.lower():
                score += 4
        return score

async def test_verifier():
    verifier = MastodontVerifier()
    test_text = """
    Рекомендую использовать сталь Ст20 согласно ГОСТ 1050-2013. 
    Допуски по среднему классу точности ГОСТ 30893.1.
    """
    result = await verifier.verify(test_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_verifier())
