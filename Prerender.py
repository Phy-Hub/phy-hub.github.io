from playwright.sync_api import sync_playwright
import os
import re

def build_prerendered_page():
    target_file = "special-relativity.html"

    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    # 1. Read the original file and separate frontmatter from HTML
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find content between the first two sets of ---
    # It looks for '---', then any text (including newlines), then '---'
    frontmatter_pattern = re.compile(r'^(---\s*\n.*?\n---\s*\n)', re.DOTALL)
    match = frontmatter_pattern.match(content)

    frontmatter = ""
    html_content = content

    if match:
        frontmatter = match.group(1)
        html_content = content[len(frontmatter):]
        print("Frontmatter detected and isolated.")

    # 2. Save a temporary version of the HTML without frontmatter for Playwright
    # This prevents the browser from moving the metadata into the <body>
    temp_file = "temp_render.html"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_url = f"file://{os.path.abspath(temp_file)}"

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
            except Exception:
                print("Warning: Could not find rendered math.", flush=True)

            print("Cleaning up DOM and restoring animation classes...", flush=True)
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

    # 3. Combine frontmatter back with the rendered HTML
    print(f"Overwriting {target_file} with frontmatter + rendered HTML...", flush=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(frontmatter + rendered_html)

    # 4. Cleanup temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    print(f"Success! {target_file} has been successfully updated.", flush=True)

if __name__ == "__main__":
    build_prerendered_page()