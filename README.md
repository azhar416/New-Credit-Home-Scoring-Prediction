# Credit Home Scoring Prediction
Final Project Zenius (Studi Independen)

Problem : https://www.kaggle.com/competitions/home-credit-default-risk/overview

Aplikasi ini bertujuan untuk melakukan prediksi pada nasabah Home Credit apakah peminjam akan gagal bayar atau tidak.

## Data
Data yang disediakan pada kaggle antara lain :
1. application_{train|test}.csv
- This is the main table, broken into two files for Train (with TARGET) and Test (without TARGET).
- Static data for all applications. One row represents one loan in our data sample.

2. bureau.csv
- All client's previous credits provided by other financial institutions that were reported to Credit Bureau (for clients who have a loan in our sample).
- For every loan in our sample, there are as many rows as number of credits the client had in Credit Bureau before the application date.

3. bureau_balance.csv
- Monthly balances of previous credits in Credit Bureau.
- This table has one row for each month of history of every previous credit reported to Credit Bureau – i.e the table has (#loans in sample * # of relative previous credits * # of months where we have some history observable for the previous credits) rows.

4. POS_CASH_balance.csv
- Monthly balance snapshots of previous POS (point of sales) and cash loans that the applicant had with Home Credit.
- This table has one row for each month of history of every previous credit in Home Credit (consumer credit and cash loans) related to loans in our sample – i.e. the table has (#loans in sample * # of relative previous credits * # of months in which we have some history observable for the previous credits) rows.

5. credit_card_balance.csv
- Monthly balance snapshots of previous credit cards that the applicant has with Home Credit.
- This table has one row for each month of history of every previous credit in Home Credit (consumer credit and cash loans) related to loans in our sample – i.e. the table has (#loans in sample * # of relative previous credit cards * # of months where we have some history observable for the previous credit card) rows.

6. previous_application.csv
- All previous applications for Home Credit loans of clients who have loans in our sample.
- There is one row for each previous application related to loans in our data sample.

7. installments_payments.csv
- Repayment history for the previously disbursed credits in Home Credit related to the loans in our sample.
- There is a) one row for every payment that was made plus b) one row each for missed payment.
- One row is equivalent to one payment of one installment OR one installment corresponding to one payment of one previous Home Credit credit related to loans in our sample.

8. HomeCredit_columns_description.csv
- This file contains descriptions for the columns in the various data files.

## Create New Dataset
EDA dan Pembuatan Dataset : `/Colab (Trial n Error)/Prepare_Data.ipynb`

### Cleaning application_train.csv
Karena tabel utama yang digunakan adalah `application_train.csv`, perlu dilakukan pembersihan data terlebih dahulu. Tabel ini memiliki missing data yang sangat banyak sehingga lebih baik untuk dilakukan drop pada beberapa kolom yang memiliki persentase missing value yang tinggi. 

Tabel ini juga memiliki `TARGET` yang tidak seimbang (imbalance target) yaitu `92% TARGET 0` dan `8% TARGET 1`. Sehingga lebih baik untuk melakukan drop pada beberapa record data dengan target 0 sehingga mengurangi ketidak seimbangan target (undersampling).

### Feature Engineering
Melakukan feature engineering dengan menambahkan beberapa kolom (fitur) pada dataset yang memungkinkan dapat meningkatkan performa dari model nantinya.

Fitur - fitur yang ditambahkan antara lain :
1. CREDIT_INCOME_PERCENT (AMT_CREDIT / AMT_INCOME_TOTAL)
2. ANNUITY_INCOME_PERCENT (AMT_ANNUITY / AMT_INCOME_TOTAL)
3. CREDIT_TERM (AMT_ANNUITY / AMT_CREDIT)
4. DAYS_EMPLOYED_PERCENT (DAYS_EMPLOYED / DAYS_BIRTH)

Dataset ini juga menggunakan beberapa tabel lain yang telah dilakukan agregasi sebagai tambahan fitur pada dataset yang baru.

Tabel lain yang digunakan antara lain :
1. bureau.csv
2. previous_application.csv
3. POS_CASH_balance.csv

Dataset akhir untuk pelatihan memiliki 179.793 Record data dan 201 Feature. 

Sementara dataset yang akan digunakan untuk deployment memiliki 307.511 Record data dan 201 Feature.

## Models
### Training Model
Matrix yang digunakan adalah `ROC AUC` dan `Confusion Matrix` yang berfokus kepada `Recall`.

Model yang dilatih (Setiap model dilakukan Hypertuning Parameter):

1. Logistic Regression

Parameter : 
- Solver : lbfgs
- penalty : l2
- Max_iter : 2500

2. K-Nearest Neighbors

Parameter : 
- n_neighbors : 7
- weights : uniform
- leaf_size : 50
- metric : minkowski

3. Random Forest

Parameter :
- bootstrap : False
- criterion : entropy
- max_depth : 16
- n_estimators : 200
- n_jobs : -1
- random_state : 42

4. Ensemble Model (Logistic Regression, K-Nearest Neighbors, Random Forest) dengan Majority Voting (Hard Voting dan Soft Voting)

### Evaluasi Model
1. Logistic Regression
- Best Threshold: 0.1359
- Recall: Recall : 0.6357
- ROC AUC Score : 0.6357

2. KNN
- Best Threshold: 0.2857
- Recall: Recall : 0.5932
- ROC AUC Score : 0.5932

3. Random Forest
- Best Threshold: 0.1404
- Recall: Recall : 0.7581
- ROC AUC Score : 0.7581

4. Ensemble Model Soft Voting
- Best Threshold: 0.1626
- Recall: Recall : 0.7092
- ROC AUC Score : 0.7092

5. Ensemble Model Hard Voting
- Best Threshold: - (karena tidak memprediksi probabilitas)
- Recall: Recall : 0.5657
- ROC AUC Score : 0.5657

## Deployment
Proses deployment menggunakan StreamLit karena mudah digunakan dan langsung terintegrasi dengan GitHub.

Link Deployment : https://azhar416-new-credit-home-scoring-prediction-web-app-w83t1t.streamlit.app/