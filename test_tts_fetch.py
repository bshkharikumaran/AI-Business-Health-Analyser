import urllib.request
import urllib.parse

def test_tts():
    text = 'வணக்கம் உங்கள் பிசினஸ் சுருக்கம் நன்மையாக உள்ளது'
    encoded_text = urllib.parse.quote(text)
    url = f'https://translate.google.com/translate_tts?ie=UTF-8&tl=ta&client=tw-ob&q={encoded_text}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read()
            print(f"TTS SUCCESS! Audio Content-Type: {response.headers.get('Content-Type')}, Size: {len(content)} bytes")
            return len(content) > 1000
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

if __name__ == "__main__":
    test_tts()
