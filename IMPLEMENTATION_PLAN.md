# Implementation Plan — PySastrawi

Diturunkan dari [SPEC.md](./SPEC.md). Berisi pekerjaan untuk menutup gap yang tercatat di SPEC §9 (Konstrain & Keputusan Desain) dan §10 (Status & Item Terdefer), serta gap pengujian pada SPEC §8.

---

## 1. Tujuan

1. **Menghilangkan semua item terdefer yang aman dikerjakan** tanpa memutus API publik (SPEC §9–§10).
2. **Menutup gap pengujian** yang tersisa (SPEC §8; gap tercatat di audit: `VisitorProvider` construction).
3. **Meningkatkan kualitas dokumentasi data** (SPEC §6, item M8).
4. **Mempertahankan invariant inti**: tanpa dependensi eksternal, Python ≥ 3.8, 178+ test lulus.

> **Status putaran**: Fase 1–6 **SELESAI** ✅ (Agustus 2026). Fase 4 adalah rilis major **v2.0.0** (IP-4.1 ABC, IP-4.2 rename, IP-4.3 dievaluasi → TIDAK di-wire). Fase 5 (release engineering) **selesai**: CHANGELOG, wheel/sdist, verifikasi instalasi, tag + GitHub Release. Fase 6 (validasi KBBI) **selesai**: pilot 216 kata turunan → **96.8%** akurasi, 7 kegagalan dalam 5 kategori.

## 2. Prinsip Kerja

| Prinsip | Sumber |
|---------|--------|
| Hanya stdlib + `re`; tidak ada dependensi baru | SPEC §1, §9 |
| Tidak ada perubahan perilaku stemming yang diamati | SPEC §4 |
| Perubahan API publik hanya backward-compatible | SPEC §9 |
| Semua task diakhiri dengan test suite hijau | SPEC §8 |
| Item yang "breaking" dipindah ke backlog major version | SPEC §9, §10 |

## 3. Definisi Selesai (Definition of Done)

- [x] Test suite penuh lulus: `python -m unittest discover tests -p '*_test*.py' -v`
- [x] Jumlah test tidak berkurang (baseline 178 → **195**)
- [x] Tidak ada dependensi baru di `setup.py`/`pyproject.toml`
- [x] `__init__.py` tetap kosong (0/11 non-empty; konvensi import path lengkap)
- [x] Status task diperbarui di `SPEC.md` §10 (kolom Status / tabel terdefer)

---

## 4. Baseline

- Test: **178 lulus** (`.venv\Scripts\python.exe -m unittest discover tests -p '*_test*.py'` dengan `PYTHONPATH=src`, atau `pip install -e .`)
- Kamus aktif: `kata-dasar.txt` ≈ 29.932 baris; rujukan: `kata-dasar.original.txt` ≈ 42.355 baris (selisih 12.423)
- Placeholder docstring `"""description of class"""`: **13 file**
- Modul dengan `__all__`: **0**

### Hasil (post-implementasi)

- Test: **187 lulus** (+9: 2 konkurensi cache, 7 VisitorProvider) → **190** setelah Fase 3 (error-path factory + stem) → **195** setelah coverage 100% (follow-up: getter, cabang ECS/defensif, guard rule)
- Versi: **2.0.0** (Fase 4: IP-4.1 ABC + IP-4.2 rename → rilis major)
- Placeholder docstring: **0**
- Modul dengan `__all__`: **7** (modul kelas publik; `__init__.py` tetap kosong)
- Data: `StopWordRemover/data/stop-words.txt` (809 kata), `Stemmer/data/README.md`
- Analisis kamus: 14.779 kata unik hanya di orisinal (dihapus), 2.771 hanya di aktif (ditambahkan)

---

## 5. Fase Pekerjaan

### Fase 1 — Hardening non-breaking ✅ DONE

