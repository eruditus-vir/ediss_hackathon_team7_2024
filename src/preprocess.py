import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_regression


def remove_invalid_data(df, columns_with_defined_valid_values=None):
    """
    Remove invalid data from the DataFrame.

    Parameters:
    df (DataFrame): The DataFrame to clean.
    columns_with_defined_valid_values (dict): A dictionary where keys are column names and values are lists of valid values.

    Returns:
    DataFrame: A cleaned DataFrame with invalid rows removed.
    """
    cleaned_df = df.copy()

    # Remove rows with invalid values as defined by the user
    if columns_with_defined_valid_values:
        for column, valid_values in columns_with_defined_valid_values.items():
            cleaned_df = cleaned_df[cleaned_df[column].isin(valid_values)]

    # Remove rows with NaN values in specified columns
    cleaned_df = cleaned_df.dropna()

    return cleaned_df


def train_test_split_custom(feature_track_df, number_of_ids=4):

    while True:
        random_ids = feature_track_df['subject'].sample(n=number_of_ids).tolist()

        haves = 0
        for id in random_ids:
            if len(feature_track_df["risk_outcome"].value_counts()) > 1:
                haves +=1

        if haves >= int(number_of_ids/2):
            break

    # random_ids will contain n randomly selected subject IDs
    print(haves)
    print(random_ids)

    filtered_df = feature_track_df[feature_track_df['subject'].isin(random_ids)]

    # min_risk = filtered_df['risk_outcome'].value_counts().idxmin()
    # max_risk = filtered_df['risk_outcome'].value_counts().idxmax()
    # min_risk_extracted = filtered_df[filtered_df['risk_outcome'] == min_risk]
    # max_risk_extracted = filtered_df[filtered_df['risk_outcome'] == max_risk].sample(n=len(min_risk_extracted))
    #
    # df_concatenated = pd.concat([min_risk_extracted, max_risk_extracted], ignore_index=True)

    merged_df = feature_track_df.merge(filtered_df, indicator=True, how='outer')

    # Filter out the rows that are from the subset
    result_df = merged_df[merged_df['_merge'] == 'left_only'].drop('_merge', axis=1)

    return result_df, filtered_df


def train_test_split_divide_laps(feature_track_df, number_of_ids=4):

    while True:
        random_ids = feature_track_df['subject'].sample(n=number_of_ids).tolist()

        haves = 0
        for id in random_ids:
            if len(feature_track_df["risk_outcome"].value_counts()) > 1:
                haves +=1

        if haves >= int(number_of_ids/2):
            break

    # random_ids will contain n randomly selected subject IDs
    print(haves)
    print(random_ids)

    filtered_df = feature_track_df[feature_track_df['subject'].isin(random_ids)]

    all_ids_filtered = []

    for id in random_ids:
        filter_results = []
        id_df = filtered_df[filtered_df.subject == id]
        laps = list(id_df.lap.value_counts().index)
        print(laps)

        for i in range(0, len(laps), 2):
            print(i)
            filter_results.append(id_df[id_df.lap == laps[i]])
            i+=2 # missing one index

        final_result_per_id = pd.concat(filter_results)

        all_ids_filtered.append(final_result_per_id)

    result_test = pd.concat(all_ids_filtered)

    merged_df = feature_track_df.merge(result_test, indicator=True, how='outer')

    # Filter out the rows that are from the subset
    result_df = merged_df[merged_df['_merge'] == 'left_only'].drop('_merge', axis=1)

    return result_df, result_test

def selection_top_features(cleaned_feature_track, number_of_features=20):
    X = cleaned_feature_track.drop('risk_outcome', axis=1)
    y = cleaned_feature_track['risk_outcome']

    # Calculate mutual information
    mi = mutual_info_regression(X, y)
    mi_series = pd.Series(mi, index=X.columns)

    # Remove features starting with "car_" or "Car_"
    mi_series = mi_series[~mi_series.index.str.startswith('car_') & ~mi_series.index.str.startswith('Car_')]

    # Sort the series after filtering
    mi_series = mi_series.sort_values(ascending=False)

    # Plotting
    plt.figure(figsize=(10, 30))
    sns.barplot(x=mi_series.values, y=mi_series.index)
    plt.title('Mutual Information with Risk Outcome')
    plt.xlabel('Mutual Information Score')
    plt.ylabel('Features')
    plt.show()

    # Get top 10 features based on mutual information scores after filtering
    top_features = mi_series.head(number_of_features)
    return top_features