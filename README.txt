Progress:

1. data user input dari login.html
2. data masuk ke backend, lalu diubah menjadi datafreme

next:
- df diubah menjadi df hasil feature enginering (df_1) dengan FeatureEnginering.joblib
- df_1 dinormalisasi ( semua data diubah menjadi range 0 - 1) dengan model MinMaxScaler.joblib

FeatureEnginering.joblib:

def age_group(age):        
    if 20 <= age <40:
        return 1 # high prob
    elif 40 <= age <= 50:
        return 2 # medium prob
    elif 50 < age <= 60:
        return 3 # low prob
    elif age > 60:
        return 4

df_train['age_catg'] = df_train['age'].apply(age_group)

