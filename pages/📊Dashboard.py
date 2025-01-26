import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


# Sample DataFrame (replace with your actual DataFrame)
df = pd.read_csv('BakuApartmentDataset.csv')

for i in ['ipoteka','kupçalı','təmirli','yeni_tikili']:
    df[i] = df[i].apply(lambda x: 'Bəli' if int(x) == 1 else 'Xeyr')

st.sidebar.image("logo1.png", use_container_width = True, width = 5)

# Filter UI components
st.sidebar.title("Filtrlər")

# Filter by qiymət (Price range)
price_min, price_max = int(df['qiymət'].min()), int(df['qiymət'].max())
price_filter = st.sidebar.slider("Qiymət (₼)", min_value=price_min, max_value=price_max, value=(price_min, price_max), format="₼%d")

# Yer filter (Location) with dynamic matching options
# yer_filter = st.sidebar.text_input("Yer", "")
# yer_options = df['yer'].unique()  # Get unique location options from the dataframe
# filtered_yer_options = [yer for yer in yer_options if yer_filter.lower() in yer.lower()]  # Filter options based on input
# yer_selected = st.sidebar.selectbox("Seçimlər", options=filtered_yer_options)

st.sidebar.header("Yer Filter")
yer_filter = st.sidebar.text_input("Yer", "")
yer_options = df['yer'].unique()
filtered_yer_options = [yer for yer in yer_options if yer_filter.lower() in yer.lower()]
select_all = st.sidebar.checkbox("Hamısını seç")  # Checkbox for "Select All"

if select_all:
    yer_selected = filtered_yer_options  # Select all filtered options
else:
    yer_selected = st.sidebar.multiselect("Seçimlər", options=filtered_yer_options, default=[])
# yer_filter = st.sidebar.multiselect('Yer', options=df['yer'].unique(), default=df['yer'].unique())


# Filter by otaq_sayı (Number of rooms)
otaq_sayı_min, otaq_sayı_max = int(df['otaq_sayı'].min()), int(df['otaq_sayı'].max())
otaq_sayı_filter = st.sidebar.slider("Otaq Sayı", min_value=otaq_sayı_min, max_value=otaq_sayı_max, value=(otaq_sayı_min, otaq_sayı_max))

# Filter by sahə (Area)
sahə_min, sahə_max = int(df['sahə'].min()), int(df['sahə'].max())
sahə_filter = st.sidebar.slider("Sahə (m²)", min_value=sahə_min, max_value=sahə_max, value=(sahə_min, sahə_max), format="%d m²")

# Mərtəbə filter (Floor)
mertebe_min, mertebe_max = int(df['mərtəbə_faktiki'].min()), int(df['mərtəbə_faktiki'].max())
mertebe_filter = st.sidebar.slider("Evin Mərtəbəsi", min_value=mertebe_min, max_value=mertebe_max, value=(mertebe_min, mertebe_max))


# Bina Mərtəbə filter (Floor)
mertebeb_min, mertebeb_max = int(df['mərtəbə_bina'].min()), int(df['mərtəbə_bina'].max())
mertebeb_filter = st.sidebar.slider("Binanın Mərtəbəsi", min_value=mertebeb_min, max_value=mertebeb_max, value=(mertebeb_min, mertebeb_max))


# Multiple choice filters
yeni_tikili_filter = st.sidebar.multiselect('Yeni Tikili', options=['Bəli', 'Xeyr'], default=['Bəli', 'Xeyr'])
təmirli_filter = st.sidebar.multiselect('Təmirli', options=['Bəli', 'Xeyr'], default=['Bəli', 'Xeyr'])
kupçalı_filter = st.sidebar.multiselect('Kupçalı', options=['Bəli', 'Xeyr'], default=['Bəli', 'Xeyr'])
ipoteka_filter = st.sidebar.multiselect('İpoteka', options=['Bəli', 'Xeyr'], default=['Bəli', 'Xeyr'])

# ipoteka_filter = st.sidebar.radio(
#     'İpoteka', 
#     options=['Bəli', 'Xeyr'], 
#     index= 0  # This sets the default option to 'Bəli'
# )

# Apply filters to the DataFrame
filtered_df = df[
    (df['qiymət'] >= price_filter[0]) & (df['qiymət'] <= price_filter[1]) &
    (df['otaq_sayı'] >= otaq_sayı_filter[0]) & (df['otaq_sayı'] <= otaq_sayı_filter[1]) &
    (df['sahə'] >= sahə_filter[0]) & (df['sahə'] <= sahə_filter[1]) &
    (df['yer'].isin(yer_selected)) &
    # (df['yer'].isin(yer_filter)) &
    (df['mərtəbə_faktiki'] >= mertebe_filter[0]) & (df['mərtəbə_faktiki'] <= mertebe_filter[1]) &
    (df['mərtəbə_bina'] >= mertebeb_filter[0]) & (df['mərtəbə_bina'] <= mertebeb_filter[1]) &
    (df['yeni_tikili'].isin(yeni_tikili_filter)) &
    (df['təmirli'].isin(təmirli_filter)) &
    (df['kupçalı'].isin(kupçalı_filter)) &
    (df['ipoteka'].isin(kupçalı_filter))    
    # (df['ipoteka'] == ipoteka_filter)
]

# Helper function to create a bar chart
def create_bar_chart_45(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='darkgreen',
                line=dict(color='white', width=0.2)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.1,
        xaxis=dict(title=x_title, tickangle=45, tickfont=dict(size=14, family='Arial', color='white')),
        yaxis=dict(title=y_title, tickfont=dict(size=14, family='Arial', color='white')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=80, b=110)
    )
    return fig

def create_bar_chart(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='darkgreen',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=24, family='Verdana', color='white'),
        title_x=0.1,
        xaxis=dict(title=x_title, tickfont=dict(size=14, family='Arial', color='white')),
        yaxis=dict(title=y_title, tickfont=dict(size=14, family='Arial', color='white')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=80, b=110)
    )
    return fig

