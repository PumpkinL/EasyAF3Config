# EasyAF3Config

A Python library for easily creating and managing AlphaFold3 configuration files.

## Installation

```bash
git clone https://github.com/PumpkinL/EasyAF3Config.git
cd EasyAF3Config
pip install .
```

## Usage

### Command Line Interface

EasyAF3Config provides command-line tools for working with AlphaFold3 configurations:

```bash
# Convert a FASTA file to AlphaFold3 compatible JSON
fa2json --fasta input.fasta --json output.json
```

### Python API

```python
from easyaf3config.core.config import AfJobConfig
from easyaf3config.utils.fasta import create_job_config_from_fasta

# Create a job configuration from a FASTA file
job_config = create_job_config_from_fasta(
    fasta_path="input.fasta",
    job_name="my_job",
    model_seeds=[5311],
    dialect="alphafold3",
    version=1
)

# Convert to dictionary and save as JSON
import json
with open("output.json", "w") as f:
    json.dump(job_config.to_dict(), f, indent=4)
```

## Features

- Convert FASTA files to AlphaFold3 compatible JSON format
- Support for protein, DNA, and RNA sequences
- Customizable job configuration
- Command line interface for easy use
- More features coming soon!

## License

MIT
