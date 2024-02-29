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
