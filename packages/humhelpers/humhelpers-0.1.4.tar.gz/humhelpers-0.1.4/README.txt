Provides different shortcuts functions (helpers) for humanity.

Created to be something like Ramda or Lodash for Python, but without
functional style.


For strings:

`reverse` - Reverse a string.
`replace` -
	Replaces one substring in string to another.
	Analog to string method with same name,
	but also adds ability to change direction, from which to replace substring.


For collections:

`get` - Returns or element from collection by index (key), or None if not found.


For asyncio:

`run_async` - Asynchronously runs coroutine (function, defind with 'async def') until it completes.
