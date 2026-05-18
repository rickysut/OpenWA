# FrappeWA - WhatsApp Integration untuk Frappe Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Frappe Framework](https://img.shields.io/badge/Frappe-v14+-blue.svg)](https://frappeframework.com)

Aplikasi Frappe untuk integrasi WhatsApp menggunakan whatsapp-web.js dengan dashboard lengkap dan API RESTful.

## ✨ Fitur Utama

- 🔄 **Multi-Session**: Kelola beberapa sesi WhatsApp sekaligus
- 📤 **Kirim Pesan**: API untuk mengirim pesan teks, gambar, video, dokumen, dan audio
- 📥 **Terima Pesan**: Webhook handler real-time untuk pesan masuk
- 🎨 **Dashboard Modern**: UI lengkap di dalam Frappe Desk dengan workspace khusus
- 🔗 **Webhook Integration**: Trigger webhook otomatis ke sistem eksternal
- 📊 **Logging & Monitoring**: Catat semua aktivitas, status pengiriman, dan error
- ⏰ **Scheduler Otomatis**: Auto-cleanup sesi dan pesan lama
- 🔐 **Role-based Access**: Permissions untuk WhatsApp Manager dan User

## 🏗️ Struktur Aplikasi

```
frappewa/
├── frappewa/
│   ├── doctype/
│   │   ├── wa_session/       # Manajemen sesi WhatsApp (QR Code, status connection)
│   │   ├── wa_message/       # Log semua pesan masuk/keluar dengan status
│   │   ├── wa_contact/       # Database kontak WhatsApp
│   │   ├── wa_settings/      # Konfigurasi global aplikasi
│   │   └── wa_webhook_log/   # Audit log untuk webhook
│   ├── api.py                # API endpoints & background jobs
│   ├── whatsapp_service.py   # Service layer untuk komunikasi dengan Node.js
│   ├── utils.py              # Utility functions & installation hooks
│   └── workspace/            # Dashboard UI configuration
├── hooks.py                  # Frappe hooks configuration
├── pyproject.toml            # Python dependencies
└── README.md                 # Dokumentasi ini
```

## 📋 Prasyarat

Sebelum instalasi, pastikan Anda memiliki:

- ✅ **Frappe Framework** versi 14 atau lebih baru
- ✅ **Python** 3.10+
- ✅ **Node.js** 16+ (untuk service whatsapp-web.js terpisah)
- ✅ **Redis** (untuk Frappe caching & queues)
- ✅ **MariaDB** atau **PostgreSQL** (database)

## 🚀 Instalasi

### Langkah 1: Install App di Bench Frappe

```bash
cd ~/frappe-bench

# Download app dari repository
bench get-app https://github.com/rickysut/FrappeWA.git

# Install app ke site Anda
bench install-app frappewa

# Jalankan migrasi database
bench migrate
```

### Langkah 2: Setup Node.js Service (Required)

FrappeWA memerlukan service Node.js terpisah yang menjalankan `whatsapp-web.js`. Anda dapat membuat service sederhana seperti berikut:

```bash
# Buat direktori untuk Node service
mkdir ~/whatsapp-node-service && cd ~/whatsapp-node-service

# Initialize project
npm init -y
npm install whatsapp-web.js qrcode-terminal express body-parser

# Buat file index.js (implementasi sesuai kebutuhan)
# Pastikan service berjalan di port yang akan dikonfigurasi (default: 3000)
```

**Catatan**: Implementasi detail Node.js service ada di dokumentasi terpisah atau repository contoh.

### Langkah 3: Konfigurasi Awal

1. **Start Frappe Bench**:
   ```bash
   bench start
   ```

2. **Buka Frappe Desk** di browser (biasanya `http://localhost:8000`)

3. **Konfigurasi WA Settings**:
   - Navigasi ke **WA Settings** dari menu
   - Isi **Node Service URL** (contoh: `http://localhost:3000`)
   - Simpan konfigurasi

4. **Pastikan Worker Berjalan**:
   ```bash
   # Di terminal terpisah
   bench start --workers
   ```

## 📖 Cara Penggunaan

