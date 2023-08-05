# Grammar
Grammar is a Python library for natural language processing.

## Installation
You can use pip to install grammar.
```bash
pip install grammar
```

## Dependencies
Grammar uses Vineyard and Graphviz to visualize graphs of the document.

## Usage

### Creating a Document
```python
from grammar import Document

# create document
document = Document("He also begat and brought up five pairs of male children.")
```

### Entity Graph
```python
display(document.entity_graph.render())
```
![](https://github.com/idin/grammar/blob/master/pictures/entity_graph.png)

### Document Graph
```python
display(document.graph.render())
```
![](https://github.com/idin/grammar/blob/master/pictures/document_graph.png)

### Masking
