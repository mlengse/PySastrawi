# Changelog

Semua perubahan penting pada PySastrawi didokumentasikan di berkas ini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.1.0/),
dan proyek ini mengikuti [Semantic Versioning](https://semver.org/lang/id/).

## [2.0.0] - 2026-08-02

Rilis major dengan **perubahan API yang memutus kompatibilitas** (breaking). Sebelum
pemutakhiran dari versi 1.x, baca bagian *Breaking changes* di bawah.

### Breaking changes

- **Interface sekarang `abc.ABC` + `@abstractmethod`** (`IP-4.1`). Kelas yang
  mewarisi `*Interface` wajib mengimplementasikan seluruh metode abstrak; instansiasi
  langsung interface atau subclass yang belum lengkap kini memunculkan `TypeError`.
  Interface yang terdampak: `DictionaryInterface`, `CacheInterface`,
  `StemmerInterface`, `ContextInterface`, `RemovalInterface`.
- **Penamaan metode/atribut diubah dari camelCase ke snake_case** (`IP-4.2`).
  Contoh:
  - `CachedStemmer(delegatedStemmer)` → `CachedStemmer(delegated_stemmer)`
  - `stemmer.normalizedText` → `stemmer.normalized_text`
  - `removal.removedPart` / `removal.affixType` → `removal.removed_part` / `removal.affix_type`
  - `context.stopProcess()` / `context.processIsStopped` → `context.stop_process()` / `context.process_is_stopped()`
  - `stemmerFactory.resultCache`, `stemmerFactory.cachedStemmer`, `stemmerFactory.dictionaryFile` → `result_cache`, `cached_stemmer`, `dictionary_file`
  - `stopWordRemoverFactory.stopWords`, `stopWordRemoverFactory.stopWordRemover` → `stop_words`, `stop_word_remover`
  - Konstanta regex `InvalidAffixPairSpecification.invalidAffixes` → `_INVALID_AFFIXES`
- **Python minimum tetap `>=3.8`**; tidak ada perubahan pada dependensi (tetap hanya stdlib + `re`).

### Fixed

- **Bug laten injeksi regex** di 5 visitor: penghapusan afiks memakai
  `re.sub(result, '', ...)` yang memperlakukan hasil disambiguator sebagai pola
  regex. Kini memakai `str.replace(result, '', 1)` (`H1`).
- **Double normalization** pada `CachedStemmer` yang menormalisasi teks dua kali
  sebelum mendelegasikan ke `Stemmer`; kini langsung mendelegasi ke `stem_word()` (`M1`).
- **`setup.py` `long_description`** yang menimpa isi README dengan string polos (`H3`).
- **`setup.cfg` `universal=1`** yang mengklaim dukungan Python 2 padahal hanya Python 3 (`H4`).
- **Sisa Python 2** (`from io import open`, kompatibilitas `basestring`, `codecs.open`) dihapus (`M6`).
- **Parameter `isDev`** yang mati di `StemmerFactory` dihapus (`M2`).
- **Konstanta `APC_KEY`** yang tidak terpakai dihapus (`L5`).
- **Typo "wether"** → "whether" di `Context.py` (`L3`).
- **Deklarasi gaya lama** `TextNormalizer(object)` → `TextNormalizer()` (`L4`).
- **`Context.restore_prefix()`** memakai `removals[0]` langsung menggantikan loop-and-break (`L10`).

### Added

- **`InvalidAffixPairSpecification` regex di-precompile** sebagai konstanta kelas
  (`M4`). Catatan: spec ini sengaja **tidak di-wire** ke pipeline stemming — hasil
  evaluasi menunjukkan wiring justru menurunkan akurasi (lihat `IMPLEMENTATION_PLAN.md`
  catatan IP-4.3).
- **`__all__`** pada modul kelas publik: `StemmerFactory`, `Stemmer`, `CachedStemmer`,
  `StopWordRemoverFactory`, `StopWordRemover`, `ArrayDictionary`, `ArrayCache` (`IP-1.4`).
- **`ArrayCache` thread-safe** dengan `threading.Lock` + test konkurensi (`IP-1.2`).
- **Daftar visitor dibekukan** sebagai `tuple` di `VisitorProvider` (`IP-1.1`).
- **Stop words dipindah ke file data** `StopWordRemover/data/stop-words.txt` (±809 kata);
  API `get_stop_words()` dipertahankan (`IP-2.1`).
- **Dokumentasi `kata-dasar.original.txt`** di `Stemmer/data/README.md` (`IP-2.2`).
- **Docstring asli** menggantikan 13 placeholder `"""description of class"""` (`IP-1.3`).
- **CI GitHub Actions** (`.github/workflows/ci.yml`) menggantikan Travis CI; menjalankan
  `unittest` pada Python 3.8–3.12 (`386dfc2`).
- **Konfigurasi coverage** (`.coveragerc`, branch coverage) dan **test jalur error**:
  `ValueError` saat input melebihi batas, `RuntimeError` saat file data hilang.
- **Test konstruksi `VisitorProvider`** (+7 test) dan test konkurensi cache (+2 test).
- Total test: **190**, coverage **~98%**.

## Sebelum 2.0.0

Riwayat versi 1.x tidak terdokumentasi di berkas ini; lihat `git log` untuk detail.
Versi terakhir sebelum rilis ini: **1.2.1**.
