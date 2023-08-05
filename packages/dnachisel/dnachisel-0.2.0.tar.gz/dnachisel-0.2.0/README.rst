.. raw:: html

    <p align="center">
    <img alt="DNA Chisel Logo" title="DNA Chisel" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/DnaChisel/master/docs/_static/images/title.png" width="450">
    <br /><br />
    </p>

.. image:: https://travis-ci.org/Edinburgh-Genome-Foundry/DnaChisel.svg?branch=master
   :target: https://travis-ci.org/Edinburgh-Genome-Foundry/DnaChisel
   :alt: Travis CI build status

.. image:: https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/DnaChisel/badge.svg?branch=master
   :target: https://coveralls.io/github/Edinburgh-Genome-Foundry/DnaChisel?branch=master


DNA Chisel (complete documentation `here <https://edinburgh-genome-foundry.github.io/DnaChisel/>`_) is a Python library to optimize the nucleotides of DNA sequences with respect to a set of constraints and optimization objectives. It can be used for codon-optimizing the genes of a sequence for a particular organism, modifying a sequence to meet the constraints of a DNA provider while preserving genes, and much more.

DNA Chisel comes with more than 15 types of optimizations and constraints and allows users to define new specifications in Python, making the library suitable for a large range of automated sequence design applications, or complex custom design projects.

Example of use
---------------

In this basic example we generate a random sequence and optimize it so that

- It will be rid of BsaI sites.
- GC content will be between 30% and 70% on every 50bp window.
- The reading frame at position 500-1400 will be codon-optimized for *E. coli*.

Here is the code to achieve that:

.. code:: python

    from dnachisel import *

    # DEFINE THE OPTIMIZATION PROBLEM

    problem = DnaOptimizationProblem(
        sequence=random_dna_sequence(10000),
        constraints=[
            EnforceTranslation((500, 1400)),
            AvoidPattern(enzyme="BsaI"),
            EnforceGCContent(mini=0.3, maxi=0.7, window=50)
        ],
        objectives=[CodonOptimize(species='e_coli', location=(500, 1400))]
    )

    # SOLVE THE CONSTRAINTS, OPTIMIZE WITH RESPECT TO THE OBJECTIVE

    problem.resolve_constraints()
    problem.optimize()

    # PRINT SUMMARIES TO CHECK THAT CONSTRAINTS PASS

    print(problem.constraints_text_summary())
    print(problem.objectives_text_summary())

DnaChisel implements advanced constraints such as the preservation of coding
sequences,  or the inclusion or exclusion of advanced patterns (see
`this page <https://edinburgh-genome-foundry.github.io/DnaChisel/ref/builtin_specifications.html>`_
for an overview of available specifications), but it is also easy to implement your own constraints and objectives as subclasses
of ``dnachisel.Specification``.

DnaChisel also implements features for verification and troubleshooting. For
instance by generating optimization reports:

.. code:: python

    from dnachisel.reports import optimization_with_report
    optimization_with_report(target="report.zip", problem=some_problem)

Here is an example of summary report:

.. raw:: html

    <p align="center">
    <img alt="report" title="report" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/DnaChisel/master/docs/_static/images/report_screenshot.jpg" width="600">
    <br /><br />
    </p>

How it works
------------

DnaChisel hunts down every constraint breach and suboptimal region by recreating local version of the problem around these regions. Each type of constraint can be locally *reduced* and solved in its own way, to ensure fast and reliable resolution.

Below is an animation of the algorithm in action:

.. raw:: html

    <p align="center">
    <img alt="DNA Chisel algorithm" title="DNA Chisel" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/DnaChisel/master/docs/_static/images/dnachisel_algorithm.gif" width="800">
    <br />
    </p>

Installation
-------------

You can install DnaChisel through PIP

.. code::

    sudo pip install dnachisel

Alternatively, you can unzip the sources in a folder and type

.. code::

    sudo python setup.py install

To be able to generate plots and reports, run

.. code::

    sudo pip install dna_features_viewer weasyprint

License = MIT
--------------

DnaChisel is an open-source software originally written at the `Edinburgh Genome Foundry
<http://edinburgh-genome-foundry.github.io/home.html>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/DnaChisel>`_ under the MIT licence (¢ Edinburg Genome Foundry). Everyone is welcome to contribute !

More biology software
-----------------------

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Edinburgh-Genome-Foundry.github.io/master/static/imgs/logos/egf-codon-horizontal.png
  :target: https://edinburgh-genome-foundry.github.io/

DNA Chisel is part of the `EGF Codons <https://edinburgh-genome-foundry.github.io/>`_ synthetic biology software suite for DNA design, manufacturing and validation.
