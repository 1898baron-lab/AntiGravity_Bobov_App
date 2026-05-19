import sys
import os
import time
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')

cookie_str = """SEARCH_SAMESITE=CgQInKAB; __Secure-BUCKET=CN0B; _gcl_au=1.1.317542184.1771917909; _ga=GA1.1.1966662142.1771917910; AEC=AaJma5uvmgwVCEhYuc7aOvMOPu6XsmbADhtU1cIf-tOwBJd-FVj1Xj1ieMA; SID=g.a0009QikLAwOqH6x9kn193qVxh64_llCyuZDl92Kdm9Xmd7Ubkuexh_D4e9ziHvgj41gZEfX0AACgYKAbYSARYSFQHGX2MiejNlj9PD5tJK_eJ5rKKeiRoVAUF8yKr1h2aCQsYx5J2ctTkZ2it70076; __Secure-1PSID=g.a0009QikLAwOqH6x9kn193qVxh64_llCyuZDl92Kdm9Xmd7UbkueWXbqdD5AuWAZ49S2K9AbPgACgYKAXgSARYSFQHGX2MiXYAvaVW3mx51kxyxyaJdLRoVAUF8yKoobm4wmo_Ybr8PmHkgyo2f0076; __Secure-3PSID=g.a0009QikLAwOqH6x9kn193qVxh64_llCyuZDl92Kdm9Xmd7UbkueicF24KwP4S3-cDguB1Sp1AACgYKAU0SARYSFQHGX2MiQwl9msiRf5ZvPndplHfIDRoVAUF8yKqd7Kal77saynkds9MZVGgY0076; HSID=A4Elie-NUuxgIJcLv; SSID=AmO4EWamDfiVrGBII; APISID=hCUBMmEZWMTcpgC9/AqXhbhyDAmt7-NiA6; SAPISID=7VbZlFlDEPWgBNDF/AFgEUgtRtwcPzpOQD; __Secure-1PAPISID=7VbZlFlDEPWgBNDF/AFgEUgtRtwcPzpOQD; __Secure-3PAPISID=7VbZlFlDEPWgBNDF/AFgEUgtRtwcPzpOQD; _ga_BF8Q35BMLM=GS2.1.s1779076140$o47$g1$t1779076143$j57$l0$h0; __Secure-ENID=33.SE=VmvBH1TvN8MQvEzTRUOFLPpZhfGEfRrEUZMVYxUObh90KOWAeDglTAqGcQnwlBKKx80DHWALf2MCcjOfnHJgwrBAqylDPBeArug2C-avwVyxw5FiZm2s3FAoexOg2qE3LWrerArBsnvTFhmTT6eD-i62K4beDuKfGMxlqsy1bqA9tro2Y2l13pDN7OCmQcJFUYJdyGcuTdI1rtnvvOdrBz4km1fsx3esghswINfaAD01WKSBVUKk3w5wMW_jBI8oMv6hWDPdvKZSZ08aFPbshyx-LXs0bKxSi3kO_80hJ6Ts-_qlyuaLnNldRQBRqEwv8jb7FJ6ggHD1kXbZGa8eE3ASm6oNJXBDBmAatyAZ8Q1gN1FNAcQu9TC_sdWnyRvSuURMmTR0Dpw2e2laRoqUG0DIdxR4pt4baHVyhltZs9vqdVEeI5Nk6kWlhszLf-_ny3aydjus_Q; NID=531=E9ZknXYfCWwxeDyeekUScW3a8b-Sn80klkcbi5ZP64co4VO775meqh6ohr9vqwIjAdplIe6f7PmmOub9EwS8tGGeMPPSFoqeDwlc4MP3jz03_q2-v5k1yf1n1hZpswZ1kfPR3lBhsjH-j-xSxi6YmudQwf70FS0Yx3TLnI8cnwpkUWMgaeBdB2sIMLILYEM2xX39h5A23Icrr1BelpL8YIk0zUNRIZPHrCNMqjTP4HaDbyo9DWUG99jw1Z1ew594hiueLEHcWADRy1k8LrgD2EFoZuai1SVk-UP2tbPeXeN9sVG7UCrLMAUxNJflvIFEFTEeMiZLD-A6MLLfrvZuZRDdGkW_7HhMs-i3jhMlSTNiXohs43nwUKC6JTJhjQYhvONvd6ofMALEArgkmvfwdWU89VmtXWxkA2OEnfalQzFJtax9lJripvtzRclOV7V1R4vnQgD9miOxmJkOJ_o4-P84YklPoFrEqishxMSGtb6Qsrgn03sMj86QmusijshRVIR1JdOg-1Ml8PZNWhwj4ADEVckjQt95u62DKnDk1qnESIM0cS7i2qm9WSfNuZMhcGLpiQ87uHRS9zX6TZ1BvVy6zCfmzaayPqltQ6l1XePaPEpntocWwsSqEOHmXwwZOD3qUTACcNgi_4UbPjGkukrrhQeeN_K9nrLTtvdNqF1aipYXgYc8RH4fVQsWS4_YZ45UanWrgVVx3l_m6yGokdJcnKnwhhXxWrlPHr8VfKyRBairyDT1khPqniJdmQTIfE6yjKXTXOk7k5JUTkMPwx3gojYeIDoK79g_HH1KAjoaC6NiT5sYBeuTuKASEUbaygNAD9lJqeLX2idIXXfnSiyVsMuUayHml8MVWrGkwo6YUKFo_WbJrEE2a3taBHfX0NYfRKY713z8z3Ol2T8IkQZWo-w0-y06cqKKu3GpcBw8Xh9EctEEt26f_68DZrCfM03FM3Ev0_m0WnLQKWFuDJzvEcVAq0-RImojN-ULfMpLCs-1zdwjzGDqkdvwGyx-KYcgmrlbojs2gSFtcdYqn2NISse2IYu_3rb-GhNwFORdmqDcst32xzKH3SuiVGrSvHxwS_K3HijoR0BCc-PifxnAyIIrWhMyq7-8px02LYjL6Oc7EiqM37DFV0fOnRqwNOL0XIj3-gCphrz4tLB51hFn6dyv8GoLDr18POn499cZX8UqFm7AjrwIb_Q1iqUld2ln_LsmL5subpYowBl3NWTBHbBS8thlIpUKi_XcNqDaTSneTJegUE0y5hl3jWHlc9EDJrm-YM-_OmY7Xoc8SXUVVd6eR5clyHMd4W8YTKGXX5IoVhZFKe-Sjql1bAA2yISnbtvOKJExmPRljYEE_qEr8eWAzDgjV7-QbRiPrmCLiUqm8In2s16KWUHSj0l2ZTfp3u06TqIhVepWCa41AAdlESOKEatPbsgjoORQntqsZ8_1EuL-Q_aMHKFcMD0QAqGeAhRrsiYz7l_-RSC8azPZi0NFOsxCW9eTwWXwn_Htc_NQsMqDF8aV3EY6_qTgei81_i85b42jCGS4qhTcCz4O0_Bq3DxZpXBozyy4gYTVITkB6WPOab8UiQnsde3sQG9miH_LzqVXhdFQnYsf0iHJH6PgkFXwt5C7_vL42jJFZN20ETJAbYLPOfqnPvnJO4E-0jyFuT8h4ub1CqKuqqCLgi8O_dX0J5dODJzB6QL7JXpA1CEYX2ZI14aXCw4i3ByAhGYz6OAYUfY3LZFaQYi_WuvWIicNsXJfDiomDj38uUsXAo32070N6YSRETFcf5ujeTq1EW94BRtI8vdMLIyqloAteXBGFC0FVNSgRB5B; __Secure-1PSIDTS=sidts-CjIBhkeRd7Ngg8uV2pj55FKKXSSqnIQ6eBqxKJFFXRUUoyDiMApoePaENXc_KrXpJzMduBAA; __Secure-3PSIDTS=sidts-CjIBhkeRd7Ngg8uV2pj55FKKXSSqnIQ6eBqxKJFFXRUUoyDiMApoePaENXc_KrXpJzMduBAA; CONSISTENCY=AKctkzn44YCLdhzTe_mEWB2t67EqJ7NKZsCcItx2n2kwyj74vpviaq1KZwvVnCT6L2z4vlDb0HjSBzUAhKeI0oXcMLQeMFlfwtbOSr7ts7y_fzgD7TYThQnzlNaxHuJUd_QH-Ya-fW3c; COMPASS=gemini-pd=CjwACWuJV93jFYb_b6k1ZbZc5AVi75OXfwVJx6huPFdJgLZgT-iphNSBtyIyTho-2Gurv4U86El7hPmdVFUQ6ve00AYaaAAJa4lXQxwFRXazAvOYIBuJdPaN9tEGpFKeoze0BzVQgYfMaRhXGdL0InAmPEjNaCrsF8OT6pDyxSBffW_cYuYVjgnTwPIBpi2TmhHbHXLy5t-fVKHYbXtZd2nanyR1Le7yUN3il5MhIAEqcggBEJD4tNAGGmgACWuJV83vb5Do5_9-VOEDJav8AS0qF51IpzhRolC88-Y9axYzhL1wDuNsI3V771bYuIeSmvmRWLzUSvLCH8u7trZ0TF6o_5z9OX2QzZO_l3jQ4LJoGYC84E5WynzpxhzZhi0Bw0lTajAB:gemini-hl=CkkACWuJV4Jq7gXnYGXm-CCWRGf1MNczIJ0yMsen8R98zb0fdd_v1HDcw_-Y0Gxw7WZu_GGVl89NUAGecp6EG6tM_DjudIlkdiK-EOS7r9AGGnUACWuJV_kiU_jUc9hoxHUYxQ7kyldxc5_6aInux5rnud5QOy7JtsXY-R7CXyK0bx2JAbo6taLrKNkuRhqxs12jwrRQq186kbjAv4qqxCPO2tGFIZ6K1iJDJ2rMmQb_-mGUNVUduoUAnGxZSf9qO4rAN4YtuZUgATAB; _ga_WC57KJ50ZZ=GS2.1.s1779165803$o145$g1$t1779166024$j45$l0$h0; SIDCC=AKEyXzWpGl7HV1cwiSn5l6MzaVNQVNoXSuqhk2veln3snNcDMsABY8A4gAIAjcemlXva7MeHiMs; __Secure-1PSIDCC=AKEyXzX4JHxQj-yH1WBCnrqiWnsrddXdBwB_aaQQB4Tdrb1uR9r0Zb1O_kBwhYG5t779XjXJy6Y; __Secure-3PSIDCC=AKEyXzWteP2-V1sTMnKB5RceWnIa_Bl5W93u2ZAp_cbFvKCYDl3mf9qCj6u4m-TBM84zc_m1EsM"""

cookies = []
for item in cookie_str.split('; '):
    if '=' in item:
        name, value = item.split('=', 1)
        cookies.append({
            'name': name.strip(),
            'value': value.strip(),
            'url': 'https://gemini.google.com'
        })

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies(cookies)
    
    page = context.new_page()
    # Go to the URL the user specified
    print("Navigating to Gemini...")
    page.goto('https://gemini.google.com/u/1/app/d0cd10e79a509c2c?pageId=none', timeout=60000)
    page.wait_for_selector('message-content', timeout=20000)
    time.sleep(5) # Allow for dynamic loading
    
    # Extract the messages
    messages = page.locator('message-content').all_inner_texts()
    
    output_path = r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\BOBOV\Gemini_Chat_Extraction.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Gemini Chat Extraction: d0cd10e79a509c2c\n\n")
        for i, msg in enumerate(messages):
            role = "USER" if i % 2 == 0 else "GEMINI"
            f.write(f"## {role}\n{msg}\n\n")
            
    print(f"Extracted {len(messages)} messages to {output_path}")
    browser.close()
