# SPEC — PySastrawi

## 1. Ringkasan

PySastrawi adalah pustaka *stemming* Bahasa Indonesia berbasis Python murni. Tujuannya: mereduksi kata berimbuhan menjadi bentuk dasar (kata dasar) dari suatu teks. Ini adalah port Python dari [Sastrawi PHP](https://github.com/sastrawi/sastrawi) dan mengimplementasikan algoritma **ECS (Effective Confix Stripping)** dengan pola **visitor pipeline**, berdasarkan riset Asian J. (2007) "Effective Techniques for Indonesian Text Retrieval".

- **Bahasa**: Python
- **Versi minimum**: `>= 3.8` (`python_requires` di `setup.py`)
- **Dependensi eksternal**: **tidak ada** (hanya stdlib + `re`)
- **Lisensi**: MIT; kamus kata dasar dari Kateglo (CC-BY-NC-SA 3.0)

---

## 2. Target dan Batasan

| Properti | Nilai |
|----------|-------|
| Algoritma inti | Improved ECS (Nazief & Adriani, CS Stemmer, ECS) |
| Batas panjang input | `MAX_CHARACTER_LENGTH = 1_000_000` karakter |
| Validasi input | `TypeError` bila bukan `str`; `ValueError` bila melebihi batas |
| Normalisasi | lowercase, non `[a-z0-9 -]` → spasi, kolaps spasi, `strip()` |
| Output tak ditemukan | kata dikembalikan sebagaimana aslinya (bukan di-stem) |
| Cache | LRU in-memory via `OrderedDict`, default `max_size=100_000`; thread-safe (`threading.Lock`) |

---

## 3. API Publik

### 3.1 Stemming

```python
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()      # -> CachedStemmer
stemmer.stem("Perekonomian Indonesia sedang dalam pertumbuhan")
# -> "ekonomi indonesia sedang dalam tumbuh"
```

Kelas yang terlibat:

- **`StemmerFactory`**
  - `create_stemmer() -> CachedStemmer` — membangun `ArrayDictionary` dari `data/kata-dasar.txt`, membungkus `Stemmer` dengan `CachedStemmer` ber-`ArrayCache`.
  - `get_words()`, `get_words_from_file()` — membaca file kamus (UTF-8, split `\n`).
  - `RuntimeError` bila file kamus tidak ditemukan.
- **`Stemmer`** (`Stemmer.py`)
  - `stem(text) -> str` — validasi, normalisasi, split per kata, lalu `stem_word`.
  - `stem_word(word) -> str` — router: plural vs singular.
  - `is_plural(word) -> bool`, `stem_plural_word(word)`, `stem_singular_word(word)`.
- **`CachedStemmer`** (decorator atas `Stemmer`)
  - `stem(text) -> str` — normalisasi + split, per kata: `cache.has(word)` → ambil dari cache, selain itu delegasi `delegatedStemmer.stem_word(word)` lalu simpan ke cache.
  - `get_cache()` — akses objek cache.
  - `__init__(cache, delegatedStemmer)`.

### 3.2 Stop Word Remover

```python
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StopWordRemoverFactory()
remover = factory.create_stop_word_remover()
remover.remove("yang dan di")  # -> ""
```

- **`StopWordRemoverFactory`** — `create_stop_word_remover()`, `get_stop_words()` (membaca dari `data/stop-words.txt`, ~809 kata), `get_stop_words_from_file()`; `RuntimeError` bila file data tidak ditemukan.
- **`StopWordRemover`** — `remove(text)`, `get_dictionary()`. Validasi `TypeError`/`ValueError` sama dengan Stemmer.

### 3.3 Dictionary

- **`ArrayDictionary(words=None)`** — basis `set` (lookup O(1)).
  - `contains(word) -> bool`, `count() -> int`
  - `add(word)`, `add_words(words)` — kata kosong/whitespace ditolak.

### 3.4 Cache

- **`ArrayCache(max_size=100_000)`** — LRU via `OrderedDict`.
  - `set(key, value)`, `get(key)` (touch → pindah ke belakang), `has(key)`.
  - Evict item paling lama (`popitem(last=False)`) saat melebihi `max_size`.

---

## 4. Algoritma Stemming

### 4.1 Alur `Stemmer.stem`

```
text
 └─ validasi (str, <= MAX_CHARACTER_LENGTH)
    └─ normalisasi (TextNormalizer)
       └─ split(' ')
          └─ per kata → stem_word(word)
```

### 4.2 Plural (`stem_word`)

- **`is_plural(word)`**: true jika mengandung `-`. Kecuali pola `-(ku|mu|nya|lah|kah|tah|pun)` dengan kata dasar tanpa `-` (mis. `nikmat-Ku` → singular).
- **`stem_plural_word(plural)`**:
  1. Pecah pada `-` terakhir → `[kiri, kanan]`.
  2. Jika `kanan` adalah salah satu sufiks `ku|mu|nya|lah|kah|tah|pun` dan `kiri` masih mengandung `-` → pindahkan sufiks (mis. `malaikat-malaikat-nya` → `malaikat`, `malaikat-nya`).
  3. Stem kedua bagian (`stem_singular_word`).
  4. Jika `kanan` tidak ada di kamus dan hasil stem-nya sama dengan kata asal → coba `me` + `kanan` (mis. `meniru-nirukan` → `tiru`).
  5. Jika kedua root sama → kembalikan root; selain itu → kembalikan kata plural asli.

### 4.3 Singular (`stem_singular_word`) — Pipeline `Context`

`Context` (`Context.py`) mengeksekusi urutan langkah (mengikuti nomor langkah ECS):

1. **Step 1**: jika kata sudah ada di kamus → selesai.
2. **Visitor awal**: `DontStemShortWord` (hentikan proses bila `len(word) <= 3`).
3. **Confix Stripping** (hanya jika `PrecedenceAdjustmentSpecification.is_satisfied_by(original_word)`):
   - Pola yang memicu: `^be(.*)lah$`, `^be(.*)an$`, `^me(.*)i$`, `^di(.*)i$`, `^pe(.*)i$`, `^ter(.*)i$`.
   - Lakukan **hapus prefix dulu** lalu **hapus suffix** (urutan terbalik dari normal).
   - Jika gagal → restore `original_word`, kosongkan `removals`, lanjut ke urutan normal.
4. **Step 2–3**: hapus suffix.
5. **Step 4–5**: hapus prefix (maksimum **3 iterasi**).
6. **ECS loop pengembalian akhiran** (`loop_pengembalian_akhiran`): restore prefix, lalu untuk setiap removal suffix terbalik, coba kombinasikan `-k`/sufiks asli dengan penghapusan prefix lagi.
7. **Step 6**: `result = current_word` jika ada di kamus, selain itu `result = original_word`.

### 4.4 Visitor

Semua visitor menerapkan `visit(context)`:

| Visitor | Aksi | Afiks |
|---------|------|-------|
| `DontStemShortWord` | stop proses bila kata ≤ 3 huruf | — |
| `RemoveInflectionalParticle` | hapus sufiks `lah\|kah\|tah\|pun` (opsional `-` di depan) | `P` |
| `RemoveInflectionalPossessivePronoun` | hapus sufiks `ku\|mu\|nya` (opsional `-` di depan) | `PP` |
| `RemoveDerivationalSuffix` | hapus sufiks `is\|isme\|isasi\|i\|kan\|an` | `DS` |
| `RemovePlainPrefix` | hapus prefiks `di\|ke\|se` | `DP` |
| `PrefixDisambiguator` | terapkan daftar aturan disambiguator | `DP` |

Penghapusan afiks menggunakan `str.replace(removed, '', 1)` (bukan regex) untuk menghindari injeksi pola.

### 4.5 `AbstractDisambiguatePrefixRule.visit`

- Iterasi disambiguator, ambil hasil pertama yang ada di kamus.
- Jika tidak ada yang cocok di kamus, **hasil disambiguator terakhir tetap dipakai** sebagai "best guess" (perilaku ECS yang disengaja, bukan bug; mendukung kasus `memberdayakan → daya` dan `memperbarui → baru`).
- Catat `Removal` bertipe `DP`, perbarui `current_word`.

### 4.6 Tipe Afiks (`Removal.affix_type`)

| Kode | Makna |
|------|-------|
| `P`  | Partikel (inflectional) |
| `PP` | Possessive pronoun (inflectional) |
| `DS` | Derivational suffix |
| `DP` | Derivational prefix |

`is_suffix_removal()` = tipe `DS`, `PP`, atau `P`.

---

## 5. Aturan Disambiguator (1–42)

- Berlokasi di `src/Sastrawi/Morphology/Disambiguator/`.
- **Rule 22 dan 33 sengaja tidak ada** — bukan bug (AGENTS.md menegaskan hal ini).
- Tiap kelas mengimplementasikan `disambiguate(word) -> Optional[str]` via `re.match`; mengembalikan `None` bila pola tidak cocok.
- Beberapa rule memiliki sub-rule (mis. 1a/1b, 6a/6b, 17a–17d, 30a–30c, 37–40 a/b).
- Urutan aplikasi ditentukan di `VisitorProvider.py` (daftar `PrefixDisambiguator`), dikelompokkan: rule ber-`ber`, `be`, `me`, `pe`, `ter`, infix `em/el/er`, lalu rule khusus Sastrawi (`ku-A`, `kau-A`).

---

## 6. Format Data

### 6.1 Kamus kata dasar

- **File**: `src/Sastrawi/Stemmer/data/kata-dasar.txt`
- **Isi**: ~29.932 kata (versi aktif); `kata-dasar.original.txt` berisi ~41.940 kata unik (versi rujukan/orisinal).
- **Selisih**: 14.779 kata unik hanya di orisinal (dihapus), 2.771 hanya di aktif (ditambahkan). Karakterisasi lengkap di [`Stemmer/data/README.md`](src/Sastrawi/Stemmer/data/README.md) — mencakup bentuk berimbuhan (ber-`rootWord`), reduplikasi, nama diri, dan kata daerah.
- **Format**: satu kata per baris, UTF-8, dipisah `\n`, di-load oleh `StemmerFactory.get_words_from_file()`.
- Dikirim via `package_data={'': ['data/*.txt']}` di `setup.py`.

### 6.2 Stop words

- **File**: `src/Sastrawi/StopWordRemover/data/stop-words.txt` (~809 kata, satu per baris).
- Dibaca oleh `StopWordRemoverFactory.get_stop_words_from_file()`; `get_stop_words()` tetap menjadi API publik.
- Dikirim via `package_data` yang sama (`data/*.txt`).

---

## 7. Struktur Repository

```
src/Sastrawi/
├── Dictionary/            ArrayDictionary, DictionaryInterface
├── Stemmer/
│   ├── Cache/             CacheInterface, ArrayCache (LRU)
│   ├── ConfixStripping/   PrecedenceAdjustmentSpecification
│   ├── Context/
│   │   ├── Visitor/       VisitorProvider, DontStemShortWord, Remove*,
│   │   │                  PrefixDisambiguator, AbstractDisambiguatePrefixRule
│   │   ├── Context.py, ContextInterface.py
│   │   └── Removal.py, RemovalInterface.py
│   ├── Filter/            TextNormalizer
│   ├── data/              kata-dasar.txt, kata-dasar.original.txt, README.md
│   ├── Stemmer.py, StemmerInterface.py, StemmerFactory.py, CachedStemmer.py
├── Morphology/
│   ├── Disambiguator/     DisambiguatorPrefixRule1..42 (tanpa 22, 33)
│   └── InvalidAffixPairSpecification.py   (utilitas; tidak dipakai pipeline)
└── StopWordRemover/       StopWordRemover, StopWordRemoverFactory, data/stop-words.txt

tests/
├── UnitTests/             per-modul (dictionary, cache, context, visitor, disambiguator, …)
├── FunctionalTests/       kasus stemming fungsional (subTest)
└── IntegrationTests/      StemmerFactory + end-to-end (subTest)
```

Artifak Visual Studio (`Sastrawi.sln`, `*.pyproj`, `*.vs/`) **bukan** bagian dari build — diabaikan.

---

## 8. Pengujian

- **Framework**: `unittest` (gunakan `assertEqual`, bukan `assertEquals` yang deprecated).
- **Menjalankan semua test**:
  ```bash
  python -m unittest discover tests -p '*_test*.py' -v
  ```
- **Satu modul**:
  ```bash
  python -m unittest tests/UnitTests/Stemmer/stemmer_test.py -v
  ```
- **Status saat ini**: **190 test lulus**.
- Cakupan: aturan disambiguator 1–42, pipeline Context, visitor, dictionary, cache hit/miss + **konkurensi**, validasi input (`TypeError`/`ValueError`), jalur error factory (`RuntimeError` saat file data hilang), stop word remover, **konstruksi `VisitorProvider`**, fungsional + integrasi (pakai `subTest`).
- **Coverage**: ~96% (branch coverage via `coverage`, lihat `.coveragerc`; `source = Sastrawi`, `branch = True`). Yang tidak ter-cover: metode `pass` pada `*Interface.py`, `__init__.py` kosong, dan beberapa cabang defensif/dead code (`Context.py:52,128`, `Stemmer.py:71`, getter `Removal.py:14,20`).
- **CI**: workflow GitHub Actions di `.github/workflows/CI.yml` — install `pip install -e .` + `unittest discover` pada Python 3.8–3.12 (push `master`/`main`, pull request).
- Catatan: karena `Sastrawi` berlokasi di `src/`, test dijalankan dengan paket ter-install (`uv pip install -e .`) atau `PYTHONPATH=src`.

---

## 9. Konstrain & Keputusan Desain

- **Tanpa dependensi eksternal** — hanya stdlib; minimal risiko supply chain.
- **`__init__.py` semua kosong** — import harus path lengkap, mis. `from Sastrawi.Stemmer.StemmerFactory import StemmerFactory`.
- **Interface (`*Interface.py`) tidak memakai `abc.ABC`** — metode hanya `pass`. Didefer (breaking change).
- **Naming campuran camelCase/snake_case** — warisan port PHP, mis. `normalizedText` vs `current_word`. Refactor breaking didefer ke major version.
- **`Context.restore_prefix()`** memakai `removals[0]` (bukan loop-and-break).
- **Cache `ArrayCache` thread-safe** — operasi `set/get/has` dilindungi `threading.Lock`.
- **`__all__`** ada pada modul kelas publik (`StemmerFactory`, `Stemmer`, `CachedStemmer`, `StopWordRemover`, `StopWordRemoverFactory`, `ArrayDictionary`, `ArrayCache`); `__init__.py` tetap kosong.
- **Daftar visitor `VisitorProvider` dibekukan** sebagai `tuple` (urutan pipeline tidak berubah).

---

## 10. Status & Item Terdefer

Perbaikan audit (H1–H4, M1–M8, L1–L10, perbaikan test) yang ditandai FIXED sudah dikerjakan. Tambahan yang sudah diselesaikan via [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md): thread-safe `ArrayCache` (L8), `VisitorProvider` → `tuple` (M7), docstring asli (L1), `__all__` publik, stop words ke data file (L7), dan dokumentasi `kata-dasar.original.txt` (M8).

Item yang **sengaja didefer**:

| Item | Alasan |
|------|--------|
| Refactor penamaan camelCase → snake_case (L2) | Breaking public API; untuk major version |
| Migrasi interface ke ABC (M5) | Breaking untuk subclass; prioritas rendah |
| `InvalidAffixPairSpecification` (M3) | Dead code ber-test; dipertahankan sebagai utilitas |
