import pandas as pd
from database_utilities import MongoHandler

def convert_to_base(series):
    if 'float' in str(series.dtype):
        return [float(x) for x in series.values]
    elif 'int' in str(series.dtype):
        return [int(x) for x in series.values]
    elif 'str' in str(series.dtype):
        return [str(x) for x in series.values]
    else:
        raise ValueError('Expected dtype to be one of (float, int, str)')


def parse_contents(filename):
    if 'csv' in filename:
        df = pd.read_csv(filename)
    else:
        raise ValueError('File must be CSV.')
    #
    t = pd.date_range(start='2012-07-01T12', periods=125, freq='0.25H').to_pydatetime()
    times = [x.strftime('%c') for x in t]
    docs = []
    for key in df.keys():
        docs.append({'name': key, 'timestamp': times, key: convert_to_base(df[key])})
    return docs


def main():
    docs = parse_contents('test.csv')
    db_client = MongoHandler()
    db_client.upload(docs)


if __name__ == '__main__':
    main()
