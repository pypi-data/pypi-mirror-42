"""inherit from equilibrator_cache.models.compound.Compound an add phases."""
# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
from collections import namedtuple
from typing import Set, Tuple

import numpy as np
from equilibrator_cache import Compound
from equilibrator_cache.reaction import Reaction
from equilibrator_cache.thermodynamic_constants import legendre_transform

from . import Q_, R, ccache, ureg


AQUEOUS_PHASE_NAME = 'aqueous'
GAS_PHASE_NAME = 'gas'
LIQUID_PHASE_NAME = 'liquid'
SOLID_PHASE_NAME = 'solid'

PhaseInfo = namedtuple("phase_info", "shorthand "
                                     "standard_abundance "
                                     "physiolical_abundance "
                                     "dimensionality")

PHASE_INFO_DICT = {
    AQUEOUS_PHASE_NAME: PhaseInfo("(aq)", Q_("1 M"), Q_("1 mM"),
                                  "[concentration]"),
    GAS_PHASE_NAME: PhaseInfo("(g)", Q_("1 bar"), Q_("1 mbar"), "[pressure]"),
    SOLID_PHASE_NAME: PhaseInfo("(s)", None, None, None),
    LIQUID_PHASE_NAME: PhaseInfo("(l)", None, None, None)
}

# dictionary of compounds that can be non aqueous. The values are tuples of
# possible phases, starting with the default phase
NON_AQUEOUS_COMPOUND_DICT = {
    "MNXM2": (LIQUID_PHASE_NAME, ),  # H2O
    "MNXM89": (SOLID_PHASE_NAME, ),  # sulfur
    "MNXM4": (AQUEOUS_PHASE_NAME, GAS_PHASE_NAME),  # O2
    "MNXM195": (AQUEOUS_PHASE_NAME, GAS_PHASE_NAME),  # H2
    "MNXM724": (AQUEOUS_PHASE_NAME, GAS_PHASE_NAME),  # N2
    "MNXM13": (AQUEOUS_PHASE_NAME, GAS_PHASE_NAME),  # CO2
    "MNXM10881": (AQUEOUS_PHASE_NAME, GAS_PHASE_NAME),  # CO
}

MicroSpecie = namedtuple("microspecie", "standard_dgf num_protons charge")

# list of compounds that can also be in non aqueous phases. The values are the
# formation energy, number of protons and charge. Values are from [Alberty's
# Thermodynamics of Biochemical Reactions, 2003]. If the standard_dgf is
# None, use the value from component_contribution
PHASED_COMPOUND_DICT = {
    ("MNXM4", GAS_PHASE_NAME): MicroSpecie(
        standard_dgf=Q_("0 kJ/mol"), num_protons=0, charge=0),  # O2
    ("MNXM195", GAS_PHASE_NAME): MicroSpecie(
        standard_dgf=Q_("0 kJ/mol"), num_protons=2, charge=0),  # H2
    ("MNXM724", GAS_PHASE_NAME): MicroSpecie(
        standard_dgf=Q_("0 kJ/mol"), num_protons=0, charge=0),  # N2
    ("MNXM13", GAS_PHASE_NAME): MicroSpecie(
        standard_dgf=Q_("-394.36 kJ/mol"), num_protons=0, charge=0),  # CO2
    ("MNXM10881", GAS_PHASE_NAME): MicroSpecie(
        standard_dgf=Q_("-137.17 kJ/mol"), num_protons=0, charge=0),  # CO
    ("MNXM89", SOLID_PHASE_NAME): MicroSpecie(
        standard_dgf=Q_("0 kJ/mol"), num_protons=0, charge=0),  # S8
}


