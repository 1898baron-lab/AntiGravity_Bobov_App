import requests
import json
import os

# Куки из твоего лога (подставил актуальные)
COOKIES = {
    "__Secure-next-auth.session-token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..y_-Q3bFpXhqAEcIE.Zj_Xks7Iv4uz5Rbh1Hn0TcMSo-8vpf6bCQp6F5N0H5gwUlzX4vW8hXtQC4MCbmFFPb7gCzSEku62pixHbq7gQgujyDdvcTqaX37AJaG1nUsknnlfMYIUM4k1GZwk1byLqRRMjPDrzwwwqFbF9e4xyfilDiH7fRC3szx698_c_iXUb4QJ8geTt8dy4zn0LaQMc0jwCErnk1qNdpcM2BpR9ytNqhDyrGLgdRxhDJrgmt2Jgg1cwkb9eyQfaCH-4sJB6wnpXO8CszXSbxXTYWSqgO0wrLi7QcFZnHx3sDrOCCgt8_DiuUme0Kqfcs9VHSyswrUN12yNbl64jcFS_VUfCOculTwr3y-PO7De6wD4yIR3YTpvQRR471Ogt13wgxtBMPuQo_l2CeSz-o3l4UNWbsMBcA_qxCTaZYUc6UVqHtIY5D1GmTkLrjXZzplPPWTczcNtKJJ58ZDoWrMhnV6adk_Zggoz074Af0Heu80asr2iBLxlYCM5e3_NZyrrdJo6T6EkE_yawWPUk-vMjgB_fept15YfyL07utk4rwqhfIT5Ud6D2N5dLsLaaNEzPQnjl06ooIx7q4emf2BgWjk4oWcJRiaAHmm5F0N4TKQ4iB6tKOQpIFbig8tE1D_4c69cWfljh0DfVye8oWphnHVHZoEMamUWIH-C1XS03Qygihu3w8IdnBwtD3B5eP-g3UDQpJe0eXtnRJ-DoJKd3XxUN2hKmLs-vyUfL61NN9KFOHKYAscfsAu5DvYmSqr8b0NCnwCAYsGAvpjE-p-xLpG2rdSL_tCI5KyDe2OjL3BqBxxY-djsouJOS7F1opcbS9qiMRZgOBQyuhYrqftyhHz92P_Vwx6ShHNru9wTTMA-3EdCd4qmV1p5siktPEf3wX7G5MjNFN6k7YlJkRZ5W2UhC2pPNNxKbnBKLpKBzJDh2brVSTB-dGx7WT5wOKFD66cITGk60cnLRIpzQjqHwxHwxOyujnROdZS3KAGyDmsEfe4b2IxuG5M1nHggWJo1RERWd7J5xF-FdkBOCMQBsHwwZSGJ2ZpuPS4B8MKwyEoXgNzCP_5DpbgBnsZcOWZgwPNKnJW7xVsYOuLV8gm1efLvrSsv8LuDrHOqrCxZYQj35hkuuZepuHHwuevckjeYqK88gU0oeH4QFygcAvIl5q31FuJic6ZhpGoJeb2L7vks6bbSG48Z0iDFLPOGPUFG2dXtaRBZwHXlRVpzeGioX1bD25pyMyjePJQbyk0tZcV37deyG6BF-MOqOavttm4DY4KXCAIqzQ3j2dSUg6jcXTKy26Drg6M6jMq5P24HjnNu-hKPkzg5uCtCMEdeCbnarWe_Rq5fXek5KdseKm2Pw9AxkpeQOxTVpO-Ez07QS5fU1Ov-YQ99WeSbVwRVuRdZBYDsZXVytuf1KRU9Ty9D6B8Cf3IBPQ6YB31GFAcE6HgOXAkJih8KANzOAZVmmnFJ1YF7iRilo2cdk8_QnmEaVj2Uux5T9ThPnWEIBVB6PfSb9xpO2eaFYAjJhCqcnQKSsiRtKisiaRlDGOqai35LL8qFdUSqWkICZVWCkF4vyIVcqGFs5yMEKBhZR49zip7ks6Dpy2rYgx4pmhzn_oiydiOsZGnCYEItZSJsm0LRb29ic4nrVRWUT2XaZJU9kHBv5aOtvm5lAGAT_ECCh6TYlVgyqqYn_yV88SHJcCY86cMBIzULQs0U5UpTPCoYDH7fiVVhIeLGX-0Sld7ksUi4_q5W7vP5vlQyS-V6Skjb4Kp2qvnRXH8Hb6e7ytDslXmWYQArjE_LtHH9wAQMdpQxIzm8hbsJkabOW7WzfPjW_V3HzbzymDCn7xYRje0UOCf8cf-59ywnpMDms-AyLEYQSPGIhNVXV-o_AZu1swVjdeFyd8OAgSSDRzEJO2jfCJxTGNQSA05nUggMTxlTvQJOLOUnqcQvOK947ZcCx1eNlmXJUoShRvmiBgrKTklu9R9_DOjtNT2f58RHpsSRDi-mIh2qc5io5mjO1DdwWncqdQ-jLGjx3VuHNLryC2AnLRoi9t67jxd4A4KMVjVzM2ctOJlkEO26winreBpALk42fSvZhoqAR01z5JnNUoFU-LrqCQI-jbWopSbWQnlTop8C6bsOqmA0vu59WyAHNr3rStrhsELnTbhg-C8KB1_3tVwKDsXEJPE08oqOKPo-LXcdxunsxoaONM_n63p-t3_uo-T037HIHnu5XTh_4dV2LeY_-gACavfdSEpazIziVV_eWHA3fxApl6gFoGZ5m2KiejaeBiETMvuA9IgGr_Tx_whUzeNRpvnvm7UzdHvVqLVu-vrOxLqq6KEsaPXU5ySjy2gr2ZKpK53mujnUMb2SS1AUzly7pqNZrI0inpWuQ4nFmrEf_tIIi-mVsa9no1H4-ilKUqumgbrGdSgeUN__BRxcOcexX8ilfIuj1rkxXyfobn5XrQ8CMc6EpqPlxwYfiQRk8fv7ZGPWKGOnyISS2D1eiJroweTc7N5dDtFImv1E6UsGvl_BjI6fpZs6OpdKsSXsPbAAOLb7wD0n7YxCId0PeF4xsv6QjqcaBauX6Z4R1rJwfYT4Kxj_uLIO_i2EAaQMgLvL3RlkVAirPTnxwWigoSdFs7IZzoPnmUETqis44KM05JdxXv74rFoTdjbjHlk7NhDxs3FI7ilt4DBdA2dhuob_oVZ16s8k9PfwNFcLPw_Roou2aCZT1D270TCVIVNneonRIcmItPkEXRDpGxCnE8HCl5QJJCyrGqIrJvIjYKQHDrp1Euikwnt3hxtB0S4JqqrpbmnMOIOKI-E9aalSp4jKUIdPnsKDcxJm2Vc3nyWV-1ROjlfcQviANRcaaerleb-WRMvO7YMkPcDLYKc86Z5usmKa7b7CJ1MbkAL_keeaJwzxWPDEifREkb6Ix1n9kv7jUXBp03QiVlNirVnHpMlqouRkMC9BISeJwNvp8Yrvv2oFbRI4IpGNZYFhei5RAxSTHxEDn_QzpLzlUhHPsXdcC-gGUIw7noXVZnXZmV-m2Hwqct3ti1GFwQwKKxwbe2Mn19BXAUPVL7gxcTQzKnCUjfmiO7ybnn1AgnS2zQCANCY-2QXOxaX6hHaK1zxgYRWZp7AW7V0ofi7esxX4g3RrR-zDjj3H_Ty6B9bKZJksV9XPScyBp6HQ3Smkb0gef3PCc8fhtDgKULOGcnpIQwO153gRay9I9Qk1HeSY7Uysung7UOpxUM41TgLqfljcjj3ERhN_kQzifcBb5nntyBA-xwHDxBEiv4sMGCxuMEjCXla86JiuXRBDABE0zhwYgYOQeFIpRmlo_GLhG3pP-TKk1xR8BJ1ky4ZaTTkic4jLf8qLC9EX2U52BEmVv6QaFC1KBZ8QMLIPlTHzLC8sea2p-nvF8r-e3eh74bcIo74KCJuIwtyTKLBCNORxC061dSyYmDofrVfwYNN-W1yy1jG2EeUtXZjEV_djB2jWEtThLOCAHwkwF3STKIxsB42XHx5hvzQw9zI8i3Nci56veXFEN4VVJt-8pfZRv3ac_VM0Zr78BCmH5tI1X4AB-xnB3OjGR0Wuk3cC7v_g5SG5AlYInidzQpysPR_eChmEbl7D4SZqsxfjibeWlOPt49wy6udX_mu6_AFyV3r77fetNY-t-ou1I0aQ5v212BZTHvyTxerNDn7z3wtHKKAmClZmsOb_pHDp4aSg9-CrrXLf5LVwkNZ82e70YsB3kLA0w48--FW5szHbOwhpf1EuKxrYGvpBQbZ8l7UKGTIHgPIhRfgNXK_81Bzl_2g5HNpXKoGbOemqHLfW.4WkfzfJAh3uUfk7VXlSNpA",
    "oai-did": "cd9b942f-5371-4f41-988c-91e08a5dbf4f",
    "cf_clearance": "sdBbJSEYy65xcX2ua1s5N8.CEZh3zSFz_Ye3W58lmU8-1777951294-1.2.1.1-Z.0ar3gTZ3S3Xg4GX2WXaLvK2iT1d7_E6ad8YVgBtOtxETUox3ggT8wB4YpCv3GCUgPiAyrpDXn9ELdrVmpzWTAU5eeTURiRcoEF_QCwiVxKUc1THkcq3og21oUtOTB.ID_IJW0gpNuW7W2QjWOV4s_y4OCJh_kI4vAjVJ2lK5JUSVR81_q7Kr1mkuhhg.oqn7uKhdSOwjmxBwtuu1qwnFGKawdHZ64NkWwfOqFKAy5NOF.TIg1e7wJX8dpdEA86Jpfxw_GT7vGhVZdN5HkLI80WrExySoGS_Jlmo4yz3iwvM9klq._1dZoXsb8VnjSaSqkaLfCTopU8_U59U76pYBZvREQjfq3HRer85mgoJ5U7CJdt2Atwu3awbhoKNTpZxkBevUc836bXJaufLV.x0aUpWJVfDntoFgcqWPqxaGI"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://chatgpt.com/",
    "Alt-Used": "chatgpt.com"
}

def export_all_conversations():
    print("[INFO] Attempting to fetch all conversations via API...")
    
    # URL для получения списка чатов
    list_url = "https://chatgpt.com/backend-api/conversations?offset=0&limit=100&order=updated"
    
    response = requests.get(list_url, cookies=COOKIES, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        print(f"[SUCCESS] Found {len(items)} conversations.")
        
        output_dir = r"C:\ANTIGRAVITY\1\obsidian_brain\Archives\ChatGPT_Full_Dump"
        os.makedirs(output_dir, exist_ok=True)
        
        # Сохраняем общий список
        with open(os.path.join(output_dir, "conversations_list.json"), "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
            
        print(f"[INFO] List saved. Parsing for keywords...")
        
        keywords = ["велосипед", "стажировка", "бобов", "закреп"]
        for conv in items:
            title = conv.get("title", "")
            id = conv.get("id")
            
            if any(kw in title.lower() for kw in keywords):
                print(f" -> MATCH FOUND: '{title}' (ID: {id})")
                # Здесь можно добавить скачивание конкретного чата по ID
                
    else:
        print(f"[ERROR] API Request failed: {response.status_code}")
        print(f"Details: {response.text[:500]}")

if __name__ == "__main__":
    export_all_conversations()
