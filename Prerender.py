from playwright.sync_api import sync_playwright
import os

def build_prerendered_page():
    # Only one file path needed now
    target_file = "special-relativity.html"

    # Get the absolute path so the browser can find it locally
    file_url = f"file://{os.path.abspath(target_file)}"

    with sync_playwright() as p:
        print(f"Launching headless browser to process {target_file}...", flush=True)

        with p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--disable-crash-reporter",
                "--disable-logging",
                "--incognito",
                "--disable-dev-shm-usage"
            ]
        ) as browser:

            page = browser.new_page()
            print("Loading handbook and waiting for MathJax...", flush=True)
            page.goto(file_url)

            # Wait for MathJax to finish processing the equations
            try:
                page.wait_for_selector("mjx-container", state="attached", timeout=15000)
                page.wait_for_timeout(2000)
            except Exception as e:
                print("Warning: Could not find rendered math. Did the page load correctly or are there no equations?", flush=True)

            print("Cleaning up DOM, removing unwanted scripts, and restoring animation classes...", flush=True)
            page.evaluate("""
                const scripts = document.querySelectorAll('script');
                scripts.forEach(script => {
                    const srcLower = script.src ? script.src.toLowerCase() : '';
                    if (srcLower.includes('mathjax') || srcLower.includes('jquery') || srcLower.includes('moment')) {
                        script.remove();
                    }
                    else if (!script.src && script.textContent.includes('MathJax')) {
                        script.remove();
                    }
                });

                const article = document.querySelector('article');
                if (article) {
                    article.classList.add('initial-load');
                }

                if (document.body) {
                    document.body.classList.remove('start-fade');
                    if (document.body.getAttribute('class') === '') {
                        document.body.removeAttribute('class');
                    }
                }
            """)

            # Extract the fully rendered HTML
            rendered_html = page.content()

        # The browser is now closed, so it's safe to overwrite the file

        print(f"Overwriting {target_file} with rendered HTML...", flush=True)

        # Open the original file in 'w' (write) mode to replace its contents
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        print(f"Success! {target_file} has been successfully overwritten.", flush=True)

if __name__ == "__main__":
    if os.path.exists("special-relativity.html"):
        build_prerendered_page()
    else:
        print("Error: special-relativity.html not found in the current directory.", flush=True)