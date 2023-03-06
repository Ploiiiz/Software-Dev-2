import bson

def rename(dataframe):
    df = dataframe
    df.index.names = ['timestamp']
    df.columns = [i[3:] for i in df.columns]
    return df