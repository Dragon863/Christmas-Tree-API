# Runshaw Tree API

This is a simple API for the Runshaw Hack Club Christmas tree project. It allows you to write effects for the tree, but also test them on a pygame based simulator before deploying them to the tree.

## Installation

Use pip in a terminal. Example:
```bash
pip install git+https://github.com/Runshaw-Hack-Club/Christmas-Tree-API
```

## Example Usage

```python
import time
from runshawtree import controller

# Set debug to False to run on the tree
tree = controller.Tree(debug=True, num_leds=200)

for i in range(tree.backend.num_leds):
    tree.set_pixel(i, (255, 255, 255))
    tree.show()
    time.sleep(0.05)
tree.clear()
tree.show()
```

## Note
When running with debug set to `False`, the default neopixel config will be for a GBR strip. You can pass this to the `Tree` constructor if you have a different strip, for example:
```python
tree = controller.Tree(debug=False, num_leds=200, order=["red", "green", "blue"])
```