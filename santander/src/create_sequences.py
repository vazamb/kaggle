import pandas as pd
import pickle

y_cols = ['ind_ahor_fin_ult1', 'ind_aval_fin_ult1', 'ind_cco_fin_ult1',
          'ind_cder_fin_ult1', 'ind_cno_fin_ult1', 'ind_ctju_fin_ult1',
          'ind_ctma_fin_ult1', 'ind_ctop_fin_ult1', 'ind_ctpp_fin_ult1',
          'ind_deco_fin_ult1', 'ind_deme_fin_ult1', 'ind_dela_fin_ult1',
          'ind_ecue_fin_ult1', 'ind_fond_fin_ult1', 'ind_hip_fin_ult1',
          'ind_plan_fin_ult1', 'ind_pres_fin_ult1', 'ind_reca_fin_ult1',
          'ind_tjcr_fin_ult1', 'ind_valo_fin_ult1', 'ind_viv_fin_ult1',
          'ind_nomina_ult1', 'ind_nom_pens_ult1', 'ind_recibo_ult1']

def create_sequence(df):
    X = []
    y= []
    X_full =[]
    admin_cols = ['fecha_dato', 'ncodpers']
    unique_ids = df["ncodpers"].unique()
    processed_users = []
    print(len(unique_ids))

    for idx, user in enumerate(unique_ids):
        user_obs = df[df["ncodpers"] == user]
        X_user = user_obs.drop(admin_cols, axis=1).values
        y_user = user_obs[y_cols].values

        # X are all values up to the second last month
        # y_train (the desired output) is are the product columns
        # of the month after the last training example
        X.append(X_user[:-1])
        X_full.append(X_user)
        y.append(y_user[-1])

        processed_users.append(user)

        if idx%100 == 0:
            print(idx)

        # Drop user rows to speed up later lookups
        if idx%10000 == 0:
            print("Dropping {0} users".format(len(processed_users)))
            df = df[~df["ncodpers"].isin(processed_users)]
            print("{0} rows left".format(len(df)))
            processed_users = []

    return X, y, unique_ids, X_full


if __name__ == "__main__":
    df = pd.read_pickle("../data/training_transformed.pickle")

    X_train, y_train, ordered_ids, full_dataset = create_sequence(df)
    with open("../data/X_train.pickle", "wb") as handler:
        pickle.dump(X_train, handler)

    with open("../data/y_train.pickle", "wb") as handler:
        pickle.dump(y_train, handler)

    with open("../data/training_ids.pickle", "wb") as handler:
        pickle.dump(ordered_ids, handler)

    with open("../data/training_submission.pickle", "wb") as handler:
        pickle.dump(full_dataset, handler)

    print(len(X_train))
    print(len(y_train))