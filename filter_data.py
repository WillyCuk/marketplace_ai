class filteringData:

    def filter_data(self, dataframe, keyword):
        # dataframe['product price'] = dataframe['product price'].replace('-', 0)
        dataframe['product price'] = dataframe['product price'].astype(float)

        dataframe['product rating'] = dataframe['product rating'].astype(float)
        dataframe['product sell count'] = dataframe['product sell count'].astype(
            int)
        dataframe = dataframe[dataframe['product name'].str.contains(
            keyword, case=False)]
        # Filter out rows where any column has a 0 value
        dataframe = dataframe[(dataframe != 0).all(axis=1)]

        return dataframe

    def filter_kota(self, dataframe, kota):
        dataframe = dataframe[dataframe['product location'].str.contains(
            kota, case=False)]

        return dataframe
