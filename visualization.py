#!/usr/bin/env python3
"""
Create crystal clear visualization for Diff Algorithm Analysis - Final Version
Professional academic styling with formal presentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_final_clear_visualization():
    """Create the clearest possible visualization from the dataset."""
    
    # Read the dataset
    print("Loading dataset...")
    df = pd.read_csv('dataset.csv')
    print(f"Loaded {len(df):,} records")
    
    # Set professional, formal style
    plt.style.use('classic')
    plt.rcParams.update({
        'font.size': 14,
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'figure.titlesize': 18,
        'font.family': 'serif'
    })
    
    # Create a simple 2x2 layout with more space
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(24, 20))
    fig.suptitle('Git Diff Algorithm Comparison\nMyers vs Histogram Algorithm Analysis', 
                fontsize=18, fontweight='bold', y=0.96)
    
    # Plot 1: Overall Agreement - Simple and Clear
    discrepancy_counts = df['discrepancy'].value_counts()
    agreement_count = discrepancy_counts.get('No', 0)
    disagreement_count = discrepancy_counts.get('Yes', 0)
    total = agreement_count + disagreement_count
    
    agreement_pct = (agreement_count / total * 100) if total > 0 else 0
    disagreement_pct = (disagreement_count / total * 100) if total > 0 else 0
    
    colors = ['#708090', '#B22222']  # Slate Gray for Agreement, Fire Brick for Disagreement
    sizes = [agreement_count, disagreement_count]
    labels = [f'Agreement\n{agreement_count:,} files\n{agreement_pct:.1f}%',
              f'Disagreement\n{disagreement_count:,} files\n{disagreement_pct:.1f}%']
    
    if disagreement_count > 0:
        wedges, texts = ax1.pie(sizes, labels=labels, colors=colors,
                               startangle=90, labeldistance=1.1,
                               textprops={'fontsize': 12})
    else:
        ax1.pie([agreement_count], labels=[f'Perfect Agreement\n{agreement_count:,} files\n100.0%'],
               colors=[colors[0]], textprops={'fontsize': 12})
    
    ax1.set_title('Algorithm Agreement Distribution', fontweight='bold', pad=20, fontsize=16)
    
    # Plot 2: Repository Comparison - Clear Bar Chart
    repo_data = []
    for repo in sorted(df['repository'].unique()):
        repo_df = df[df['repository'] == repo]
        total = len(repo_df)
        disagreements = len(repo_df[repo_df['discrepancy'] == 'Yes'])
        rate = (disagreements / total * 100) if total > 0 else 0
        repo_data.append({'repo': repo.upper(), 'rate': rate, 'total': total, 'disagreements': disagreements})
    
    repo_names = [d['repo'] for d in repo_data]
    repo_rates = [d['rate'] for d in repo_data]
    
    bars = ax2.bar(repo_names, repo_rates, 
                   color=['#778899', '#2F4F4F', '#696969'],  # Light Slate Gray, Dark Slate Gray, Dim Gray
                   edgecolor='black', linewidth=3, width=0.6)
    
    ax2.set_title('Disagreement Rate by Repository', fontweight='bold', pad=20, fontsize=16)
    ax2.set_ylabel('Disagreement Rate (%)', fontweight='bold', fontsize=18)
    ax2.set_xlabel('Repository', fontweight='bold', fontsize=18)
    
    # Add clear value labels on bars
    for bar, data in zip(bars, repo_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(repo_rates)*0.01,
                f'{height:.2f}%\n({data["disagreements"]:,} of {data["total"]:,})', 
                ha='center', va='bottom', fontsize=12)
    
    ax2.set_ylim(0, max(repo_rates) * 1.2)
    ax2.grid(True, alpha=0.2)
    
    # Plot 3: File Type Analysis - Horizontal bars for clarity
    file_type_stats = []
    for ft in df['file_type'].unique():
        ft_df = df[df['file_type'] == ft]
        total = len(ft_df)
        disagreements = len(ft_df[ft_df['discrepancy'] == 'Yes'])
        rate = (disagreements / total * 100) if total > 0 else 0
        if total >= 10:  # Only include file types with sufficient data
            file_type_stats.append({
                'file_type': ft.upper(),
                'total': total,
                'disagreements': disagreements,
                'rate': rate
            })
    
    ft_df = pd.DataFrame(file_type_stats).sort_values('rate', ascending=True)
    
    colors_ft = plt.cm.viridis(np.linspace(0, 1, len(ft_df)))
    bars = ax3.barh(ft_df['file_type'], ft_df['rate'], 
                    color='#696969',  # Dim Gray
                    edgecolor='black', linewidth=1.0)
    
    ax3.set_title('Disagreement Rate by File Type', fontweight='bold', pad=20, fontsize=16)
    ax3.set_xlabel('Disagreement Rate (%)', fontsize=14)
    ax3.set_ylabel('File Type', fontsize=14)
    
    # Add value labels
    for i, (bar, row) in enumerate(zip(bars, ft_df.itertuples())):
        width = bar.get_width()
        ax3.text(width + max(ft_df['rate'])*0.02, bar.get_y() + bar.get_height()/2.,
                f'{width:.2f}% ({row.disagreements:,}/{row.total:,})', 
                ha='left', va='center', fontsize=12)
    
    ax3.set_xlim(0, max(ft_df['rate']) * 1.3)
    ax3.grid(True, alpha=0.2, axis='x')
    
    # Plot 4: Key Statistics Summary
    ax4.axis('off')
    
    # Calculate comprehensive statistics
    total_files = len(df)
    total_disagreements = len(df[df['discrepancy'] == 'Yes'])
    overall_agreement_rate = ((total_files - total_disagreements) / total_files * 100) if total_files > 0 else 0
    overall_disagreement_rate = (total_disagreements / total_files * 100) if total_files > 0 else 0
    
    # Find best and worst performers
    best_repo = min(repo_data, key=lambda x: x['rate'])
    worst_repo = max(repo_data, key=lambda x: x['rate'])
    
    # Most/least problematic file types
    if file_type_stats:
        best_ft = min(file_type_stats, key=lambda x: x['rate'])
        worst_ft = max(file_type_stats, key=lambda x: x['rate'])
    else:
        best_ft = worst_ft = {'file_type': 'N/A', 'rate': 0}
    
    # Create comprehensive summary
    summary_text = f"""Analysis Results Summary

