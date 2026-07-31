from flask import Blueprint, request, jsonify
from services.translator_service import translate_text

translate_bp = Blueprint("translate", __name__)


@translate_bp.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()

    text = data.get("text")
    target_language = data.get("target_language", "ur")

    if not text:
        return jsonify({"error": "text is required"}), 400

    try:
        translated = translate_text(text, target_language)
    except Exception as e:
        return jsonify({"error": "Translation failed", "details": str(e)}), 500

    return jsonify({
        "original_text": text,
        "translated_text": translated,
        "target_language": target_language
    }), 200