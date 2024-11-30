# Runshaw Tree API

This is a simple API for the Runshaw Hack Club Christmas tree project. It allows you to write effects for the tree, but also test them on a pygame based simulator

## Installation

Use pip in a terminal. Example:
```bash
pip install git+https://github.com/Runshaw-Hack-Club/Christmas-Tree-API
```

## Example Usage

```python
import time
from runshawtree import controller

tree = controller.Tree(debug=True, num_leds=200)
for i in range(tree.backend.num_leds):
    tree.set_pixel(i, (255, 255, 255))
    tree.show()
    time.sleep(0.05)
tree.clear()
tree.show()
```