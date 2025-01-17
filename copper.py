import pandas as pd
import numpy as np
import streamlit as st
import re
from streamlit_option_menu import option_menu
st.set_page_config(layout="wide")
def setting_bg(background_image_url):
        st.markdown(f""" 
        <style>
            .stApp {{
                background: url('{background_image_url}') no-repeat center center fixed;
                background-size: cover;
                transition: background 0.5s ease;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #f3f3f3;
                font-family: 'Roboto', sans-serif;
            }}
            .stButton>button {{
                color: #4e4376;
                background-color: #f3f3f3;
                transition: all 0.3s ease-in-out;
            }}
            .stButton>button:hover {{
                color: #f3f3f3;
                background-color: #2b5876;
            }}
            .stTextInput>div>div>input {{
                color: #4e4376;
                background-color: #f3f3f3;
            }}
        </style>
        """, unsafe_allow_html=True)

# Example usage with a background image URL
background_image_url = "https://5.imimg.com/data5/SG/AY/MY-3865594/copper-pipe-500x500.png"
setting_bg(background_image_url)

st.markdown("""<div style='border:5px solid black; background-color:yellow; padding:10px;'> 
            <h1 style='text-align:center; color:red;'>Industrial Copper Modeling</h1> </div>""", 
            unsafe_allow_html=True)

selected = option_menu(None, ["Home","Menu"], 
                    icons=["home","Menu"],
                    default_index=0,
                    orientation="horizontal",
                    styles={"nav-link": {"font-size": "25px", "text-align": "centre", "margin": "0px", "--hover-color": "#AB63FA", "transition": "color 0.3s ease, background-color 0.3s ease"},
                            "icon": {"font-size": "25px"},
                            "container" : {"max-width": "6000px", "padding": "10px", "border-radius": "5px"},
                            "nav-link-selected": {"background-color": "black", "color": "white"}})
if selected == "Home":
    st.markdown("## :red[**Overview :**]  :green[The copper industry faces challenges in predicting selling prices and lead classification. However, by utilizing advanced techniques such as data normalization, outlier detection and handling, and by using tree-based models, we can provide accurate predictions and optimize pricing decisions and leads classification]")

