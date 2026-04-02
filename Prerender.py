from playwright.sync_api import sync_playwright
import os

def render_and_overwrite():
    # The file is both our input and our output
    target_file = "special-relativity.html"

    # Get the absolute path so the browser can find it locally
    file_url = f"file://{os.path.abspath(target_file)}"

    with sync_playwright() as p:
        print(f"Launching headless browser to process {target_file}...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading handbook and waiting for MathJax...")
        page.goto(file_url)

        # Wait for MathJax to finish processing the equations
        try:
            # We look for <mjx-container> which MathJax creates when it renders
            page.wait_for_selector("mjx-container", state="attached", timeout=15000)
            # Add a 2-second buffer to ensure the AMS numbering pass finishes completely
            page.wait_for_timeout(2000)
        except Exception as e:
            print("Warning: Could not find rendered math. Did the page load correctly or are there no equations?")

        # Extract the fully rendered HTML exactly as the browser sees it
        rendered_html = page.content()
        browser.close()

        # Cleanup: Remove the MathJax script tag so the final page doesn't try to load it again
        print("Cleaning up script tags...")
        mathjax_script = '<script defer="" async="" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>'
        rendered_html = rendered_html.replace(mathjax_script, '')

        # Overwrite the original file with the pre-rendered HTML
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        print(f"Success! {target_file} has been successfully overwritten with the pre-rendered version.")

if __name__ == "__main__":
    # Make sure the file actually exists before running
    if os.path.exists("special-relativity.html"):
        render_and_overwrite()
    else:
        print("Error: special-relativity.html not found in the current directory.")