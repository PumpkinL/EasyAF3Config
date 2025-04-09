"""
Command-line interface for converting FASTA files to AlphaFold3 compatible JSON format.
"""

import argparse
import json
import sys
from pathlib import Path

from easyaf3config.utils.fasta import create_job_config_from_fasta


def parse_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert FASTA files to AlphaFold3 compatible JSON format"
    )
    
    parser.add_argument(
        "--fasta", 
        required=True, 
        help="Path to input FASTA file"
    )
    
    parser.add_argument(
        "--json", 
        required=True, 
        help="Path to output JSON file"
    )
    
    parser.add_argument(
        "--job-name", 
        help="Job name (defaults to FASTA filename without extension)"
    )
    
    parser.add_argument(
        "--model-seeds", 
        type=int, 
        nargs="+", 
        default=[5311], 
        help="Model seeds to use (default: 5311)"
    )
    
    parser.add_argument(
        "--dialect", 
        default="alphafold3", 
        choices=["alphafold3"], 
        help="Model dialect (default: alphafold3)"
    )
    
    parser.add_argument(
        "--version", 
        type=int, 
        default=1, 
        choices=[1, 2], 
        help="Configuration version (default: 1)"
    )
    
    return parser.parse_args(args)


def main(args=None):
    """Main entry point for the fa2json command."""
    args = parse_args(args)
    
    try:
        # Extract file paths
        fasta_path = Path(args.fasta)
        json_path = Path(args.json)
        
        # Use filename as job name if not provided
        job_name = args.job_name or fasta_path.stem
        
        print(f"Converting {fasta_path} to {json_path}")
        print(f"Job name: {job_name}")
        print(f"Model seeds: {args.model_seeds}")
        
        # Create job configuration
        af_job = create_job_config_from_fasta(
            fasta_path=fasta_path,
            job_name=job_name,
            model_seeds=args.model_seeds,
            dialect=args.dialect,
            version=args.version
        )
        
        # Save to JSON file
        with open(json_path, "w") as json_file:
            json.dump(af_job.to_dict(), json_file, indent=4)
            
        print(f"Successfully created {json_path}")
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
