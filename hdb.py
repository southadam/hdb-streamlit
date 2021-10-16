import streamlit as st
import pandas as pd
import plotly.express as px



st.write("""
# Resale HDB Analysis
2017 - 2021
""")


df = pd.read_csv("hdb.csv")
#df= df.convert_dtypes()
new = df["month"].str.split("-", n = 1, expand = True)
df.drop(columns =["month"], inplace = True)
df['year']=new[0]
df['month']=new[1]
df['year']=df['year'].astype('int64')
df['month']=df['month'].astype('int64')
#min_year = df['year'].min()
#max_year = df['year'].max()
df['psf'] = df['resale_price'] / (df['floor_area_sqm'] * 10.7639 )
df['psf'] = df['psf'].astype("float").round(2)
df_median = df.groupby(["town","flat_type","year"])["resale_price"].median().reset_index()
df_sum = df.groupby(["town","flat_type","year"])["resale_price"].sum().reset_index()
df_psf = df.groupby(["year","town"])["psf"].median().reset_index()
df_type_psf = df.groupby(["year","flat_type"])["psf"].median().reset_index()
flattype = df['flat_type'].unique()
flattype.sort()
df['flat_type'].unique()


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.sidebar.title('Choose to interact')

flat_type_select = st.sidebar.multiselect(
        "Choose Flat Types", list(flattype), ["5 ROOM", "4 ROOM", "3 ROOM","2 ROOM","1 ROOM","EXECUTIVE","MULTI-GENERATION"])

year_select = st.sidebar.multiselect(
        "Choose Years", list(df['year'].unique()), [2021,2020,2019,2018,2017])

town_select = st.sidebar.multiselect(
        "Choose Town", list(df['town'].unique()), ["WOODLANDS","BISHAN","JURONG EAST","ANG MO KIO","BUKIT MERAH","CENTRAL AREA","CLEMENTI","GEYLANG"])

if not flat_type_select:
    st.error("Please select at least one flat type.")
elif not year_select:
    st.error("Please select at least one year.")
elif not town_select:
    st.error("Please select at least one town.")
else:

    df_x = df[(df['flat_type'].isin(flat_type_select)) & (df['year'].isin(year_select)) & (df['town'].isin(town_select))]
    xmedian = df_median[(df_median['flat_type'].isin(flat_type_select)) & (df_median['year'].isin(year_select)) & (df_median['town'].isin(town_select))]
    xsum = df_sum[(df_sum['flat_type'].isin(flat_type_select)) & (df_sum['year'].isin(year_select)) & (df_sum['town'].isin(town_select))]
    xpsf = df_psf[(df_psf['year'].isin(year_select)) & (df_psf['town'].isin(town_select))]
    xtypepsf = df_type_psf[(df_type_psf['year'].isin(year_select)) & (df_type_psf['flat_type'].isin(flat_type_select))]

fig = px.bar(xsum, x='town', y="resale_price", color="flat_type",
                   labels={'town': 'Township',
                           'resale_price': 'Resale Value'},
                    category_orders={"flat_type": ["1 ROOM","2 ROOM","3 ROOM","4 ROOM","5 ROOM","EXECUTIVE","MULTI-GENERATION"]},
                   title='Total Resale Value by Township', height=500)

fig2 = px.bar(xmedian, x="town", y="resale_price", color="flat_type",category_orders={"flat_type": ["1 ROOM","2 ROOM","3 ROOM","4 ROOM","5 ROOM","EXECUTIVE","MULTI-GENERATION"]},
              title='Median Resale Value by Township')

fig3 = px.scatter(df_x, y="town", x="resale_price", color="flat_type",
                      labels={
                          'town': 'Town',
                          'resale_price': 'Resale Value',
                          'flat_type': 'Flat Type'
                      },
                    category_orders={"flat_type": ["1 ROOM","2 ROOM","3 ROOM","4 ROOM","5 ROOM","EXECUTIVE","MULTI-GENERATION"]},
                    title='Understanding Resale Value of HDB Flat Area & Types', height=500)

fig4 = px.scatter(xmedian, y="town", x="resale_price", color="flat_type",
    labels = {
                 'town': 'Township',
                 'resale_price': 'Resale Value',
                 'flat_type': 'Flat Type'
             }, category_orders={"flat_type": ["1 ROOM","2 ROOM","3 ROOM","4 ROOM","5 ROOM","EXECUTIVE","MULTI-GENERATION"]},
                  title='Understanding the Median Prices of  HDB Flat Area & Types', height=500
    )

fig5 = px.line(xpsf, x="year", y="psf", color='town',
               title='Per Square Foot Prices of  HDB Town', height=500)
fig5.update_xaxes(type='category')

fig6 = px.line(xtypepsf, x="year", y="psf", color='flat_type',
               title='Per Square Foot Prices of  HDB Type', height=500)
fig6.update_xaxes(type='category')

st.plotly_chart(fig,use_container_width=True)
st.plotly_chart(fig2,use_container_width=True)
st.plotly_chart(fig3,use_container_width=True)
st.plotly_chart(fig4,use_container_width=True)
st.plotly_chart(fig5,use_container_width=True)
st.plotly_chart(fig6,use_container_width=True)
#st.bar_chart(df_bar['resale_price'])

