# delta-e

This is the documentation of **delta-e**.

:::{note}
This is the main page of your project's [Sphinx] documentation.
It is formatted in [reStructuredText]. Add additional pages
by creating rst-files in `docs` and adding them to the [toctree] below.
Use then [references] in order to link them from this page, e.g.
{ref}`authors` and {ref}`changes`.

It is also possible to refer to the documentation of other Python packages
with the [Python domain syntax]. By default you can reference the
documentation of [Sphinx], [Python], [NumPy], [SciPy], [matplotlib],
[Pandas], [Scikit-Learn]. You can add more by extending the
`intersphinx_mapping` in your Sphinx's `conf.py`.

The pretty useful extension [autodoc] is activated by default and lets
you include documentation from docstrings. Docstrings can be written in
[Google style] (recommended!), [NumPy style] and [classical style].
:::

## Contents

```{toctree}
:maxdepth: 2

Overview <readme>
About <About>
Contributions & Help <contributing>
License <license>
Authors <authors>
Changelog <changelog>
Module Reference <api/modules>
```

<!--
## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
-->

[autodoc]: https://www.sphinx-doc.org/en/master/ext/autodoc.html
[classical style]: https://www.sphinx-doc.org/en/master/domains.html#info-field-lists
[google style]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[matplotlib]: https://matplotlib.org/contents.html#
[numpy]: https://numpy.org/doc/stable
[numpy style]: https://numpydoc.readthedocs.io/en/latest/format.html
[pandas]: https://pandas.pydata.org/pandas-docs/stable
[python]: https://docs.python.org/
[python domain syntax]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain
[references]: https://www.sphinx-doc.org/en/stable/markup/inline.html
[restructuredtext]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
[scikit-learn]: https://scikit-learn.org/stable
[scipy]: https://docs.scipy.org/doc/scipy/reference/
[sphinx]: https://www.sphinx-doc.org/
[toctree]: https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
