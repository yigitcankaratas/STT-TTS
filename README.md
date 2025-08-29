## Özellikler
- Türkçe konuşmayı metne çevirir (Vosk STT)
- Girilen metni Türkçe ses dosyasına çevirir (Coqui TTS)

## Kurulum
1. Gerekli Python paketlerini yükleyin:
   ```bash
   pip install vosk sounddevice TTS flask websockets
   ```
2. `vosk-model-small-tr-0.3` Türkçe STT modelini indirin ve proje klasörüne ekleyin.
3. Coqui TTS için Türkçe model otomatik olarak indirilir.
4. Proje dosya yapısı örneği:
   ```
   ├── server.py
   ├── static/
   │   └── index.html
   ├── vosk-model-small-tr-0.3/
   ```

## Çalıştırma
1. Sunucuyu başlatın:
   ```bash
   python server.py
   ```
2. Tarayıcıdan arayüze erişin:
   - WebSocket için: `ws://localhost:2700`
   - Statik dosyalar için: `http://localhost:5000/static/index.html`

## Kullanım
- "Başlat" ile ses kaydını başlatın, "Durdur" ile bitirin.
- "Metinden Sese" alanına metin girip "TTS Oynat" butonuna basın.
- Oluşan ses dosyasını dinleyin.

## Not
- TTS dosyası `static/tts_output.wav` olarak kaydedilir.

## Gereksinimler
- Python 3.11
- Vosk STT modeli (Türkçe)
- Coqui TTS
- Flask
- Websockets
