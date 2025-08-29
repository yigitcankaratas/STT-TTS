import asyncio
import websockets
import pyaudio
import json

async def stt_client():
    uri = "ws://localhost:2700"
    async with websockets.connect(uri) as websocket:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=8000)

        print("🎤 Dinleniyor... (CTRL+C ile çık)")
        try:
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                await websocket.send(data)
                response = await websocket.recv()
                try:
                    result = json.loads(response)
                    if "partial" in result and result["partial"]:
                        print(f"(Partial): {result['partial']}")
                    if "text" in result and result["text"]:
                        print(f"(Text): {result['text']}")
                except Exception:
                    print(response)
        except KeyboardInterrupt:
            print("🛑 Çıkış yapılıyor...")
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
    asyncio.run(stt_client())