class Condition(object):
    """A class for defining the conditions of a compound.

    I.e. the phase and the abundance.
    """

    def __init__(self, phase: str, abundance: ureg.Quantity = None):
        """Create a new condition object."""
        assert phase in PHASE_INFO_DICT, f"Unknown phase: {phase}"
        self._phase = phase
        self._abundance = abundance or self.standard_abundance

    @property
    def phase(self) -> str:
        """Return the phase."""
        return self._phase

    @property
    def abundance(self) -> ureg.Quantity:
        """Return the abundance."""
        return self._abundance

    @property
    def standard_abundance(self) -> ureg.Quantity:
        """Return the standard abundance in this phase."""
        return PHASE_INFO_DICT[self._phase].standard_abundance

    @property
    def physiolical_abundance(self) -> ureg.Quantity:
        """Return the default physiological abundance in this phase."""
        return PHASE_INFO_DICT[self._phase].physiolical_abundance

    @property
    def dimensionality(self) -> str:
        """Return the dimensionality of the abundance in this phase.

        E.g. [concentration] for aqueous phase, or [pressure] for gas phase.
        :return: the dimensionality in this phase, or None if abundance is
        fixed.
        """
        return PHASE_INFO_DICT[self._phase].dimensionality

    @property
    def ln_abundance(self) -> float:
        """Return the log of the ratio between given and std abundances."""
        if self.standard_abundance is None:
            return 0.0  # when the phase does not allow relative abundances
        if self._abundance is None:
            return 0.0  # when the phase does not allow relative abundances
        else:
            return np.log(float(self._abundance / self.standard_abundance))

    @property
    def ln_physiological_abundance(self) -> float:
        """Return the log of the ratio between phys and std abundances."""
        if self.standard_abundance is None:
            return 0.0  # when the phase does not allow relative abundances
        if self.physiolical_abundance is None:
            return 0.0  # when the phase does not allow relative abundances
        else:
            return np.log(
                float(self.physiolical_abundance / self.standard_abundance))

    @abundance.setter
    def abundance(self, abundance: ureg.Quantity) -> None:
        """Change the phase of a specific compound.

        :param abundance: the new abundance in the correct units
        :return:
        """
        if abundance is None:
            return

        assert self.standard_abundance is not None, (
            f"compounds in {self.phase} phase cannot have a relative abundance."
        )

        assert abundance.check(self.dimensionality), (
            f"compounds in {self.phase} phase must have their abundance in "
            f"units of {self.dimensionality}."
        )

        self._abundance = abundance

    def reset_abundance(self) -> None:
        """Reset the abundance to standard abundance."""
        self._abundance = self.standard_abundance

    @property
    def is_physiological(self) -> bool:
        """Return True iff the abundance is the same as the physiological.

        :return: True if the abundance is in physiological conditions,
        or if the abundance if fixed in this phase anyway.
        """
        if self.standard_abundance is None:
            return True  # when the phase does not allow relative abundances
        if self.physiolical_abundance is None:
            return True  # when the phase does not allow relative abundances
        else:
            return self._abundance == self.standard_abundance


