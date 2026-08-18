import sys
import re
import urllib.request
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def _fetch_tts_chunk(chunk_text, lang):
    encoded_text = urllib.parse.quote(chunk_text)
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={lang}&client=tw-ob&q={encoded_text}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=8) as response:
        return response.read()

def test_multilingual_tts():
    tamil_paragraph = "வணக்கம்! உங்கள் பிசினஸ் சுருக்கம்: மொத்த Net ARR $8.45 Million (வளர்ச்சி +18.4%), பிசினஸ் ஹெல்த் ஸ்கோர் 100-க்கு 47 (Attention Required). அடுத்த மாத உத்தேச விற்பனை ₹196.6k. இருப்பில் Cotton Sarees உள்ளிட்ட 2 பொருட்களுக்கு உடனடி ரீஆர்டர் தேவை. வாடிக்கையாளர் பாசிட்டிவ் ரேட்டிங் 57.1% (NPS: +21)."
    
    clean_text = re.sub(r'[*_`#~]', '', tamil_paragraph).strip()
    lang_base = "ta"

    chunks = []
    sentences = re.split(r'([.!?,;\n]+)', clean_text)
    current = ""
    for i in range(0, len(sentences), 2):
        part = sentences[i]
        punct = sentences[i+1] if i+1 < len(sentences) else ""
        seg = (part + punct).strip()
        if not seg:
            continue
        if len(current) + len(seg) + 1 <= 180:
            current = (current + " " + seg).strip()
        else:
            if current:
                chunks.append(current)
            current = seg
    if current:
        chunks.append(current)

    print(f"Split into {len(chunks)} chunks:")
    for idx, c in enumerate(chunks):
        print(f"  Chunk {idx+1} ({len(c)} chars): {c}")

    audio_bytes = bytearray()
    for c in chunks:
        audio_bytes.extend(_fetch_tts_chunk(c, lang_base))

    print(f"Total concatenated MP3 size: {len(audio_bytes)} bytes")
    assert len(audio_bytes) > 20000, "Audio too small!"
    print("SUCCESS: Full Tamil spoken audio generated perfectly!")

if __name__ == "__main__":
    test_multilingual_tts()
