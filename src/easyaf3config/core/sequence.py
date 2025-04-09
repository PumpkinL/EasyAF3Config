"""
Sequence classes for representing protein, DNA, and RNA sequences.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class Modification:
    """
    Represents a post-translational modification (PTM) on a sequence.
    
    Attributes:
        ptmType: The type of post-translational modification
        ptmPosition: The position of the modification in the sequence (1-indexed)
    """
    ptmType: str
    ptmPosition: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the modification to a dictionary representation."""
        return {
            "ptmType": self.ptmType,
            "ptmPosition": self.ptmPosition
        }
    
    def __repr__(self):
        return str(self.to_dict())


@dataclass
class Sequence:
    """
    Base class for biological sequences.
    
    Attributes:
        id: Unique identifier for the sequence
        sequence: The actual sequence string
        type: The type of sequence (protein, dna, or rna) - set automatically
        modifications: Optional list of post-translational modifications
        unpairedMsa: Optional unpaired multiple sequence alignment
        unpairedMsaPath: Optional path to unpaired MSA file
        pairedMsa: Optional paired multiple sequence alignment
        pairedMsaPath: Optional path to paired MSA file
        templates: Optional templates for structure prediction
    """
    id: str = field()
    sequence: str = field()
    type: str = field(init=False)  # type field is set automatically
    modifications: Optional[List[Modification]] = field(default=None)
    unpairedMsa: Optional[str] = field(default=None)
    unpairedMsaPath: Optional[Union[str, Path]] = field(default=None)
    pairedMsa: Optional[str] = field(default=None)
    pairedMsaPath: Optional[Union[str, Path]] = field(default=None)
    templates: Optional[dict] = field(default=None)

    def __post_init__(self):
        """Initialize after dataclass initialization."""
        self.type = self._get_type()  # Set type after initialization
        self._validate_fields()
        self._process_modifications()

    def _validate_fields(self):
        """Validate required fields and field combinations."""
        if not all([self.type, self.id, self.sequence]):
            raise ValueError("type, id, and sequence are required fields")
        
        if self.unpairedMsa and self.unpairedMsaPath:
            raise ValueError("unpairedMsa and unpairedMsaPath are mutually exclusive")
        if self.pairedMsa and self.pairedMsaPath:
            raise ValueError("pairedMsa and pairedMsaPath are mutually exclusive")
        
        self._validate_sequence()

    def _validate_sequence(self):
        """Validate sequence format - implemented by subclasses."""
        pass

    def _process_modifications(self):
        """Process modifications field to ensure all items are Modification objects."""
        if isinstance(self.modifications, list):
            self.modifications = [
                mod if isinstance(mod, Modification)
                else Modification(**mod)
                for mod in self.modifications
            ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the sequence to a dictionary representation."""
        result = {
            self.type: {
                "id": self.id,
                "sequence": self.sequence
            }
        }
        
        if self.modifications:
            result[self.type]["modifications"] = [
                mod.to_dict() for mod in self.modifications
            ]
            
        for field_name in ["unpairedMsa", "unpairedMsaPath", 
                          "pairedMsa", "pairedMsaPath", "templates"]:
            value = getattr(self, field_name)
            if value is not None:
                result[self.type][field_name] = value
                
        return result

    def __repr__(self):
        return str(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> 'Sequence':
        """Create a Sequence object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Input must be a dictionary")
        
        # Get sequence type (protein, dna, or rna)
        sequence_type = cls._get_type()
        
        # Get data for the corresponding type
        type_data = data.get(sequence_type)
        if not type_data:
            raise ValueError(f"Invalid format: missing '{sequence_type}' key")
        
        # Check required fields
        if 'id' not in type_data or 'sequence' not in type_data:
            raise ValueError("Missing required fields: 'id' and 'sequence' are required")
        
        return cls(
            id=type_data.get('id'),
            sequence=type_data.get('sequence'),
            modifications=type_data.get('modifications'),
            unpairedMsa=type_data.get('unpairedMsa'),
            unpairedMsaPath=type_data.get('unpairedMsaPath'),
            pairedMsa=type_data.get('pairedMsa'),
            pairedMsaPath=type_data.get('pairedMsaPath'),
            templates=type_data.get('templates')
        )

    @classmethod
    def _get_type(cls) -> str:
        """Get sequence type - implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement _get_type()")


@dataclass
class ProteinSequence(Sequence):
    """
    Protein sequence class.
    
    Validates that the sequence contains only valid amino acid characters.
    """
    def _validate_sequence(self):
        """Validate protein sequence."""
        valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")
        if not all(aa in valid_amino_acids for aa in self.sequence.upper()):
            raise ValueError("Invalid protein sequence: contains invalid amino acids")

    @classmethod
    def _get_type(cls) -> str:
        return "protein"


@dataclass
class DNASequence(Sequence):
    """
    DNA sequence class.
    
    Validates that the sequence contains only valid DNA nucleotide characters.
    """
    def _validate_sequence(self):
        """Validate DNA sequence."""
        valid_nucleotides = set("ATCG")
        if not all(nt in valid_nucleotides for nt in self.sequence.upper()):
            raise ValueError("Invalid DNA sequence: contains invalid nucleotides")

    @classmethod
    def _get_type(cls) -> str:
        return "dna"


@dataclass
class RNASequence(Sequence):
    """
    RNA sequence class.
    
    Validates that the sequence contains only valid RNA nucleotide characters.
    """
    def _validate_sequence(self):
        """Validate RNA sequence."""
        valid_nucleotides = set("AUCG")
        if not all(nt in valid_nucleotides for nt in self.sequence.upper()):
            raise ValueError("Invalid RNA sequence: contains invalid nucleotides")

    @classmethod
    def _get_type(cls) -> str:
        return "rna"
