import streamlit as st
import pickle
import bz2file as bz2
import pandas as pd
import numpy as np

root_model = './Model'
root_dataset = './Dataset'

rf_model = root_model + '/RF_Model.pbz2'
ensemble_model = root_model + '/Ensemble_3_Soft.pbz2'
dataset = root_dataset + '/predict_data.bz2'
dataset_predict = root_dataset + '/predict_data_ohe.bz2'

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

def decompress_dataset(file):
    data = pd.read_csv(file, compression='bz2')
    return data

def query_data(dataframe, id):
    dataframe = decompress_dataset(dataframe)
    dataframe = dataframe[dataframe['SK_ID_CURR'] == id]
    return dataframe

def main():
       
    st.title("Home Credit Default Prediction!")
    with st.form(key='id'):
        curr_id = st.number_input("Input Your Customer ID", min_value=100002, max_value=456255)
        submit_button = st.form_submit_button()
    
    if submit_button:
        predict_data = query_data(dataset, curr_id)
        predict_data.replace([np.inf, -np.inf], 0, inplace=True)
        predict_data = predict_data.drop(['TARGET'], axis=1)
        predict_data = predict_data.fillna(0)
        X_test = query_data(dataset_predict, curr_id)
        X_test.replace([np.inf, -np.inf], 0, inplace=True)
        X_test.fillna(0, inplace=True)

        if predict_data.shape[0] == 0: 
            st.write("Data Tidak Ditemukan dalam Application Train Dataset")

        else:
            # Load Model
            model = decompress_pickle(rf_model)
            
            st.write("Data Customer", "with {} Columns".format(predict_data.shape[1]))
            st.dataframe(predict_data)

            X_test = X_test.drop(['SK_ID_CURR', 'TARGET'], axis=1)
            [prediction] = model.predict_proba(X_test.values)[::,1]
            
            st.write("Probabilitas gagal bayar : {}".format(prediction))
            if prediction > 0.1404:
                st.write("Prediksi: Kemungkinan Besar Customer Akan Gagal Bayar")
            if prediction <= 0.1404:
                st.write("Prediksi: Kemungkinan Besar Customer Tidak Akan Gagal Bayar")

if __name__ == '__main__':
    main()
