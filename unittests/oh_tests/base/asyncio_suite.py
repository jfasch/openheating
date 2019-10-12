import asyncio
import unittest


class AsyncioTest(unittest.TestCase):

    def test__basic(self):
        handled = False
        async def handle_exceptions(awaitable):
            try:
                await awaitable
            except Exception:
                nonlocal handled
                handled = True

        async def task():
            raise Exception('bummer')

        loop = asyncio.get_event_loop()
        loop.run_until_complete(handle_exceptions(task()))
        self.assertTrue(handled)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(AsyncioTest)

if __name__ == '__main__':
    unittest.main()