| ID | Task | Ref | File | Kriteria Diterima | Status |
|----|------|-----|------|-------------------|--------|
| IP-1.1 | Bekukan daftar visitor menjadi `tuple` | SPEC §9 (M7) | `VisitorProvider.py` | `get_visitors()`/`get_suffix_visitors()`/`get_prefix_visitors()` mengembalikan `tuple`; test Context & fungsional tetap lulus; pemanggil internal tidak mutasi list | ✅ |
| IP-1.2 | Jadikan `ArrayCache` thread-safe | SPEC §9 (L8) | `ArrayCache.py` (+ test) | `set/get/has` dilindungi `threading.Lock`; semantik LRU tidak berubah; tambah test konkurensi sederhana | ✅ (+2 test konkurensi) |
| IP-1.3 | Ganti 13 placeholder docstring `"""description of class"""` | SPEC §9 (L1) | 13 file (lihat §7) | Tidak ada lagi `description of class` di `src/`; docstring mendeskripsikan tanggung jawab kelas | ✅ |
| IP-1.4 | Tambah `__all__` pada modul publik | SPEC §9 | modul kelas publik (lihat deviasi) | `from Sastrawi import ...` tetap berfungsi; `dir(module)` terbatas pada ekspor | ✅ |

**Catatan IP-1.1**: jangan ubah `Context.accept_prefix_visitors` yang membaca `len(self.removals)` — hanya jenis koleksi dari provider yang dibekukan.

### Fase 2 — Data & Dokumentasi ✅ DONE

| ID | Task | Ref | File | Kriteria Diterima | Status |
|----|------|-----|------|-------------------|--------|
| IP-2.1 | Pindahkan stop words ke file data | SPEC §6.2 (L7) | `src/Sastrawi/StopWordRemover/data/stop-words.txt` + `StopWordRemoverFactory.py` | `get_stop_words()` tetap ada & mengembalikan himpunan kata yang sama; file dibaca UTF-8; `package_data` menyertakan `StopWordRemover/data/*.txt`; test `stop_word_remover_factory_test.py` tetap lulus | ✅ |
| IP-2.2 | Dokumentasikan `kata-dasar.original.txt` | SPEC §6.1 (M8) | `src/Sastrawi/Stemmer/data/README.md` | README menjelaskan asal file, ukuran kedua file, selisih 12.423 kata, dan metode (analisis linguistik via KBBI) | ✅ |
| IP-2.3 | Tambah test konstruksi `VisitorProvider` | SPEC §8 (gap audit) | `tests/UnitTests/Stemmer/Context/Visitor/visitor_provider_test.py` | Assertion: 3 daftar tidak kosong, jenis sesuai Fase 1, berisi instance tipe yang diharapkan, urutan suffix `lah/kah/tah/pun` → `ku/mu/nya` → derivasional | ✅ (+7 test) |

### Fase 3 — Regresi & Verifikasi ✅ DONE

| ID | Task | Ref | Kriteria Diterima | Status |
|----|------|-----|-------------------|--------|
| IP-3.1 | Jalankan regresi penuh setelah tiap fase | SPEC §8 | `unittest discover` hijau di akhir tiap fase; jumlah test tidak berkurang | ✅ 187 test |
| IP-3.2 | Smoke test instalasi | SPEC §8 | `pip install -e .` berhasil; import `StemmerFactory` & `StopWordRemoverFactory` di interpreter bersih tanpa `PYTHONPATH`; contoh dari SPEC §3.1 & §3.2 menghasilkan output sesuai | ✅ via `uv pip install -e .` |
| IP-3.3 | Verifikasi batas input & validasi | SPEC §2 | `TypeError` untuk non-`str`, `ValueError` untuk > 1.000.000 karakter (sudah di-cover test; konfirmasi tanpa regresi) | ✅ |

### Fase 4 — Rilis major v2.0.0 ✅ DONE

