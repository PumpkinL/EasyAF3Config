"""
EasyAF3Config - A tool to easily create and manage AlphaFold3 configuration files.
"""

__version__ = "0.1.0"

# Import core classes for easy access
from easyaf3config.core.config import AfJobConfig, Dialect, Version
from easyaf3config.core.sequence import (DNASequence, Modification, ProteinSequence,
                                        RNASequence, Sequence)
from easyaf3config.utils.fasta import create_job_config_from_fasta, load_sequences_from_fasta

__all__ = [
    "AfJobConfig",
    "Dialect",
    "Version",
    "Sequence",
    "ProteinSequence",
    "DNASequence",
    "RNASequence",
    "Modification",
    "load_sequences_from_fasta",
    "create_job_config_from_fasta",
]
