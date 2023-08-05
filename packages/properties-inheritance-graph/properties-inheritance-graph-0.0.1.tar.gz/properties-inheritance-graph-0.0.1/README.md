properties-inheritance-graph
----------------------------

[![pypi](https://img.shields.io/pypi/v/properties-inheritance-graph.svg)](https://pypi.org/project/properties-inheritance-graph)
[![travis](https://travis-ci.org/seequent/properties-inheritance-graph.svg?branch=master)](https://travis-ci.org/seequent/properties-inheritance-graph)
[![codecov](https://codecov.io/gh/seequent/properties-inheritance-graph/branch/master/graph/badge.svg?token=yyj42i2C5k)](https://codecov.io/gh/seequent/properties-inheritance-graph)

The purpose of this library is to quickly and easily create UML graphs
that show inheritance structure of `HasProperties` class hierarchies.
For more information on `HasProperties` classes, see
[properties](https://github.com/seequent/properties).

To install

```
pip install properties_inheritance_graph
```

then in Python

```python
from properties_inheritance_graph import make_graph
import omf  # or any other library built on properties

graph, registry = make_graph(
    registry=omf.PointSetElement._REGISTRY,
    expand_props=True,
    only_new_props=True,
    abstract_regex='^.*Model$',
)
```

In the above example, the properties-based [OMF](https://github.com/gmggroup/omf)
library is used for demonstration.

To render these graphs to file or in a Jupyter notebook, you may use
[nxpd](https://github.com/chebee7i/nxpd). [Graphviz](https://graphviz.gitlab.io/)
must also be installed.

```python
import nxpd
nxpd.draw(graph, filename='inheritance_graph.png')
```

![Inheritance Graph](https://raw.githubusercontent.com/seequent/properties-inheritance-graph/master/docs/inheritance_graph.png)