def create_bar_chart_head(x_data, y_data, title, x_title, y_title):
    fig = go.Figure(data=[
        go.Bar(
            x=x_data,
            y=y_data,
            marker=dict(
                color='darkgreen',
                line=dict(color='white', width=0.07)
            )
        )
    ])
    fig.update_layout(
        title=title,
        title_font=dict(size=22, family='Verdana', color='white'),
        title_x=0.04,
        xaxis=dict(title=x_title, tickfont=dict(size=14, family='Arial', color='white')),
        yaxis=dict(title=y_title, tickfont=dict(size=14, family='Arial', color='white')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        margin=dict(l=70, r=50, t=80, b=110)
    )
    return fig


# Grouping data
grouped_data_yer = filtered_df.groupby('yer')['qiymət'].mean()
grouped_data_otaq = filtered_df.groupby('otaq_sayı')['qiymət'].mean()
grouped_data_sahə = filtered_df.groupby('sahə')['qiymət'].mean()
grouped_data_mərtəbə = filtered_df.groupby('mərtəbə_faktiki')['qiymət'].mean()
grouped_data_tikili = filtered_df.groupby('yeni_tikili')['qiymət'].mean()

# Creating all the charts
fig1 = create_bar_chart_45(grouped_data_yer.index, grouped_data_yer.values, 'Yerlər üzrə evlərin ortalama qiymətləri', 'Yer', 'Orta Qiymət')
fig2 = create_bar_chart(grouped_data_otaq.index, grouped_data_otaq.values, 'Otaq sayı üzrə evlərin ortalama qiymətləri', 'Otaq Sayı', 'Orta Qiymət')
fig3 = create_bar_chart(grouped_data_sahə.index, grouped_data_sahə.values, 'Sahə üzrə evlərin ortalama qiymətləri', 'Sahə', 'Orta Qiymət')
fig4 = create_bar_chart(grouped_data_mərtəbə.index, grouped_data_mərtəbə.values, 'Mərtəbə üzrə evlərin ortalama qiymətləri', 'Mərtəbə', 'Orta Qiymət')
fig5 = create_bar_chart_head(grouped_data_tikili.index, grouped_data_tikili.values, 'Yeni / Köhnə Tikili üzrə evlərin ortalama qiymətləri', 'Yeni Tikili', 'Orta Qiymət')

# 6. Comparison of prices based on `yer` and `yeni_tikili`
grouped_data_yer_tikili = filtered_df.groupby(['yer', 'yeni_tikili'])['qiymət'].mean().unstack()

fig6 = go.Figure()

# Check if both 'Bəli' and 'Xeyr' are available in the data
if 'Bəli' in grouped_data_yer_tikili and 'Xeyr' in grouped_data_yer_tikili:
    grouped_data_yer_tikili = grouped_data_yer_tikili.sort_values(by='Bəli', ascending=False)
    fig6.add_trace(go.Bar(name='Yeni Tikili', x=grouped_data_yer_tikili.index, y=grouped_data_yer_tikili['Bəli'], marker_color='darkgreen'))
    fig6.add_trace(go.Bar(name='Köhnə Tikili', x=grouped_data_yer_tikili.index, y=grouped_data_yer_tikili['Xeyr'], marker_color='darkred'))
# Check if only 'Bəli' is available
elif 'Bəli' in grouped_data_yer_tikili:
    grouped_data_yer_tikili = grouped_data_yer_tikili.sort_values(by='Bəli', ascending=False)
    fig6.add_trace(go.Bar(name='Yeni Tikili', x=grouped_data_yer_tikili.index, y=grouped_data_yer_tikili['Bəli'], marker_color='darkgreen'))
# Check if only 'Xeyr' is available
elif 'Xeyr' in grouped_data_yer_tikili:
    grouped_data_yer_tikili = grouped_data_yer_tikili.sort_values(by='Xeyr', ascending=False)
    fig6.add_trace(go.Bar(name='Köhnə Tikili', x=grouped_data_yer_tikili.index, y=grouped_data_yer_tikili['Xeyr'], marker_color='darkred'))

# Update layout for the plot
fig6.update_layout(
    title='Yerlər üzrə Yeni və Köhnə Tikili evlərin qiymətləri',
    title_font=dict(size=22, family='Verdana', color='white'),
    title_x=0.09,
    xaxis=dict(title='Yer', tickangle=45, tickfont=dict(size=14, family='Arial', color='white')),
    yaxis=dict(title='Orta Qiymət', tickfont=dict(size=14, family='Arial', color='white')),
    barmode='group',
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=70, r=50, t=80, b=110)
)


# # 7. Distribution of prices across different `otaq_sayı`
# fig7 = go.Figure(data=[
#     go.Histogram(x=filtered_df['otaq_sayı'], y=filtered_df['qiymət'], nbinsx=10)
# ])
# fig7.update_layout(
#     title='Otaq Sayı üzrə qiymətlərin bölgüsü',
#     title_font=dict(size=24, family='Verdana', color='white'),
#     title_x=0.1,
#     xaxis=dict(title='Otaq Sayı', tickfont=dict(size=14, family='Arial', color='white')),
#     yaxis=dict(title='Qiymət', tickfont=dict(size=14, family='Arial', color='white')),
#     plot_bgcolor='black',
#     paper_bgcolor='black',
#     margin=dict(l=70, r=50, t=80, b=110)
# )

# # 9. Comparison of prices by `mərtəbə_faktiki` (Floor level)
# fig9 = create_bar_chart(grouped_data_mərtəbə.index, grouped_data_mərtəbə.values, 'Mərtəbə üzrə evlərin qiymətləri', 'Mərtəbə', 'Orta Qiymət')