if selected  == "Menu":
        tab1, tab2 = st.tabs(["PREDICT SELLING PRICE", "PREDICT STATUS"])
        with tab1:
            status_options = ['Won', 'Draft', 'to be approved', 'lost', 'Not lost for AM', 'Wonderful', 'Revised', 'Offered','Offerable']
            item_type_options = ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
            country_options = [28., 25., 30., 32., 78., 27., 77., 113., 79., 26., 39., 40., 84., 80., 107., 89.]
            application_options = [10., 41., 28., 59., 15., 4., 38., 56., 42., 26., 27., 19., 20., 66., 29., 22., 40., 25., 67.,
                                    79., 3., 99., 2., 5., 39., 69., 70., 65., 58., 68.]
            product = ['611993', '611728', '628112', '628117', '628377', '640400', '640405', '640665','611993', '929423819',
                        '1282007633', '1332077137', '164141591', '164336407',
                        '164337175', '1665572032', '1665572374', '1665584320', '1665584642', '1665584662',
                        '1668701376', '1668701698', '1668701718', '1668701725', '1670798778', '1671863738',
                        '1671876026', '1690738206', '1690738219', '1693867550', '1693867563', '1721130331', '1722207579']

            with st.form('my_form'):
                col1, col2, col3 = st.columns([5, 2, 5])
                with col1:
                    st.write(' ')
                    status = st.selectbox('Status', status_options, key=1)
                    item_type = st.selectbox('Item Type', item_type_options, key=2)
                    country = st.selectbox('Country', sorted(country_options), key=3)
                    application = st.selectbox('Application', sorted(application_options), key=4)
                    product_ref = st.selectbox('Product Reference', product, key=5)
                with col3:
                    quantity_tons = st.text_input('Enter Quantity Tons (Min:1 & Max:1000000000)')
                    thickness = st.text_input('Enter thickness (Min:0.18 & Max:400)')
                    width = st.text_input('Enter width(Min:1, Max:2990)')
                    customer = st.text_input('customer ID (Min:12458, Max:2147483647)')
                    submit_button = st.form_submit_button(label='Predict Selling Price')
                    st.markdown('''''', unsafe_allow_html=True)

                flag = 0
                pattern = r'^(?:\d+|\d*\.\d+)$'
                for i in [quantity_tons, thickness, width, customer]:
                    if re.match(pattern, i):
                        pass
                    else:
                        flag = 1
                        break

            if submit_button and flag == 1:
                if len(i) == 0:
                    st.write('please enter a valid number space not allowed')
                else:
                    st.write('you have entered an invalid value: ', i)

            if submit_button and flag == 0:
                import pickle

                with open(r'model.pkl', 'rb') as file:
                    loaded_model = pickle.load(file)
                with open(r'scaler.pkl', 'rb') as f:
                    scaler_loaded = pickle.load(f)

                with open(r'ohe.pkl', 'rb') as f:
                    ohe_loaded = pickle.load(f)

                with open(r'ohe2.pkl', 'rb') as f:
                        ohe2_loaded = pickle.load(f)

                new_sample = np.array([[np.log(float(quantity_tons)), application, np.log(float(thickness)), float(width),
                                        country, float(customer), int(product_ref), item_type, status]])
                new_sample_ohe = ohe_loaded.transform(new_sample[:, [7]]).toarray()
                new_sample_be = ohe2_loaded.transform(new_sample[:, [8]]).toarray()
                new_sample = np.concatenate((new_sample[:, [0, 1, 2, 3, 4, 5, 6, ]], new_sample_ohe,new_sample_be), axis=1)
                new_sample1 = scaler_loaded.transform(new_sample)
                new_pred = loaded_model.predict(new_sample1)[0]
                st.write('## :green[Predicted selling price:] ', np.exp(new_pred))

        with tab2:
            with st.form('my_form1'):
                col1, col2, col3 = st.columns([5, 1, 5])
                with col1:
                    cquantity_tons = st.text_input('Enter Quantity Tons (Min:1 & Max:1000000000.0)')
                    cthickness = st.text_input('Enter thickness (Min:0.18 & Max:400)')
                    cwidth = st.text_input('Enter width (Min:1, Max:2990)')
                    ccustomer = st.text_input('customer ID (Min:12458, Max:2147483647)')
                    cselling = st.text_input("Selling Price (Min:1, Max:100001015)")

                with col3:
                    st.write(' ')
                    citem_type = st.selectbox("Item Type", item_type_options, key=21)
                    ccountry = st.selectbox("Country", sorted(country_options), key=31)
                    capplication = st.selectbox("Application", sorted(application_options), key=41)
                    cproduct_ref = st.selectbox("Product Reference", product, key=51)
                    csubmit_button = st.form_submit_button(label="PREDICT STATUS")

                cflag = 0
                pattern = r"^(?:\d+|\d*\.\d+)$"
                for k in [cquantity_tons, cthickness, cwidth, ccustomer, cselling]:
                    if re.match(pattern, k):
                        pass
                    else:
                        cflag = 1
                        break

            if csubmit_button and cflag == 1:
                if len(k) == 0:
                    st.write("please enter a valid number space not allowed")
                else:
                    st.write("You have entered an invalid value: ", k)

            if csubmit_button and cflag == 0:
                import pickle

                with open(r"cmodel.pkl", 'rb') as file:
                    cloaded_model = pickle.load(file)

                with open(r'cscaler.pkl', 'rb') as f:
                    cscaler_loaded = pickle.load(f)

                with open(r"cohe.pkl", 'rb') as f:
                    cohe_loaded = pickle.load(f)

                new_sample = np.array([[np.log(float(cquantity_tons)), np.log(float(cselling)), capplication,
                                        np.log(float(cthickness)), float(cwidth), ccountry, int(ccustomer), int(product_ref),
                                        citem_type]])
                new_sample_ohe = cohe_loaded.transform(new_sample[:, [8]]).toarray()
                new_sample = np.concatenate((new_sample[:, [0, 1, 2, 3, 4, 5, 6, 7]], new_sample_ohe), axis=1)
                new_sample = cscaler_loaded.transform(new_sample)
                new_pred = cloaded_model.predict(new_sample)
                if new_pred == 1:
                    st.write('## :green[The Status is Won] ')
                else:
                    st.write('## :red[The status is Lost] ')
