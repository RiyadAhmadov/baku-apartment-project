import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64


# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# # Path to your image
# image_path = r"C:\Users\HP\OneDrive\İş masası\Streamlit\logo1.png"
# image_base64 = image_to_base64(image_path)

# st.sidebar.markdown(
#     f"""
#     <div style="display: flex; justify-content: center;">
#         <img src="data:image/png;base64,{image_base64}" width="230">
#     </div>
#     """,
#     unsafe_allow_html=True
# )

st.set_page_config(page_title="Home Page", page_icon="🏠")


st.sidebar.image("logo1.png", use_container_width = True, width = 5)

data = pd.read_csv('BakuApartmentData.csv', index_col='Unnamed: 0')

# Title Section
st.title("🏠 Mənzillərin Qiymət Proqnozlaşdırılması Layihəsi")

# Introduction Section
st.subheader("📋 Layihə Haqqında")
st.markdown("""
Bu layihə, mənzillərin qiymətlərinin proqnozlaşdırılması üçün hazırlanmışdır. 
Layihənin əsas məqsədi, müxtəlif xüsusiyyətlərə əsaslanaraq mənzilin dəyərini təxmin edə biləcək dəqiq bir maşın öyrənməsi modeli yaratmaqdır.
""")

# Dataset Overview Section
st.subheader("📊 Məlumat Dəstəsi (Dataset)")
st.markdown("""
Layihədə istifadə olunan məlumat dəstəsi aşağıdakı sütunları əhatə edir:

- **price**: Mənzilin satış qiyməti (hədəf dəyişən).
- **location**: Mənzilin yerləşdiyi ərazi.
- **rooms**: Mənzildəki otaq sayı.
- **square**: Mənzilin ümumi sahəsi (m²).
- **floor**: Mənzilin yerləşdiyi mərtəbə.
- **new_building**: Mənzilin yeni tikili olub-olmaması (Bəli/Xeyr).
- **has_repair**: Mənzildə təmirin olub-olmaması (Bəli/Xeyr).
- **has_bill_of_sale**: Satış sənədinin olub-olmaması (Bəli/Xeyr).
- **has_mortgage**: İpoteka imkanının olub-olmaması (Bəli/Xeyr).
""")

# Display a Preview of the Dataset
st.write("🔍 **Məlumat Dəstəsinə Baxış:**")
st.dataframe(data.head())  # Display the first 5 rows of the dataset

# Project Objectives Section
st.subheader("🎯 Layihənin Məqsədi")
st.markdown("""
- **Problemin Təsviri**: Mənzil bazarında qiymətlərin dəyişkənliyi və müxtəlif xüsusiyyətlərin mənzil dəyərinə təsirini anlamaq.
- **Hədəf**: Yuxarıdakı xüsusiyyətlərdən istifadə edərək mənzilin satış qiymətini proqnozlaşdırmaq üçün yüksək performanslı model qurmaq.
""")

# Benefits Section
st.subheader("🌟 Layihənin Faydaları")
st.markdown("""
- **Alıcılar üçün üstünlüklər**: Mənzil alarkən müxtəlif xüsusiyyətlər əsasında qiymətləri müqayisə etməyə kömək edir.
- **Satıcılar üçün üstünlüklər**: Mənzilin bazar dəyərini daha yaxşı anlamağa dəstək olur.
- **Sektor üçün üstünlüklər**: Daşınmaz əmlak bazarında daha məlumatlı qərarlar qəbul edilməsini təmin edir.
""")

# File Download Section
st.markdown("---")
st.write("📥 **Məlumat Dəstəsini Yükləyin:**")

# Create a download button
csv_data = data.to_csv().encode('utf-8')  # Convert the DataFrame to CSV and encode it
st.download_button(
    label="CSV Faylını Yüklə",
    data=csv_data,
    file_name='BakuApartmentData.csv',
    mime='text/csv'
)

# Closing Note
st.markdown("---")
st.write("💡 Daha ətraflı məlumat üçün layihə sənədlərinə baxın və ya əlaqə saxlayın.")