# 8. Price correlation with `sahə` (Area)
fig8 = go.Figure(data=[
    go.Scatter(x=filtered_df['sahə'], y=filtered_df['qiymət'], mode='markers', marker=dict(color='blue'))
])
fig8.update_layout(
    title='Sahə üzrə qiymətlərin korelasyonu',
    title_font=dict(size=24, family='Verdana', color='white'),
    title_x=0.1,
    xaxis=dict(title='Sahə', tickfont=dict(size=14, family='Arial', color='white')),
    yaxis=dict(title='Qiymət', tickfont=dict(size=14, family='Arial', color='white')),
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=70, r=50, t=80, b=110)
)

# 10. Average price per square meter in each city (`yer`)
fig10 = filtered_df.groupby('yer').apply(lambda x: (x['qiymət'] / x['sahə']).mean())
fig10_chart = create_bar_chart_45(fig10.index, fig10.values, 'Hər kvadrat metr üzrə qiymət', 'Yer', 'Qiymət per m²')

# 11. Correlation between `otaq_sayı` and `sahə`
fig11 = go.Figure(data=[
    go.Scatter(x=filtered_df['otaq_sayı'], y=filtered_df['sahə'], mode='markers', marker=dict(color='red'))
])
fig11.update_layout(
    title='Otaq Sayı ilə Sahə arasındakı korelasiya',
    title_font=dict(size=24, family='Verdana', color='white'),
    title_x=0.1,
    xaxis=dict(title='Otaq Sayı', tickfont=dict(size=14, family='Arial', color='white')),
    yaxis=dict(title='Sahə', tickfont=dict(size=14, family='Arial', color='white')),
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=70, r=50, t=80, b=110)
)

# 12. Distribution of `qiymət` based on the `yeni_tikili` column
fig12 = go.Figure(data=[
    go.Box(y=filtered_df[filtered_df['yeni_tikili'] == 'Bəli']['qiymət'], name='Yeni Tikili', boxmean='sd'),
    go.Box(y=filtered_df[filtered_df['yeni_tikili'] == 'Xeyr']['qiymət'], name='Köhnə Tikili', boxmean='sd')
])
fig12.update_layout(
    title='Yeni və Köhnə Tikili üzrə Qiymətlərin Bölgüsü',
    title_font=dict(size=24, family='Verdana', color='white'),
    title_x=0.1,
    xaxis=dict(title='Yeni Tikili', tickfont=dict(size=14, family='Arial', color='white')),
    yaxis=dict(title='Qiymət', tickfont=dict(size=14, family='Arial', color='white')),
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=70, r=50, t=80, b=110)
)

fig13 = go.Figure()
for i in filtered_df['otaq_sayı'].unique():
    fig13.add_trace(
        go.Box(
            y=filtered_df[filtered_df['otaq_sayı'] == i]['qiymət'],
            name=f'{i}', 
            boxmean='sd'  # Show mean and standard deviation
        )
    )

fig13.update_layout(
    title='Otaq sayları üzrə Qiymətlərin Bölgüsü',
    title_font=dict(size=24, family='Verdana', color='white'),
    title_x=0.1,
    xaxis=dict(title='Otaq Sayı', tickfont=dict(size=14, family='Arial', color='white')),
    yaxis=dict(title='Qiymət', tickfont=dict(size=14, family='Arial', color='white')),
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=70, r=50, t=80, b=110)
)


filtered_df1 = filtered_df.copy()
bins = [0, 150, 300, 450, 600, 750, 900, float('inf')]
labels = ['0-150 m²','150-300 m²','300-450 m²','450-600 m²','600-750 m²','750-900 m²','900+ m²']
filtered_df1['sahə_cut'] = pd.cut(filtered_df['sahə'], bins, labels=labels)


fig14 = go.Figure()
for i in filtered_df1['sahə_cut'].unique():
    fig14.add_trace(
        go.Box(
            y=filtered_df1[filtered_df1['sahə_cut'] == i]['qiymət'],
            name=f'{i}', 
            boxmean='sd'  # Show mean and standard deviation
        )
    )

fig14.update_layout(
    title='Sahələrin kateqoriyaları üzrə Qiymətlərin Bölgüsü',
    title_font=dict(size=22, family='Verdana', color='white'),
    title_x=0.01,
    xaxis=dict(title='Sahənin kateqoriyası', tickfont=dict(size=14, family='Arial', color='white')),
    yaxis=dict(title='Qiymət', tickfont=dict(size=14, family='Arial', color='white')),
    plot_bgcolor='black',
    paper_bgcolor='black',
    margin=dict(l=70, r=50, t=80, b=110)
)

# Streamlit app layout
st.title("🏠 Ev Qiymətlərinin Analizi")

formatted_mean = f"₼{df['qiymət'].mean():,.2f}"
max_binamertebe = df['mərtəbə_bina'].max()
average_area = f"{df['sahə'].mean():,.2f} m²" 

def metric_card(label, value):
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 10px; background-color:rgb(2, 13, 24);">
            <p style="font-size: 18px; color:rgb(0, 107, 14); font-weight: bold; margin: 0;">{label}</p>
            <p style="font-size: 24px; color:rgb(255, 223, 223); margin: 0;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display metrics in columns
col1, col2, col3 = st.columns(3)

with col1:
    metric_card("Ortalama Qiymət", formatted_mean)

with col2:
    metric_card("Maksimum Mərtəbə Sayı", max_binamertebe)

with col3:
    metric_card("Ortalama Mənzil Sahəsi", average_area)

st.header('📍 Yerlər Üzrə Analiz')

