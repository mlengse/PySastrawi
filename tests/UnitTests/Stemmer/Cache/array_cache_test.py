import unittest
from threading import Thread

from Sastrawi.Stemmer.Cache.ArrayCache import ArrayCache


class TestArrayCache(unittest.TestCase):
    def setUp(self):
        self.cache = ArrayCache()

    def test_has_returns_false_for_missing_key(self):
        self.assertFalse(self.cache.has('missing'))

    def test_set_and_has_and_get(self):
        self.cache.set('key', 'value')
        self.assertTrue(self.cache.has('key'))
        self.assertEqual('value', self.cache.get('key'))

    def test_get_returns_none_for_missing_key(self):
        self.assertIsNone(self.cache.get('missing'))

    def test_overwrite_value(self):
        self.cache.set('key', 'first')
        self.cache.set('key', 'second')
        self.assertEqual('second', self.cache.get('key'))

    def test_multiple_keys(self):
        self.cache.set('a', '1')
        self.cache.set('b', '2')
        self.assertTrue(self.cache.has('a'))
        self.assertTrue(self.cache.has('b'))
        self.assertEqual('1', self.cache.get('a'))
        self.assertEqual('2', self.cache.get('b'))

    def test_concurrent_access(self):
        errors = []

        def worker(base):
            try:
                for i in range(100):
                    key = base + str(i)
                    self.cache.set(key, i)
                    self.assertEqual(i, self.cache.get(key))
                    self.assertTrue(self.cache.has(key))
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [Thread(target=worker, args=('t%d-' % t,)) for t in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual([], errors)

    def test_concurrent_eviction_stays_within_max_size(self):
        cache = ArrayCache(max_size=10)

        def worker(base):
            for i in range(100):
                cache.set(base + str(i), i)

        threads = [Thread(target=worker, args=('t%d-' % t,)) for t in range(8)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertLessEqual(len(cache.data), 10)


if __name__ == '__main__':
    unittest.main()
