from playwright.sync_api import sync_playwright
import os

def build_prerendered_page():
    source_file = "special-relativity.html"
    output_file = "special-relativity.html"

    # Get the absolute path so the browser can find it locally
    file_url = f"file://{os.path.abspath(source_file)}"

    with sync_playwright() as p:
        print(f"Launching headless browser to process {source_file}...", flush=True)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading handbook and waiting for MathJax...", flush=True)
        page.goto(file_url)

        # Wait for MathJax to finish processing the equations
        try:
            # We look for <mjx-container> which MathJax creates when it renders
            page.wait_for_selector("mjx-container", state="attached", timeout=15000)
            # Add a 2-second buffer to ensure the AMS numbering pass finishes completely
            page.wait_for_timeout(2000)
        except Exception as e:
            print("Warning: Could not find rendered math. Did the page load correctly or are there no equations?", flush=True)

        print("Cleaning up DOM, removing unwanted scripts, and restoring animation classes...", flush=True)
        page.evaluate("""
            // 1. Find and remove MathJax, jQuery, and Moment.js scripts
            const scripts = document.querySelectorAll('script');
            scripts.forEach(script => {
                const srcLower = script.src ? script.src.toLowerCase() : '';

                // Remove external MathJax, jQuery, or Moment.js
                if (srcLower.includes('mathjax') || srcLower.includes('jquery') || srcLower.includes('moment')) {
                    script.remove();
                }
                // Remove inline MathJax configuration
                else if (!script.src && script.textContent.includes('MathJax')) {
                    script.remove();
                }
            });

            // 2. Restore the 'initial-load' classes so real users see the CSS animation
            const article = document.querySelector('article');
            if (article) {
                article.classList.add('initial-load');
            }

            // 3. Remove 'start-fade' class from the body tag
            if (document.body) {
                document.body.classList.remove('start-fade');

                // Optional fallback: if 'start-fade' leaves an empty class attribute, clean it up
                if (document.body.getAttribute('class') === '') {
                    document.body.removeAttribute('class');
                }
            }
        """)

        # Extract the fully rendered HTML exactly as the browser sees it now
        rendered_html = page.content()
        browser.close()

        # Write to the dist/ directory, keeping your original source file safe!
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        print(f"Success! Prerendered file safely built and saved to: {output_file}", flush=True)

if __name__ == "__main__":
    # Make sure the file actually exists before running
    if os.path.exists("special-relativity.html"):
        build_prerendered_page()
    else:
        print("Error: special-relativity.html not found in the current directory.", flush=True)