st.write(f""">Verilmiş datasetdə toplamda <strong style='color: green;'>{df['yer'].nunique()}</strong> sayda yer var. 
Bunlar arasında <strong style='color: green;'>{df[df['ünvan_tipi']=='m.']['yer'].nunique()}</strong> sayda metro, 
<strong style='color: green;'>{df[df['ünvan_tipi']=='r.']['yer'].nunique()}</strong> sayda rayon, 
<strong style='color: green;'>{df[df['ünvan_tipi']=='q.']['yer'].nunique()}</strong> sayda qəsəbə var.""", 
unsafe_allow_html=True)


st.subheader('📊 Ümumi elan sayı:')
# Display metrics in columns
col1, col2, col3 = st.columns(3)

rayon = df[df['ünvan_tipi']=='r.']['yer'].shape[0]
metro = df[df['ünvan_tipi']=='m.']['yer'].shape[0]
qesebe = df[df['ünvan_tipi']=='q.']['yer'].shape[0]

with col1:
    metric_card("Rayon", rayon)

with col2:
    metric_card("Qəsəbə", metro)

with col3:
    metric_card("Metro", qesebe)

st.subheader('🏠 Evlərin ortalama qiymətləri:')

st.write('>İndi isə gəlin, yerlər üzrə evlərin ortalama qiymətlərinə baxaq:')


if filtered_df['yer'].nunique() < 10 and filtered_df['yer'].nunique() > 0: 
    st.write(
        f"İlk olaraq <strong style='color: green;'>{','.join(filtered_df['yer'].unique())}</strong> üzrə evlərin ortalama qiymətləri (barchart):", 
        unsafe_allow_html=True
        )
elif filtered_df['yer'].nunique() == df['yer'].nunique(): 
    st.write(f'İlk olaraq bütün yerlər üzrə evlərin ortalama qiymətləri (sütun qrafiki):')
elif filtered_df['yer'].nunique() < df['yer'].nunique() and filtered_df['yer'].nunique() > 0: 
    st.write(
            f"İlk olaraq <strong style='color: green;'>{filtered_df['yer'].nunique()}</strong> yer üzrə evlərin ortalama qiymətləri (barchart):", 
            unsafe_allow_html=True
            )
else:
    st.write(f'Zəhmət olmasa yer seçin.')

st.plotly_chart(fig1)

df1 = df.groupby(by = ['yer'])['qiymət'].mean().reset_index()
df1['tip'] = df1['yer'].apply(lambda x: str(x).split()[-1])
df1['qiymət'] = df1['qiymət'].apply(lambda x: round(x,1))
yer_q_min = df1[df1['tip'] == 'q.'][df1[df1['tip'] == 'q.']['qiymət'] == df1[df1['tip'] == 'q.']['qiymət'].min()]['yer'].iloc[0]
yer_q_max = df1[df1['tip'] == 'q.'][df1[df1['tip'] == 'q.']['qiymət'] == df1[df1['tip'] == 'q.']['qiymət'].max()]['yer'].iloc[0]
yer_r_min = df1[df1['tip'] == 'r.'][df1[df1['tip'] == 'r.']['qiymət'] == df1[df1['tip'] == 'r.']['qiymət'].min()]['yer'].iloc[0]
yer_r_max = df1[df1['tip'] == 'r.'][df1[df1['tip'] == 'r.']['qiymət'] == df1[df1['tip'] == 'r.']['qiymət'].max()]['yer'].iloc[0]
yer_m_min = df1[df1['tip'] == 'm.'][df1[df1['tip'] == 'm.']['qiymət'] == df1[df1['tip'] == 'm.']['qiymət'].min()]['yer'].iloc[0]
yer_m_max = df1[df1['tip'] == 'm.'][df1[df1['tip'] == 'm.']['qiymət'] == df1[df1['tip'] == 'm.']['qiymət'].max()]['yer'].iloc[0]


st.header('📊 Analitik Baxış:')

st.write(f""">Rayonlar üzrə minimum ortalama məbləğ <strong style='color: green;'>{yer_r_min}</strong> səviyyəsində qeydə alınıb. 
Əlavə olaraq, maksimum ortalama məbləğ <strong style='color: green;'>{yer_r_max}</strong> səviyyəsində qeydə alınıb.""", unsafe_allow_html=True)

st.write(f""">Metrolar üzrə isə minimum ortalama məbləğ <strong style='color: green;'>{yer_m_min}</strong> səviyyəsində qeydə alınıb. 
Əlavə olaraq, maksimum ortalama məbləğ <strong style='color: green;'>{yer_m_max}</strong> səviyyəsində qeydə alınıb.""", unsafe_allow_html=True)

st.write(f""">Qəsəbələr üzrə minimum ortalama məbləğ <strong style='color: green;'>{yer_q_min}</strong> səviyyəsində qeydə alınıb. 
Əlavə olaraq, maksimum ortalama məbləğ <strong style='color: green;'>{yer_q_max}</strong> səviyyəsində qeydə alınıb.""", unsafe_allow_html=True)

qesebe = df1[df1['tip'] == 'q.']
qesebe['x'] = qesebe["qiymət"].apply(lambda x: str(round((x/qesebe['qiymət'].min()),1)) + 'x')
qesebe_sorted = qesebe.sort_values(by='x',ascending = False).reset_index(drop = True)[['yer','qiymət','x']]

rayon = df1[df1['tip'] == 'r.']
rayon['x'] = rayon["qiymət"].apply(lambda x: str(round((x/rayon['qiymət'].min()),1)) + 'x')
rayon_sorted = rayon.sort_values(by='x',ascending = False).reset_index(drop = True)[['yer','qiymət','x']]

metro = df1[df1['tip'] == 'm.']
metro['x'] = metro["qiymət"].apply(lambda x: str(round((x/metro['qiymət'].min()),1)) + 'x')
metro_sorted = metro.sort_values(by='x',ascending = False).reset_index(drop = True)[['yer','qiymət','x']]

