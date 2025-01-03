import pandas as pd


def encode_categorical(df):
    from sklearn.preprocessing import OneHotEncoder

    ohe = OneHotEncoder(sparse_output=False, drop="first")  # drop='first' to avoid
    # multicollinearity
    cat_columns = df.select_dtypes(include=["object"]).columns
    encoded_array = ohe.fit_transform(df[cat_columns])
    encoded_df = pd.DataFrame(
        encoded_array, columns=ohe.get_feature_names_out(cat_columns), index=df.index
    )
    df_encoded = pd.concat([df.drop(cat_columns, axis=1), encoded_df], axis=1)
    return df_encoded, ohe


def decode_categorical(df, ohe, original_columns):
    cat_columns = original_columns.select_dtypes(include=["object"]).columns
    encoded_columns = ohe.get_feature_names_out(cat_columns)
    decoded_array = ohe.inverse_transform(df[encoded_columns])
    decoded_df = pd.DataFrame(decoded_array, columns=cat_columns, index=df.index)
    df_decoded = pd.concat([df.drop(encoded_columns, axis=1), decoded_df], axis=1)
    return df_decoded
