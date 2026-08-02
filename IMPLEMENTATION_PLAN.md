# Implementation Plan — PySastrawi

Diturunkan dari [SPEC.md](./SPEC.md). Berisi pekerjaan untuk menutup gap yang tercatat di SPEC §9 (Konstrain & Keputusan Desain) dan §10 (Status & Item Terdefer), serta gap pengujian pada SPEC §8.

---

## 1. Tujuan

1. **Menghilangkan semua item terdefer yang aman dikerjakan** tanpa memutus API publik (SPEC §9–§10).
2. **Menutup gap pengujian** yang tersisa (SPEC §8; gap tercatat di audit: `VisitorProvider` construction).
3. **Meningkatkan kualitas dokumentasi data** (SPEC §6, item M8).
4. **Mempertahankan invariant inti**: tanpa dependensi eksternal, Python ≥ 3.8, 178+ test lulus.

## 2. Prinsip Kerja

| Prinsip | Sumber |
|---------|--------|
| Hanya stdlib + `re`; tidak ada dependensi baru | SPEC §1, §9 |
| Tidak ada perubahan perilaku stemming yang diamati | SPEC §4 |
| Perubahan API publik hanya backward-compatible | SPEC §9 |
| Semua task diakhiri dengan test suite hijau | SPEC §8 |
| Item yang "breaking" dipindah ke backlog major version | SPEC §9, §10 |

## 3. Definisi Selesai (Definition of Done)

- [ ] Test suite penuh lulus: `python -m unittest discover tests -p '*_test*.py' -v`
- [ ] Jumlah test tidak berkurang (baseline 178; idealnya bertambah)
- [ ] Tidak ada dependensi baru di `setup.py`/`pyproject.toml`
- [ ] `__init__.py` tetap kosong (konvensi import path lengkap)
- [ ] Status task diperbarui di `pysastrawi.md` (kolom Status / tabel terdefer)

---

## 4. Baseline

- Test: **178 lulus** (`.venv\Scripts\python.exe -m unittest discover tests -p '*_test*.py'` dengan `PYTHONPATH=src`, atau `pip install -e .`)
- Kamus aktif: `kata-dasar.txt` ≈ 29.932 baris; rujukan: `kata-dasar.original.txt` ≈ 42.355 baris (selisih 12.423)
- Placeholder docstring `"""description of class"""`: **13 file**
- Modul dengan `__all__`: **0**

---

## 5. Fase Pekerjaan

### Fase 1 — Hardening non-breaking

| ID | Task | Ref | File | Kriteria Diterima |
|----|------|-----|------|-------------------|
| IP-1.1 | Bekukan daftar visitor menjadi `tuple` | SPEC §9 (M7) | `VisitorProvider.py` | `get_visitors()`/`get_suffix_visitors()`/`get_prefix_visitors()` mengembalikan `tuple`; test Context & fungsional tetap lulus; pemanggil internal tidak mutasi list |
| IP-1.2 | Jadikan `ArrayCache` thread-safe | SPEC §9 (L8) | `ArrayCache.py` (+ test) | `set/get/has` dilindungi `threading.Lock`; semantik LRU tidak berubah; tambah test konkurensi sederhana |
| IP-1.3 | Ganti 13 placeholder docstring `"""description of class"""` | SPEC §9 (L1) | 13 file (lihat §7) | Tidak ada lagi `description of class` di `src/`; docstring mendeskripsikan tanggung jawab kelas |
| IP-1.4 | Tambah `__all__` pada modul publik | SPEC §9 | `Sastrawi/__init__.py`, `Stemmer/__init__.py`, `StopWordRemover/__init__.py`, `Dictionary/__init__.py`, `Cache/__init__.py` | `from Sastrawi import ...` tetap berfungsi; `dir(module)` terbatas pada ekspor |

**Catatan IP-1.1**: jangan ubah `Context.accept_prefix_visitors` yang membaca `len(self.removals)` — hanya jenis koleksi dari provider yang dibekukan.

### Fase 2 — Data & Dokumentasi

| ID | Task | Ref | File | Kriteria Diterima |
|----|------|-----|------|-------------------|
| IP-2.1 | Pindahkan stop words ke file data | SPEC §6.2 (L7) | `src/Sastrawi/StopWordRemover/data/stop-words.txt` + `StopWordRemoverFactory.py` | `get_stop_words()` tetap ada & mengembalikan himpunan kata yang sama; file dibaca UTF-8; `package_data` menyertakan `StopWordRemover/data/*.txt`; test `stop_word_remover_factory_test.py` tetap lulus |
| IP-2.2 | Dokumentasikan `kata-dasar.original.txt` | SPEC §6.1 (M8) | `src/Sastrawi/Stemmer/data/README.md` | README menjelaskan asal file, ukuran kedua file, selisih 12.423 kata, dan metode (analisis linguistik via KBBI) |
| IP-2.3 | Tambah test konstruksi `VisitorProvider` | SPEC §8 (gap audit) | `tests/UnitTests/Stemmer/Context/Visitor/visitor_provider_test.py` | Assertion: 3 daftar tidak kosong, jenis sesuai Fase 1, berisi instance tipe yang diharapkan, urutan suffix `lah/kah/tah/pun` → `ku/mu/nya` → derivasional |