Dataset Overview:
• Total Files Analyzed: {total_files:,}
• Algorithm Disagreements: {total_disagreements:,}
• Overall Agreement Rate: {overall_agreement_rate:.2f}%
• Overall Disagreement Rate: {overall_disagreement_rate:.2f}%

Repository Performance:
• Best Agreement: {best_repo['repo']} ({best_repo['rate']:.2f}% disagreement)
• Most Disagreements: {worst_repo['repo']} ({worst_repo['rate']:.2f}% disagreement)

File Type Analysis:
• Most Problematic: {worst_ft['file_type']} ({worst_ft['rate']:.2f}% disagreement)
• Most Reliable: {best_ft['file_type']} ({best_ft['rate']:.2f}% disagreement)

Key Findings:
• {overall_agreement_rate:.1f}% of files show identical diff outputs
• Disagreements indicate different algorithmic strategies
• Both Myers and Histogram algorithms are functionally correct
• Choice depends on specific use cases and requirements"""
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes, fontsize=12,
            verticalalignment='top', fontfamily='serif',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.3))
    
    # Adjust layout with more top margin to avoid title overlap
    plt.tight_layout()
    plt.subplots_adjust(top=0.90, hspace=0.4, wspace=0.25)
    
    # Save with maximum quality
    plt.savefig('Figure_1.png', dpi=300, bbox_inches='tight', 
               facecolor='white', edgecolor='none', format='png')
    print("Visualization saved as 'Figure_1.png'")
    
    
    # Display final statistics
    print(f"\nFINAL ANALYSIS SUMMARY:")
    print(f"=" * 50)
    print(f"Total files analyzed: {total_files:,}")
    print(f"Algorithm agreements: {total_files - total_disagreements:,} ({overall_agreement_rate:.2f}%)")
    print(f"Algorithm disagreements: {total_disagreements:,} ({overall_disagreement_rate:.2f}%)")
    print(f"Most problematic file type: {worst_ft['file_type']} ({worst_ft['rate']:.2f}% disagreement)")
    print(f"Repository with most disagreements: {worst_repo['repo']} ({worst_repo['rate']:.2f}%)")
    print(f"Repository with best agreement: {best_repo['repo']} ({best_repo['rate']:.2f}% disagreement)")
    print(f"=" * 50)
    
    return df

if __name__ == "__main__":
    df = create_final_clear_visualization()
    print("\nVISUALIZATION COMPLETE!")
