import streamlit as st

# Set the background image URL
background_image_url = 'https://images.pexels.com/photos/1366919/pexels-photo-1366919.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'

# Define the Streamlit app layout
def app_layout():
    st.sidebar.title('New Mail')
    st.sidebar.header('Accounts:')
    st.sidebar.text('example@gmail.com')
    st.sidebar.header('Folders')
    st.sidebar.text('Inbox')
    st.sidebar.text('More')

    st.title('Inbox - One-example')
    search_input = st.text_input('Search', '')

    st.write('Nothing has arrived yet')

# Set the background image using CSS
def set_background():
    st.markdown(
        f"""
        <style>
            .reportview-container {{
                background: url({background_image_url});
                background-size: cover;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Run the Streamlit app
if __name__ == '__main__':
    set_background()
    app_layout()
