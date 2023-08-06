Grot
====

**Grot** is a noun and means **arrowhead** in polish language.

Makes graphviz usage simpler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Much less headache. Gets you faster into the point.

.. code:: python


    from grot import Grot

    g = Grot(filename='example_01', format='png')

    one = g.node("It is\neaiser")
    two = "to define"
    three = g.node("graphs")

    g.edge(one, two, three)

    assert g.source == r"""digraph test_grot {
        graph [fontname=helvetica nodesep=0.5 ranksep=0.5 sep=0.4]
        node [color="#13136c" fontname=helvetica penwidth=1.8 shape=box]
        edge [fontname=helvetica]
        n_a [label="It is\neaiser"]
        n_1 [label=graphs]
        n_d [label="to define" shape=none]
        n_a -> n_d
        n_d -> n_1
    }"""
    # to generate a pdf, call:

    g.render()

|Rendered graph image|

It will generate a ``example_01.png`` file in current directory.

Refer to tests for more features information.

.. |Rendered graph image| image:: tests/example_01.png?raw=true



