from sklearn.model_selection import train_test_split

def split_data(data, test_size=0.2, random_state=42):
    """
    Splits the dataset into training and testing subsets.

    Args:
        data (pandas.DataFrame): The dataset to be split.
        test_size (float): The proportion of the dataset to include in the test split.
