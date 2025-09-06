"""
Diff Algorithm Analysis
Comparing Myers vs Histogram diff algorithms across three repositories
"""

import os
import subprocess
import pandas as pd
from pydriller import Repository
from tqdm import tqdm

# Repository paths
repositories = [
    ("fastapi", "/home/set-iitgn-vm/STT_A4/fastapi"),
    ("nginx", "/home/set-iitgn-vm/STT_A4/nginx"),
    ("openhands", "/home/set-iitgn-vm/STT_A4/OpenHands")
]

def get_diff(repo_dir, parent, child, path, algorithm):
    """Get git diff using specified algorithm"""
    if not parent or not path:
        return None
    
    cmd = [
        "git", "diff",
        "-w",
        "--ignore-blank-lines",
        f"--diff-algorithm={algorithm}",
        parent,
        child,
        "--",
        path
    ]
    
    try:
        result = subprocess.check_output(
            cmd,
            cwd=repo_dir,
            stderr=subprocess.STDOUT
        )
        return result.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError:
        return None

def classify_file_type(file_path):
    """Simple file type classification"""
    if not file_path:
        return "Unknown"
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.py', '.js', '.c', '.cpp', '.java', '.go', '.rs', '.php']:
        return "Source"
    elif ext in ['.md', '.txt', '.rst', '.adoc']:
        return "Documentation"
    elif ext in ['.json', '.yml', '.yaml', '.xml', '.toml', '.ini', '.cfg']:
        return "Config"
    elif ext in ['.html', '.css', '.scss']:
        return "Web"
    elif ext in ['test.py', '_test.py'] or 'test' in file_path:
        return "Test"
    else:
        return "Other"

def main():
    rows = []
    
    for repo_name, repo_path in repositories:
        print(f"\nAnalyzing {repo_name} repository...")
        
        if not os.path.exists(repo_path):
            print(f"Repository path {repo_path} does not exist, skipping...")
            continue
        
        repo = Repository(repo_path)
        commits = list(repo.traverse_commits())
        
        # Limit to 1000 commits for manageable dataset
        commits = commits[:1000]
        
        for commit in tqdm(commits, desc=f"Processing {repo_name} commits"):
            parents = commit.parents
            parent = parents[0] if parents else None
            
            if not parent:
                continue
            
            repo_dir = commit.project_path
            
            for file in commit.modified_files:
                path = file.new_path or file.old_path
                if not path:
                    continue
                
                # Get diffs using both algorithms
                diff_myers = get_diff(repo_dir, parent, commit.hash, path, "myers")
                diff_histogram = get_diff(repo_dir, parent, commit.hash, path, "histogram")
                
                if diff_myers is None or diff_histogram is None:
                    continue
                
                # Check if diffs are different
                discrepancy = "Yes" if diff_myers != diff_histogram else "No"
                
                rows.append({
                    "repository": repo_name,
                    "old_file_path": file.old_path,
                    "new_file_path": file.new_path,
                    "commit_sha": commit.hash,
                    "parent_commit_sha": parent,
                    "commit_message": commit.msg[:100] + "..." if len(commit.msg) > 100 else commit.msg,
                    "file_type": classify_file_type(path),
                    "file_extension": os.path.splitext(path)[1].lower() if path else "",
                    "diff_myers": diff_myers,
                    "diff_histogram": diff_histogram,
                    "discrepancy": discrepancy
                })
    
    # Create DataFrame and save
    df = pd.DataFrame(rows)
    df.to_csv("dataset.csv", index=False)
    
    # Print summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"Total files analyzed: {len(df):,}")
    print(f"Algorithm disagreements: {len(df[df['discrepancy'] == 'Yes']):,}")
    print(f"Agreement rate: {len(df[df['discrepancy'] == 'No']) / len(df) * 100:.2f}%")
    
    print("\nRepository breakdown:")
    for repo_name, _ in repositories:
        repo_df = df[df['repository'] == repo_name]
        if len(repo_df) > 0:
            disagreements = len(repo_df[repo_df['discrepancy'] == 'Yes'])
            print(f"  {repo_name}: {disagreements:,}/{len(repo_df):,} disagreements ({disagreements/len(repo_df)*100:.2f}%)")
    
    print(f"\nDataset saved as 'dataset.csv'")
    return df

if __name__ == "__main__":
    main()
