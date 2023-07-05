import streamlit as st

# Set page config
st.set_page_config(
    page_title="COLA",
    page_icon="🌍",
    layout="centered",
)

# Page title
st.title("COLA")

# Quote
st.markdown(
    """
    > "There is no Planet B 🌍."
    """,
)
st.sidebar.title("About")
st.sidebar.info(
    """
    - Web App URL: <https://rbachati-cdpop-webapp-app-ugs378.streamlit.app/>
    - GitHub repository: <https://github.com/rbachati/cdpop_webapp>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Patrict Jantz
    [GitHub](https://github.com/forest-rev) |[LinkedIn]()
    """
)


# Additional Text Content
st.markdown(
    """
    ## What is COLA?
    COLA is a web application dedicated to promoting awareness about environmental sustainability.
    We provide data-driven insights and resources to help individuals and organizations make more eco-friendly decisions.
    """
)

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.image("./background.jpg")
    st.image("./200.webp", use_column_width=True)

with row1_col2:
    st.image("https://github.com/giswqs/data/raw/main/timelapse/goes.gif")
    st.image("https://github.com/giswqs/data/raw/main/timelapse/fire.gif")
    

# More links or navigation
st.markdown(
    """
    ---
    ##### Explore More
    - [About Us](#)
    - [Our Mission](#)
    - [Contact Us](#)
    - [Source Repository](https://github.com/rbachati/cdpop_webapp)
    """,
)

with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
