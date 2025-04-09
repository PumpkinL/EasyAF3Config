"""Tests for sequence module."""

import pytest

from easyaf3config.core.sequence import (DNASequence, Modification, ProteinSequence,
                                        RNASequence, Sequence)


def test_modification():
    """Test Modification class."""
    mod = Modification(ptmType="phosphorylation", ptmPosition=42)
    assert mod.ptmType == "phosphorylation"
    assert mod.ptmPosition == 42

    # Test to_dict method
    mod_dict = mod.to_dict()
    assert mod_dict["ptmType"] == "phosphorylation"
    assert mod_dict["ptmPosition"] == 42


def test_protein_sequence():
    """Test ProteinSequence class."""
    # Valid protein sequence
    protein = ProteinSequence(id="test_protein", sequence="ACDEFGHIKLMNPQRSTVWY")
    assert protein.id == "test_protein"
    assert protein.sequence == "ACDEFGHIKLMNPQRSTVWY"
    assert protein.type == "protein"

    # Test to_dict method
    protein_dict = protein.to_dict()
    assert "protein" in protein_dict
    assert protein_dict["protein"]["id"] == "test_protein"
    assert protein_dict["protein"]["sequence"] == "ACDEFGHIKLMNPQRSTVWY"

    # Test invalid protein sequence
    with pytest.raises(ValueError):
        ProteinSequence(id="invalid", sequence="ACDEFGHIKLMNPQRSTVWYZ")


def test_dna_sequence():
    """Test DNASequence class."""
    # Valid DNA sequence
    dna = DNASequence(id="test_dna", sequence="ATCGATCG")
    assert dna.id == "test_dna"
    assert dna.sequence == "ATCGATCG"
    assert dna.type == "dna"

    # Test invalid DNA sequence
    with pytest.raises(ValueError):
        DNASequence(id="invalid", sequence="ATCGZ")


def test_rna_sequence():
    """Test RNASequence class."""
    # Valid RNA sequence
    rna = RNASequence(id="test_rna", sequence="AUCGAUCG")
    assert rna.id == "test_rna"
    assert rna.sequence == "AUCGAUCG"
    assert rna.type == "rna"

    # Test invalid RNA sequence
    with pytest.raises(ValueError):
        RNASequence(id="invalid", sequence="AUCGT")


def test_sequence_with_modifications():
    """Test Sequence with modifications."""
    mods = [
        Modification(ptmType="phosphorylation", ptmPosition=1),
        Modification(ptmType="acetylation", ptmPosition=5)
    ]

    protein = ProteinSequence(
        id="modified_protein",
        sequence="ACDEFGHIKLMNPQRSTVWY",
        modifications=mods
    )

    # Test that modifications are correctly included in to_dict
    protein_dict = protein.to_dict()
    assert "modifications" in protein_dict["protein"]
    assert len(protein_dict["protein"]["modifications"]) == 2
    assert protein_dict["protein"]["modifications"][0]["ptmType"] == "phosphorylation"
    assert protein_dict["protein"]["modifications"][1]["ptmType"] == "acetylation"