st.write(f""">Gəlin indi qəsəbələrin ortalama mənzil qiymətlərinin minimumdan 
(<strong style='color: green;'>{yer_q_min}</strong> - <strong style='color: green;
'>{df1[df1['tip'] == 'q.']['qiymət'].min().round(1)} ₼</strong>) neçə x fərqləndiyinə baxaq:""",unsafe_allow_html=True)

qesebe_sorted.columns = ['Yer','Ortalama Evin Qiyməti (₼)','Minimumla Müqayisə']
qesebe_sorted

st.write(f""">Gəlin indi rayonların ortalama mənzil qiymətlərinin minimumdan 
(<strong style='color: green;'>{yer_r_min}</strong> - <strong style='color: green;
'>{df1[df1['tip'] == 'r.']['qiymət'].min().round(1)} ₼</strong>) neçə x fərqləndiyinə baxaq:""",unsafe_allow_html=True)

rayon_sorted.columns = ['Yer','Ortalama Evin Qiyməti (₼)','Minimumla Müqayisə']
rayon_sorted

st.write(f""">Gəlin indi isə metroların ortalama mənzil qiymətlərinin minimumdan 
(<strong style='color: green;'>{yer_m_min}</strong> - <strong style='color: green;
'>{df1[df1['tip'] == 'm.']['qiymət'].min().round(1)} ₼</strong>) neçə x fərqləndiyinə baxaq:""",unsafe_allow_html=True)

metro_sorted.columns = ['Yer','Ortalama Evin Qiyməti (₼)','Minimumla Müqayisə']
metro_sorted


# --------------

st.header('🏠 Otaq Sayları Üzrə Analiz:')

st.write(f""">Verilmiş datasetdə maksimum <strong style='color: green;'>{df['otaq_sayı'].max()}</strong> otaqlı mənzil var. 
Minimum isə <strong style='color: green;'>{df['otaq_sayı'].min()}</strong> otaqlı mənzil var.""",
unsafe_allow_html=True)

st.subheader('📊 Ümumi elan sayı:')

otaq_sayı = df.groupby(by='otaq_sayı').agg(
    Ortalama_Qiymət=('qiymət', 'mean'), 
    Elan_Sayı=('qiymət', 'count')
).reset_index()

otaq_sayı.columns = ['Otaq Sayı','Ortalama Evin Qiyməti (₼)','Elan Sayı']
otaq_sayı[['Otaq Sayı','Elan Sayı']]

st.write('>İndi isə, otaq sayına görə evlərin ortalama qiymətlərinə nəzər salaq:')

st.plotly_chart(fig2)

st.header('📊 Analitik Baxış:')

st.write(f""">Təbii olaraq, otaq sayı artdıqca mənzilin ortalama qiyməti də yüksəlir. Lakin istisna olaraq, <strong style='color: green;'>12</strong> otaqlı <strong style='color: green;'>1</strong> mənzildə daha aşağı ortalama məbləğ qeydə alınıb. 
Verilmiş <strong style='color: green;'>15</strong> otaqlı <strong style='color: green;'>1</strong> mənzildə isə daha yüksək ortalama qiymət müşahidə olunub. 
<strong style='color: green;'> (Bunların başlıca səbəbləri: sahə, yer və digər faktorlardır.)</strong>""", unsafe_allow_html=True)

st.write(f""">Həmçinin, otaq sayı <strong style='color: green;'>20</strong> olan <strong style='color: green;'>1</strong> mənzilin ortalama qiyməti kəskin dəyişməyib.""", unsafe_allow_html=True)

st.header('Otaqlar üzrə qiymətlərin dağılımlarına baxaq:')

st.plotly_chart(fig13)

st.write(f""">İndi isə otaqlar üzrə <strong style='color: green;'>coeffeicient of variance</strong> tapaq.""",unsafe_allow_html=True)

agg_df = df.groupby(by='otaq_sayı').agg(qiymət_std=('qiymət', 'std'), qiymət_mean=('qiymət', 'mean'), qiymət_sayı=('qiymət','count')).reset_index()
agg_df['qiymət_cov'] = (100 * (agg_df['qiymət_std'] / agg_df['qiymət_mean'])).round(2)
agg_df['qiymət_cov1'] = (100 * (agg_df['qiymət_std'] / agg_df['qiymət_mean'])).round(2).astype(str) + '%'
agg_df['qiymət_std1'] = agg_df['qiymət_std'].round(2).astype(str) + ' ₼'
agg_df['qiymət_mean1'] = agg_df['qiymət_mean'].round(2).astype(str) + ' ₼'

agg_df = agg_df.rename(columns={
    'otaq_sayı': 'Otaq Sayı',
    'qiymət_std1': 'Qiymət Standart Sapma',
    'qiymət_mean1': 'Qiymət Ortalama',
    'qiymət_cov1': 'Qiymət Dəyişkənlik Əmsalı',
    'qiymət_sayı': 'Mənzillərin Sayı'
})
agg_df = agg_df[agg_df['Mənzillərin Sayı']>2]
agg_df[['Otaq Sayı', 'Mənzillərin Sayı', 'Qiymət Standart Sapma', 'Qiymət Ortalama', 'Qiymət Dəyişkənlik Əmsalı']]

st.write(f""">Məlumat onu göstərir ki, ən çox qiymət dəyişkənliyi otaqlarının sayı <strong style='color: green;'>{agg_df[agg_df['qiymət_cov'] == agg_df['qiymət_cov'].max()]['Otaq Sayı'].iloc[0]}
</strong> olan mənzillərdə <strong style='color: green;'>{agg_df[agg_df['qiymət_cov'] == agg_df['qiymət_cov'].max()]['Qiymət Dəyişkənlik Əmsalı'].iloc[0]}</strong> olaraq müəyyən edilib.""",unsafe_allow_html=True)
st.write(f""">Digər tərəfdən ən az qiymət dəyişkənliyi otaqlarının sayı <strong style='color: green;'>{agg_df[agg_df['qiymət_cov'] == agg_df['qiymət_cov'].min()]['Otaq Sayı'].iloc[0]}
</strong> olan mənzillərdə <strong style='color: green;'>{agg_df[agg_df['qiymət_cov'] == agg_df['qiymət_cov'].min()]['Qiymət Dəyişkənlik Əmsalı'].iloc[0]}</strong> olaraq müəyyən edilib.""",unsafe_allow_html=True)




