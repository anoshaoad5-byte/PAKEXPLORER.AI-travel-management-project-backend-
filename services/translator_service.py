from deep_translator import GoogleTranslator


def translate_text(text, target_language="ur"):
    if not text:
        return ""

    translated = GoogleTranslator(source="auto", target=target_language).translate(text)
    return translated