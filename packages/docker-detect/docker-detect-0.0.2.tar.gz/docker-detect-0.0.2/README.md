## Docker/Kubernetes/LXC container detection

Tries to detect whether the current process is running inside Docker/Kubernetes/LXC container.


## Installation

```bash

    $ pip install -U docker-detect

```


## Example

Import and call `is_inside_container()`

```python

    >>> from dockerdetect import is_inside_container()
    >>> is_inside_container()
    True

```

