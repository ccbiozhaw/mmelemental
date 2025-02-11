from pydantic import Field, validator, root_validator
from typing import Optional, List
from mmelemental.types import Array
from mmelemental.models.base import ProtoModel

__all__ = ["CharmmMulti"]


class CharmmMulti(ProtoModel):
    """
    Charmm-style dihedral potential: Energy = energy * (1 + cos(periodicity * angle - phase)).
    """

    energy: List[Array[float]] = Field(
        ...,
        description="Dihedral energy constant. Default unit is kJ/mol.",
    )
    energy_units: Optional[str] = Field(
        "kJ/mol", description="Dihedral energy constant unit."
    )
    periodicity: List[Array[int]] = Field(
        ...,
        description="Dihedral periodicity factor, must be >= 0.",
    )
    phase: List[Array[float]] = Field(
        ...,
        description="Dihedral phase angle. Default unit is degrees.",
    )
    phase_units: Optional[str] = Field(
        "degrees", description="Dihedral phase angle unit."
    )

    @validator("energy", "periodicity", "phase", allow_reuse=True)
    def _valid_shape(cls, v):
        assert v[-1].shape, "Array must be 2D!"
        return v

    @validator("periodicity", allow_reuse=True)
    def _valid_periodicity(cls, v):
        for arr in v:
            assert (arr >= 0).all(), "Dihedral periodicity must be >= 0."
        return v

    # @root_validator(allow_reuse=True)
    def _valid_arrays(cls, values):
        energy_len = len(values["energy"])
        periodicity_len = len(values["periodicity"])
        phase_len = len(values["phase"])
        assert (
            energy_len == periodicity_len == phase_len
        ), f"Energy ({energy_len}), periodocity ({periodicity_len}), and phase ({phase_len}) must have the same shape."
        return values
