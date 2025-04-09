"""Tests for config module."""

import pytest

from easyaf3config.core.config import AfJobConfig, Dialect, Version
from easyaf3config.core.sequence import ProteinSequence


def test_dialect_enum():
    """Test Dialect enum."""
    assert Dialect.ALPHAFOLD3 == "alphafold3"
    assert Dialect("alphafold3") == Dialect.ALPHAFOLD3

    # Test invalid dialect
    with pytest.raises(ValueError):
        Dialect("invalid_dialect")


def test_version_enum():
    """Test Version enum."""
    assert Version.V1 == 1
    assert Version.V2 == 2
    assert Version(1) == Version.V1

    # Test invalid version
    with pytest.raises(ValueError):
        Version(3)


def test_af_job_config():
    """Test AfJobConfig class."""
    # Create test sequences
    seq1 = ProteinSequence(id="seq1", sequence="ACDEFG")
    seq2 = ProteinSequence(id="seq2", sequence="HIJKLM")

    # Create job config
    job_config = AfJobConfig(
        name="test_job",
        modelSeeds=[1, 2, 3],
        sequences=[seq1, seq2],
        dialect=Dialect.ALPHAFOLD3,
        version=Version.V1
    )

    assert job_config.name == "test_job"
    assert job_config.modelSeeds == [1, 2, 3]
    assert len(job_config.sequences) == 2
    assert job_config.dialect == Dialect.ALPHAFOLD3
    assert job_config.version == Version.V1

    # Test to_dict method
    config_dict = job_config.to_dict()
    assert config_dict["name"] == "test_job"
    assert config_dict["modelSeeds"] == [1, 2, 3]
    assert len(config_dict["sequences"]) == 2
    assert config_dict["dialect"] == "alphafold3"
    assert config_dict["version"] == 1

    # Test validation
    with pytest.raises(ValueError):
        AfJobConfig(
            name="",  # Empty name should raise error
            modelSeeds=[1],
            sequences=[seq1],
            dialect=Dialect.ALPHAFOLD3
        )

    with pytest.raises(ValueError):
        AfJobConfig(
            name="test_job",
            modelSeeds=[],  # Empty model seeds should raise error
            sequences=[seq1],
            dialect=Dialect.ALPHAFOLD3
        )

    with pytest.raises(ValueError):
        AfJobConfig(
            name="test_job",
            modelSeeds=[1],
            sequences=[],  # Empty sequences should raise error
            dialect=Dialect.ALPHAFOLD3
        )
