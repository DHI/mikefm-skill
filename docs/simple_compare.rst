.. _simple_compare:

Simple time series comparison
#############################

If all you need to do is to compare two point time series, the workflow is 
very simple and described below. The general many-to-many comparison is decribed 
in the `getting started guide <getting_started.html>`_.


Workflow
********

The simplified fmskill workflow consists of these four steps:

#. Specify **model result**
#. Specify **observation**
#. **compare()**
#. Analysis and plotting


1. Specify model result
=======================

The model result can be either a dfs0 or a DataFrame. It needs to have a single item only.

.. code-block:: python

    from mikeio import Dfs0
    fn_mod = '../tests/testdata/SW/ts_storm_4.dfs0'
    df_mod = Dfs0(fn_mod).read(items=0).to_dataframe()


2. Specify Observation
======================
The observation can be either a dfs0, a DataFrame or a PointObservation object. 
It needs to have a single item only.

.. code-block:: python

    fn_obs = '../tests/testdata/SW/eur_Hm0.dfs0'


3. compare()
============
The `compare() <api.html#fmskill.connection.compare>`_ method will interpolate the modelresult to the time of the observation
and return an object that can be used for analysis and plotting

.. code-block:: python

    import fmskill
    c = fmskill.compare(fn_obs, df_mod)


4. Analysis and plotting
========================

The returned `PointComparer <api.html#fmskill.comparison.PointComparer>`_ can make
scatter plots, skill assessment, time series plots etc.


.. code-block:: python

    c.plot_timeseries()
    c.skill()
    c.scatter()