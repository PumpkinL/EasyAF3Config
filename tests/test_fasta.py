"""Tests for FASTA utilities."""

import os
import tempfile
from pathlib import Path

import pytest

from easyaf3config.core.config import AfJobConfig
from easyaf3config.core.sequence import ProteinSequence
from easyaf3config.utils.fasta import create_job_config_from_fasta, load_sequences_from_fasta


@pytest.fixture
def sample_fasta_file():
    """Create a temporary FASTA file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".fasta", delete=False) as tmp:
        tmp.write(b">seq1\nACDEFGHIKL\n>seq2\nMNPQRSTVWY\n")
        tmp_path = tmp.name

    yield tmp_path

    # Clean up
    os.unlink(tmp_path)


def test_load_sequences_from_fasta(sample_fasta_file):
    """Test loading sequences from a FASTA file."""
    sequences = load_sequences_from_fasta(sample_fasta_file)

    assert len(sequences) == 2
    assert isinstance(sequences[0], ProteinSequence)
    assert isinstance(sequences[1], ProteinSequence)

    assert sequences[0].id == "seq1"
    assert sequences[0].sequence == "ACDEFGHIKL"
    assert sequences[1].id == "seq2"
    assert sequences[1].sequence == "MNPQRSTVWY"

    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        load_sequences_from_fasta("non_existent_file.fasta")


def test_create_job_config_from_fasta(sample_fasta_file):
    """Test creating a job config from a FASTA file."""
    job_config = create_job_config_from_fasta(
        fasta_path=sample_fasta_file,
        job_name="test_job",
        model_seeds=[42],
        dialect="alphafold3",
        version=1
    )

    assert isinstance(job_config, AfJobConfig)
    assert job_config.name == "test_job"
    assert job_config.modelSeeds == [42]
    assert len(job_config.sequences) == 2
    assert job_config.dialect.value == "alphafold3"
    assert job_config.version.value == 1

    # Test with default values
    job_config = create_job_config_from_fasta(
        fasta_path=sample_fasta_file,
        job_name="test_job"
    )

    assert job_config.modelSeeds == [1]  # Default model seed
    assert job_config.dialect.value == "alphafold3"  # Default dialect
    assert job_config.version.value == 1  # Default version
