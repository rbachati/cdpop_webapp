# streamlit_app.py
from streamlit_authenticator import check_password
import streamlit as st
from ipysheet import from_dataframe, to_dataframe
import ipysheet
import streamlit as st
import pandas as pd
import os

# Set the title of the app
st.set_page_config(page_title="CDPOP Simulation Model", page_icon=":bar_chart:", layout="wide")
st.title("LandScape Genetics (CDPOP)")
        
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True
    
if check_password():
    # Define function to run CDPOP script
    def run_cdpop(input_file_path, output_file_path):
        # Change directory to where the CDPOP script is located
        os.chdir(os.path.join(os.path.dirname(__file__), "CDPOP", "src"))
        
        # Run the CDPOP script with input and output file paths
        os.system(f"python CDPOP.py {input_file_path} {output_file_path}")

    def main():
        
        # Define input and output file paths
        input_file = st.sidebar.file_uploader("Upload input CSV file", type=["csv"])
        if input_file is not None:
            input_path = os.path.abspath(input_file.name)
            input_df = pd.read_csv(input_file, encoding='utf-8')

        output_path = st.sidebar.text_input("Output file path", value=os.path.join(os.getcwd(), "output.csv"))

        # Define the editable columns
        editable_cols = [
            "xyfilename",
            "output_years",
            "output_unicor",
            "dispcdmat",
            "matemovethresh",
            "Fdispmovethresh",
            "Mdispmovethresh",
        ]
        
        # Define new column names
        new_col_names = {
            "xyfilename": "XY Locations file",
            "output_years": "generations/years of saved genotypes",
            "output_unicor": "xy locations for output years",
            "dispcdmat": "dispersal cost distance matrix",
            "matemovethresh": "mating distance threshold",
            "Fdispmovethresh": "Female Dispersion Threshold",
            "Mdispmovethresh": "Male Dispersion Threshold",
        }

        # If input file is specified, load and edit the input CSV file
        if 'input_df' in locals():

            # Add a checkbox to control the visibility of the table
            show_df = st.checkbox("select the checkbox for the parameters file")

            # If the checkbox is checked, display the table
            if show_df:
                st.write(input_df)

            st.header("Edit input parameter file")
            # Make a copy of your dataframe with only the columns you want to be editable
            editable_df = input_df[editable_cols].copy()
            
            #Rename the columns
            editable_df.rename(columns=new_col_names, inplace=True)

            # Use the experimental data editor
            edited_df = st.data_editor(editable_df, num_rows="dynamic", key="data_editor")

            # Handle any changes made in the data editor
            if st.session_state.data_editor:
                # Convert the new column names back to the original names
                edited_df.rename(columns={v: k for k, v in new_col_names.items()}, inplace=True)
                # Update the original dataframe with the changes made in the data editor
                input_df.update(edited_df)

            if st.button("Save changes"):
                input_df.to_csv(input_path, index=False)
                st.success("Changes saved successfully!")

            # Add a Run button and a progress bar
            if st.button("Run"):
                with st.spinner('Running CDPOP...'):
                    run_cdpop(input_path, output_path)
                st.success('Done running CDPOP.')

    if __name__ == "__main__":
        main()