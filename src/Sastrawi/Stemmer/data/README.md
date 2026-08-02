# Kamus Kata Dasar — PySastrawi

## File

| File | Kata unik | Peran |
|------|-----------|-------|
| `kata-dasar.txt` | ~29.932 | **Kamus aktif** — di-load oleh `StemmerFactory.get_words_from_file()` |
| `kata-dasar.original.txt` | ~41.940 | **Rujukan/orisinal** — daftar lengkap turunan Kateglo sebelum pembersihan |

Keduanya berformat satu kata per baris (UTF-8). Hanya `kata-dasar.txt` yang dikirim dan dipakai saat stemming.

## Mengapa ada dua file?

`kata-dasar.original.txt` adalah daftar mentah dari sumber Kateglo (lisensi CC-BY-NC-SA 3.0).
`kata-dasar.txt` adalah versi aktif yang telah dibersihkan. Kamus stemmer **hanya boleh berisi kata dasar**
(bentuk leksem), karena pipeline ECS mencari kata dasar setelah menghapus afiks.

## Analisis selisih (per 2026-08)

- **Hanya di original** (dihapus): **14.779 kata**
- **Hanya di aktif** (ditambahkan): **2.771 kata**
- Selisih total di dokumen audit (±12.423) berbeda dari angka unik karena menghitung baris, termasuk duplikat/baris kosong.

### Karakteristik kata yang dihapus (sampel + heuristik)

| Kategori | Proporsi | Contoh |
|----------|----------|--------|
| Bentuk berimbuhan (kata turunan) | sampai ~10% (heuristik awalan `me/ber/ter/di/ke/pe/se`) | `mengurah` → rootWord KBBI `urah` |
| Reduplikasi / bentuk jamak | 3,1% | `hawar-hawar`, `ngak-ngik-ngok`, `bula-bula` |
| Non-alfabet (singkatan, tanda baca) | 460 kata | entri 1–2 huruf, `a.c.` |
| Nama diri / geografis / etnis | beberapa sampel terverifikasi | `eritrea` (negara), `nimboran` (suku), `balobe` |
| Kosakata teknik/argo/daerah | beberapa sampel | `aseptis`, `aponeurosis`, `ajuh` (Madura), `nyonyot` (Jawa) |

### Verifikasi linguistik

Cross-reference dengan KBBI pada sampel acak menunjukkan kata-kata yang dihapus sebagian besar
adalah **bentuk infleksi/derivasi** (punya `rootWord`), **nama diri**, atau **kata daerah** —
bukan kandidat kata dasar yang diperlukan untuk stemming.

> Catatan: analisis ini bersifat karakterisasi awal; proporsi pastinya memerlukan pengecekan KBBI satu per satu.

## Regenerasi

Untuk menghasilkan ulang `kata-dasar.txt` dari sumber orisinal, cocokkan terhadap daftar kata dasar KBBI
dan buang entri ber-`rootWord`, reduplikasi, serta nama diri sebelum di-commit.
