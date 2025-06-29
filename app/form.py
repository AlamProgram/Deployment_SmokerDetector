from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, BooleanField, SubmitField
                    # Ambil berbagai jenis 'kotak input'
                    # StringField: input akan dianggap String
                    # PasswordField: input di Field ini akan dianggap sebagai Passwor, ketika user mengetik akan tampil seperti simbol ******
                    # BooleanField: Ini adalah jenis kotak input untuk kotak centang (checkbox)
                    # SubmitField: input di Field ini akan dianggap sebagai perintah submit
from wtforms.validators import DataRequired, NumberRange

class UserForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=20, message='Age must be at least 20')], render_kw={"placeholder": "min 20 (years)"})
    height = IntegerField('Height', validators=[DataRequired()], render_kw={"placeholder": "(cm)"})
    weight = IntegerField('Weight', validators=[DataRequired(),], render_kw={"placeholder": "(kg)"})
    eyesight_left = FloatField('Eyesight Left', validators=[DataRequired(), NumberRange(min=0.1, max=2.0)], render_kw={"placeholder":"0.1 (so bad) - 2 (good)"})
    eyesight_right = FloatField('Eyesight Right', validators=[DataRequired(), NumberRange(min=0.1, max=2.0)], render_kw={"placeholder": "0.1 (so bad) - 2 (good)"})
    
    hearing_left = IntegerField('Hearing Left', validators=[DataRequired(), NumberRange(min=1, max=2)], render_kw={"placeholder": "1 (bad) or 2 (good)"})
    hearing_right = IntegerField('Hearing Right', validators=[DataRequired(), NumberRange(min=1, max=2)], render_kw={"placeholder": "1 (bad) or 2 (good)"})
    
    systolic = IntegerField('Systolic', validators=[DataRequired(), NumberRange(min=90, max=180)], render_kw={"placeholder": "90 - 180 (mmHg)"})
    relaxation = IntegerField('Relaxation', validators=[DataRequired(), NumberRange(min=60, max=120)], render_kw={"placeholder": "60 - 120 (mmHg)"})
    
    fasting_blood_sugar = IntegerField('Fasting Blood Sugar', validators=[DataRequired(), NumberRange(min=70, max=126)], render_kw={"placeholder": "70 - 126 (mg/dL)"})
    
    cholesterol = IntegerField('Cholesterol', validators=[DataRequired(), NumberRange(min=125, max=200)], render_kw={"placeholder": "125 - 200 (mg/dL)"})
    triglyceride = IntegerField('Triglyceride', validators=[DataRequired(), NumberRange(min=50, max=150)], render_kw={"placeholder": "50 - 150 (mg/dL)"})
    hdl = IntegerField('HDL', validators=[DataRequired(), NumberRange(min=40, max=100)], render_kw={"placeholder": "40 - 100 (mg/dL)"})
    ldl = IntegerField('LDL', validators=[DataRequired(), NumberRange(min=50, max=130)], render_kw={"placeholder": "50 - 130 (mg/dL)"})
    hemoglobin = FloatField('Hemoglobin', validators=[DataRequired(), NumberRange(min=12, max=17.5)], render_kw={"placeholder": "12 - 17.5 (g/dL)"})
    urine_protein = IntegerField('Urine Protein', validators=[DataRequired(), NumberRange(min=0, max=4)], render_kw={"placeholder": "0 - 4"})
    serum_creatine = FloatField('Serum Creatine', validators=[DataRequired(), NumberRange(min=0.1, max=9.9)], render_kw={"placeholder": "0.1 - 9.9 (mg/dL)"})
    AST = IntegerField('AST', validators=[DataRequired(), NumberRange(min=8, max=33)], render_kw={"placeholder": '8 - 33 (Units/L)'})
    ALT = IntegerField('ALT', validators=[DataRequired(), NumberRange(min=7, max=56)], render_kw={"placeholder": '7 - 56 (Units/L)'})
    Gtp = IntegerField('Gtp', validators=[DataRequired(),NumberRange(min=8, max=61)], render_kw={"placeholder": '8 - 61 (Units/L)'})
    dental_caries = IntegerField('Dental Caries', validators=[NumberRange(min=0, max=1)], render_kw={"placeholder": "0 (no) or 1 (yes)"})
    submit = SubmitField('Submit')



'''
 0   age                    111479 non-null  int64  
 1   height(cm)             111479 non-null  int64  
 2   weight(kg)             111479 non-null  int64  
 3   eyesight(left)         111479 non-null  float64
 4   eyesight(right)        111479 non-null  float64
 5   hearing(left)          111479 non-null  int64  
 6   hearing(right)         111479 non-null  int64  
 7   systolic               111479 non-null  int64  
 8   relaxation             111479 non-null  int64  
 9   fasting blood sugar    111479 non-null  int64  
 10  Cholesterol            111479 non-null  int64  
 11  triglyceride           111479 non-null  int64  
 12  HDL                    111479 non-null  int64  
 13  LDL                    111479 non-null  int64  
 14  hemoglobin             111479 non-null  float64
 15  Urine protein          111479 non-null  int64  
 16  serum creatinine       111479 non-null  float64
 17  AST                    111479 non-null  int64  
 18  ALT                    111479 non-null  int64  
 19  Gtp                    111479 non-null  int64  
 20  dental caries          111479 non-null  int64  
 21  smoking                111479 non-null  int64  
 22  age_catg               111479 non-null  int64  
 23  %smoker_age            111479 non-null  float64
 24  BMI                    111479 non-null  float64
 25  BMI_catg               111479 non-null  int64  
 26  %smoker_BMI_catg       111479 non-null  float64
 27  ESL_catg               111479 non-null  int64  
 28  %ESL                   111479 non-null  float64
 29  ESR_catg               111479 non-null  int64  
 30  %ESR                   111479 non-null  float64
 31  BloodPressure          111479 non-null  int64  
 32  %smoker_BloodPressure  111479 non-null  float64
 33  BS_catg                111479 non-null  int64  
 34  %smoker_BS_catg        111479 non-null  float64
 35  chol_catg              111479 non-null  int64  
 36  %smoker_chol_catg      111479 non-null  float64
 37  HDL_catg               111479 non-null  int64  
 38  %smoker_HDL_catg       111479 non-null  float64
 39  LDL_catg               111479 non-null  int64  
 40  %smoker_LDL_catg       111479 non-null  float64
 41  tri_catg               111479 non-null  int64  
 42  %smoker_tri_catg       111479 non-null  float64
 43  hemo_catg              111479 non-null  int64  
 44  %smoker_hemo_catg      111479 non-null  float64
 45  UP_1                   111479 non-null  int64  
 46  %smoker_UP_1           111479 non-null  float64
 47  SC_catg                111479 non-null  int64  
 48  %smoker_SC             111479 non-null  float64
 49  AST_catg               111479 non-null  int64  
 50  %smoker_AST_catg       111479 non-null  float64
 51  ALT_catg               111479 non-null  int64  
 52  %smoker_ALT_catg       111479 non-null  float64
 53  Gtp_catg               111479 non-null  int64  
 54  %smoker_Gtp_catg       111479 non-null  float64
 55  %smoker_DC             111479 non-null  float64

''' 


    