### 1️⃣ Membuat Session WhatsApp Baru

1. Buka workspace **FrappeWA** dari dashboard
2. Klik pada card **Sessions** > **Add Session**
3. Isi field:
   - **Session Name**: Nama unik (contoh: `Marketing`, `Support`, `Sales`)
   - **Description**: Deskripsi opsional
4. Simpan document
5. Session akan menghasilkan QR Code (lihat field **QR Code** di session)
6. Scan QR Code dengan WhatsApp di ponsel Anda (WhatsApp > Linked Devices)
7. Status akan berubah menjadi **Connected** setelah berhasil

### 2️⃣ Mengirim Pesan

#### Opsi A: Via Dashboard Frappe

1. Buka **Messages** dari workspace FrappeWA
2. Klik **Add Message**
3. Isi form:
   - **Session**: Pilih session yang aktif
   - **Phone Number**: Nomor tujuan (format: `+628123456789`)
   - **Message Type**: Teks/Media
   - **Content**: Isi pesan atau URL media
   - **Reply To**: (Opsional) ID pesan yang dibalas
4. Simpan
5. Pesan akan diproses secara asynchronous via Background Job
6. Pantau status di kolom **Status** (Pending → Sent/Failed)

#### Opsi B: Via API REST

```bash
curl -X POST https://your-frappe-site.com/api/method/frappewa.frappewa.whatsapp_service.send_message \
  -H "Authorization: token your_api_key_or_bearer_token" \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "Marketing",
    "phone_number": "+628123456789",
    "message": "Hello from FrappeWA! 🚀",
    "media_url": null,
    "media_type": null
  }'
```

**Response Contoh**:
```json
{
  "message": "Message queued successfully",
  "data": {
    "name": "MSG-2024-00001",
    "status": "Pending"
  }
}
```

### 3️⃣ Setup Webhook untuk Pesan Masuk

Untuk menerima notifikasi pesan masuk ke sistem eksternal:

1. Buka **Session** yang ingin dikonfigurasi
2. Enable toggle **Enable Webhook**
3. Isi **Webhook URL** dengan endpoint server Anda (contoh: `https://yourdomain.com/api/whatsapp-webhook`)
4. Simpan session

Setiap kali ada:
- Pesan masuk
- Perubahan status pesan
- Update status session

FrappeWA akan mengirim HTTP POST request ke URL tersebut dengan payload JSON.

**Contoh Payload Webhook**:
```json
{
  "event": "message_received",
  "session": "Marketing",
  "data": {
    "from": "+628123456789",
    "message": "Hello",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## 🔌 API Endpoints

Semua API mengikuti standar Frappe REST API. Gunakan API Key atau Session Token untuk autentikasi.

| Method | Endpoint | Deskripsi | Auth Required |
|--------|----------|-----------|---------------|
| `POST` | `/api/method/frappewa.frappewa.whatsapp_service.send_message` | Kirim pesan (queue via worker) | ✅ |
| `GET` | `/api/method/frappewa.frappewa.whatsapp_service.get_qr_code?session=MySession` | Ambil QR Code base64 | ✅ |
| `POST` | `/api/method/frappewa.frappewa.api.handle_incoming_message` | Handle pesan masuk (dari Node service) | ✅ (internal) |
| `GET` | `/api/resource/WASession` | List semua sessions | ✅ |
| `GET` | `/api/resource/WAMessage` | List semua messages (dengan filter) | ✅ |
| `POST` | `/api/resource/WAMessage` | Buat message baru | ✅ |

**Dokumentasi API Lengkap**: Kunjungi `/api/method/frappewa.*` di site Frappe Anda untuk daftar lengkap.

## ⚙️ Background Jobs

FrappeWA memanfaatkan Frappe Queue & Worker untuk operasi asynchronous:

| Job Name | Frequency | Deskripsi |
|----------|-----------|-----------|
| `send_message_job` | On-demand | Mengirim pesan ke Node service |
| `cleanup_old_sessions` | Daily (00:00) | Hapus session inactive > 30 hari |
| `cleanup_old_messages` | Daily (01:00) | Hapus pesan > 90 hari |

**Cek Status Worker**:
```bash
bench --site your-site-name show-scheduler-status
```

**Manual Trigger Job**:
```python
import frappe
from frappewa.frappewa.api import cleanup_old_sessions

