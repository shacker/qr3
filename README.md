QR3
=====

**QR3** helps you create and work with **queue, capped collection (bounded queue), deque, and stack** data structures for **Redis**.
Redis is well-suited for implementations of these abstract data structures, and QR makes it even easier to work with the structures in Python.

Quick Setup
------------

You will need:

- [redis](http://redis.io/download "Redis") — version 2.0 or better
- [redis-py](http://github.com/andymccurdy/redis-py "redis-pi")

Redis is available in many package managers by default, or built from source.
redis-py is available via `setuptools` or `pip`:

```
sudo pip install redis
```

Then install `qr`:

```
pip install qr3
```

Or if working from a local checkout of this package:

```
python setup.py install
```

To run tests:
```
python -m unittest discover -v
```

Responding to PR's
------------------
Given that this package primarily supports internal use cases, we cannot guarantee a
specific response time on PRs for new features. However, we will do our best to
consider them in a timely fashion.

We do commit to reviewing anything related to a security issue in a timely manner.
We ask that you first submit anything of that nature to security@doctorondemand.com
prior to creating a PR and follow responsible disclosure rules.

Thanks for your interest in helping with this package!

Basics of QR
------------------

QR queues store serialized Python objects (using [cPickle](http://docs.python.org/library/pickle.html) by default), but that can be changed by
setting the serializer on a per-queue basis.  This means "Python object in, and Python object out." There are a few constraints
on what can be pickled, and thus put into queues:

- `None`, `True`, and `False`
- Integers, long integers, floating point numbers, complex numbers
- Normal and Unicode strings
- Tuples, lists, sets, and dictionaries containing only picklable objects
- Functions defined at the top level of a module
- Built-in functions defined at the top level of a module
- Classes that are defined at the top level of a module
- Instances of such classes whose `__dict__` or `__setstate__()` is picklable (see section 'The pickle protocol' for details)

You probably know this already, but here's the 20-second overview of these data structures.

A **queue**:

* You push elements to the back of the queue and pop elements from the front.
* With respect to the elements, it's first in, first out (FIFO).

A **capped collection**:

* Another name for (what is essentially) a bounded queue.
* You push elements to the back, and once a maximum collection size is reached, the oldest element(s) is trimmed.

A **deque**, or double-ended queue:

* You can push values to the front *or* back of a deque, and pop elements from the front *or* back of the deque.

A **stack**, or, as they say in German, a 'Stapelspeicher':

* You can push elements to the back of the stack and pop elements from the back of the stack.
* It's last in, first out (LIFO).

A **priority queue**

* Push elements into a priority queue with *scores*, and then retrieve the elements in order of their respective scores.
* Values stored in the priority queue are unique.

Using QR
-------------------------------------

QR contains a few small classes to represent each data structure. To get access to one of the data structures, you create an instance. You can pass custom options for the underlying Redis instance as keyword arguments. For example:

```python
from qr3.qr import Queue

Queue('brand_new_queue_name', host='localhost', port=9000)
```

* A first-position **key** argument is required for all objects. It's the string name of the Redis **key** you want to be associated with the new data structure.

A Queue
--------

Let's create a Beatles queue, circa 1962.

	>> from qr import Queue
	>> bqueue = Queue('Beatles')

You are now the owner of a `Queue` object (`bqueue`), associated with the underlying Redis key 'Beatles'.

	>> bqueue.push('Pete')
	>> bqueue.push('John')
	>> bqueue.push('Paul')
	>> bqueue.push('George')

Unfortunately, George Martin doesn't like Pete Best, so it's time to pop him. Since Pete was first in:

	>> bqueue.pop()
	'Pete'

Ringo joins:

	>> bqueue.push('Ringo')

We can return the elements from the queue. Each class in QR includes two return-style methods: **elements** and **elements_as_json**.

* Call **elements()**, and you'll get back a Python list.

* Call **elements_as_json()**, and you'll get back the list as a JSON object.

For example:

	>> bqueue.elements()
	['Ringo', 'George', 'Paul', 'John']

	>> bqueue.elements_as_json()
	'['Ringo', 'George', 'Paul', 'John']'

A Capped Collection
--------------------

Radiohead is adding a band member. Radiohead has a max of five members, so someone is going to have to get kicked out of the band. We'll do this with a Capped Collection.

	>> from qr import CappedCollection
	>> radiohead_cc = CappedCollection('Radiohead', 5)

	>> radiohead_cc.push('Ed')
	>> radiohead_cc.push('Colin')
	>> radiohead_cc.push('Thom')
	>> radiohead_cc.push('Jonny')
	>> radiohead_cc.push('Phil')

	>> radiohead_cc.elements()
	['Phil', 'Jonny', 'Thom', 'Colin', 'Ed']

Now it's time for Donald to join the group.

	>> radiohead_cc.push('Donald')

And our new Radiohead is :

	>> radiohead_cc.elements()
	['Donald', 'Phil', 'Jonny', 'Thom', 'Colin']

A Deque
--------

If you wanted a deque for the Rolling Stones:

	>> from qr import Deque
	>> stones_deque = Deque('Stones')

The deque has different methods:

* push_front()
* push_back()
* pop_front()
* pop_back()

A Stack
--------

The Kinks stack is:

	>> from qr import Stack
	>> kinks_stack = Stack('Kinks')

The stack has the same methods as the queue.

A Priority Queue
----------------

Suppose you want to process various tasks in an order other than you received them. Instead you can
base this processing on a score associated with each task. Maybe you want to process bands in the order of how
many fans they have:

	>> from qr import PriorityQueue
	>> pr = PriorityQueue('bands')
	>> pr.push('The Beatles', 1e7)
	>> pr.push('Some Small Band', 1)
	>> pr.push('They Might Be Giants', 1e6)
	>> pr.pop()
	'Some Small Band'
	>> pr.pop()
	'They Might Be Giants'
	>> pr.pop()
	'The Beatles'

It's important to note that items in the queue are sorted by a score in ascending order, meaning
that the items with the least score is popped off first. Additionally, values stored in the priority
queue are unique. So, if you insert the same value twice with different scores, the value will only
appear once in the queue, with the second score provided:

	>> pr.push('The Beatles', 1e7)
	>> pr.push('The Beatles', 1.1e7)
	>> len(pr)
	1
	>> # There's still only one copy of 'The Beatles'
	>> pr.peek(withscores=True)
	('The Beatles', 11000000.0)

In addition to the values themselves, the `pop` and `peek` commands also support the argument
`withscores`, which returns a tuple of the value and its score when set to `True`.

All Queue Types
---------------

All queues have certain additional features. For example, you can add multiple elements at once:

	>> from qr import Queue
	>> q = Queue('widgets')
	>> q.extend(['foo', 'bar', 'sprockets'])

You can also get the number of elements in the queue like you would from any normal Python list:

	>> len(q)
	3

You can also look up a particular element from the queue (or range of elements). **Note carefully**: in Redis, lists are linked lists, and so index lookups are **O(n) to lookup the n'th position**. Although this functionality available in qr, you should be careful looking up large indices. Looking at the front or back of the queue is cheap, though:

	>> q[0]
	'foo'
	>> q[1:2]
	['bar', 'sprockets']
	>> q[-1]
	'sprockets'
	>> q.peek()
	'foo'

You can also put most Python objects into queues, and you get the same object back when you pop it.

	>> from widgets import Widget
	>> from sprockets import Sprocket
	>> q = Queue('work')
	# Put a sproket, widget and string in the queue
	>> q.extend([Sproket('foo'), Widget('bar'), 'Frank Sinatra'])
	>> q.pop()
	<sprocket.Sproket object>
	>> q.pop()
	<widget.Widget object>
	>> q.pop()
	'Frank Sinatra'

Additions, More
-----------------------

Thanks to mafr for initial tests and dlecocq/seomoz for serialization work.

Author: Ted Nyman | @tnm


MIT License
------------

Copyright (c) Ted Nyman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
