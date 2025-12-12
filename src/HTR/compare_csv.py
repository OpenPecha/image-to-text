import pandas as pd
import argparse
import sys
from pathlib import Path


def read_csv_file(file_path):
    """Read CSV file and return DataFrame with id and transcript columns."""
    try:
        df = pd.read_csv(file_path)
        
        # Check if required columns exist
        required_columns = ['id', 'transcript']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing columns {missing_columns} in file {file_path}")
            print(f"Available columns: {list(df.columns)}")
            return None
        
        # Select only id and transcript columns
        return df[['id', 'transcript']].copy()
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None


def compare_csv_files(file1_path, file2_path):
    """Compare two CSV files on id and transcript columns."""
    print(f"Comparing files:")
    print(f"File 1: {file1_path}")
    print(f"File 2: {file2_path}")
    print("-" * 50)
    
    # Read both files
    df1 = read_csv_file(file1_path)
    df2 = read_csv_file(file2_path)
    
    if df1 is None or df2 is None:
        return False
    
    # Basic statistics
    print(f"File 1 records: {len(df1)}")
    print(f"File 2 records: {len(df2)}")
    print("-" * 50)
    
    # Remove duplicates and sort for comparison
    df1_clean = df1.drop_duplicates().sort_values('id').reset_index(drop=True)
    df2_clean = df2.drop_duplicates().sort_values('id').reset_index(drop=True)
    
    # Find records only in file1
    only_in_file1 = df1_clean[~df1_clean['id'].isin(df2_clean['id'])]
    
    # Find records only in file2
    only_in_file2 = df2_clean[~df2_clean['id'].isin(df1_clean['id'])]
    
    # Find common IDs
    common_ids = set(df1_clean['id']).intersection(set(df2_clean['id']))
    
    # Find records with same ID but different transcript
    different_transcripts = []
    for id_val in common_ids:
        transcript1 = df1_clean[df1_clean['id'] == id_val]['transcript'].iloc[0]
        transcript2 = df2_clean[df2_clean['id'] == id_val]['transcript'].iloc[0]
        
        if transcript1 != transcript2:
            different_transcripts.append({
                'id': id_val,
                'transcript_file1': transcript1,
                'transcript_file2': transcript2
            })
    
    # Print results
    print(f"Records only in file 1: {len(only_in_file1)}")
    if len(only_in_file1) > 0:
        print("Sample records only in file 1:")
        print(only_in_file1.head(10).to_string(index=False))
        print()
    
    print(f"Records only in file 2: {len(only_in_file2)}")
    if len(only_in_file2) > 0:
        print("Sample records only in file 2:")
        print(only_in_file2.head(10).to_string(index=False))
        print()
    
    print(f"Records with same ID but different transcript: {len(different_transcripts)}")
    if different_transcripts:
        print("Sample records with different transcripts:")
        for i, diff in enumerate(different_transcripts[:5]):  # Show first 5
            print(f"ID: {diff['id']}")
            print(f"  File 1: {diff['transcript_file1']}")
            print(f"  File 2: {diff['transcript_file2']}")
            print()
    
    print(f"Common records with identical transcript: {len(common_ids) - len(different_transcripts)}")
    
    # Summary
    print("-" * 50)
    print("SUMMARY:")
    print(f"Total unique IDs in file 1: {len(df1_clean)}")
    print(f"Total unique IDs in file 2: {len(df2_clean)}")
    print(f"Common IDs: {len(common_ids)}")
    print(f"IDs only in file 1: {len(only_in_file1)}")
    print(f"IDs only in file 2: {len(only_in_file2)}")
    print(f"IDs with different transcripts: {len(different_transcripts)}")
    
    return True


def save_differences_to_csv(file1_path, file2_path, output_dir="comparison_results"):
    """Save comparison results to CSV files."""
    df1 = read_csv_file(file1_path)
    df2 = read_csv_file(file2_path)
    
    if df1 is None or df2 is None:
        return False
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Remove duplicates and sort
    df1_clean = df1.drop_duplicates().sort_values('id').reset_index(drop=True)
    df2_clean = df2.drop_duplicates().sort_values('id').reset_index(drop=True)
    
    # Save records only in file1
    only_in_file1 = df1_clean[~df1_clean['id'].isin(df2_clean['id'])]
    only_in_file1.to_csv(f"{output_dir}/only_in_file1.csv", index=False)
    
    # Save records only in file2
    only_in_file2 = df2_clean[~df2_clean['id'].isin(df1_clean['id'])]
    only_in_file2.to_csv(f"{output_dir}/only_in_file2.csv", index=False)
    
    # Save records with different transcripts
    common_ids = set(df1_clean['id']).intersection(set(df2_clean['id']))
    different_transcripts = []
    
    for id_val in common_ids:
        transcript1 = df1_clean[df1_clean['id'] == id_val]['transcript'].iloc[0]
        transcript2 = df2_clean[df2_clean['id'] == id_val]['transcript'].iloc[0]
        
        if transcript1 != transcript2:
            different_transcripts.append({
                'id': id_val,
                'transcript_file1': transcript1,
                'transcript_file2': transcript2
            })
    
    if different_transcripts:
        diff_df = pd.DataFrame(different_transcripts)
        diff_df.to_csv(f"{output_dir}/different_transcripts.csv", index=False)
    
    print(f"Comparison results saved to {output_dir}/ directory")
    return True


def main():
    parser = argparse.ArgumentParser(description='Compare two CSV files on id and transcript columns')
    parser.add_argument('file1', help='Path to first CSV file')
    parser.add_argument('file2', help='Path to second CSV file')
    parser.add_argument('--save-results', action='store_true', 
                       help='Save comparison results to CSV files')
    parser.add_argument('--output-dir', default='comparison_results',
                       help='Directory to save results (default: comparison_results)')
    
    args = parser.parse_args()
    
    # Check if files exist
    if not Path(args.file1).exists():
        print(f"Error: File {args.file1} does not exist")
        sys.exit(1)
    
    if not Path(args.file2).exists():
        print(f"Error: File {args.file2} does not exist")
        sys.exit(1)
    
    # Compare files
    success = compare_csv_files(args.file1, args.file2)
    
    if success and args.save_results:
        save_differences_to_csv(args.file1, args.file2, args.output_dir)


if __name__ == "__main__":
    main()
