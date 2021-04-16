import pytest
import numpy as np

from fmskill.model import ModelResult, ModelResultCollection
from fmskill.observation import PointObservation


def test_basic():

    m_st8_in = ModelResult("tests/testdata/ECOLAB/st8_ECO.dfs0", name="Odense_IN")
    m_st8_in.add_observation(
        PointObservation(
            "tests/testdata/ECOLAB/obs/st8_waterquality_variables.dfs0", item="IN"
        ),
        item="St 8 ECO (-1 m): IN, Inorganic nitrogen, g N/m3",
    )

    m_st17_in = ModelResult("tests/testdata/ECOLAB/st17_ECO.dfs0", name="Odense_IN")
    m_st17_in.add_observation(
        PointObservation(
            "tests/testdata/ECOLAB/obs/st17_waterquality_variables_top.dfs0", item="IN"
        ),
        item="St 17 ECO (-1 m): IN, Inorganic nitrogen, g N/m3",
    )

    cc1 = m_st8_in.extract()
    cc2 = m_st17_in.extract()

    cc1.add_comparer(cc2[0])

    assert cc1.score() > 0.0
