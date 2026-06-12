# 🔐 Fraud Detection — Streamlit App

Web app fraud detection berbasis Machine Learning, dibangun dengan Streamlit.

## 📁 Struktur Folder

```
streamlit_app/
├── app.py               ← Kode utama Streamlit
├── requirements.txt     ← Library yang dibutuhkan
├── README.md            ← Panduan ini
└── models/
    ├── best_model_*.pkl ← Model hasil training (dari Colab)
    └── scaler.pkl       ← Scaler hasil training (dari Colab)
```

> ⚠️ Folder `models/` harus kamu buat sendiri dan isi dengan file `.pkl` dari Colab.

---

## 🚀 Cara Deploy ke Streamlit Cloud (Gratis)

### STEP 1 — Siapkan file model
Download dari Google Colab (STEP 10 di notebook training):
- `best_model_*.pkl`
- `scaler.pkl`

Taruh di folder `models/` di dalam project ini.

### STEP 2 — Upload ke GitHub
1. Buat akun di [github.com](https://github.com) jika belum punya
2. Buat repository baru → nama bebas, misal `fraud-detection-app`
3. Upload semua file ini ke repository:
   - `app.py`
   - `requirements.txt`
   - `models/best_model_*.pkl`
   - `models/scaler.pkl`

### STEP 3 — Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository: `fraud-detection-app`
5. Branch: `main`
6. Main file path: `app.py`
7. Klik **"Deploy!"**
8. Tunggu 2–3 menit → app kamu live! 🎉

### ✅ Hasil
Kamu akan mendapatkan link permanen seperti:
```
https://namakamu-fraud-detection-app.streamlit.app
```

---

## 💻 Cara Jalankan di Lokal (Opsional)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Buka browser ke `http://localhost:8501`

---

## 🔧 Fitur App
- Form input transaksi lengkap (amount, kategori, waktu, lokasi)
- Gauge chart probabilitas fraud (hijau/kuning/merah)
- Bar chart faktor risiko
- Tabel detail transaksi
- Rekomendasi tindakan otomatis
- Tombol contoh transaksi normal & fraud
