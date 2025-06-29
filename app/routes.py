
from app import app                 # Impor instance 'app' dari __init__.py Anda
from flask import render_template   # Impor render_template juga
from app.form import UserForm
from flask import flash, redirect   # flash: untuk memunculkan pesan singkat seperti "Login BErhasil!" atau "Data Tidak Valid" 
                                    # redirect:
from flask import url_for           # url_for: biar gak perlu ganti2 nama url satu2 kalau suatu haru mau ganti nama link url
import pandas as pd
import os                           # Untuk manajemen path
import numpy as np                  # Untuk manipulasi array dan operasi numerik
import tensorflow as tf             # Untuk memuat model TensorFlow
import joblib                       # Untuk memuat model dan scaler yang sudah disimpan
from FE_model import CustomFeatureEngineer  # Pastikan ini sesuai dengan nama file feature engineering Anda

# --- Konfigurasi dan Pemuatan Model ---
# Path ke direktori tempat model, scaler, dan feature engineering disimpan
# Pastikan folder 'model' ada di dalam folder 'app' Anda (misal: my_flask_app/app/model/)
MODEL_DIR = os.path.join(app.root_path, 'model')
        # app.root_path: akan mangarahakn kita pada folder app 
        # app.root_path, 'model': folder app --> folder model
'''
├── venv/               < --- ini adalah rooth path PROYEK
├── run.py              <-- File untuk menjalankan aplikasi
└── app/                <-- Ini adalah 'root path' APLIKASI Flask Anda (tempat app didefinisikan)
    ├── __init__.py     <-- app = Flask(__name__) biasanya ada di sini
    ├── routes.py       <-- File ini yang Anda sedang kerjakan
    ├── forms.py
    └── model/
        └── model.joblib, dll
        
'''


model = None
feature_engineer = None
scaler = None

# Tambahkan blok try-except untuk memuat model, scaler, dan feature engineer
# Ini harus dilakukan SEKALI saat aplikasi dimulai
try:
    # Memuat Fe, scaler, dan model
    feature_engineer = joblib.load(os.path.join(MODEL_DIR, 'CustomFeatureEngineering.joblib'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'MinMaxScaler.joblib'))
    model = joblib.load(os.path.join(MODEL_DIR, 'Smoker_NN.joblib'))

    print("\n--- Semua komponen pipeline ML berhasil dimuat di routes.py ---")
except FileNotFoundError as e:
    print(f"ERROR: Satu atau lebih file pipeline ML tidak ditemukan di {MODEL_DIR}. Detail: {e}")
    # Anda mungkin ingin menangani ini lebih baik di aplikasi produksi, misal menghentikan aplikasi
except Exception as e:
    print(f"ERROR: Terjadi kesalahan lain saat memuat pipeline ML di routes.py: {e}")


# Ini adalah urutan kolom yang diharapkan oleh DataFrame input ORIGINAL Anda
# sebelum feature engineering (total 21 kolom, termasuk age di awal)
ORIGINAL_FEATURE_COLUMNS_ORDER = [
    'age', 'height(cm)', 'weight(kg)', 'eyesight(left)', 'eyesight(right)',
    'hearing(left)', 'hearing(right)', 'systolic', 'relaxation',
    'fasting blood sugar', 'Cholesterol', 'triglyceride', 'HDL', 'LDL',
    'hemoglobin', 'Urine protein', 'serum creatinine', 'AST', 'ALT', 'Gtp',
    'dental caries'
]


# --- Rute Aplikasi Flask ---

@app.route('/')
@app.route('/index')                    # jika user mengakses url/index maka jalankan perintah di bawah
def index():
    return render_template('index.html', title='Home')
                                                

@app.route('/login', methods=['GET', 'POST'])                               # jika user mengetik url/login maka jalankan perintah dibawah
                                                                            # GET, ketika user pertamakali ke URL\login, fungsi GET akan menampilkan formulir
                                                                            # POST, ketika user mengirim formulir login, fungsi POST adalah mengirimkan data formulir 
