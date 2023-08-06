eQuilibrator-API
================
[![pipeline status](https://gitlab.com/elad.noor/equilibrator-api/badges/master/pipeline.svg)](https://gitlab.com/elad.noor/equilibrator-api/commits/master)
[![coverage report](https://gitlab.com/elad.noor/equilibrator-api/badges/master/coverage.svg)](https://gitlab.com/elad.noor/equilibrator-api/commits/master)
[![Join the chat at https://gitter.im/equilibrator-devs/equilibrator-api](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/equilibrator-devs/equilibrator-api?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


A command-line API with minimal dependencies for calculation of standard 
thermodynamic potentials of biochemical reactions using the data found on 
[eQuilibrator](http://equilibrator.weizmann.ac.il/).
Does not require any network connections.

## Current Features

* Example scripts for singleton and bulk calculations.
* Calculation of standard Gibbs potentials of reactions (together with confidence intervals).
* Calculation of standard reduction potentials of half-cells.

To access more advanced features, such as adding new compounds that are not
available in the KEGG database, try using our full-blown
[Component Contribution](https://github.com/eladnoor/component-contribution)
package.

## Cite us

If you plan to use results from equilibrator-api in a scientific publication,
please cite our paper:

Noor E, Haraldsdóttir HS, Milo R, Fleming RMT. Consistent estimation of Gibbs 
energy using component contributions. PLoS Comput Biol. 2013;9: e1003098.

## Installation

The easiest way to get eQuilibrator-API up an running is using PyPI:
```
pip install equilibrator-api
```

Alternatively, you could install from source. Make sure you have [git-lfs](https://git-lfs.github.com/)
installed before cloning the repository:
```
git clone https://gitlab.com/elad.noor/equilibrator-api.git
cd equilibrator-api
python setup.py install
```

## Example Usage

Import the API and create an instance. Creating the EquilibratorAPI class
instance reads all the data that is used to calculate thermodynamic potentials of reactions.

```python
from equilibrator_api import ComponentContribution, Reaction, Q_
eq_api = ComponentContribution(p_h=Q_("6.5"), ionic_strength=Q_('200 mM')) # set pH and I
```

You can parse a reaction from a KEGG-style reaction string. The example given
is ATP hydrolysis to ADP and inorganic phosphate.

```python
rxn_str = "KEGG:C00002 + KEGG:C00001 = KEGG:C00008 + KEGG:C00009"
rxn = Reaction.parse_formula(rxn_str)
```

We highly recommend that you check that the reaction is atomically balanced
(conserves atoms) and charge balanced (redox neutral). We've found that it's
easy to accidentally write unbalanced reactions in this KEGG-style format and
so we always check ourselves.

```python
if not rxn.is_balanced():
	print('%s is not balanced' % rxn)
```

Now we know that the reaction is "kosher" and we can safely proceed to
calculate the standard change in Gibbs potential due to this reaction.

```python
# You control the pH and ionic strength!
# ionic strength is in Molar units.
standard_dg_prime, uncertainty = eq_api.standard_dg_prime(rxn)
print("dG0' = %s \u00B1 %s\n" % (standard_dg_prime, uncertainty))
```

You can also calculate the [reversibility index](https://doi.org/10.1093/bioinformatics/bts317) for this reaction.

```python
ln_RI = eq_api.ln_reversibility_index(rxn)
print('ln(Reversibility Index) = %s\n' % ln_RI)
```

The reversibility index is a measure of the degree of the reversibility of the
reaction that is normalized for stoichiometry. If you are interested in
assigning reversibility to reactions we recommend this measure because 1:2
reactions are much "easier" to reverse than reactions with 1:1 or 2:2 reactions.
You can see the paper linked above for more information.

### Example of pathway analysis using Max-min Driving Force:
Download an example pathway, run Max-min Driving Force analysis and generate two result figures
```python
from equilibrator_api import Pathway
from urllib.request import urlopen
url = "https://gitlab.com/elad.noor/equilibrator-api/raw/develop/tests/test_unit/pathway.tsv"
pp = Pathway.from_sbtab(urlopen(url))
mdf_res = pp.calc_mdf()
print('MDF = %s' % mdf_res.mdf)
mdf_res.reaction_plot.show()
mdf_res.compound_plot.show()
```

## Dependencies:
- python >= 3.6
- equilibrator-cache (latest)
- component-contribution (latest)
- sbtab
- numpy
- scipy
- optlang
- pandas
- nltk
- pyparsing
- matplotlib
- quilt
- pint
