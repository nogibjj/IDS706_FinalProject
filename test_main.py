from main import *

def test_func():
    df = loadDf("https://people.sc.fsu.edu/~jburkardt/data/csv/oscar_age_female.csv")
    descriptive_df = describeData(df)
    assert isinstance(df, pd.DataFrame)
    assert 'max' in descriptive_df.index
    assert df.shape[0]==89
    print(descriptive_df)
    print(df)
    plotData(df)
test_func()