| ID | Task | Ref | File | Kriteria Diterima | Status |
|----|------|-----|------|-------------------|--------|
| IP-4.1 | Migrasi interface ke `abc.ABC` | SPEC §9 (M5) | `DictionaryInterface.py`, `CacheInterface.py`, `StemmerInterface.py`, `RemovalInterface.py`, `ContextInterface.py` (+ `Context.py`, `Removal.py`, `Stemmer.py`, `CachedStemmer.py`, `ArrayDictionary.py` di-wire) | Semua interface `abc.ABC` dengan `@abstractmethod`; kelas konkret inherit interface dan mengimplementasikan semua abstract method; probe membuktikan `BadDictionary/BadCache/BadContext/BadRemoval` diblokir `TypeError` | ✅ |
| IP-4.2 | Refactor penamaan camelCase → snake_case | SPEC §9 (L2) | seluruh `src/` + test yang memakai nama lama | `normalizedText`, `delegatedStemmer`, `resultCache`, `stopWords`, `dictionaryFile`, `removedPart`, `invalidAffixes` (dst.) → snake_case; `setup.py` → `2.0.0`; 190 test hijau | ✅ |
| IP-4.3 | Evaluasi integrasi `InvalidAffixPairSpecification` ke pipeline | SPEC §10 (M3) | `Context.py` (percobaan, di-revert), `InvalidAffixPairSpecification.py` (M4) | Keputusan berbasis bukti: **TIDAK di-wire** — guard `remove_prefixes()` membuat 16 test gagal & menurunkan akurasi (perbandingan KBBI); spec dipertahankan sebagai utilitas; regex di-precompile | ✅ (dievaluasi, ditolak) |

**Catatan IP-4.1**: `ContextInterface` method yang di-abstract-kan: `get_original_word`, `set_current_word`, `get_current_word`, `get_dictionary`, `stop_process`, `process_is_stopped`, `add_removal`, `get_removals`. Test mock visitor diubah dari `context.current_word = ...` menjadi `context.stop_process()` (`dont_stem_short_word_test.py`, `visitors_test.py`).

**Catatan IP-4.2**: sisa pattern camelCase setelah scan seluruh repo hanya terdapat di **docstring** disambiguator (`berV`, `rV`, `beC1erC2`, `mengV`, `kV`, `ngV`, `menyV`, `nyV`, `sV`, `mempA/V`, `pA/V`, `berCAP`) — itu notasi aturan dari paper Asian J., **dibiarkan**.

**Catatan IP-4.3 (bukti empiris)**: dengan guard `if self._invalid_affix_pair.is_satisfied_by(self.original_word): return` di awal `Context.remove_prefixes()`:
- 16 test suite gagal.
- Output yang tadinya benar jadi salah: `dimakan→dimakan` (benar: `makan`), `berlari→berlari` (benar: `lari`), `perkataan→perkataan` (benar: `kata`), `dipukulan→dipukulan` (benar: `pukul`).
- Upstream PHP `sastrawi/sastrawi` juga tidak pernah me-wire spec ini (hanya dipakai di test-nya sendiri; test `perkataan` bahkan berkomentar `// wtf?`).
- Keputusan: spec dipertahankan sebagai utilitas ber-test + regex di-precompile (M4); tidak di-wire untuk menghindari penurunan akurasi.

### Fase 5 — Release engineering v2.0.0 ✅ DONE

