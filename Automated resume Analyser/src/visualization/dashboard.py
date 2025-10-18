"""
Visualization dashboard for resume analysis results
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class ResultsVisualizer:
    def __init__(self):
        """Initialize the visualizer with default styles"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def plot_score_distribution(self, results_df):
        """Plot distribution of match scores"""
        plt.figure(figsize=(10, 6))
        plt.hist(results_df['match_score'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Candidate Match Scores')
        plt.xlabel('Match Score (%)')
        plt.ylabel('Number of Candidates')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('score_distribution.png')
        plt.show()
    
    def plot_top_candidates(self, results_df, top_n=10):
        """Plot top N candidates by match score"""
        top_candidates = results_df.nlargest(top_n, 'match_score')
        
        plt.figure(figsize=(12, 8))
        bars = plt.barh(range(len(top_candidates)), top_candidates['match_score'], color='lightgreen')
        plt.yticks(range(len(top_candidates)), top_candidates['candidate'])
        plt.xlabel('Match Score (%)')
        plt.title(f'Top {top_n} Candidates by Match Score')
        plt.gca().invert_yaxis()  # Highest score at top
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{width:.1f}%', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig('top_candidates.png')
        plt.show()
    
    def plot_skills_coverage(self, results_data):
        """Plot skills coverage analysis"""
        # This would require detailed skills data from the analysis
        # Implementation would depend on how skills are stored
        pass
    
    def generate_summary_report(self, results_df):
        """Generate a summary statistics report"""
        summary = {
            'total_candidates': len(results_df),
            'average_score': results_df['match_score'].mean(),
            'median_score': results_df['match_score'].median(),
            'highest_score': results_df['match_score'].max(),
            'lowest_score': results_df['match_score'].min(),
            'std_deviation': results_df['match_score'].std()
        }
        
        print("SUMMARY STATISTICS")
        print("=" * 30)
        for key, value in summary.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        return summary

def create_dashboard(results_file):
    """Create a dashboard from results file"""
    try:
        df = pd.read_csv(results_file)
        visualizer = ResultsVisualizer()
        
        # Generate summary report
        summary = visualizer.generate_summary_report(df)
        
        # Create visualizations
        visualizer.plot_score_distribution(df)
        visualizer.plot_top_candidates(df)
        
        print("\nDashboard generated successfully!")
        print("Files created:")
        print("- score_distribution.png")
        print("- top_candidates.png")
        
    except Exception as e:
        print(f"Error creating dashboard: {e}")

if __name__ == "__main__":
    # Example usage
    # create_dashboard('candidate_ranking.csv')
    pass