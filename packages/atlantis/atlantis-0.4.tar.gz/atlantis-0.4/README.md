# atlantis
Python library for natural language processing

## Usage
```python
from atlantis import Document

# create document
document = Document("He also begat and brought up five pairs of male children.")

# render entity graph
print('Entity Graph')
display(document.entity_graph.render())

# render document graph
print('Document Graph')
display(document.graph.render())
```