| ID | Task | Ref | Kriteria Diterima | Status |
|----|------|-----|-------------------|--------|
| IP-5.1 | Tulis `CHANGELOG.md` v2.0.0 | SPEC §10 | Mencatat breaking changes (ABC, rename), perbaikan, dan tambahan sejak v1.2.1; format Keep a Changelog | ✅ `CHANGELOG.md` |
| IP-5.2 | Build wheel + sdist | SPEC §7 | `python -m build` menghasilkan `dist/Sastrawi-2.0.0-*.whl` & `.tar.gz`; `twine check dist/*` lulus | ✅ `pysastrawi-2.0.0-py3-none-any.whl` + `.tar.gz`; `twine check` PASSED (perlu `MANIFEST.in` agar sdist menyertakan README/LICENSE/data) |
| IP-5.3 | Verifikasi instalasi dari wheel bersih | SPEC §3, §8 | `pip install dist/*.whl` di venv baru (tanpa `PYTHONPATH`); contoh SPEC §3.1 & §3.2 output sesuai; data file ter-packaging | ✅ venv bersih (`uv venv` + wheel): §3.1 → `ekonomi indonesia sedang dalam tumbuh`, §3.2 → `''` |
| IP-5.4 | Tag `v2.0.0` + GitHub Release | — | Tag annotated `v2.0.0`; release notes merujuk CHANGELOG | ✅ tag `v2.0.0` + [release](https://github.com/mlengse/PySastrawi/releases/tag/v2.0.0) |

### Fase 6 — Validasi akurasi vs KBBI ✅ DONE

> **Catatan metode**: ekspor bulk per huruf (`kbbi_ekspor_stem_mapping`) timeout untuk semua huruf yang dicoba; diganti dengan `kbbi_daftar_kata_turunan` untuk **16 kata dasar** yang dikurasi (mewakili prefiks meN-, beR-, teR-, peN-, se-, ke-…-an, -kan/-i/-an, reduplikasi) → **216 kata turunan** sebagai ground truth (KBBI). Sejak follow-up, dataset **full** tersedia lokal (`kbbi-harvester-cdn/lexicon/derived_to_root.json`, 33.268 pasangan) → lihat `tools/kbbi_full_benchmark.py` dan hasil di §9.

| ID | Task | Ref | Kriteria Diterima | Status |
|----|------|-----|-------------------|--------|
| IP-6.1 | Ekspor dataset mapping stem KBBI | SPEC §4 | Dataset kata berimbuhan → `rootWord` (via tool KBBI) sebagai ground truth | ✅ `tools/kbbi_validation_data.json` (216 pasangan, 16 kata dasar) |
| IP-6.2 | Benchmark stemmer vs KBBI | SPEC §4 | Skor akurasi keseluruhan + daftar kata yang menyimpang | ✅ **96.8%** (209/216); `tools/kbbi_benchmark.py`; 7 mismatch |
| IP-6.3 | Kategorisasi kegagalan & rekomendasi | SPEC §10 | Pisahkan "perlu perbaikan rule" vs "perilaku ECS yang disengaja"; usulan prioritas | ✅ 5 kategori; lihat tabel di bawah |

**Kategorisasi 7 kegagalan (IP-6.3)**

| Kategori | Kata | Output | Akar masalah |
|----------|------|--------|--------------|
| A. Over-removal sufiks → tabrakan kata kamus | `pejalan`→`pejal`, `selari`→`selar` | sufiks `-an`/`-i` dibuang dulu (prioritas sufiks) lalu jatuh ke kata kamus lain (`pejal`, `selar`); prefiks `pe-`/`se-` tidak sempat diproses | Prioritas sufiks-dulu ECS; aturan `pe-`/`se-` tidak dijangkau |
| B. `-nya` salah diuraikan (possesif vs akar) | `menanya`→`mena`, `penanya`→`pena` | `-nya` dianggap pronomina posesif, padahal bagian akar `tanya`; hasil `mena`/`pena` = kata kamus lain | `RemoveInflectionalPossessivePronoun` naif untuk akar berakhiran `-nya` |
| C. Ambigu p-luluh `mem-V` | `memakani`→`pakan` | Rule 13b (`mem-V`→`p-…`) menghasilkan `pakan` (kata kamus) karena 13a (`m-…`) gagal di tahap antara `makani`; `-i` belum sempat dibuang | Disambiguator memakai hasil terakhir bila tidak ada yang cocok di kamus; order prefiks-dulu |
| D. Kata majemuk berimbuhan (compound) | `menumbuhkembangkan`→(tidak berubah) | Akar ganda `tumbuh`+`kembang`; ECS tidak punya rule | Diluar cakupan ECS (bukan rule, tapi segmentasi kata majemuk) |
| E. Prefiks `te-` tidak didukung | `tetumbuhan`→(tidak berubah) | Hanya `teR-` yang punya disambiguator; `te-` polos tidak ada rule | Kandidat rule baru (mirip `teR-` yang menyerap `/r/`) |

**Rekomendasi prioritas (IP-6.3)**
1. **P1 (rule kecil, dampak besar)**: tambah disambiguator `te-` → turunkan `te-{k…}`? Perlu verifikasi pola (`tetumbuhan`→`tumbuh`; cek `ketua`, `telur`, dst. dulu). Kelas E.
2. **P2**: perbaiki urutan untuk kasus A — bila hasil over-removal sufiks adalah kata kamus yang juga "sufiks-panjang" dari bentuk berprefiks valid, coba balik urutan (contoh `pejalan`: coba `pe-` dulu → `jalan`). Terkait `PrecedenceAdjustmentSpecification`.
3. **P3**: p-luluh (C) — perlu bukti lebih banyak; `memakani` jarang, tapi `membacai`, `mengenai`-type perlu ditinjau. Jangan ubah tanpa data tambahan (meningkatkan risiko regresi, lihat IP-4.3).
4. **P4 (bukan rule)**: kelas B dan D adalah limitasi desain ECS/naif; dokumentasikan saja.

> **Catatan ketelitian**: beberapa "mismatch" sebenarnya perilaku sah — e.g. `berikut`→`ikut`, `kinerja`→`kerja`, `menumbuhkembangkan` dianggap kata leksem utuh. Skor 96.8% pada 216 kata turunan = pilot terkurasi; untuk angka menyeluruh perlu dataset full KBBI (ekspor bulk timeout).

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

> Dependensi terpenuhi: IP-2.3 dijalankan setelah IP-1.1; seluruh IP-3.x hijau.

---

## 7. Daftar File yang Terkena

**Fase 1**
1. `src/Sastrawi/Stemmer/Context/Visitor/VisitorProvider.py` (IP-1.1, IP-1.3) ✅
2. `src/Sastrawi/Stemmer/Cache/ArrayCache.py` (IP-1.2, IP-1.4) ✅
3. `tests/UnitTests/Stemmer/Cache/array_cache_test.py` (IP-1.2) ✅
4. Docstring (IP-1.3, 13 file): `StopWordRemoverFactory.py`, `StopWordRemover.py`, `CacheInterface.py`, `ArrayDictionary.py`, `CachedStemmer.py`, `TextNormalizer.py`, `ContextInterface.py`, `Removal.py`, `RemovalInterface.py`, `DontStemShortWord.py`, `AbstractDisambiguatePrefixRule.py`, `PrefixDisambiguator.py`, `VisitorProvider.py` ✅
5. `__all__` (IP-1.4, **deviasi**: modul kelas publik, bukan `__init__.py`): `StemmerFactory.py`, `Stemmer.py`, `CachedStemmer.py`, `StopWordRemoverFactory.py`, `StopWordRemover.py`, `ArrayDictionary.py`, `ArrayCache.py` ✅

**Fase 2**
6. `src/Sastrawi/StopWordRemover/data/stop-words.txt` (baru, IP-2.1) ✅
7. `src/Sastrawi/StopWordRemover/StopWordRemoverFactory.py` (IP-2.1) ✅
8. ~~`setup.py` — `package_data`~~ (**tidak perlu diubah**; `data/*.txt` sudah mencakup paket `StopWordRemover`) ✅
9. `src/Sastrawi/Stemmer/data/README.md` (baru, IP-2.2) ✅
10. `tests/UnitTests/Stemmer/Context/Visitor/visitor_provider_test.py` (baru, IP-2.3) ✅

**Dokumen pelacak**
11. `SPEC.md` — sinkronisasi perilaku baru (Cache thread-safe, stop words data file, `__all__`, hasil kamus, status Fase 1–6 + follow-up) ✅

**Fase 4 (v2.0.0)**
13. Interface → `abc.ABC` (IP-4.1): `Dictionary/DictionaryInterface.py`, `Stemmer/StemmerInterface.py`, `Stemmer/Cache/CacheInterface.py`, `Stemmer/Context/RemovalInterface.py`, `Stemmer/Context/ContextInterface.py` ✅
14. Kelas konkret di-wire + rename snake_case (IP-4.2): `ArrayDictionary.py`, `Context.py`, `Removal.py`, `Stemmer.py`, `CachedStemmer.py`, `StemmerFactory.py`, `StopWordRemoverFactory.py`, `Visitor/DontStemShortWord.py`, `Visitor/Remove*.py`, `Visitor/AbstractDisambiguatePrefixRule.py`, `setup.py` (`2.0.0`) ✅
15. Test mock di-update (IP-4.2): `tests/UnitTests/Stemmer/Context/Visitor/dont_stem_short_word_test.py`, `visitors_test.py` ✅
16. IP-4.3: `Morphology/InvalidAffixPairSpecification.py` — M4 precompile regex; **tidak di-wire** ke `Context.py` ✅

**Fase 5 (v2.0.0)**
17. `CHANGELOG.md` (baru, IP-5.1) — Keep a Changelog, mencakup breaking (ABC + rename), Fixed/Added sejak v1.2.1 ✅
18. `MANIFEST.in` (baru, IP-5.2) — `include README.md/CHANGELOG.md/LICENSE` + `recursive-include src/Sastrawi *.txt`; sdist sebelumnya gagal build karena `README.md` tidak ikut ✅

---

## 8. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi | Hasil |
|--------|--------|----------|-------|
| IP-1.1 mengubah urutan/karakter pipeline karena koleksi dianggap list oleh kode lain | Salah stemming | Audit pemanggil sebelum berubah; regresi Fase 1; hanya jenis koleksi yang diubah, bukan urutan | ✅ Tidak ada regresi; pipeline stabil |
| IP-1.2 lock menimbulkan bottleneck | Perf menurun | Lock per-call kecil; simpan baseline benchmark sebelum & sesudah | ✅ Lock per-operasi minimal; test konkurensi lulus |
| IP-2.1 memecah API `get_stop_words()` | Breaking | Pertahankan metode; file hanya sumber data internal | ✅ API dipertahankan; 809 kata identik |
| IP-2.2 salah mendokumentasikan asal kata | Informasi menyesatkan | Verifikasi via tool KBBI; tulis sebagai "analisis awal" bila tidak pasti | ✅ Verifikasi KBBI: `mengurah`→`urah`, `eritrea`=negara |
| Docstring massal mengubah perilaku | — | Docstring tidak mengubah kode; hanya string literal | ✅ Tidak ada perubahan perilaku |

---

## 9. Verifikasi Akhir

```bash
# dari root repo, paket ter-install (uv pip install -e .) atau:
PYTHONPATH=src
python -m unittest discover tests -p '*_test*.py' -v
python -m unittest tests/UnitTests/Stemmer/Context/Visitor/visitor_provider_test.py -v
```

**Hasil (putaran Fase 1–3)**: 190 test OK. Coverage ~96% (branch) dengan jalur error (`TypeError`/`ValueError`, `RuntimeError` file data hilang) ter-cover; sisa yang tidak ter-cover adalah abstract method interface, `__init__.py` kosong, dan dead code defensif. CI GitHub Actions (`.github/workflows/ci.yml`) menjalankan `pip install -e .` + `unittest discover` pada Python 3.8–3.12. Smoke test instalasi: contoh SPEC §3.1 → `ekonomi indonesia sedang dalam tumbuh yang bangga`, §3.2 → `''`; semua data file ter-packaging.

**Hasil (Fase 4 / v2.0.0)**: seluruh task IP-4.1–4.3 selesai. Interface → `abc.ABC` (probe: instansiasi kelas `Bad*` gagal `TypeError`, semua kelas konkret tetap instantiate); rename camelCase → snake_case tuntas (scan repo bersih; sisa hanya notasi rule di docstring). IP-4.3 dievaluasi dan **ditolak** (wiring menurunkan akurasi; bukti di catatan IP-4.3). Suite: **190 test OK**, coverage naik ke **~98%** (14 stmt miss: `Context.py:29,32,35,38,50,71,147`, `Removal.py:14,20`, `Stemmer.py:72`, fallback Rule 3/7/9/24).

Kriteria rilis putaran ini: **terpenuhi** — seluruh task Fase 1–4 selesai, suite hijau (190), tidak ada placeholder docstring tersisa, tidak ada camelCase di kode (hanya docstring rule), dan `SPEC.md` §10 merefleksikan status terbaru.

**Hasil (Fase 5 / release v2.0.0)**: `CHANGELOG.md` + `MANIFEST.in` ditulis; `python -m build` → `dist/pysastrawi-2.0.0-py3-none-any.whl` + `.tar.gz`; `twine check` PASSED; instalasi terverifikasi di venv bersih (SPEC §3.1/§3.2 lulus). Tag annotated `v2.0.0` + GitHub Release dibuat. Suite tetap **190 test OK**.

**Hasil (Fase 6 / validasi KBBI)**: dataset 216 kata turunan dari 16 kata dasar (KBBI, via `kbbi_daftar_kata_turunan`; ekspor bulk timeout) → akurasi **96.8%** (209/216). 7 kegagalan → 5 kategori: A) over-removal sufiks → tabrakan kata kamus (`pejalan`→`pejal`, `selari`→`selar`); B) `-nya` salah urai (`menanya`→`mena`, `penanya`→`pena`); C) p-luluh `mem-V` (`memakani`→`pakan`); D) kata majemuk (`menumbuhkembangkan`); E) prefiks `te-` tak didukung (`tetumbuhan`). Rekomendasi: P1 rule `te-`, P2 urutan prefiks-dulu untuk kasus A, P3 tinjau p-luluh tanpa data tambahan, P4 dokumentasi untuk B/D.

