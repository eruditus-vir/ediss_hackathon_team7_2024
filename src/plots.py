import matplotlib.pyplot as plt
import seaborn as sns

def plot_correlation_matrices(simulated_df, tracked_df, features_to_correlate):
    """
    Plot correlation matrices for simulated and tracked datasets.

    Parameters:
    simulated_df (DataFrame): The simulated dataset DataFrame.
    tracked_df (DataFrame): The tracked dataset DataFrame.
    features_to_correlate (list): List of feature column names to correlate.
    """
    # Filter datasets based on the features to correlate
    sim_corr = simulated_df[features_to_correlate].corr()
    track_corr = tracked_df[features_to_correlate].corr()

    # Plotting
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    sns.heatmap(sim_corr, annot=True, cmap='coolwarm', ax=ax[0])
    ax[0].set_title('Correlation Matrix - Simulated Dataset')

    sns.heatmap(track_corr, annot=True, cmap='coolwarm', ax=ax[1])
    ax[1].set_title('Correlation Matrix - Tracked Dataset')

    plt.show()


import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

def compare_datasets_with_pca(df1, df2, comparison_columns, label_column=None):
    """
    Compare two datasets using PCA and visualize in 2D plot.

    Parameters:
    df1, df2 (DataFrame): The two DataFrames to compare.
    comparison_columns (list): List of columns to use for PCA.
    label_column (str, optional): Column name to use for labeling points. If None, label by dataset.

    Returns:
    None: The function plots the PCA comparison.
    """
    # Prepare the data
    df1_pca = df1[comparison_columns].copy()
    df2_pca = df2[comparison_columns].copy()
    df1_pca['Dataset'] = 'Track'
    df2_pca['Dataset'] = 'Simulation'

    # Append dataset prefix to label column if it exists
    if label_column:
        df1_pca['Label'] = df1[label_column].astype(str) + '_Track'
        df2_pca['Label'] = df2[label_column].astype(str) + '_Simulation'
    else:
        df1_pca['Label'] = 'Track'
        df2_pca['Label'] = 'Simulation'

    combined_df_pca = pd.concat([df1_pca, df2_pca], ignore_index=True)

    # Perform PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(combined_df_pca[comparison_columns])
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    pca_df['Label'] = combined_df_pca['Label']

    # Plotting
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Label', style='Label', s=100)
    plt.title("PCA Comparison between Track and Simulation Datasets")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()
    plt.show()

# Example usage:
# compare_datasets_with_pca(feature_track_df, feature_simulation_df, comparison_columns=['col1', 'col2', ...], label_column='your_label_column')
