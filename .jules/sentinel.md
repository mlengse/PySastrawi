## 2024-02-14 - Unbounded Cache Growth in Library
**Vulnerability:** The default `ArrayCache` implementation grew indefinitely, leading to potential Denial of Service (DoS) via memory exhaustion in long-running applications.
**Learning:** Even simple in-memory caches need bounds. Libraries often assume short-lived processes (like CLI tools), but in web servers, this becomes a critical memory leak.
**Prevention:** Always implement `max_size` and eviction policies (LRU) for any cache. Default to safe limits.

## 2024-05-22 - Unbounded Input in Text Processing
**Vulnerability:** `StopWordRemover.remove()` accepted strings of any length, potentially causing memory exhaustion (DoS) when splitting massive strings into lists.
**Learning:** Text processing libraries are prime targets for DoS via large payloads. Never assume input size is reasonable.
**Prevention:** Enforce `MAX_CHARACTER_LENGTH` limits on all public APIs accepting string input. Validate input types to fail fast.
