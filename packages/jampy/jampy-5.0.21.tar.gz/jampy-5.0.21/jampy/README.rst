The JamPy Package
=================

**Jeans Anisotropic Modelling of Galactic Dynamics**

.. image:: https://img.shields.io/pypi/v/jampy.svg
        :target: https://pypi.org/project/jampy/
.. image:: https://img.shields.io/badge/arXiv-0806.0042-orange.svg
        :target: https://arxiv.org/abs/0806.0042
.. image:: https://img.shields.io/badge/DOI-10.1111/...-green.svg
        :target: https://doi.org/10.1111/j.1365-2966.2008.13754.x

JamPy is a Python implementation of the Jeans Anisotropic Modelling (JAM)
formalism of `Cappellari (2008) <http://adsabs.harvard.edu/abs/2008MNRAS.390...71C>`_,
for galactic dynamics, in spherical and axisymmetric geometry.

JamPy also includes the updates for proper motions in axisymmetric and
spherical geometry of `Cappellari (2012) <http://arxiv.org/abs/1211.7009>`_ and
`Cappellari (2015) <http://arxiv.org/abs/1504.05533>`_ respectively.

.. contents:: :depth: 1

Attribution
-----------

If you use this software for your research, please cite 
`Cappellari (2008) <http://adsabs.harvard.edu/abs/2008MNRAS.390...71C>`_. 
And if you use it for proper motions, also cite the relevant papers above.
The BibTeX entry for the main JAM paper is::

    @ARTICLE{Cappellari2008,
        author = {{Cappellari}, M.},
        title = "{Measuring the inclination and mass-to-light ratio of
            axisymmetric galaxies via anisotropic Jeans models of stellar
            kinematics}",
        journal = {MNRAS},
        eprint = {0806.0042},
        year = 2008,
        volume = 390,
        pages = {71-86},
        doi = {10.1111/j.1365-2966.2008.13754.x}
    }

Installation
------------

install with::

    pip install jampy

Without writing access to the global ``site-packages`` directory, use::

    pip install --user jampy

Documentation
-------------

Full documentation is contained in the individual files headers.

Usage examples are contained in the directory  ``jampy/examples``, which is
copied by ``pip`` within the ``site-packages`` folder.

What follows is the documentation of one of the main procedures, extracted from
the Python file header.
