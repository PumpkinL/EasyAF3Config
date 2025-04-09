"""
Configuration classes for AlphaFold3 jobs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from easyaf3config.core.sequence import DNASequence, ProteinSequence, RNASequence, Sequence


class Dialect(str, Enum):
    """
    Supported model dialects.
    """
    ALPHAFOLD3 = "alphafold3"


class Version(int, Enum):
    """
    Supported configuration versions.
    """
    V1 = 1
    V2 = 2


@dataclass
class AfJobConfig:
    """
    AlphaFold job configuration.
    
    Attributes:
        name: Job name
        modelSeeds: List of model seeds to use
        sequences: List of sequences to process
        dialect: Model dialect to use
        version: Configuration version
        bondedAtomPairs: Optional list of bonded atom pairs
        userCCD: Optional user-defined chemical component dictionary
    """
    name: str
    modelSeeds: List[int]
    sequences: List[Sequence]
    dialect: Dialect
    version: Version = field(default=Version.V2)
    bondedAtomPairs: Optional[List[Any]] = field(default=None)
    userCCD: Optional[str] = field(default=None)

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.name:
            raise ValueError("Job name is required")
        
        if not self.modelSeeds or len(self.modelSeeds) < 1:
            raise ValueError("At least one model seed is required")
            
        if not self.sequences:
            raise ValueError("At least one sequence is required")
            
        if isinstance(self.version, int):
            try:
                self.version = Version(self.version)
            except ValueError:
                raise ValueError(f"Unsupported version: {self.version}. Supported versions are {[v.value for v in Version]}")
            
        if isinstance(self.dialect, str):
            try:
                self.dialect = Dialect(self.dialect)
            except ValueError:
                raise ValueError(f"Unsupported dialect: {self.dialect}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the job configuration to a dictionary representation."""
        result = {
            "name": self.name,
            "modelSeeds": self.modelSeeds,
            "sequences": [
                seq.to_dict() for seq in self.sequences
            ],
            "dialect": self.dialect.value,
            "version": self.version.value
        }
        
        if self.bondedAtomPairs is not None:
            result["bondedAtomPairs"] = self.bondedAtomPairs
        if self.userCCD is not None:
            result["userCCD"] = self.userCCD
            
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'AfJobConfig':
        """Create an AfJobConfig object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")
        
        # Process sequences field
        sequences = []
        sequences_data = data.get('sequences', [])
        
        # sequences field must be a list
        if not isinstance(sequences_data, list):
            raise ValueError("sequences must be a list")
        
        # Map sequence types to corresponding classes
        sequence_types = {
            "protein": ProteinSequence,
            "rna": RNASequence,
            "dna": DNASequence,
        }
        
        # Process each sequence data
        for seq_data in sequences_data:
            # Validate sequence data is a dictionary
            if not isinstance(seq_data, dict):
                raise ValueError(f"Invalid sequence data format: {seq_data}")
                
            # Iterate through each type key-value pair in sequence data
            for seq_type, seq_content in seq_data.items():
                # Get corresponding sequence class
                sequence_class = sequence_types.get(seq_type.lower())
                if not sequence_class:
                    raise ValueError(f"Unsupported sequence type: {seq_type}")
                
                # Create sequence instance and add to list
                try:
                    sequence = sequence_class(
                        id=seq_content.get('id'),
                        sequence=seq_content.get('sequence'),
                        modifications=seq_content.get('modifications'),
                        unpairedMsa=seq_content.get('unpairedMsa'),
                        unpairedMsaPath=seq_content.get('unpairedMsaPath'),
                        pairedMsa=seq_content.get('pairedMsa'),
                        pairedMsaPath=seq_content.get('pairedMsaPath'),
                        templates=seq_content.get('templates')
                    )
                    sequences.append(sequence)
                except Exception as e:
                    raise ValueError(f"Failed to create {seq_type} sequence: {str(e)}")
        
        return cls(
            name=data.get('name'),
            modelSeeds=data.get('modelSeeds', []),
            sequences=sequences,
            dialect=data.get('dialect'),
            version=data.get('version', Version.V2),
            bondedAtomPairs=data.get('bondedAtomPairs'),
            userCCD=data.get('userCCD')
        )

    def __repr__(self):
        return str(self.to_dict())