def predict_form():
    form = UserForm()                                                      # dari file form.py akses kelas LoginForm()
    prediction_result = None
    prediction_class = None
    smoker_probability = None
    
    # --- 1. Ambil Data dari Form --- 
      
    # Semua logika pemrosesan data dan prediksi HARUS di dalam blok ini
    if form.validate_on_submit():
        # Cek apakah semua komponen ML pipeline berhasil dimuat
        if model is None or scaler is None or feature_engineer is None:
            flash("Sistem prediksi tidak dapat dimuat. Mohon hubungi administrator.", 'error')
            return render_template('login.html', title='Smoker Prediction Form', form=form,
                                   prediction_result=prediction_result, prediction_class=prediction_class,
                                   smoker_probability=smoker_probability)   

        try:
            form_data_dict = {                                                  #membuat dictionary yang isinya adalah data yg user input dari login.html                                                           
                        'age': form.age.data,                                   #form.age.data artinya akses data dari form.py, lalu akses field 'age', lalu ambil data yang user input 
                        'height(cm)': form.height.data,
                        'weight(kg)': form.weight.data,
                        'eyesight(left)': form.eyesight_left.data,
                        'eyesight(right)': form.eyesight_right.data,
                        'hearing(left)': form.hearing_left.data,
                        'hearing(right)': form.hearing_right.data,
                        'systolic': form.systolic.data,
                        'relaxation': form.relaxation.data,
                        'fasting blood sugar': form.fasting_blood_sugar.data,
                        'Cholesterol': form.cholesterol.data,
                        'triglyceride': form.triglyceride.data,
                        'HDL': form.hdl.data,
                        'LDL': form.ldl.data,
                        'hemoglobin': form.hemoglobin.data,
                        'Urine protein': form.urine_protein.data,
                        'serum creatinine': form.serum_creatine.data,
                        'AST': form.AST.data,
                        'ALT': form.ALT.data,
                        'Gtp': form.Gtp.data,
                        'dental caries': form.dental_caries.data
                    }
            
            # --- 2. Konversi Data ke DataFrame ---
            # Buat DataFrame Pandas dari data input, pastikan urutan kolom sesuai ORIGINAL_FEATURE_COLUMNS_ORDER
            input_values_original_order = [form_data_dict[col] for col in ORIGINAL_FEATURE_COLUMNS_ORDER]
                # ini adalah teknik List Comprehension
                # struktur sintaks: [ekspresi for item in iterable]
                    # peran: membuat nama dan urutan kolom sesuai dengan urutan yang diinginkan model, sebagaimana ketika model dulu dilatih
                    # urutannya mengacu pada ORIGINAL_FEATURE_COLUMNS_ORDER
                    # variabel = [] ,  artinya kita membuat list
                    # ekspresi: apa yang dilakukan (isi dari fungsi) di setiap iterasi
                    # iterable: objek/ varibel / list yang memungkinkan proses 1 per 1 berurutan
                    # item: variabel sementara untuk proses iterasi
                        # ekspresi for item in iterable
                            #artinya: lakukan "expresi" untuk setiap item sesuai urutan di dalam list iterable
                            #dgn kata lain, ambil setiap NILAI dari variabel form_data_dict sesuai dengan urutan dalam ORIGINAL_FEATURE_COLUMNS_ORDER 

                        # konteks kode kita:
                        # ekspresi: form_data_dict[col], dictionary[x], artinya mengakses nilai dari variabel col atau x dari variabel dictionary
                        # col atau x: adalah nama variabel sementara 
                        # col akan menjadi penghubung antara ORIGINAL_FEATURE_COLUMNS_ORDER & form_data_dict



            original_df = pd.DataFrame([input_values_original_order], columns=ORIGINAL_FEATURE_COLUMNS_ORDER)      
                # pakai nama df_train agar namanya sama persis dengan nama di google colab ketika kita melakukan feature enginering. kalau namanya beda, lu harus meneysuaikan lagi dan itu RIBET!
                # struktur sintaks: pd.DataFrame(data, columns=list_of_column_names)
                # kenapa [variabel]:
                    # karena pandas biasa mengolah data tabel. 
                    # dan karena isi input_values_original_order adalah list data saja, seperti [A, B, C]
                    # dengan mengubah [[A, B, C]], kita memberi pandas data kita 'seakan2' dalam bentuk tabel
                    # kita memberi tahunya bahwa, [A, B, C] adalah baris pertama dalam kolom suatu tabel

            print("\n--- Input DataFrame (Urutan Asli untuk Custom FE) ---")
            print(original_df)
            print("------------------------------------------------------\n")

            # --- 3. Feature Engineering ---

            X_engineered_df = feature_engineer.transform(original_df).copy()
            

            print("\n--- Data Setelah Custom Feature Engineering (DataFrame) ---")
            print(X_engineered_df.head())
            print(f"Shape after FE: {X_engineered_df.shape}")
            print(f"Columns after FE: {list(X_engineered_df.columns)}")                 # untuk cek, apakah nama kolom sudah sesuai dengan yg diinginkkan model
            print("----------------------------------------------------------\n")


            # --- 4. Normalisasi Data ---
            X_scaled_np_array = scaler.transform(X_engineered_df)

            print("\n--- Data Setelah MinMaxScaler (NumPy Array) ---")
            print(X_scaled_np_array)
            print(f"Shape after Scaling: {X_scaled_np_array.shape}")
            print("---------------------------------------------------\n")

            

        # --- 5. Prediksi dengan Model Neural Network ---
            # Model Keras membutuhkan input NumPy array, seringkali float32
            # model.predict() pada Keras mengembalikan probabilitas
            y_pred_proba_raw = model.predict(X_scaled_np_array.astype(np.float32))[0][0] # Ambil probabilitas untuk kelas positif (smoking=1)

      


            # --- 5. Tampilkan Hasil ---
                    # Tentukan kelas berdasarkan threshold (misal 0.51)
            predicted_class_value = 1 if y_pred_proba_raw >= 0.51 else 0
            
            smoker_probability = y_pred_proba_raw # Probabilitas untuk kelas '1' (Perokok)
            
            if predicted_class_value == 1: # Asumsi 1 adalah 'Perokok'
                prediction_class = "Perokok"
                flash("Prediksi: Perokok")
            else: # Asumsi 0 adalah 'Bukan Perokok'
                prediction_class = "Bukan Perokok"
                flash("Prediksi: Bukan Perokok")

                prediction_result = f"Probabilitas Perokok: {smoker_probability:.2%}" # Format sebagai persentase
                print(f"Prediksi berhasil: {prediction_class} ({prediction_result})")

        except Exception as e:
            flash(f"Terjadi kesalahan saat memproses data atau melakukan prediksi: {e}", 'error')
            prediction_result = f"Error dalam Prediksi: {e}"
            prediction_class = "N/A"
            smoker_probability = None
            print(f"Error prediksi: {e}")
        


    return render_template('login.html', title='Sign In', form=form) 
                                                                            # form sis kiri =, merujjuk pada variabel form yang ada di login.html
                                                                            # form sisi kanan =, merujuk pada form = LoginForm()

                                                                            