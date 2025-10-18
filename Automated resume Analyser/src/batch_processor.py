"""
Batch processing script for analyzing multiple resumes
"""
import os
import sys
import argparse
from main import analyze_resumes_from_directory

def main():
    parser = argparse.ArgumentParser(description="Automated Resume Analysis System - Batch Processor")
    parser.add_argument("--resumes-dir", required=True, help="Directory containing resume files")
    parser.add_argument("--job-description", required=True, help="Path to job description file")
    parser.add_argument("--output", default="results.csv", help="Output file for results")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.resumes_dir):
        print(f"Error: Resumes directory '{args.resumes_dir}' does not exist.")
        sys.exit(1)
    
    if not os.path.exists(args.job_description):
        print(f"Error: Job description file '{args.job_description}' does not exist.")
        sys.exit(1)
    
    print("Automated Resume Analysis System - Batch Processor")
    print("=" * 50)
    print(f"Resumes Directory: {args.resumes_dir}")
    print(f"Job Description: {args.job_description}")
    print(f"Output File: {args.output}")
    print("=" * 50)
    
    try:
        results = analyze_resumes_from_directory(args.resumes_dir, args.job_description)
        print(f"\nProcessing complete. Results saved to {args.output}")
    except Exception as e:
        print(f"Error during processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()