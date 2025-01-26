import streamlit as st
import pandas as pd
import joblib
import pickle
import re
from sklearn.ensemble import RandomForestRegressor

# Set up the Streamlit app
st.set_page_config(page_title="Model Prediction", layout="centered")

# Page title
st.markdown("<h1 style='color: #FFFFFF; font-weight: bold;'>🏠 Qiymət Proqnozlaşdırılması</h1>", unsafe_allow_html=True)

# Sidebar with an image
st.sidebar.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="https://cdn3d.iconscout.com/3d/premium/thumb/ai-home-3d-icon-download-in-png-blend-fbx-gltf-file-formats--wifi-logo-house-smart-artificial-intelligence-pack-science-technology-icons-8877577.png?f=webp" width="190">
    </div>
    """,
    unsafe_allow_html=True
)

# Load data and model (replace with your model file if available)
data = pd.read_csv('BakuApartmentData.csv')

model = joblib.load('random_forest_price_model.pkl')  # Ensure this file exists in your directory

# Rename columns to Azerbaijani
data.rename(columns={
    'price': 'qiymət',
    'location': 'yer',
    'rooms': 'otaqlar',
    'square': 'kvadrat',
    'floor': 'mərtəbə',
    'new_building': 'yeni_tikili',
    'has_repair': 'təmirli',
    'has_bill_of_sale': 'kupçalı',
    'has_mortgage': 'ipoteka'
}, inplace=True)


data['mərtəbə_faktiki'] = data['mərtəbə'].apply(lambda x: str(x).split('/')[0])
data['mərtəbə_bina'] = data['mərtəbə'].apply(lambda x: str(x).split('/')[1]) 

data['mərtəbə_bina'] = data['mərtəbə_bina'].astype(int)
data['mərtəbə_faktiki'] = data['mərtəbə_faktiki'].astype(int)

# Form for user input
st.markdown("<h3>Hörmətli müştəri zəhmət olmasa məlumatları daxil edin.</h3>", unsafe_allow_html=True)
with st.form("prediction_form"):
    name = st.text_input("Adınızı daxil edin: ")
    surname = st.text_input("Soyadınızı daxil edin: ")
    yer = st.selectbox("Yer", data['yer'].unique())
    otaqlar = st.number_input("Otaqların Sayı", min_value=1, max_value=10, step=1)
    kvadrat = st.number_input("Kvadrat (m²)", min_value=float(data['kvadrat'].min()), max_value=float(data['kvadrat'].max()), step=1.0)
    mərtəbə_bina = st.number_input("Binanın Ümumi Mərtəbəsi", min_value=data['mərtəbə_bina'].min(), max_value=data['mərtəbə_bina'].max(), step=1)
    mərtəbə_fakt = st.number_input("Evin Mərtəbəsi", min_value=data['mərtəbə_faktiki'].min(), max_value=data['mərtəbə_faktiki'].max(), step=1)
    yeni_tikili = st.selectbox("Yeni Tikili", ["Bəli", "Xeyr"])
    təmirli = st.selectbox("Təmirli", ["Bəli", "Xeyr"])
    kupçalı = st.selectbox("Kupçalı", ["Bəli", "Xeyr"])
    ipoteka = st.selectbox("İpoteka", ["Bəli", "Xeyr"])
    mail = st.text_input("Ətraflı məlumat əldə etmək istəyirsinizsə mailinizi qeyd edin: ")

    # Submit button
    submit_button = st.form_submit_button("Mənzilin Qiymətini Proqnoz Edin")

if submit_button:
    if mail:
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_pattern, mail):
            if mərtəbə_bina < mərtəbə_fakt:
                st.warning('⚠ Xəta: Hörmətli müştəri binanın ümumi mərtəbəsi evin mərtəbəsindən kiçik ola bilməz.')
            else:
                yeni_tikili_value = 1 if yeni_tikili == "Bəli" else 0
                təmirli_value = 1 if təmirli == "Bəli" else 0
                kupçalı_value = 1 if kupçalı == "Bəli" else 0
                ipoteka_value = 1 if ipoteka == "Bəli" else 0

                # Prepare input data
                input_data = pd.DataFrame({
                    'yer': [yer],  # Ensure location is encoded appropriately if necessary
                    'otaq_sayı': [otaqlar],
                    'sahə': [kvadrat],
                    'mərtəbə_faktiki': [mərtəbə_fakt],
                    'mərtəbə_bina': [mərtəbə_bina],
                    'yeni_tikili': [yeni_tikili_value],
                    'təmirli': [təmirli_value],
                    'kupçalı': [kupçalı_value],
                    'ipoteka': [ipoteka_value],
                    'mail': [mail]
                })

                mail_table = input_data.copy()

                del input_data['mail']
                input_data['mərtəbə_faktiki'] = input_data['mərtəbə_faktiki'].astype('int')
                input_data['mərtəbə_bina'] = input_data['mərtəbə_bina'].astype('int')
                input_data['ünvan_tipi'] = input_data['yer'].apply(lambda x: str(x).split(' ')[-1]) 
                input_data['mərtəbə_faizi'] = input_data['mərtəbə_faktiki']/input_data['mərtəbə_bina']
                input_data['1_otaq_sahəsi'] = input_data['sahə']/input_data['otaq_sayı']
                        
                if input_data['ünvan_tipi'].iloc[0] == 'm.':
                    input_data['ünvan_tipi_m.'] = 1
                    input_data['ünvan_tipi_q.'] = 0
                    input_data['ünvan_tipi_r.'] = 0
                elif input_data['ünvan_tipi'].iloc[0] == 'r.':
                    input_data['ünvan_tipi_m.'] = 0
                    input_data['ünvan_tipi_q.'] = 0
                    input_data['ünvan_tipi_r.'] = 1
                else:
                    input_data['ünvan_tipi_m.'] = 0
                    input_data['ünvan_tipi_q.'] = 1
                    input_data['ünvan_tipi_r.'] = 0

                with open('scaling_params.pkl', 'rb') as f:
                    scaling_params = pickle.load(f)

                columns_to_normalize = ['1_otaq_sahəsi', 'sahə', 'otaq_sayı', 'mərtəbə_faktiki', 'mərtəbə_bina']
                for column in columns_to_normalize:
                    min, max = scaling_params[column]['min'], scaling_params[column]['max']
                    input_data[column] = (input_data[column] - min) / max

                value_counts = data['yer'].value_counts().reset_index()
                list_others = value_counts[value_counts['count']<50]['yer'].to_list()
                
                for i in ['yer__20 Yanvar m.', 'yer__28 May m.', 'yer__7-ci mikrorayon q.',
                    'yer__8 Noyabr m.', 'yer__8-ci kilometr q.', 'yer__8-ci mikrorayon q.',
                    'yer__9-cu mikrorayon q.', 'yer__Abşeron r.', 'yer__Avtovağzal m.',
                    'yer__Azadlıq Prospekti m.', 'yer__Ağ şəhər q.', 'yer__Badamdar q.',
                    'yer__Bakıxanov q.', 'yer__Bayıl q.', 'yer__Biləcəri q.',
                    'yer__Binəqədi r.', 'yer__Dərnəgül m.', 'yer__Elmlər Akademiyası m.',
                    'yer__Gənclik m.', 'yer__Hövsan q.', 'yer__Həzi Aslanov m.',
                    'yer__Həzi Aslanov q.', 'yer__Koroğlu m.', 'yer__Köhnə Günəşli q.',
                    'yer__Masazır q.', 'yer__Memar Əcəmi m.', 'yer__Nardaran q.',
                    'yer__Neftçilər m.', 'yer__Nizami m.', 'yer__Nizami r.',
                    'yer__Nəriman Nərimanov m.', 'yer__Nərimanov r.', 'yer__Nəsimi m.',
                    'yer__Nəsimi r.', 'yer__Qara Qarayev m.', 'yer__Qaraçuxur q.',
                    'yer__Sabunçu r.', 'yer__Sahil m.', 'yer__Səbail r.',
                    'yer__Xalqlar Dostluğu m.', 'yer__Xətai r.', 'yer__Yasamal q.',
                    'yer__Yasamal r.', 'yer__Yeni Günəşli q.', 'yer__Yeni Yasamal q.',
                    'yer__others', 'yer__İnşaatçılar m.', 'yer__İçəri Şəhər m.',
                    'yer__Şah İsmayıl Xətai m.', 'yer__Əhmədli m.', 'yer__Əhmədli q.']:
                    input_data[i] = 0

                yer = input_data['yer'].iloc[0]
                if yer in list_others:
                    input_data['others'] = 1
                else: 
                    input_data[f'yer__{yer}'] = 1

                # SVD - Dimension Reduction
                with open('svd_model.pkl', 'rb') as f:
                    svd = pickle.load(f)

                with open('svd_explained_variance.pkl', 'rb') as f:
                    explained_variance = pickle.load(f)
                
                yer_columns = [col for col in input_data.columns if col.startswith('yer__')]
                yer_df = input_data[yer_columns]
                new_data_svd = svd.transform(yer_df)  
                yer_svd_df = pd.DataFrame(new_data_svd, columns=[f'yer_svd_{i+1}' for i in range(new_data_svd.shape[1])])
                input_data = pd.concat([input_data.drop(columns=yer_columns), yer_svd_df], axis=1)

                for i in ['kupçalı', 'ipoteka', 'mərtəbə_faizi', 'yer','ünvan_tipi','ünvan_tipi_m.', 'ünvan_tipi_r.',
            'yer_svd_1', 'yer_svd_2']:
                    del input_data[i]

                input_data = input_data[['otaq_sayı', 'sahə', 'yeni_tikili', 'təmirli', 'mərtəbə_faktiki','mərtəbə_bina','1_otaq_sahəsi','ünvan_tipi_q.','yer_svd_3','yer_svd_4','yer_svd_5']]

                rf_reg = joblib.load('random_forest_price_model.pkl')

                predictions = rf_reg.predict(input_data)

                min, max = scaling_params['qiymət']['min'], scaling_params['qiymət']['max']
                predictions = (predictions[0] * max) + min

                # mail send
                
                import streamlit as st
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart

                # SMTP server and port
                SMTP_SERVER = "smtp.gmail.com"
                SMTP_PORT = 587

                # Function to send email
                def send_email(email_to, app_password, subject, body):
                    try:
                        # Create email content
                        msg = MIMEMultipart()
                        msg['To'] = email_to
                        msg['From'] = 'riyadehmedov03@gmail.com'
                        msg['Subject'] = subject
                        msg.attach(MIMEText(body, 'plain'))  # Attach the body as plain text

                        # Attach the HTML body
                        msg.attach(MIMEText(body, 'html'))  # Set content type to HTML

                        # Connect to the SMTP server and send the email
                        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                            server.starttls()  # Secure connection
                            server.login('riyadehmedov03@gmail.com', app_password)  # Use App Password
                            server.sendmail('riyadehmedov03@gmail.com', email_to, msg.as_string())

                        return True  # Email sent successfully
                    except Exception as e:
                        st.error(f"Error sending email: {e}")  # Display error message
                        return False  # Email failed to send

                # Example usage
                email_to = mail_table['mail'].iloc[0]  # Extract email from DataFrame
                app_password = 'ogfp zzmi uhxh vdkd'  # Replace with your App Password
                subject = f"{name} {surname} | Evin Məbləği"

                # Body of the email with additional code/information
                mail_table_html = mail_table.to_html(index=False)  # Convert DataFrame to HTML table

                # Body of the email with the table
                body = f"""
                <html>
                    <body>
                        <p>Hər vaxtınız xeyir {name} {surname},</p>
                        <p>Mənzilin proqnozlaşdırılmış qiyməti: <strong>{predictions:.2f} AZN</strong>.</p>
                        <p>Daxil etdiyiniz məlumatlar:</p>
                        {mail_table_html}  <!-- Insert the HTML table here -->
                        <p>Təşəkkür edirik!</p>
                    </body>
                </html>
                """

                # Send email
                if send_email(email_to, app_password, subject, body):
                    st.success(f"🎉 Təşəkkür edirik, {name} {surname}! Mənzilin proqnozlaşdırılmış qiyməti: {predictions:.2f} AZN. Əlavə olaraq mail ünvanınıza ətraflı məlumat göndərildi.")
                else:
                    st.error("Email göndərilmədi. Xahiş edirik yenidən cəhd edin.")
        else:
            st.warning("⚠ Xəta: Zəhmət olmasa düzgün mail ünvanı qeyd edin.")
    else:
        if mərtəbə_bina < mərtəbə_fakt:
            st.warning('⚠ Xəta: Hörmətli müştəri binanın ümumi mərtəbəsi evin mərtəbəsindən kiçik ola bilməz.')
        else:
            yeni_tikili_value = 1 if yeni_tikili == "Bəli" else 0
            təmirli_value = 1 if təmirli == "Bəli" else 0
            kupçalı_value = 1 if kupçalı == "Bəli" else 0
            ipoteka_value = 1 if ipoteka == "Bəli" else 0

            # Prepare input data
            input_data = pd.DataFrame({
                'yer': [yer],  # Ensure location is encoded appropriately if necessary
                'otaq_sayı': [otaqlar],
                'sahə': [kvadrat],
                'mərtəbə_faktiki': [mərtəbə_fakt],
                'mərtəbə_bina': [mərtəbə_bina],
                'yeni_tikili': [yeni_tikili_value],
                'təmirli': [təmirli_value],
                'kupçalı': [kupçalı_value],
                'ipoteka': [ipoteka_value]
            })

            input_data['mərtəbə_faktiki'] = input_data['mərtəbə_faktiki'].astype('int')
            input_data['mərtəbə_bina'] = input_data['mərtəbə_bina'].astype('int')
            input_data['ünvan_tipi'] = input_data['yer'].apply(lambda x: str(x).split(' ')[-1]) 
            input_data['mərtəbə_faizi'] = input_data['mərtəbə_faktiki']/input_data['mərtəbə_bina']
            input_data['1_otaq_sahəsi'] = input_data['sahə']/input_data['otaq_sayı']
                    
            if input_data['ünvan_tipi'].iloc[0] == 'm.':
                input_data['ünvan_tipi_m.'] = 1
                input_data['ünvan_tipi_q.'] = 0
                input_data['ünvan_tipi_r.'] = 0
            elif input_data['ünvan_tipi'].iloc[0] == 'r.':
                input_data['ünvan_tipi_m.'] = 0
                input_data['ünvan_tipi_q.'] = 0
                input_data['ünvan_tipi_r.'] = 1
            else:
                input_data['ünvan_tipi_m.'] = 0
                input_data['ünvan_tipi_q.'] = 1
                input_data['ünvan_tipi_r.'] = 0

            with open('scaling_params.pkl', 'rb') as f:
                scaling_params = pickle.load(f)

            columns_to_normalize = ['1_otaq_sahəsi', 'sahə', 'otaq_sayı', 'mərtəbə_faktiki', 'mərtəbə_bina']
            for column in columns_to_normalize:
                min, max = scaling_params[column]['min'], scaling_params[column]['max']
                input_data[column] = (input_data[column] - min) / max

            value_counts = data['yer'].value_counts().reset_index()
            list_others = value_counts[value_counts['count']<50]['yer'].to_list()
            
            for i in ['yer__20 Yanvar m.', 'yer__28 May m.', 'yer__7-ci mikrorayon q.',
                'yer__8 Noyabr m.', 'yer__8-ci kilometr q.', 'yer__8-ci mikrorayon q.',
                'yer__9-cu mikrorayon q.', 'yer__Abşeron r.', 'yer__Avtovağzal m.',
                'yer__Azadlıq Prospekti m.', 'yer__Ağ şəhər q.', 'yer__Badamdar q.',
                'yer__Bakıxanov q.', 'yer__Bayıl q.', 'yer__Biləcəri q.',
                'yer__Binəqədi r.', 'yer__Dərnəgül m.', 'yer__Elmlər Akademiyası m.',
                'yer__Gənclik m.', 'yer__Hövsan q.', 'yer__Həzi Aslanov m.',
                'yer__Həzi Aslanov q.', 'yer__Koroğlu m.', 'yer__Köhnə Günəşli q.',
                'yer__Masazır q.', 'yer__Memar Əcəmi m.', 'yer__Nardaran q.',
                'yer__Neftçilər m.', 'yer__Nizami m.', 'yer__Nizami r.',
                'yer__Nəriman Nərimanov m.', 'yer__Nərimanov r.', 'yer__Nəsimi m.',
                'yer__Nəsimi r.', 'yer__Qara Qarayev m.', 'yer__Qaraçuxur q.',
                'yer__Sabunçu r.', 'yer__Sahil m.', 'yer__Səbail r.',
                'yer__Xalqlar Dostluğu m.', 'yer__Xətai r.', 'yer__Yasamal q.',
                'yer__Yasamal r.', 'yer__Yeni Günəşli q.', 'yer__Yeni Yasamal q.',
                'yer__others', 'yer__İnşaatçılar m.', 'yer__İçəri Şəhər m.',
                'yer__Şah İsmayıl Xətai m.', 'yer__Əhmədli m.', 'yer__Əhmədli q.']:
                input_data[i] = 0

            yer = input_data['yer'].iloc[0]
            if yer in list_others:
                input_data['others'] = 1
            else: 
                input_data[f'yer__{yer}'] = 1

            # SVD - Dimension Reduction
            with open('svd_model.pkl', 'rb') as f:
                svd = pickle.load(f)

            with open('svd_explained_variance.pkl', 'rb') as f:
                explained_variance = pickle.load(f)
            
            yer_columns = [col for col in input_data.columns if col.startswith('yer__')]
            yer_df = input_data[yer_columns]
            new_data_svd = svd.transform(yer_df)  
            yer_svd_df = pd.DataFrame(new_data_svd, columns=[f'yer_svd_{i+1}' for i in range(new_data_svd.shape[1])])
            input_data = pd.concat([input_data.drop(columns=yer_columns), yer_svd_df], axis=1)

            for i in ['kupçalı', 'ipoteka', 'mərtəbə_faizi', 'yer','ünvan_tipi','ünvan_tipi_m.', 'ünvan_tipi_r.',
        'yer_svd_1', 'yer_svd_2']:
                del input_data[i]

            input_data = input_data[['otaq_sayı', 'sahə', 'yeni_tikili', 'təmirli', 'mərtəbə_faktiki','mərtəbə_bina','1_otaq_sahəsi','ünvan_tipi_q.','yer_svd_3','yer_svd_4','yer_svd_5']]

            rf_reg = joblib.load('random_forest_price_model.pkl')

            predictions = rf_reg.predict(input_data)

            min, max = scaling_params['qiymət']['min'], scaling_params['qiymət']['max']
            predictions = (predictions[0] * max) + min

            st.success(f"🎉 Təşəkkür edirik, {name} {surname}! Mənzilin proqnozlaşdırılmış qiyməti: {predictions:.2f} AZN.")