class PhasedCompound(object):
    """A class that combines a equilibrator_api Compound and a Condition."""

    def __init__(self, compound: Compound, condition: Condition = None):
        """Create a new PhasedCompound object."""
        self.compound = compound
        self.condition = condition or Condition(self.possible_phases[0])

    @staticmethod
    def get_default(compound: Compound) -> Condition:
        """Get the default phase of a compound.

        :param compound: a Compound
        :return: the default phase
        """
        if compound.mnx_id in NON_AQUEOUS_COMPOUND_DICT:
            return Condition(NON_AQUEOUS_COMPOUND_DICT[compound.mnx_id][0])
        else:
            return Condition(AQUEOUS_PHASE_NAME)

    @property
    def mnx_id(self) -> str:
        """Get the compound's MetaNetX ID."""
        return self.compound.mnx_id

    @property
    def id(self) -> int:
        """Get the compound's equilibrator internal ID."""
        return self.compound.id

    @property
    def formula(self) -> str:
        """Get the chemical formula."""
        return self.compound.formula

    @property
    def html_formula(self) -> str:
        """Get the chemical formula."""
        return re.sub(r'(\d+)', r'<sub>\1</sub>', self.compound.formula)

    @property
    def mass(self) -> float:
        """Get the chemical molecular mass."""
        return self.compound.mass

    @property
    def phase(self) -> str:
        """Get the phase."""
        return self.condition.phase

    @property
    def phase_shorthand(self) -> str:
        """Get the phase shorthand (i.e. 'l' for liquid)."""
        if self.compound.mnx_id == "MNXM60":
            # for CO2(total) there should be no indication of the phase,
            # since it is actually a combination of gas and aqueous.
            return ""
        else:
            return PHASE_INFO_DICT[self.condition.phase].shorthand

    @phase.setter
    def phase(self, phase: str) -> None:
        """Change the phase of a specific compound.

        :param phase: the new phase
        :return:
        """
        assert phase in self.possible_phases, (
            f"The phase of {self.compound} must be one of the following: "
            f"{str(self.possible_phases)}."
        )
        self.condition = Condition(phase)

    @property
    def possible_phases(self) -> Tuple[str]:
        """Get the possible phases for this compound."""
        return NON_AQUEOUS_COMPOUND_DICT.get(
            self.mnx_id, (AQUEOUS_PHASE_NAME, )
        )

    @property
    def abundance(self) -> ureg.Quantity:
        """Get the abundance."""
        return self.condition.abundance

    @abundance.setter
    def abundance(self, abundance: ureg.Quantity) -> None:
        """Change the phase of a specific compound.

        :param abundance: the new abundance in the correct units
        :return:
        """
        assert self.compound != Reaction.PROTON_COMPOUND, (
            f"Cannot directly change the relative abundance of H+. Use the pH "
            f"parameter instead for adjusting this value."
        )

        self.condition.abundance = abundance

    @property
    def ln_abundance(self) -> float:
        """Return the log of the abundance (for thermodynamic calculations)."""
        if self.compound == Reaction.PROTON_COMPOUND:
            # Since pH is an environmental parameter, we do not use the
            # concentration of protons for energy calculations
            return 0.0
        return self.condition.ln_abundance

    @property
    def ln_physiological_abundance(self) -> float:
        """Return the log of the default physiological abundance."""
        if self.compound == Reaction.PROTON_COMPOUND:
            # Since pH is an environmental parameter, we do not use the
            # concentration of protons for energy calculations
            return 0.0
        return self.condition.ln_physiological_abundance

    @property
    def is_physiological(self) -> bool:
        """Check if the abundance is physiological."""
        return self.condition.is_physiological

    @ureg.check(None, None, "[concentration]", "[temperature]")
    def get_stored_standard_dgf_prime(
            self,
            p_h: ureg.Quantity,
            ionic_strength: ureg.Quantity,
            temperature: ureg.Quantity
    ) -> ureg.Quantity:
        """Return the stored formation energy of this phased compound.

        Only if it exists, otherwise return None (and we will use
        component-contribution later to get the reaction energy).

        :param p_h:
        :param ionic_strength:
        :param temperature:
        :return: standard_dgf_prime (in kJ/mol)
        """
        ms = self.get_stored_microspecie()
        if ms is not None:
            # for compound-phase pairs in this dictionary use the stored
            # value and transform directly using the Legendre transform
            return ms.standard_dgf + legendre_transform(
                p_h=p_h, ionic_strength=ionic_strength,
                temperature=temperature, num_protons=ms.num_protons,
                charge=ms.charge
            ) * R * temperature
        else:
            # for all other compounds, we will use component_contribution
            return None

    def get_stored_standard_dgf(
            self
    ) -> ureg.Quantity:
        """Return the stored formation energy of this phased compound.

        Only if it exists, otherwise return None (and we will use
        component-contribution later to get the reaction energy).

        :return: standard_dgf (in kJ/mol)
        """
        ms = self.get_stored_microspecie()
        if ms is not None:
            # for compound-phase pairs in this dictionary use the stored
            # value
            return ms.standard_dgf
        else:
            # for all other compounds, we will use component_contribution
            return None

    def get_stored_microspecie(self) -> MicroSpecie:
        """Get the stored microspecies (from the PHASED_COMPOUND_DICT).

        :return: The MicroSpecie namedtuple with the stored formation energy,
        or None if this compound has no stored value at this phase.
        """
        return PHASED_COMPOUND_DICT.get((self.mnx_id, self.phase), None)

    def serialize(self) -> dict:
        """Return a serialized version of all the compound thermo data.

        :return: a list of dictionaries with all the microspecies data
        """
        ms_list = []
        ms = self.get_stored_microspecie()
        if ms is not None:
            ms_list.append(ms.__dict__())
        else:
            for ms in self.compound.microspecies:
                d = {"num_protons": ms.number_protons,
                     "charge": ms.charge,
                     "ddg_over_rt": ms.ddg_over_rt,
                     "num_magnesiums": 0
                     }
                ms_list.append(d)

        return {"mnx_id": self.mnx_id,
                "phase": self.phase,
                "ln_abundance": self.ln_abundance,
                "microspecies": ms_list}

    @property
    def first_name(self):
        """Get the first name that appears in the compound-cache."""
        # TODO: use MetaNetX database to get the first name
        return ccache.get_compound_first_name(self.compound)

    @property
    def names(self) -> Set[str]:
        """Get the set of all associated names in the compound cache."""
        return ccache.get_compound_names(self.compound)
