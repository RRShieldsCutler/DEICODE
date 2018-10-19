
[![Latest Github release](https://img.shields.io/github/release/cjm007/DEICODE.svg)](https://github.com/cjm007/DEICODE/releases/latest)
[![Build Status](https://travis-ci.org/cameronmartino/DEICODE.svg?branch=master)](https://travis-ci.org/cameronmartino/DEICODE)[![Coverage Status](https://coveralls.io/repos/github/cjm007/DEICODE/badge.svg?branch=master)](https://coveralls.io/github/cjm007/DEICODE?branch=master)
[![DOI](https://zenodo.org/badge/72654142.svg)](https://zenodo.org/badge/latestdoi/72654142)

deicode is a tool box for running Robust Aitchison RPCA on sparse omics datasets, linking specific features (i.e. microbes or metabolites) to beta-diversity ordination.

## Installation

To install the most up to date version of deicode, run the following command

    pip install git+https://github.com/cameronmartino/DEICODE.git

## Examples

TODO

## Usage

Command line
```sh
Usage: deicode_rpca [OPTIONS]

Runs RPCA with an rclr preprocessing step

Options:
--in_biom TEXT              Input table in biom format.
--output_dir TEXT           Location of output files.
--min_sample_depth INTEGER  Minimum Sample Sequencing Depth Cut Off
                            default=500
--help                      Show this message and exit.

Usage: deicode_log_ratio [OPTIONS]

  Runs log ratios on import features from RPCA output

Options:
  --in_biom TEXT       Input table in biom format. (optional taxa in
                       observation)
  --in_map TEXT        Input metadata in qiime stype format.
  --in_ord TEXT        RPCA output RPCA_Ordination.txt
  --output_dir TEXT    Location of output files.
  --axis INTEGER       Axis of both ordinations to use default=0
  --n_lr INTEGER       Number of log-ratios to comput default=10
  --tax_level INTEGER  If taxa included - choose level default=lowest
  --help               Show this message and exit.
```

Python
```python

from deicode.optspace import OptSpace
from deicode.preprocessing import rclr
import numpy as np

# rclr preprocessing

# numpy.ndarray - a array of counts (samples,features) with shape (M,N) where N>M
table=np.array([[3, 3, 0], [0, 4, 2], [3, 0, 1]]) 
table_rclr=rclr().fit_transform(table)

# OptSpace (RPCA)

opt=OptSpace().fit(table_rclr)
U=opt.sample_weights # numpy.ndarray - "Sample Loadings" 
V=opt.feature_weights # numpy.ndarray - "Feature Loadings" 
s=opt.s # numpy.ndarray - The singular values

# or directly transform

U,s,V=OptSpace().fit_transform(table_rclr)

```

## Simulation Benchmarking

[simulations](https://github.com/cameronmartino/DEICODE/blob/master/Benchmarking/simulations/simulations.ipynb)
[case studies](https://github.com/cameronmartino/DEICODE/blob/master/Benchmarking/case_studies/case_studies.ipynb)

## Other Resources

The code for OptSpace was translated to python from a [MATLAB package](http://swoh.web.engr.illinois.edu/software/optspace/code.html) maintained by Sewoong Oh (UIUC).

- Transforms and PCoA : [Scikit-bio](https://github.com/biocore/scikit-bio)
- Data For Examples : [Qiita](https://qiita.ucsd.edu/)
