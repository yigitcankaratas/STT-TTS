import asyncio
import websockets
import json
import vosk
import sounddevice as sd
from TTS.api import TTS
from flask import Flask, send_from_directory
import threading

# Flask uygulaması ile static klasörünü sun
app = Flask(__name__)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def run_flask():
    app.run(host='0.0.0.0', port=5000)
import os


# STT Modeli yükle
model = vosk.Model("vosk-model-small-tr-0.3")

# Coqui TTS Türkçe modelini yükle
coqui_tts = TTS(model_name="tts_models/tr/common-voice/glow-tts", progress_bar=False, gpu=False)

async def recognize(websocket):
    rec = vosk.KaldiRecognizer(model, 16000)
    while True:
        try:
            data = await websocket.recv()
            # TTS isteği mi kontrol et
            if isinstance(data, str):
                print(f"WebSocket'ten string veri alındı: {data}")
                try:
                    msg = json.loads(data)
                    print(f"JSON parse başarılı: {msg}")
                    if msg.get("type") == "tts" and msg.get("text"):
                        metin = msg["text"]
                        print(f"TTS isteği alındı: {metin}")
                        try:
                            wav_path = os.path.join("static", "tts_output.wav")
                            coqui_tts.tts_to_file(text=metin, file_path=wav_path)
                            # Dosya boyutunu ve içeriğini kontrol et
                            try:
                                file_size = os.path.getsize(wav_path)
                                print(f"TTS dosyası kaydedildi: {wav_path}, boyut: {file_size} byte")
                                if file_size < 1000:
                                    print("UYARI: Oluşan ses dosyası çok küçük, muhtemelen boştur!")
                                else:
                                    import asyncio
                                    await asyncio.sleep(0.1)
                            except Exception as size_err:
                                print(f"Dosya boyutu veya içeriği kontrol hatası: {size_err}")
                            await websocket.send(json.dumps({"tts_path": "/static/tts_output.wav", "tts_size": file_size}))
                        except Exception as tts_err:
                            print(f"TTS hata: {tts_err}")
                            await websocket.send(json.dumps({"tts_error": str(tts_err)}))
                        continue
                except Exception as e:
                    print(f"TTS JSON parse hata: {e}")
            # STT işlemi
            if rec.AcceptWaveform(data):
                result = rec.Result()
                await websocket.send(result)
            else:
                partial_json = json.loads(rec.PartialResult())
                if partial_json.get("partial"):
                    await websocket.send(json.dumps(partial_json))
        except websockets.exceptions.ConnectionClosed:
            break

async def main():
    async with websockets.serve(recognize, "0.0.0.0", 2700):
        print("Vosk STT Server çalışıyor ws://localhost:2700")
        await asyncio.Future()  # sonsuza kadar çalış
    # Flask sunucusunu ayrı bir thread'de başlat
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    # Websocket sunucusunu başlat
    asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())