**Hasil (Follow-up — P1 ditolak + coverage 100%)**: 
- **P1 (rule `te-`) DITOLAK dengan data**: dari 676 kata kamus berawalan `te-C`, rule naif (hapus `te`, sisanya harus di kamus) akan salah stem **161 kata dasar** (`tebal`→`bal`, `tebang`→`bang`, `tegas`→`gas`, `tenaga`→`naga`, `teriak`→`riak`, `tetangga`→`tangga`, `tetapi`→`tapi`, `tetamu`→`tamu`, `tetes`→`tes`, …). Morfem sebenarnya pada `tetumbuhan` adalah `teR-` (asimilasi), bukan prefiks `te-` produktif → masuk backlog, bukan rule baru.
- **Coverage 98% → 100%** (+5 test, total **195**): getter `Context`/`Removal`, cabang step-1 main-visitor (`Context.py:71`), cabang non-sufiks ECS (`Context.py:147`), guard `C == 'r'` Rule 3/7/9/24, guard `stem_plural_word` (`Stemmer.py:72`). 890 stmts / 252 branch, **0 miss**. Perilaku tidak berubah (KBBI 96.8% konsisten).

**Hasil (Follow-up — P2 ditolak + anti-regresi)**: 
- **P2 (urutan prefiks-dulu) DITOLAK dengan data**: dicoba menambah pola CS-precedence `^pe(.*)an$` dan `^se(.*)i$` (kasus A: `pejalan`→`jalan`✅, `selari`→`lari`✅) → di dataset KBBI **net +1** (210/216) tapi **regresi berat pada kata umum `pembelajaran`→`bajar`** (seharusnya `ajar`). Pola `^pe(.*)an$` memecah `pembelajaran` di titik yang salah setelah suffix-removal (`pe-belajaran`→tabrakan `bajar`), dan regresi itu **meniadakan** perbaikan (pola `+pe-an` saja = 209/216). Verdict: kata umum yang hancur tidak sebanding dengan 2 kata langka yang membaik → masuk backlog, bukan perubahan rule. Edit eksperimen di-revert; `PrecedenceAdjustmentSpecification` kembali ke 6 pola asli.
- **Anti-regresi**: test fungsional baru `['pembelajaran', 'ajar']` (di bagian `Combination of prefix + suffix`) mengunci bahwa `pembelajaran` tetap → `ajar`. Suite **195 test OK** (subtest tambahan, jumlah metode tak berubah).