st.subheader('Otaq Sayı ilə Qiymət Arasındakı Korelasiya (Scatter Qrafiki Üzrə):')
st.write(f""">Gəlin indi isə, otaq sayları ilə qiymət arasında olan əlaqəyə scatter qrafik üzərində baxaq.""")

st.plotly_chart(fig11)

st.write(f""">Aydın görünür ki, otaq sayı ilə qiymət düz mütənasib asılıdır. (Digər faktorların təsiri çox güclüdür hansı ki, qrafik tam olaraq düz mütənasib görünmür)""")

# --------------

st.header('Evin Sahəsi üzrə Analiz: 📊')

st.write(f""">Verilmiş datasetdə maksimum <strong style='color: green;'>{df['sahə'].max()}m²</strong> sahəli mənzil var. 
Minimum isə <strong style='color: green;'>{df['sahə'].min()}m²</strong> sahəli mənzil var.""",
unsafe_allow_html=True)

st.subheader('Sahələr Üzrə Evlərin Ortalama Qiymətləri: 🏡')

st.write(f""">Qrafikdən görünürki evin sahəsinə görə ortalama qiymət xətti olaraq artır.""")
st.plotly_chart(fig3)

# bins = [0, 150, 300, 450, 600, 750, 900, float('inf')]
# labels = ['0-150 m²','150-300 m²','300-450 m²','450-600 m²','600-750 m²','750-900 m²','900+ m²']
# df['sahə_cut'] = pd.cut(df['sahə'], bins, labels=labels)

st.subheader('Sahənin Kateqoriyaları: 📏')

st.write(f""">Gəlin indi isə, sahələri kateqoriyalara bölək və qiymətin dağılımlarına baxaq:""")
st.plotly_chart(fig14)
st.write(f""">Tendensiyanı rahat görə bilirik, belə ki sahə artıqca evin qiyməti də birmənalı olaraq artıq (digər təsirlər eyni olduqda).""")

st.subheader('Sahənin Korelasyonu (Scatter Qrafik Üzrə): 🔍')

st.write(f""">Gəlin indi isə, sahələr ilə qiymət arasında olan əlaqəyə scatter qrafik üzərində baxaq.""")

st.plotly_chart(fig8)

st.write(f""">Aydın görünür ki, sahə ilə qiymət düz mütənasib asılıdır.""")

st.subheader('1 Kvadrat Metr üzrə Evlərin Qiyməti: 💰')

st.write(f""">İndi isə, daha yaxşı müqayisə aparmaq üçün hər yerdə evlərin 1 m² üzrə ortalama qiymətlərinə baxaq.""")

st.plotly_chart(fig10_chart)

fig10 = df.groupby('yer').apply(lambda x: (x['qiymət'] / x['sahə']).mean())
fig10 = fig10.reset_index()
fig10.columns = ['Yer','1 m² düşən məbləğ']
fig10['1 m² düşən məbləğ'] = fig10['1 m² düşən məbləğ'].round(2)


st.write(f""">Evin 1 m² ən baha olan yer <strong style='color: green;'>{fig10[fig10['1 m² düşən məbləğ'] == fig10['1 m² düşən məbləğ'].max()]['Yer'].iloc[0]}
</strong>, harada ki, 1 m² qiyməti <strong style='color: green;'>{fig10['1 m² düşən məbləğ'].max()}₼</strong> olaraq müşahidə olunur.""",unsafe_allow_html=True)

st.write(f""">Evin 1 m² ən ucuz olduğu yer isə <strong style='color: green;'>{fig10[fig10['1 m² düşən məbləğ'] == fig10['1 m² düşən məbləğ'].min()]['Yer'].iloc[0]}
</strong>, harada ki, 1 m² qiyməti <strong style='color: green;'>{fig10['1 m² düşən məbləğ'].min()}₼</strong> olaraq müşahidə olunur.""",unsafe_allow_html=True)

# --------------

st.header('Mərtəbələr Üzrə Analiz 🏢')
st.subheader('Mərtəbələr Üzrə Evlərin Ortalama Qiyməti: 💵')

st.plotly_chart(fig4)

st.write(f""">Əslində yuxarı mərtəbəli evlərin qiyməti normalda ucuz olmalıdır. Verilmiş qrafik isə evlərin mərtəbələrinin onların ortalama 
qiymətləri ilə düz mütənasib olduğunu göstərilir.""")

st.write(f""">Amma təbii ki burda başqa faktorlar var. Filterləri tənzimlədiyimizdə görürük ki əslində qiymətlər uniforma yaxındır. Çünki düşünək ki, yüksək mərtəbəli mənzillər
yeni tikilən binalarda olur və bu o deməkdir ki onlar daha yeni mənzillərdir. Bu səbəbdən aşağı mənzilli evlərin qiymətləri kəskin üstünlük göstərə bilmir ~ çünki onların tərkibində
köhnə tikililər (4, 5-mərtəbəli binalar) var.""")



# --------------
st.header('Yeni / Köhnə Tikili Üzrə Analiz 🏚️')
st.subheader('Yeni / Köhnə Tikili Üzrə Evlərin Ortalama Qiyməti: 💲')

st.plotly_chart(fig5)

value = round(df.groupby(by = 'yeni_tikili').agg({'qiymət':'mean'}).reset_index()['qiymət'].iloc[0] / 
df.groupby(by = 'yeni_tikili').agg({'qiymət':'mean'}).reset_index()['qiymət'].iloc[1], 2)

