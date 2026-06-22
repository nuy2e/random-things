# Japanese Furigana Previewer

> **Note:** I totally vibe coded this.

A clean, web-based tool designed to automatically convert standard Japanese kanji text into HTML layout tags containing proper Furigana readings using Google's Gemini LLM. 

This tool includes a native layout stabilizer explicitly designed for light novel and web novel readers who copy text from vertical layouts (`縦書き`), where lines often paste in reverse order.

## Features
* Accurate Furigana Generation: Automatically formats complex Japanese text with standard HTML `<ruby>` and `<rt>` annotations.
* Vertical Text Parser: Optional toggle to mathematically reverse sentence line orders instantly, correcting paragraph streams copied from e-readers.
* Bypassed Security Buffers: Includes custom runtime handlers that package raw payloads directly in UTF-8 to bypass default Python environment locale crashes ('ascii' codec cannot encode...).
* New-Tab Sandboxed Visual Canvas: Deploys a browser-isolated JavaScript wrapper inside an iframe to effortlessly open and view styled, high-resolution text results without triggering browser phishing/data-URI protection blocks.
* Unrestricted Content Profiles: Lowered backend safety thresholds allow literary exploration of heavy creative content (such as action, suspense, or dark fantasy narrative text) without encountering false-positive content blocks.

## Prerequisites
Before launching the application, ensure you have Python 3.8+ installed along with the essential UI and communication libraries.

pip install streamlit requests

## Setup & API Credentials
You will need a valid Gemini API key to interact with the language engine:
1. Obtain an API key via [Google AI Studio](https://aistudio.google.com/).
2. Input your key securely into the application sidebar panel at launch.
3. **Model Selection (Optional):** By default, the application runs on `gemini-3.5-flash`. If you wish to switch models without modifying the user interface, you can manually adjust the hardcoded index tracker at the top of `main.py`:

```python
# Change the array index [0] to switch between available models:
# [0] -> High-speed default, [1] -> Low-cost utility, [2] -> Heavy reasoning
available_model_list = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"]
current_model = available_model_list[0]
```

## How to Run
Launch the web application locally by running the Streamlit command directly inside your terminal/command prompt:

streamlit run main.py

## Usage
1. Paste your target Japanese text block into the primary interface viewport.
2. If your source material came from an e-reader or a vertical-scrolling web novel layout where the sentence order got backwards during copying, tick the "Reverse line order" checkbox.
3. Provide your secret developer key in the sidebar panel.
4. Click "Generate Furigana" to review raw layout code or tap "Open Full Preview in New Tab" to view your reading sheets rendered in full size.
