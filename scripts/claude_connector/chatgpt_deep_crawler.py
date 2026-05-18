import requests
import json
import os
import re

# Новые разделенные токены из твоего лога
TOKEN_0 = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..jNVx9zhpqu6tLCml.QsKGBQCSB-qvDola7mwJ1VNyDD4MUuFOPnC7-JR6eZVbKam_BwwF70RxLyxqkdaoBM6UwMiMpz4dr6fcYX0MiL9cJnOB7QS_n235V-GFyXRzKbVEuTC9dXQeFkY3s19ChJNgycj7wPsJWVA48RRuhTlFXv85TxJNofREArf3iE-HTIAlKAwOBNeUtaPHuZNPynIVgbnM_8dLauD-Qr9b49ZtDUmR-6bKPYBWY5gX5z8r0fc36PKlx3P787nxNjl6b2K7tuFyA4wgd22rbLST7fOAODB_6MF3jhcpJFI5HS3y5q2WSlBaTYU7dfQoNRGwADlDkJrzLIxfwx3oVyTuMo_-QlAVEZ2v3O3qy9mugFlAwW5XSlu_WxMBKvc0PZO8QPu4TfngfptIsQCT-gn6gQBfVNadRTUZe22TTMr7yGRMkYAxbmmhLaruWfRqHrKLfOU8Meb2ynJ39lqS_LwQndjU_ppg8OGFZzKuvZKcOzLjo7C9s9DWkZow--JYOiSP0gud1Ew7vFS7l0Tri8ATFsWsi7YkOiDeo41ejLjAOiS4bmKfipJlhS6299bDaWZfrQicJaHAGzEdKDH0U7hSRqnu-s9bbrY8JL2cVd7rKuFTXVDNzr2b_WTc5dQdrxitYqiUPkcbokQoNJnVh63dbClUjJMV2N1yZhK3Hym6yl-Nr1gCYUuO6D_dF_7v9HZafTD7FI1DWYk9XXnexTyHcbGJfQy4xUSJlLGuVfjhnuXhGQZyvpoCb9Ni3DgfjNeiIu_ZoHKzjm9TF_KwVUakrHwUYM1aF6sj2OJfzJ2e55E2NBFPc1Tb91ASAbd2SUnoaL_ZMHGFfDaAmg8F1Dgaglc1RMVXtW1kplrdOaxmc_zu-3zWny0p-rGPd9HLwNgnrj6yZC7wdwxl406evCtbGK4wmn3UEwUQCOJBUdtcWIas2rSdlXGgclhOMrfEPOUOOFTLSfXsQcKhOeCe2VbfvvPo9GkmF0aiMNf2-artyJZgIqcAxpso_t9baPZ0cYRTUa2bPFTk6ZBinxhuZnRckasmBQbh_lJkkrR--mJOnhw6hxAnNybG_n2MHbG1AqsjMLm5_GQPIYwE9TP1KWaY_YDZzN5AObl1ZyX3JIqfjabJmuOh3NPh7_1YCa137jrnO46uqBFxod_IWcvEQ-2w7NN0vDEE7s7e-wraBJVqSIl3prr75SInxkR4VGI2p149RViBP9xtVZMDSUxuWMBkvs3Poco0LfIB_yjbo6If0lI3nssKBepnuNfeNue7AODCm9JjjLC3awg1uFiSNO1atxDcTu0mvncAL1onknIZy0-R6O7OpKIv_S-CrTYPMb41R_Ri0q9qgZvt4lSqRszu-nS72b6LwuKRcrSW39fZqfkjoRlTuVlgNhnzpmPhyy8RwNaMz9WlKpsEpLtpVgNaUnByVV6FH0uUpGVD0sazqsy8VuurxoPN707f5pgmnbCYulhV4ofUYN8mIR-v9cRSojXOmETu9ISvfrOtFEhS3eB6bHo-Yi4k4NKlysfVdY5y6Kmf8ltSCpIKLnuE9E3xL3mL7gjFLf8_5vcW1zf1ql3qBvMokO_PbUpVDdzz1MCu8Jk930IMy2ULOv2rHX22yDvwrQYlnqfuAy2a0-RFw7ccs8zz8P3-PAOareHK7SQwJv2_BFuIonM0wuTTnuT2bRnki9FGW5z17IrBTHIU0AbAqZN0PUeJ_hMHvz4dTrmtR3i1roa-8YFlg0g0epZHM2tGKrVRYbQ9dl27ysIE5-NLX4G3WS7uWOMLcbva7tEA6MF-7JweTSLHevZdKmJ7DIFmjb8lVNi4_8ZRccWmMUpEVqtrNYEQOXmlvnQ3xkO8aWsnnwIjceta4GkujixpqaRvQrLV7ovnfnAL-DfI_yT6hJQNhZ8Uc5jftamtwnidhD8Zxe9yXv_u0lXHw-pXYTMdUVASo6DF7oqTAoOkGlDX1VkvjX9MEpkzAQCatJwlN_9Jui6nRcGuw2-JzVQzVnHFh1gddnI7yUDm05g1k3jR7CCwDIO-CLsjwYoOl8bUrwfG5H7LtRIiI-1w5xg2FZbKkM0Pr1YpAt1IOnmTUd4FiQ_iLsu00FKoQvtsaySvFeNMz3X7ulnXW7Z5bb5UzKoix67Ido-OIsZ8zF2ARiOsNLPqXgknSGa3En1BsODX2BvWwAfgYGVF7FTUx7d6jpkXpsb9zszrUa2JjLgJCId4sffufSYlKyb-EJw9CUPJThHEG7KCJCFiZSA431ib_O1Y8fimK-dcwNTrR9xUzA689Y6ZJdH_KrMgr8bwXb6wjTdmVsETT5-dnY-YfOCeSAQVYXm4Dggk6Aqfvvo80fRAxP9CZv4GwAixWZ5EfxzBAxhgZ-KdljWUHRTIibOeoPO8DNQm1RNCQmEvW34UYHNqb6fYdyTgxZLvgDA16kOTZOyUyLKIFiwI1KSzi2divInMt-QwNd0v3mOWkj0G-uy7PgzBqwwmuPNi7Nc2VjpvbmWaQMdJMLbGIJjaaYtQ_Py27fdoBteMIMJZQxEB2-1m2hnD8e9BVaxytOMUmz2k4QLv3FNRhQH6u2Dq5oNNd5IboLIsn-tXto0B92rli5D6LBsgYpSk5xe_qkXQN61tBmqSgB1xAXORuTFojC-b9LKxsqz2alP5z0fppUEdKnv5OOrrwgkC2qjvKtvMfXdz6lcy_QzYTiJJJSh_Bz_KXOi1JO6rzRXtFDgZQLkXQI2EopAcINIM3k5mGoMaWtM7YtcI5V3vdjAB06lliqFhLInYs2a7QaGfXgYjllfh5_83Eqz2gD90v5r-0eRa5-gH5yRlGbEMbXisxw0-8dx-TCmbg_KVeUfOA2omlxbucVy0bopnO9pLxgVhN8FRGTVfiZMfgEoeER7vRruW2rwkZkCBhGqDQzzTjMPFHBsPxdE1ZdVJGC654_bX_OcQTEYPDTd4EVtT1ORy2nOnlJr-nTQ-VIiYAmZ5UEow3iFXiC16Deq9uid4qh0COX16ACYoACJBFKKaVJVCjhfKrRQiXPnT1IIW0OprTHdmIKOwKrn5p_hb3wzvY6o7bQIIPQHMa_HSNOGtcRM1iJdCbPjE4suyULMfE510iJcNHuCFTY6bPPfjt_KkUmYoPYkmTybZtSbpwgfNJQKiCTwBbZ-zHWiyW3O3eGwiOPlaGxca0Y8gfC5J8uUjE1x0ZY2gi854lAv6UTIMqBeJlBShLVelXJfr4QUq4Fdv729na7fvF9gOQ5Wmiu5G7zNPRYEKTb6_Q7455Pe7_B12rwmQPK2ghbzi71gkuzY-v9d9tJenBUB0ANWRxNH5HqOUGdZG_oUr2XV0QmHcZl1nUnmGGgwFwJCv3hp74_dqbGuTW9sBniYUyUX0TFLqVEpXYhC7ZqDY0OTJLAyrxdCCr5PlnZohoV8B6JqmCTHVBBA00gCj-EQ6gLtDvy67eKAB-qFRXOtpZeLA2GxQMmAds-koNXnVoXHWujvBKGs2np-faU27qIHPm9O9Zx5Yt_IHJdTcdTQv01p6-bqgEiNx0uchQJKM0uFJ386oE6zFB9QCANMWJe1ERjE1xKhT9Q1CFj8YpF7Sfx96IvaFx5EgNXL7hRkeSvfEamWWxHlE4apXUpQkrn-Slj93XB3-O9qB9k6auj38p2HAIrAqAcz_LlkkIsEsJsPwll0kcbvKsz2SjiUh7FdPk61XxpdKt4ZGa24DiWWudLo7pvyznruDbnGjXam3LKtZKmPEcjEdDnqHwjjwcL-Bj1b_-D_NFoid6ISQyup4e_DmwRtQ6DxGy7E-eLtdc31G4X8uoW8aO7V2v0Obl8N6mQjMiROoIMmd7CjC3FZKK9Zvrt0Up9NxRy0T9njZfY_L-D-yRm-sMex"
TOKEN_1 = "C8zQ5epaKZYswX88t9QHy4sIo-xS3LBgvubjqxKTIfy68vnKZ6X_J9j1EQh_XIpW2OUXIQAMZxjm57a5MF410v5lFdETV9pxBK8j_FkSsuD1O6GnXtHTwuqMorACbt5M76Lm3ZISNG9xOxyHfXJjWoTw4IccuSl6Xzj2R0yAQW__GPInb1WcSuSy4b2gVvNn2o27KQZht083VHr21nWuzcJ7EKNOwK-Eisv60FNc2Q7-EYsBhgw_1FMPBDpd65TvhTWqeDHZJpZuyabZxK3vulVP5QBilseqd4e9S_f5QdHdL2URgbCLiSPT-D2fj.1SKHYT5eCDAfUErvYTRtZQ"

