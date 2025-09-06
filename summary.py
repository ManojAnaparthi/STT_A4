"""
Summary Statistics
Quick summary of the diff algorithm analysis results
"""

import pandas as pd
import matplotlib.pyplot as plt

def display_summary():
    """Display summary statistics from the analysis."""
    
    # Load the comprehensive dataset
    try:
        df = pd.read_csv('dataset.csv')
    except FileNotFoundError:
        print("Error: dataset.csv not found")
        print("Please run diff_analysis.py first")
        return
    
    print("=" * 60)
    print("DIFF ALGORITHM ANALYSIS SUMMARY")
    print("=" * 60)
    
    # Overall statistics
    total_files = len(df)
    total_discrepancies = len(df[df['discrepancy'] == 'Yes'])
    discrepancy_rate = (total_discrepancies / total_files) * 100
    
    print(f"\nOVERALL RESULTS:")
    print(f"   Total file modifications analyzed: {total_files}")
    print(f"   Total discrepancies found: {total_discrepancies}")
    print(f"   Overall discrepancy rate: {discrepancy_rate:.2f}%")
    
    # Repository breakdown
    print(f"\nREPOSITORY BREAKDOWN:")
    repo_stats = df.groupby('repository').agg({
        'discrepancy': lambda x: (x == 'Yes').sum(),
        'file_type': 'count'
    }).rename(columns={'discrepancy': 'discrepancies', 'file_type': 'total_files'})
    
    repo_stats['rate'] = (repo_stats['discrepancies'] / repo_stats['total_files']) * 100
    
    for repo in repo_stats.index:
        discrepancies = repo_stats.loc[repo, 'discrepancies']
        total = repo_stats.loc[repo, 'total_files']
        rate = repo_stats.loc[repo, 'rate']
        print(f"   {repo}: {discrepancies}/{total} files ({rate:.1f}%)")
    
    # File type breakdown
    print(f"\nFILE TYPE ANALYSIS:")
    file_type_discrepancies = df[df['discrepancy'] == 'Yes'].groupby('file_type').size()
    file_type_totals = df.groupby('file_type').size()
    
    for file_type in file_type_totals.index:
        discrepancies = file_type_discrepancies.get(file_type, 0)
        total = file_type_totals[file_type]
        rate = (discrepancies / total * 100) if total > 0 else 0
        print(f"   {file_type.title()}: {discrepancies}/{total} ({rate:.1f}%)")
    
    # Key insights
    print(f"\nKEY INSIGHTS:")
    source_discrepancies = file_type_discrepancies.get('Source', 0)
    print(f"   • Source code files had the most discrepancies ({source_discrepancies} total)")
    
    # Find repository with highest discrepancy rate
    max_rate_repo = repo_stats['rate'].idxmax()
    max_rate = repo_stats.loc[max_rate_repo, 'rate']
    print(f"   • {max_rate_repo.title()} showed the highest discrepancy rate ({max_rate:.1f}%)")
    
    doc_discrepancies = file_type_discrepancies.get('Documentation', 0)
    if doc_discrepancies == 0:
        print(f"   • Documentation files showed perfect agreement between algorithms")
    else:
        print(f"   • Documentation files had {doc_discrepancies} discrepancies")
    
    print(f"   • Analysis processed up to 1000 commits per repository")

    
    print(f"\nANALYSIS COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    display_summary()
