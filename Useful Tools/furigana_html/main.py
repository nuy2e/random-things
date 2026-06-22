import json
import requests
import streamlit as st


def reverse_text_lines(text: str) -> str:
    """Splits a string by line breaks, reverses the line order, and joins them back.

    Useful for processing text copied from vertical (tategaki) Japanese
    novels.
    """
    lines = text.split("\n")
    return "\n".join(reversed(lines))


def generate_furigana_html(text: str, api_key: str) -> str:
    """Sends Japanese text to the Gemini API to be converted into HTML ruby tags.

    Bypasses standard SDK encoding limitations by using raw HTTP requests
    with explicit UTF-8 payload management. Lowered safety thresholds
    prevent false-positive blocks on narrative novel content.
    """

    available_model_list = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"]
    current_model = available_model_list[0] #Choose current model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={api_key}"

    prompt = (
        f"Convert the following Japanese text into clean HTML code using standard "
        f"<ruby> and <rt> tags for all kanji. Do not add any markdown formatting, "
        f"do not wrap it in ```html blocks, and do not add any extra explanations. "
        f"Just return the raw HTML string.\n\nText: {text}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ],
    }

    # Force explicit UTF-8 encoding to prevent OS-level locale mismatches
    safe_payload = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=safe_payload)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise RuntimeError(f"API Error ({response.status_code}): {response.text}")


def render_preview_button(html_content: str):
    """Renders a browser-isolated button inside a secure iframe to bypass top-level

    data URI security blocks, allowing a clean open-in-new-tab preview.
    """
    safe_html_for_js = json.dumps(html_content, ensure_ascii=False)

    iframe_html = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin: 0; padding: 0;">
        <button id="previewBtn" style="background-color: #FF4B4B; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-family: sans-serif;">
            🌐 Open Full Preview in New Tab
        </button>

        <script>
            var rawFurigana = {safe_html_for_js};
            var styledHtml = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{font-family: sans-serif; font-size: 32px; padding: 40px; line-height: 1.8; color: #333;}} ruby{{margin-right: 5px;}}</style></head><body>' + rawFurigana + '</body></html>';

            document.getElementById('previewBtn').onclick = function() {{
                var newTab = window.open("", "_blank");
                newTab.document.write(styledHtml);
                newTab.document.close();
            }};
        </script>
    </body>
    </html>
    """
    st.components.v1.html(iframe_html, height=60)


def main():
    st.title("Japanese Furigana Previewer")

    # Sidebar UI Configuration
    st.sidebar.title("Configuration")
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

    # Main Interface Inputs
    user_text = st.text_area("Enter Japanese text:", "日本語を勉強します。")
    reverse_lines = st.checkbox(
        "🔄 Reverse line order (for text copied from vertical novels)"
    )

    if st.button("Generate Furigana"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first!")
            return

        try:
            with st.spinner("Processing..."):
                # Handle text conditioning based on reading settings
                final_text = (
                    reverse_text_lines(user_text) if reverse_lines else user_text
                )

                # Fetch and parse Furigana HTML from Gemini
                html_output = generate_furigana_html(final_text, api_key)

                # Render outputs
                st.subheader("Generated HTML Code")
                st.code(html_output, language="html")

                st.subheader("Visual Preview")
                render_preview_button(html_output)

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()