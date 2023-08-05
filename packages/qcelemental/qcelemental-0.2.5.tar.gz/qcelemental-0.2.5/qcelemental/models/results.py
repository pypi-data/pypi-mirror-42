import json
from enum import Enum
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Extra, constr, validator

from ..util import provenance_stamp
from .common_models import (ComputeError, DriverEnum, Model, Provenance, ndarray_encoder, qcschema_input_default,
                            qcschema_output_default)
from .molecule import Molecule


class Properties(BaseModel):
    scf_one_electron_energy: float = None
    scf_two_electron_energy: float = None
    nuclear_repulsion_energy: float = None
    scf_vv10_energy: float = None
    scf_xc_energy: float = None
    scf_dispersion_correction_energy: float = None
    scf_dipole_moment: List[float] = None
    scf_total_energy: float = None
    scf_iterations: int = None
    mp2_same_spin_correlation_energy: float = None
    mp2_opposite_spin_correlation_energy: float = None
    mp2_singles_energy: float = None
    mp2_doubles_energy: float = None
    mp2_total_correlation_energy: float = None
    mp2_total_energy: float = None
    calcinfo_nbasis: int = None
    calcinfo_nmo: int = None
    calcinfo_nalpha: int = None
    calcinfo_nbeta: int = None
    calcinfo_natom: int = None
    return_energy: float = None

    class Config:
        extra = Extra.allow  # Not yet fully validated, but will accept extra for now


class ErrorEnum(str, Enum):
    convergence_error = "convergence_error"
    file_error = "file_error"
    memory_error = "memory_error"


### Primary models


class ResultInput(BaseModel):
    """The MolSSI Quantum Chemistry Schema"""
    id: str = None
    molecule: Molecule
    driver: DriverEnum
    model: Model
    schema_name: constr(strip_whitespace=True, regex=qcschema_input_default) = qcschema_input_default
    schema_version: int = 1
    keywords: dict = {}
    provenance: Provenance = provenance_stamp(__name__)

    class Config:
        allow_mutation = False
        extra = Extra.allow  # Not yet fully validated, but will accept extra for now
        json_encoders = {**ndarray_encoder}

    def dict(self, *args, **kwargs):
        if self.id is None:
            excl = kwargs.setdefault("exclude", [])
            if isinstance(excl, list):
                excl.append("id")
            elif isinstance(excl, set):
                excl |= {"id"}

        return super().dict(*args, **kwargs)

    def json_dict(self, *args, **kwargs):
        return json.loads(self.json(*args, **kwargs))


class Result(ResultInput):
    schema_name: constr(strip_whitespace=True, regex=qcschema_output_default) = qcschema_output_default
    properties: Properties = Properties()
    success: bool
    error: ComputeError = None
    return_result: Union[float, List[float], Dict[str, Any]]

    class Config(ResultInput.Config):
        # Will carry other properties
        pass

    @validator("schema_name", pre=True)
    def input_to_output(cls, v):
        """If qcschema_input is passed in, cast it to output, otherwise no"""
        if v.lower().strip() in [qcschema_input_default, qcschema_output_default]:
            return qcschema_output_default
        raise ValueError("Only {0} or {1} is allowed for schema_name, "
                         "which will be converted to {0}".format(qcschema_output_default, qcschema_input_default))