st.write(f""">Yeni tikili olan evlərin ortalama qiymətləri köhnə tikililərdən <strong style='color: green;'>{value}x</strong> dəfə çoxdur.""",unsafe_allow_html=True)

st.write(f""">İndi isə yerlər üzrə köhnə tikililərin qiymətinin yeni tikililərin qiymətindən nə qədər fərqləndiyini analiz edək.""")


x= df.groupby(by = ['yer','yeni_tikili'])['qiymət'].mean().reset_index()
x['yeni_tikili'] = x['yeni_tikili'].apply(lambda x: 'Yeni Tikili' if x == 'Bəli' else 'Köhnə Tikili')
grouped_data = x.groupby(['yer', 'yeni_tikili'])['qiymət'].mean().unstack()
grouped_data['qiymət_nisbəti'] = grouped_data['Yeni Tikili'] / grouped_data['Köhnə Tikili']
grouped_data['qiymət_nisbəti'] = grouped_data['qiymət_nisbəti'].round(2) 
result = grouped_data.reset_index()
result.columns = ['Yer','Köhnə Tikili', 'Yeni Tikili', 'Qiymət Nisbəti']
result = result[~pd.isna(result['Qiymət Nisbəti'])]
result

st.write(f""">Cədvəldən görünür ki, yerlər üzrə <strong style='color: green;'>{result[result['Qiymət Nisbəti'] == 
result['Qiymət Nisbəti'].max()]['Yer'].iloc[0]}</strong> <strong style='color: green;'>({result['Qiymət Nisbəti'].max()}x)</strong> yerləşən mənzillərin 
yeni/köhnə qiymət fərqlərində ciddi fərq var. Minimum fərq isə <strong style='color: green;'>{result[result['Qiymət Nisbəti'] == 
result['Qiymət Nisbəti'].min()]['Yer'].iloc[0]}</strong> <strong style='color: green;'>({result['Qiymət Nisbəti'].min()}x)</strong> görünür.
""",unsafe_allow_html=True)

st.write(f""">Toplamda <strong style='color: green;'>{result[result['Qiymət Nisbəti'] < 1].shape[0]} ({', '.join(result[result['Qiymət Nisbəti'] < 1]['Yer'])})</strong>  sayda yerdə köhnə tikililərin ortalama 
qiyməti yeni tikililərin ortalama qiymətindən çoxdur. (Təbii ki başqa faktorlarda var: belə ki, otaq sayı, mənzilin sahəsi və.s)""",unsafe_allow_html=True)


st.subheader('Yeni / Köhnə Tikililərin Yerlər Üzrə Evlərin Ortalama Qiyməti: 📍🏚️')

st.write('Yeni və köhnə tikili evlərin yerlər üzrə ortalama qiymətlərini aşağıdakı qrafikdə görə bilərik.')

st.plotly_chart(fig6)


grouped_data_yer_tikili = df.groupby(['yer', 'yeni_tikili'])['qiymət'].count().unstack()
grouped_data_yer_tikili.fillna(0, inplace = True)
grouped_data_yer_tikili['Toplam'] = grouped_data_yer_tikili['Bəli'] + grouped_data_yer_tikili['Xeyr']
grouped_data_yer_tikili['Yeni Tikili Elanların Faizi'] = 100*(grouped_data_yer_tikili['Bəli']/grouped_data_yer_tikili['Toplam']).round(2)
grouped_data_yer_tikili['Köhnə Tikili Elanların Faizi'] = 100*(grouped_data_yer_tikili['Xeyr']/grouped_data_yer_tikili['Toplam']).round(2)
grouped_data_yer_tikili.reset_index(inplace = True)

# Create a list of dropdown menu options for each `yer`
dropdown_options = []
pie_charts = []

for yer in grouped_data_yer_tikili["yer"].unique():
    # Filter the data for the specific `yer`
    filtered_data = grouped_data_yer_tikili[grouped_data_yer_tikili["yer"] == yer]
    labels = ["Yeni Tikili Elanların Faizi", "Köhnə Tikili Elanların Faizi"]
    values = [
        filtered_data["Yeni Tikili Elanların Faizi"].values[0],
        filtered_data["Köhnə Tikili Elanların Faizi"].values[0]
    ]
    
    # Add a pie chart trace for this `yer`
    pie_charts.append(
        go.Pie(
            labels=labels,
            values=values,
            name=yer,
            textinfo="label+percent",
            hoverinfo="label+percent+name"
        )
    )
    
    # Add a dropdown option for this `yer`
    dropdown_options.append(
        {
            "label": yer,
            "method": "update",
            "args": [
                {"visible": [i == len(pie_charts) - 1 for i in range(len(pie_charts))]},
                {"title": f"Pie Chart for {yer}"}
            ]
        }
    )

# Create the initial figure with all pie charts hidden
fig15 = go.Figure(data=pie_charts)

# Update layout to add the dropdown menu
fig15.update_layout(
    updatemenus=[
        {
            "buttons": dropdown_options,
            "direction": "down",
            "showactive": True,
            "x": 0.1,
            "xanchor": "left",
            "y": 1.15,
            "yanchor": "top",
        }
    ],
    title="Yerlər üzrə Elanlardakı Evlərin Yeni / Köhnə Olmasına Görə Sayı",
    title_font=dict(size=20),
    title_x=0.1,
    paper_bgcolor="black",
    plot_bgcolor="black",
)

# Make only the first pie chart visible initially
for i, trace in enumerate(fig15.data):
    trace.visible = i == 0

st.write(f""">Bu qrafikdən yerlər üzrə yeni və köhnə tikili evlərin elan sayını görmək olar""")

st.plotly_chart(fig15)

st.write(f""">Əlavə olaraq, aşağıdakı cədvəldən ümumi olaraq yerlər üzrə yeni və köhnə tikili evlərin elan sayını görmək olar""")

