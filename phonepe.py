import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image
import plotly.graph_objects as go



mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Praveen@123456789',
    database='phonepe'
)
cursor = mydb.cursor()





# Fetch aggregated_transaction data
cursor.execute("SELECT * FROM aggregated_transaction")
table2 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                                   "Transaction_count", "Transaction_amount"))

# Fetch aggregated_user data
cursor.execute("SELECT * FROM aggregated_user")
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Brands",
                                           "Transaction_count", "Percentage"))

# Fetch map_transaction data
cursor.execute("SELECT * FROM map_transaction")
table3 = cursor.fetchall()
map_transaction = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "District",
                                               "Transaction_count", "Transaction_amount"))

# Fetch map_user data
cursor.execute("SELECT * FROM map_user")
table4 = cursor.fetchall()
map_user = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "District",
                                         "RegisteredUser", "AppOpens"))

# Fetch top_transaction data
cursor.execute("SELECT * FROM top_transaction")
table5 = cursor.fetchall()
top_transaction = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

# Fetch top_user data
cursor.execute("SELECT * FROM top_user")
table6 = cursor.fetchall()
top_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Pincodes",
                                         "RegisteredUsers"))

# Close cursor and database connection
cursor.close()
mydb.close()

def Transaction_amount_count_Y(df, year):

    tacy= df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.line(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Purples, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.line(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered, height= 650, width= 600)
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale=px.colors.sequential.Plasma,
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600, width=600)
        fig_india_1.update_geos(visible=False)
        fig_india_1.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, title_font=dict(size=20))
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale=px.colors.sequential.Viridis,
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600, width=600)
        fig_india_2.update_geos(visible=False)
        fig_india_2.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, title_font=dict(size=20))
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df, quarter):
    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_amount = px.line(tacyg, x="States", y="Transaction_amount", 
                         title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                         markers=True, color_discrete_sequence=px.colors.sequential.Purples,
                         height=650, width=600)
    st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.line(tacyg, x="States", y="Transaction_count", 
                        title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        markers=True, color_discrete_sequence=px.colors.sequential.Bluered_r,
                        height=650, width=600)
    st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "rainbow",
                                range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "rainbow",
                                range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 600,width= 600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

            

def Aggre_Tran_Transaction_type(df, state):
    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    # Create 3D scatter plot
    fig_scatter_3d = px.scatter_3d(tacyg, x='Transaction_type', y='Transaction_count', z='Transaction_amount',
                                   title=f"{state.upper()} TRANSACTION DETAILS",
                                   color='Transaction_amount', size='Transaction_amount',
                                   color_continuous_scale=px.colors.sequential.Purples,
                                   hover_name='Transaction_type',
                                   width=800, height=600)
    
    # Update layout and styling if needed
    fig_scatter_3d.update_layout(scene=dict(
        xaxis_title='Transaction Type',
        yaxis_title='Transaction Count',
        zaxis_title='Transaction Amount'),
        margin=dict(l=0, r=0, b=0, t=30))

    # Display the 3D scatter plot
    st.plotly_chart(fig_scatter_3d)

# Aggre_User_analysis_1
def Aggre_user_plot_1(df, year):
    # Filter the DataFrame for the specified year
    aguy = df[df["Years"] == year]
    aguy.reset_index(drop=True, inplace=True)

    # Group by brands and calculate the sum of transaction count
    aguyg = aguy.groupby("Brands")["Transaction_count"].sum().reset_index()

    # Create a bubble chart
    fig_bubble = px.scatter(aguyg, x="Brands", y="Transaction_count", 
                            size="Transaction_count", color="Brands", 
                            title=f"{year} BRANDS AND TRANSACTION COUNT",
                            width=1000, height=600, hover_name="Brands", 
                            color_discrete_sequence=px.colors.sequential.haline_r)

    # Display the bubble chart
    st.plotly_chart(fig_bubble)

    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_area_1 = px.area(aguyqg, x="Brands", y="Transaction_count", title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                         width=1000, color_discrete_sequence=px.colors.sequential.Magenta_r, hover_name="Brands")
    
    st.plotly_chart(fig_area_1)

    return aguyq


#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)



#Map_tran_district
def Map_tran_District(df, state):
    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    with col1:
        fig_violin_1 = px.violin(tacyg, x="Transaction_amount", y="District", orientation="h", height=600,
                             title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_violin_1)

    with col2:
        fig_violin_2 = px.violin(tacyg, x="Transaction_count", y="District", orientation="h", height=600,
                             title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_violin_2)
        


        
# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_scatter = px.scatter(muyg, x="RegisteredUser", y="AppOpens",
                         trendline="ols", title=f"{year} REGISTERED USER vs APPOPENS",
                         width=1000, height=800, labels={"RegisteredUser": "Registered Users", "AppOpens": "App Opens"})
    st.plotly_chart(fig_scatter)
    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)


 # Group by states and calculate the sum
    muyqg = muyq.groupby("States")[["RegisteredUser", "AppOpens"]].agg(['sum', 'std'])
    muyqg.columns = ['_'.join(col) for col in muyqg.columns]
    muyqg.reset_index(inplace=True)

    # Create the line chart with error bars
    fig_error = px.scatter(muyqg, x="States", y="RegisteredUser_sum", error_y="RegisteredUser_std", 
                           title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",
                           width=1000, height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    
    fig_error.add_scatter(x=muyqg["States"], y=muyqg["AppOpens_sum"], mode='markers+lines', 
                          name='App Opens', error_y=dict(type='data', array=muyqg["AppOpens_std"]))

    st.plotly_chart(fig_error)
    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    

# top_tran_plot_1
def Top_transaction_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_top_insur_pie_1 = px.pie(tiy, values="Transaction_amount", names="Quarter", 
                                     title="TRANSACTION AMOUNT", hover_data=["Pincodes"],
                                     height=650, width=600, 
                                     color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_pie_1)

    with col2:
        fig_top_insur_pie_2 = px.pie(tiy, values="Transaction_count", names="Quarter", 
                                     title="TRANSACTION COUNT", hover_data=["Pincodes"],
                                     height=650, width=600, 
                                     color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_pie_2)


# top_user_plot_1
def top_user_plot_1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    # Calculate total RegisteredUsers per State to sort by total value
    state_totals = tuyg.groupby("States")["RegisteredUsers"].sum().reset_index()
    state_totals = state_totals.sort_values(by="RegisteredUsers", ascending=False)
    sorted_states = state_totals["States"].tolist()

    # Create a sorted version of tuyg DataFrame based on sorted_states
    tuyg_sorted = tuyg.copy()
    tuyg_sorted["States"] = pd.Categorical(tuyg_sorted["States"], categories=sorted_states, ordered=True)
    tuyg_sorted = tuyg_sorted.sort_values(by="States")

    fig_top_plot_1 = px.bar(tuyg_sorted, x="States", y="RegisteredUsers", color="Quarter", 
                            width=1000, height=800, color_discrete_sequence=px.colors.sequential.Burgyl, 
                            hover_name="States", title=f"{year} REGISTERED USERS",
                            category_orders={"States": sorted_states})
    
    st.plotly_chart(fig_top_plot_1)

    return tuy

# top_user_plot_2
def top_user_plot_2(df, state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    # Create a waterfall chart using plotly.figure_factory
    fig_top_pot_2 = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=["relative", "relative", "total", "relative", "relative"],
        x=tuys["Quarter"],
        textposition="outside",
        text=tuys["Pincodes"],
        y=tuys["RegisteredUsers"],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "green"}},
        decreasing={"marker": {"color": "red"}},
    ))

    fig_top_pot_2.update_layout(
        title="REGISTERED USERS, PINCODES, QUARTER",
        width=1000,
        height=800,
    )

    st.plotly_chart(fig_top_pot_2)
#streamlit part

st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created for PhonePe Data Visualization!
                                        Data has been cloned from Phonepe Pulse Github Repository"""})

st.sidebar.header(":red[**Welcome to the dashboard!**]")
st.title(":red[PHONEPE--PULSE--DATA--VISUALIZATION]")

with st.sidebar:
    
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION"])

if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header(":red[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        

        
    with col2:
        st.image(r"F:\Desktop\Phonepe\Phonepe gifs.gif")




elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",[ "Transaction Analysis", "User Analysis"])
        
        
        if method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)

        elif method == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Aggre_user["Years"].min(), Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)



    with tab2:

        method_2= st.radio("Select The Method",["Map Transaction", "Map User"])
        
        
        if method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:

               years = st.slider("Select The Year", 
                  map_transaction["Years"].min(), 
                  map_transaction["Years"].max(),
                  map_transaction["Years"].min(),
                  key="year_slider_map_transaction")

            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_tran_tac_Y["States"].unique())

            Map_tran_District(map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mt",map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty",
                      map_tran_tac_Y_Q["States"].unique(),
                      key="state_selectbox_map_tran_tac_Y_Q")

            Map_tran_District(map_tran_tac_Y_Q, states)


        elif method_2 == "Map User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mu",map_user["Years"].min(), map_user["Years"].max(),map_user["Years"].min())
            map_user_Y= map_user_plot_1(map_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)

    with tab3:

        method_3= st.radio("Select The Method",["Top Transaction", "Top User"])
          

        if method_3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tt",top_transaction["Years"].min(), top_transaction["Years"].max(),top_transaction["Years"].min())
            top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", top_tran_tac_Y["States"].unique())

            Top_transaction_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_tt",top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)


        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu",top_user["Years"].min(), top_user["Years"].max(),top_user["Years"].min())
            top_user_Y= top_user_plot_1(top_user, years)

            col1,col2= st.columns(2)
            with col1:
                
                states= st.selectbox("Select The State_tu", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)