**Hasil (Follow-up — dataset KBBI full + P3 ditolak)**: 
- **Dataset penuh tersedia secara lokal** di `C:\Users\aknpa\dev\bahasa\data\kbbi-harvester-cdn\lexicon\derived_to_root.json` (33.268 pasangan kata turunan → root KBBI; ekspor bulk MCP jadi tak perlu). `tools/kbbi_full_benchmark.py` (baru) memakai dataset ini.
- **Akurasi full**: **88.90%** (29.412/33.084 kata turunan single-token; 184 multi-token dilewati). Kategorisasi 3.672 mismatch:
  - **D2 over-stem tabrakan kata kamus: 1.762 (48.0%)** — over-removal sufiks menyingkap kata kamus langka (`ajakan`→`aja` karena `aja` ∈ kamus; `batikan`→`bati`). Lever akurasi terbesar = kurasi kamus, bukan rule.
  - **D3 root tak ada di kamus: 963 (26.2%)** — cakupan kamus (root KBBI ∉ `kata-dasar.txt`).
  - **R1 reduplikasi: 448 (12.2%)** — bentuk `X-Xan`/`X-berX` non-plural tidak ditangani sebagai tunggal.
  - **D1 kata turunan terdaftar sebagai dasar: 290 (7.9%)** — e.g. `abangan`, `akuan`, `bebatuan` ada di `kata-dasar.txt` sehingga tak di-stem.
  - **R2 gap rule: 206 (5.6%)** — prefiks kolektif `be-` (`bebatuan`→`batu`), artikel `al-` (`almuhit`→`muhit`), dll.
