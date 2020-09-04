from mmelemental.models.base import Base
from pydantic import Field
from typing import Any

class ToolkitMolecule(Base):
    mol: Any = Field(..., description = 'Toolkit-specific molecule object.')
    dtype: str = Field(None, description = 'Data type for mol.')

    class Config(Base.Config):
        arbitrary_types_allowed = True

    @property
    def obj_type(self):
        return self.dtype
