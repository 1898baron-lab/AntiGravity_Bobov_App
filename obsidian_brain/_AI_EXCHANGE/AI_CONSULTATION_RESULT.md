# 🏛 Консилиум ИИ: Проектирование Verifier Layer

## 🧙‍♂️ Вердикт Claude (Архитектор)
Понял структуру. Отвечаю по задаче.

Архитектура verifier.py

Главный принцип: верификатор не ищет ответ — он проверяет утверждение против известной базы. Три уровня:

python
class Verifier:
    def verify(self, claim: dict) -> VerificationResult:
        # Уровень 1 — структурная проверка
        # Уровень 2 — проверка по базе НТД
        # Уровень 3 — confidence scoring

Уровень 1 — структурная проверка (всегда):

python
def _check_structure(self, claim: dict) -> bool:
    required = ["statement", "gost_ref", "value", "units"]
    return all(k in claim for k in required)

Если агент не указал ГОСТ — вернуть confidence: "unverified", не писать в FROM_CHATGPT.md.

Уровень 2 — база НТД (локальный JSON):

python
# ntd_database.json
{
  "ГОСТ 30893.2": {
    "class_f": {"tolerance_mm": 1.0, "diagonal_mm": 1.5},
    "class_m": {"tolerance_mm": 2.0, "diagonal_mm": 3.0}
  },
  "ГОСТ 1050-2013": {
    "Steel_20": {"sigma_t": 245, "sigma_b_min": 410}
  }
}

Верификатор сверяет утверждение агента с этим файлом. Не совпало — confidence: "low".

Уровень 3 — итоговый вердикт:

python
@dataclass
class VerificationResult:
    verified: bool
    confidence: str      # "high" | "medium" | "low" | "unverified"
    gost_ref: str        # "ГОСТ 30893.2, п.3.1"
    deviation: str       # что не совпало, если есть
    approved_by: str     # "auto" | "human_required"

Встройка в agent_core.py:

python
# 4. VERIFICATION
verified_data = self._verify(results)

if verified_data["confidence"] == "unverified":
    self._record_final_response({
        "status": "HOLD — требуется ручная проверка",
        "data": verified_data
    })
    return  # не пишем непроверенный ответ

Главное правило для Росатома-контекста:

Если нет ГОСТ-ссылки с номером пункта — confidence = "unverified" автоматически. Агент пишет ответ только при high или medium.

Пушни agent_core.py в репу — встрою verifier.py туда же и покажу как они стыкуются.

---

## 🤖 Вердикт ChatGPT (Аудитор)