COOKIES = {
    "__Secure-next-auth.session-token.0": TOKEN_0,
    "__Secure-next-auth.session-token.1": TOKEN_1,
    "oai-did": "acf99edd-f923-4902-9ae9-bb76cec6d1ed"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://chatgpt.com/"
}

def deep_export():
    print("[INFO] Starting deep export with split tokens...")
    list_url = "https://chatgpt.com/backend-api/conversations?offset=0&limit=50&order=updated"
    
    response = requests.get(list_url, cookies=COOKIES, headers=HEADERS)
    
    if response.status_code == 200:
        items = response.json().get("items", [])
        print(f"[SUCCESS] Found {len(items)} chats.")
        
        output_dir = r"C:\ANTIGRAVITY\1\obsidian_brain\Archives\ChatGPT_Recovered"
        os.makedirs(output_dir, exist_ok=True)
        
        # Ключевые слова для поиска
        keywords = ["велосипед", "стажировка", "бобов", "цпти", "росатом", "закреп"]
        
        for chat in items:
            title = chat.get("title", "Untitled")
            id = chat.get("id")
            
            if any(kw in title.lower() for kw in keywords):
                print(f"[FOUND] Matching chat: '{title}' (ID: {id})")
                
                # Скачиваем содержимое конкретного чата
                detail_url = f"https://chatgpt.com/backend-api/conversation/{id}"
                detail_res = requests.get(detail_url, cookies=COOKIES, headers=HEADERS)
                
                if detail_res.status_code == 200:
                    chat_data = detail_res.json()
                    
                    # Собираем текст в Markdown
                    md_content = f"# {title}\nURL: https://chatgpt.com/c/{id}\n\n"
                    mapping = chat_data.get("mapping", {})
                    
                    for node_id in mapping:
                        node = mapping[node_id]
                        msg = node.get("message")
                        if msg and msg.get("content"):
                            role = msg.get("author", {}).get("role", "unknown")
                            parts = msg.get("content", {}).get("parts", [])
                            text = "".join([p if isinstance(p, str) else str(p) for p in parts])
                            md_content += f"### {role.upper()}\n{text}\n\n"
                    
                    # Сохраняем в Obsidian
                    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
                    file_path = os.path.join(output_dir, f"{safe_title}.md")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    print(f"[SAVED] Saved to {file_path}")
                else:
                    print(f"[ERROR] Failed to fetch chat {id}: {detail_res.status_code}")
    else:
        print(f"[ERROR] API failed: {response.status_code}")
        print(f"Details: {response.text[:200]}")

if __name__ == "__main__":
    deep_export()
