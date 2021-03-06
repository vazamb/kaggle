import numpy as np


def apk(actual, predicted, k=7):

    #return 0 if there's no element for predict
    if len(actual) == 0:
        return 0.0
    #crop the prediction if necessary
    if len(predicted)>k:
        predicted = predicted[:k]
    #Compute the apk
    score = 0.0
    num_hits = 0.0
    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    return score / min(len(actual), k)

def mapk(actual, predicted, k=7):
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

def sort_predictions_with_names(preds, names):
    preds_sorted, names_sorted = (list(t) for t in zip(*sorted(zip(preds, names), reverse=True)))

    return preds_sorted, names_sorted

def convert_to_names(arr, treshhold=1.0):
    y_cols = ['ind_cco_fin_ult1', 'ind_cder_fin_ult1', 'ind_cno_fin_ult1',
              'ind_ctju_fin_ult1', 'ind_ctma_fin_ult1', 'ind_ctop_fin_ult1',
              'ind_ctpp_fin_ult1', 'ind_deco_fin_ult1', 'ind_dela_fin_ult1',
              'ind_deme_fin_ult1', 'ind_ecue_fin_ult1', 'ind_fond_fin_ult1',
              'ind_hip_fin_ult1', 'ind_nom_pens_ult1', 'ind_nomina_ult1',
              'ind_plan_fin_ult1', 'ind_pres_fin_ult1', 'ind_reca_fin_ult1',
              'ind_recibo_ult1', 'ind_tjcr_fin_ult1', 'ind_valo_fin_ult1',
              'ind_viv_fin_ult1']

    preds_sorted, names_sorted = sort_predictions_with_names(arr, y_cols)
    predicted_additions = []
    for idx, proba in enumerate(preds_sorted):
        if proba >= treshhold:
            predicted_additions.append(names_sorted[idx])

    return predicted_additions

def calculate_delta(t_1, t):
    deltas = []
    for idx, arr in enumerate(t_1):
        t_1_products = arr
        t_products = t[idx]
        d = []
        for idx, val in enumerate(t_products):
            if val == 1 and t_1_products[idx] == 0:
                d.append(1)
            else:
                d.append(0)

        deltas.append(d)

    return np.array(deltas)

def calculate_score(added_products, predicted):
    predicted_names = []
    for i, p in enumerate(predicted):
        predicted_names.append(convert_to_names(p, 0.1))

    actual_names = []
    for i, p in enumerate(added_products):
        actual_names.append(convert_to_names(p))

    return mapk(actual_names, predicted_names)

if __name__ == "__main__":
    test = [ 0.        ,  0.        ,  0.18000002,  0.        ,  0.        ,
             0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
             0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
             0.        ,  0.        ,  0.        ,  0.        ,  0.        ,
             0.        ,  0.        ,  0.        ,  0.82      ]


    print(convert_to_names(test,0.01))
