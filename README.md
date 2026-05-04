## Introduction

HiDeF is a method for robustly resolving the hierarchical structures of networks based on multiscale community detection and the concepts of persistent homology. 

HiDeF is described in the following manuscript:  

Zheng, F., Zhang, S., Churas, C. et al., [HiDeF: identifying persistent structures in multiscale ‘omics data](https://doi.org/10.1186/s13059-020-02228-4). Genome Biol 22, 21 (2021).

## Installation 

Clone / download the repository and use `uv sync` to install the dependencies. The *pyproject.toml* file indicates the dependencies and versions of the packages needed for hidef to run correctly.

## Repo structure

- Directories for hidef_*.ipynb runs: 
    - `disease_seeds`: Some input files with seed genes for a bunch of diseases downloaded from DisGeNET.
    - `example_ppi`: Some example ppi files to use as input when running hidef
    - `output_examples`: Intended as the directory for storing hidef run outputs.

## Usage

### Running HiDeF as a command-line tool

First, install the package as instructed above.

The repo is organized so HiDeF can be used is used as a command-line tool.

To sweep the resolution profile and generate an optimized hierarchy based on pan-resolution community persistence, run a command like this in a terminal, inside the repo directory: 

`uv run python hidef/hidef_finder.py --g example_ppi/chloe_ppi.tsv --o output_examples/test_run_1_ --k 10 --minres 0.001 --maxres 200 --numthreads 20`

- `--g"`: the input graph file, with no headers
- `--o`: output file prefix
- `--minres`: Starting modularity resolution value for sweeping process
- `--maxres`: Maximum of resolution to be explored
- `--k`: Denotes a threshold for considering a community as persistent across the sweep. The higher the value, less persistent communities will be found (more strict). Normally, increasing the maximum resolution would mean for searching for a new k value as more community structures are analyzed and therefore the percentage of persistence changes. Low values may render interactions between same level communities as a result of a *too relaxed* criterion, which should not be allowed. If this happens increase k. After a number of tests k=10 emerged as a good equlibrium point for max_resolution 200.
- `--numthreads`: cpu count for Parallel processing

Other auxiliary parameters are explained in the manuscript.

You have output files for runs between 0.001 and 200 with k= 5, 10 and 20 in the `output_examples` repo.

#### Outputs
- `$out.nodes`: A TSV file describing the content (nodes in the input network) of each community. The last column of this file contains the persistence of each community.  
- `$out.edges`: A TSV file describing the parent-child relationships of communities in the hierarchy. The parent communities are in the 1st column and the children communities are in the 2nd column.  
- `$out.gml`: A file in the GML format that can be opened in Cytoscape to visualize the hierarchy (using "yFiles hierarchic layout" in Cytoscape)

This output files are afterwards used for 

### Analysing disease data over the hierarchy structure

The disease specific notebooks analyse the disease information across the hierarchy. Basically, imports the relevant hidef output files, identify clusters of the hiearchy with disease genes, performs a fisher test to identify significantly enriched persistent communities and provides simple enrichr GSEA for those communities.