frappe.enqueue("frappewa.frappewa.api.cleanup_old_sessions")
```

## 👥 Roles & Permissions

Aplikasi ini mendefinisikan 2 role utama:

| Role | Deskripsi | Akses |
|------|-----------|-------|
| **WhatsApp Manager** | Administrator penuh | CRUD semua doctypes, settings, config |
| **WhatsApp User** | Operator harian | View sessions, kirim pesan, view logs |

**Assign Role ke User**:
1. Buka **User** list di Frappe Desk
2. Pilih user yang ingin diberi akses
3. Di tab **Roles**, tambahkan role yang sesuai
4. Simpan

## 🐛 Troubleshooting

### Session tidak bisa connect / QR Code tidak muncul

1. ✅ Pastikan Node.js service berjalan dan accessible
2. ✅ Verifikasi **Node Service URL** di WA Settings benar
3. ✅ Cek firewall / network connectivity antara Frappe dan Node service
4. ✅ Lihat field **Error Log** di document WASession untuk detail error
5. ✅ Restart session (ubah status ke Stopped, lalu Started lagi)

### Pesan stuck di status "Pending"

1. ✅ Pastikan Frappe Worker berjalan: `bench start --workers`
2. ✅ Cek log worker untuk error messages
3. ✅ Verifikasi koneksi ke Node service aktif
4. ✅ Lihat field **Error Message** di document WAMessage
5. ✅ Retry pesan dengan mengubah status manual atau trigger ulang job

### Webhook tidak terkirim

1. ✅ Pastikan **Enable Webhook** aktif di session
2. ✅ Verifikasi URL webhook accessible dari server Frappe
3. ✅ Cek **WA Webhook Log** untuk melihat attempt dan response
4. ✅ Pastikan SSL/TLS valid jika menggunakan HTTPS
5. ✅ Test webhook endpoint Anda secara manual

### Error: "Module not found" atau ImportError

```bash
cd ~/frappe-bench/apps/frappewa
pip install -e .
bench migrate
```

## 🧪 Development

### Menjalankan Test (jika ada)

```bash
cd ~/frappe-bench/apps/frappewa
pytest tests/ -v
```

### Menambah Doctype Baru

```bash
cd ~/frappe-bench
bench new-doctype YourDocType --module FrappeWA
```

### Custom Script & Hooks

Lihat file `hooks.py` untuk daftar hooks yang tersedia. Anda dapat menambahkan:

- Custom API methods
- DocEvents (before_insert, after_submit, dll)
- Scheduler events tambahan
- Permission scripts

### Build Frontend (jika modifikasi workspace/UI)

```bash
cd ~/frappe-bench/apps/frappewa
yarn build
# atau
npm run build
```

## 📝 Changelog

### Version 1.0.0 (Initial Release)
- ✨ Initial release dengan fitur multi-session
- 📤 API kirim pesan teks & media
- 📥 Handler webhook pesan masuk
- 🎨 Dashboard Frappe Workspace
- ⚙️ Background jobs untuk cleanup
- 🔐 Role-based permissions

## 🤝 Kontribusi

Kami sangat terbuka untuk kontribusi! Cara berkontribusi:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit perubahan (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Guidelines**:
- Ikuti kode style yang ada (PEP 8 untuk Python)
- Tambahkan test untuk fitur baru
- Update dokumentasi jika perlu
- Jelaskan perubahan dengan jelas di PR description

## 📄 License

Distribusi di bawah **MIT License**. Lihat file [LICENSE](LICENSE) untuk detail lengkap.

## 🆘 Support & Community

- 📧 Email: [your-email@example.com]
- 💬 Issues: Buat issue di GitHub repository ini
- 📚 Dokumentasi: [Link ke dokumentasi lengkap jika ada]
- 🌐 Website: [Website Anda jika ada]

---

**Dibuat dengan ❤️ menggunakan Frappe Framework**

© 2024 Ricky Sut. All rights reserved.
