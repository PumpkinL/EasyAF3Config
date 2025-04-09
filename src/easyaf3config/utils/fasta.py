"""
Utilities for working with FASTA files.
"""

from pathlib import Path
from typing import List, Union

from Bio import SeqIO

from easyaf3config.core.config import AfJobConfig, Dialect, Version
from easyaf3config.core.sequence import ProteinSequence


def load_sequences_from_fasta(fasta_path: Union[str, Path]) -> List[ProteinSequence]:
    """
    Load sequences from a FASTA file and convert them to ProteinSequence objects.
    
    Args:
        fasta_path: Path to the FASTA file
        
    Returns:
        List[ProteinSequence]: List of protein sequence objects
    
    Raises:
        ValueError: When a sequence contains invalid characters
        FileNotFoundError: When the file does not exist
    """
    sequences = []
    
    # Ensure file path is a Path object
    fasta_path = Path(fasta_path)
    
    if not fasta_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {fasta_path}")
    
    # Count total sequences for progress reporting
    total_sequences = sum(1 for _ in SeqIO.parse(str(fasta_path), "fasta"))
    
    # Read FASTA file
    for i, record in enumerate(SeqIO.parse(str(fasta_path), "fasta")):
        print(f"Processing sequence {i+1} of {total_sequences}")
        
        # Create ProteinSequence object
        protein_seq = ProteinSequence(
            id=record.id if record.id else f"seq_{i+1}",
            sequence=str(record.seq)
        )
        sequences.append(protein_seq)
    
    return sequences


def create_job_config_from_fasta(
    fasta_path: Union[str, Path],
    job_name: str,
    model_seeds: List[int] = None,
    dialect: str = "alphafold3",
    version: int = 1
) -> AfJobConfig:
    """
    Create a complete job configuration from a FASTA file.
    
    Args:
        fasta_path: Path to the FASTA file
        job_name: Job name
        model_seeds: List of model seeds, defaults to [1]
        dialect: Model dialect, defaults to "alphafold3"
        version: Configuration version, defaults to 1
        
    Returns:
        AfJobConfig: Job configuration object
    """
    # Set default model_seeds
    if model_seeds is None:
        model_seeds = [1]
    
    # Load sequences
    sequences = load_sequences_from_fasta(fasta_path)
    
    # Create job configuration
    job_config = AfJobConfig(
        name=job_name,
        modelSeeds=model_seeds,
        sequences=sequences,
        dialect=dialect,
        version=version
    )
    
    return job_config