### Fase 3 — Regresi & Verifikasi

| ID | Task | Ref | Kriteria Diterima |
|----|------|-----|-------------------|
| IP-3.1 | Jalankan regresi penuh setelah tiap fase | SPEC §8 | `unittest discover` hijau di akhir tiap fase; jumlah test tidak berkurang |
| IP-3.2 | Smoke test instalasi | SPEC §8 | `pip install -e .` berhasil; import `StemmerFactory` & `StopWordRemoverFactory` di interpreter bersih tanpa `PYTHONPATH`; contoh dari SPEC §3.1 & §3.2 menghasilkan output sesuai |
| IP-3.3 | Verifikasi batas input & validasi | SPEC §2 | `TypeError` untuk non-`str`, `ValueError` untuk > 1.000.000 karakter (sudah di-cover test; konfirmasi tanpa regresi) |

### Fase 4 — Backlog major version (TIDAK dikerjakan di putaran ini)

| ID | Task | Ref | Alasan |
|----|------|-----|--------|
| IP-4.1 | Migrasi interface ke `abc.ABC` | SPEC §9 (M5) | Breaking untuk subclass; butuh rilis mayor |
| IP-4.2 | Refactor penamaan camelCase → snake_case | SPEC §9 (L2) | Breaking public API; rilis mayor tersendiri |
| IP-4.3 | Integrasi `InvalidAffixPairSpecification` ke pipeline | SPEC §10 (M3) | Perlu evaluasi linguistik & efek akurasi |

---

## 6. Urutan & Dependensi

```
IP-1.1 (tuple) ──────┐
IP-1.2 (lock) ───────┤
IP-1.3 (docstring) ──┼──► IP-2.3 (test VisitorProvider) ──► IP-3.x (regresi)
IP-1.4 (__all__) ────┘         │
                                ├──► IP-2.1 (stop words) ──► IP-2.2 (data README)
```

- Fase 1 & 2 independen satu sama lain dan boleh berjalan paralel.
- IP-2.3 bergantung pada IP-1.1 (menguji jenis koleksi yang dibekukan).
- IP-3.x berjalan di akhir tiap fase dan wajib lulus sebelum lanjut.

---

## 7. Daftar File yang Terkena

**Fase 1**
1. `src/Sastrawi/Stemmer/Context/Visitor/VisitorProvider.py` (IP-1.1, IP-1.3)
2. `src/Sastrawi/Stemmer/Cache/ArrayCache.py` (IP-1.2)
3. `tests/UnitTests/Stemmer/Cache/array_cache_test.py` (IP-1.2)
4. Docstring (IP-1.3): `StopWordRemoverFactory.py`, `StopWordRemover.py`, `CacheInterface.py`, `ArrayDictionary.py`, `CachedStemmer.py`, `TextNormalizer.py`, `ContextInterface.py`, `Removal.py`, `RemovalInterface.py`, `DontStemShortWord.py`, `AbstractDisambiguatePrefixRule.py`, `PrefixDisambiguator.py`, `VisitorProvider.py`
5. `__all__` (IP-1.4): `Sastrawi/__init__.py`, `Stemmer/__init__.py`, `StopWordRemover/__init__.py`, `Dictionary/__init__.py`, `Cache/__init__.py`

**Fase 2**
6. `src/Sastrawi/StopWordRemover/data/stop-words.txt` (baru, IP-2.1)
7. `src/Sastrawi/StopWordRemover/StopWordRemoverFactory.py` (IP-2.1)
8. `setup.py` — `package_data` (IP-2.1)
9. `src/Sastrawi/Stemmer/data/README.md` (baru, IP-2.2)
10. `tests/UnitTests/Stemmer/Context/Visitor/visitor_provider_test.py` (baru, IP-2.3)

**Dokumen pelacak**
11. `pysastrawi.md` — update status tiap task

---

## 8. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|--------|--------|----------|
| IP-1.1 mengubah urutan/karakter pipeline karena koleksi dianggap list oleh kode lain | Salah stemming | Audit pemanggil sebelum berubah; regresi Fase 1; hanya jenis koleksi yang diubah, bukan urutan |
| IP-1.2 lock menimbulkan bottleneck | Perf menurun | Lock per-call kecil; simpan baseline benchmark sebelum & sesudah |
| IP-2.1 memecah API `get_stop_words()` | Breaking | Pertahankan metode; file hanya sumber data internal |
| IP-2.2 salah mendokumentasikan asal kata | Informasi menyesatkan | Verifikasi via tool KBBI; tulis sebagai "analisis awal" bila tidak pasti |
| Docstring massal mengubah perilaku | — | Docstring tidak mengubah kode; hanya string literal |

---

## 9. Verifikasi Akhir

```bash
# dari root repo, paket ter-install (pip install -e .) atau:
PYTHONPATH=src
python -m unittest discover tests -p '*_test*.py' -v
python -m unittest tests/UnitTests/Stemmer/Context/Visitor/visitor_provider_test.py -v
```

Kriteria rilis putaran ini: seluruh task Fase 1–3 selesai, suite hijau, tidak ada placeholder docstring tersisa, dan `pysastrawi.md` merefleksikan status terbaru.
