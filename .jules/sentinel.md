## 2024-02-14 - Unbounded Cache Growth in Library
**Vulnerability:** The default `ArrayCache` implementation grew indefinitely, leading to potential Denial of Service (DoS) via memory exhaustion in long-running applications.
**Learning:** Even simple in-memory caches need bounds. Libraries often assume short-lived processes (like CLI tools), but in web servers, this becomes a critical memory leak.
**Prevention:** Always implement `max_size` and eviction policies (LRU) for any cache. Default to safe limits.
