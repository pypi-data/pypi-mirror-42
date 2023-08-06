# bai_stats

bai_stats is a Python library for statistical analysis.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bai_stats.

```bash
pip install bai_stats
```

## Usage

```python
import bai_stats
import scipy.stats as stats

data=stats.norm.rvs(size=100)

best_fit_distribution_table=bai_stats.best_fit_distributions(data,max_shape_par=0,plot_dist=True) 
# returns best_fit_distribution_table

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)