- **P3 (p-luluh `mem-V`) DITOLAK dengan data**: dicoba menukar urutan rule 13b/13a (`[13b, 13a]`). Di dataset full **+56** (89.07%) — 122 membaik, 66 rusak — tapi di set terkurasi **turun** 209→208/216 dan merusak **kata umum** `memakan`→`pakan` & `memasak`→`pasak` (karena `pakan`/`pasak` ∈ kamus dan jadi short-circuit). Kenapa full naik padahal curated turun: dataset lokal bias homograf (resolve ke entri terakhir — `memakani`→`pakan` di file lokal, padahal KBBI `kataDasar` resminya `makan¹`; `memadukan`→`padu` benar, `memadui`→`madu`). Verdict: **tukar urutan tidak aman** → masuk backlog bersama P1/P2.
- **Catatan kualitas data lokal**: `derived_to_root.json` memilih root terakhir untuk homograf (e.g. `memakani`→`pakan` vs `makan¹` di MCP). Untuk eksperimen rule, patokan yang andal tetap set terkurasi 216.

**Rencana berikutnya (belum dikerjakan)**: (1) kurasi kamus utk kategori D2/D1 (perlu audit kata-kata langka per huruf; risiko mengorbankan kata valid — perlu daftar kolisi dulu), (2) reduplikasi R1 bila dikehendaki. P1, P2, P3 tertutup (ditolak dengan data). Publish PyPI **di-skip** (keputusan user).