grouped_data_yer_tikili.columns = ['Yer','Yeni Tikili Elanların Sayı','Köhnə Tikili Elanların Sayı','Toplam Elanların Sayı','Yeni tikili Faizi','Köhnə Tikili Faizi']
grouped_data_yer_tikili



st.subheader('Yeni / Köhnə Tikili Evlərin Qiymət Dağılımı: 📊🏚️')

st.write(f""">Aşağıdakı qrafikdə biz yeni və köhnə tikili evlərin qiymət dağılımına baxa bilərik.""")

st.plotly_chart(fig12)

st.write(f""">Qrafikdən görünür ki, yeni tikili evlər üzrə daha yüksək outlierlar müşahidə olunur.)""",unsafe_allow_html=True)

# --------------
st.header('Yerlər üzrə Xəritə Üzərində Analiz 🏚️')
st.subheader('Elan Sayına görə Yerlərin Sıxlığı: 📢')

# st.plotly_chart(fig16)

long_lat = pd.read_excel('Azerbaijan_Locations_Lat_Long.xlsx')

df = df.merge(long_lat, on = 'yer', how = 'left')

df_group = df.groupby('yer').agg(
    Latitude=('Latitude', 'first'),  # Pick the first latitude for each location
    Longitude=('Longitude', 'first'),  # Pick the first longitude for each location
    Elan_Sayı=('yer', 'count')  # Count the occurrences of each location
).reset_index()

def map_graph(column,title):
    # Create Plotly map with a realistic base map
    fig16 = px.scatter_mapbox(df_group,
                            lat="Latitude",
                            lon="Longitude",
                            hover_name="yer",
                            size=column,  # Adjust marker size by number of announcements
                            color=column,  # Color markers based on number of announcements
                            color_continuous_scale="Viridis",  # Color scale for different levels of announcements
                            title=title,
                            zoom=5,  # Adjust zoom level for better focus
                            mapbox_style="open-street-map",  # Use OpenStreetMap for a realistic map
                            opacity=0.8)

    # Customize map layout
    fig16.update_layout(
        mapbox=dict(
            center=dict(lat=40.4, lon=49.9),  # Center the map on Azerbaijan
            style="open-street-map",  # Use OpenStreetMap style
            zoom=10  # Adjust zoom level
        ),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},  # Adjust margins
        title_font_size=20  # Adjust title font size
    )
    
    # Show the plot in Streamlit
    st.plotly_chart(fig16)

map_graph('Elan_Sayı',"Yerlər üzrə Elan Sayları")

# ========== 

st.subheader('Ortalama Evlərin Qiymətinə görə Yerlərin Göstəriciləri: 💲')

df_group = df.groupby('yer').agg(
    Latitude=('Latitude', 'first'),  # Pick the first latitude for each location
    Longitude=('Longitude', 'first'),  # Pick the first longitude for each location
    Ortalama_Məbləğ=('qiymət', 'mean')  # Count the occurrences of each location
).reset_index()

df_group['Ortalama_Məbləğ'] = df_group['Ortalama_Məbləğ'].round(2)
map_graph('Ortalama_Məbləğ',"Yerlər üzrə Ortalama Məbləğlər")

# ========== 

st.subheader('Yeni Tikililərin Faizinə görə Yerlərin Göstəriciləri: 🏬')

grouped_data_yer_tikili.rename(columns = {'Yer':'yer'}, inplace = True)

grouped_data_yer_tikili = grouped_data_yer_tikili.merge(long_lat, on = 'yer', how = 'left')

df_group = grouped_data_yer_tikili
map_graph('Yeni tikili Faizi',"Yerlər üzrə Yeni tikililərin Faizi")

# ========== 

st.subheader('Yeni / Köhnə Tikililərin Yerlər Üzrə Evlərin Ortalama Qiymətinin Nisbəti: 📍🏚️')

result.rename(columns = {'Yer':'yer'}, inplace = True)

result = result.merge(long_lat, on = 'yer', how = 'left')

df_group = result
map_graph('Qiymət Nisbəti',"Yeni Tikililərin Ortalama Qiymətlərinin Köhnə Tikililərə Olan Nisbəti")










import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server and port
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to send email
def send_email(email_from, app_password, subject, body):
    try:
        # Create email content
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = 'riyadehmedov03@gmail.com'
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Təhlükəsiz bağlantı
            server.login(email_from, app_password)  # App parolundan istifadə olunur
            server.sendmail(email_from, 'riyadehmedov03@gmail.com', msg.as_string())

        return True
    except Exception as e:
        return str(e)

# Streamlit UI
st.header("Dashboard Haqqında Geri Bildirim və Rəy Göndərmə: 📝💬")
st.write(">Bu alət, izləyicilərdən dashboard haqqında rəy və geri bildirim almaq üçün istifadə olunur. Məlumatlarınızı daxil edin və göndərin:")

# Input fields
email_from = st.text_input("Sizin Gmail Ünvanınız:", placeholder="example@gmail.com")
app_password = st.text_input("Sizin Gmail App Parolunuz:", type="password", placeholder="App Parolunu daxil edin")
subject = st.text_input("E-poçt Mövzusu:", placeholder="Mövzunu daxil edin")
body = st.text_area("Mesajınız (Geri bildirim və rəy):", placeholder="Mesajınızı bura yazın...")

# Send email button
if st.button("E-poçt Göndər"):
    if email_from and app_password and subject and body:
        # Call the send_email function
        result = send_email(email_from, app_password, subject, body)
        if result is True:
            st.success("E-poçt uğurla göndərildi!")
        else:
            st.error(f"E-poçt göndərilmədi: {result}")
    else:
        st.warning("Zəhmət olmasa bütün sahələri doldurun!")


# --------------
# m² 
# ₼
