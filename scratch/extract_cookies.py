from playwright.sync_api import sync_playwright

def get_cookies():
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            cookies = context.cookies()
            
            # Filter cookies for google.com
            google_cookies = [c for c in cookies if 'google.com' in c['domain']]
            
            # Format to header string
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in google_cookies])
            
            with open("C:\\ANTIGRAVITY\\1\\scratch\\browser_cookies.txt", "w") as f:
                f.write(cookie_str)
                
            print(f"Successfully extracted {len(google_cookies)} cookies")
            return cookie_str
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_cookies()
