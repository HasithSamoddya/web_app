import time
import sqlite3
import streamlit as st
import hashlib as hash
#-------------------------------------------------------------
connection = sqlite3.connect("web_app.db")
cursor = connection.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS person(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)
            """)

#-----------------------------------------------------------------
if "logged_in" not in st.session_state: #create the state
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
def login():
    with st.form("Login"):
        st.title("Login Page",text_alignment="center")
        username_1 = st.text_input("Username", "")
        password_1 = st.text_input("Password", "", type="password")
        with st.container(horizontal_alignment="center"):
            btn = st.form_submit_button("Sign In")
        if btn:
            encrypted_username_1 =hash.sha256(username_1.encode("utf-8")).hexdigest()
            encrypted_password_1 =hash.sha256(password_1.encode("utf-8")).hexdigest()
            cursor.execute("SELECT * FROM person WHERE username = ? AND password = ?", (encrypted_username_1, encrypted_password_1))
            result = cursor.fetchone()
            if result:
                    st.success("Login Successful")
                    st.toast("Login Successful !",icon="❤️")
                    st.session_state.username = username_1 #blah blah
                    st.balloons()
                    with st.container(horizontal_alignment="center"):
                        with st.spinner(text="Login in......"):
                            time.sleep(3)
                    st.session_state.logged_in = True
                    st.rerun()
            else:
                st.error("Incorrect credentials !")
                st.toast("Incorrect credentials !",icon="🚨")
        else:
            pass
if not st.session_state.logged_in:
    state = st.selectbox("Login/signup", ["login", "signup"], index=0)
    if state == "login":
        login()
    else:
        with st.form("Signup"):
            st.title("Signup Page",text_alignment="center")
            username = st.text_input("Username", "")
            password = st.text_input("Password", "",type="password")
            password2 = st.text_input("Confirm Password", "",type="password")
            with st.container(horizontal_alignment="center"):
                btn = st.form_submit_button("Sign Up")
            if btn:
                cursor.execute("SELECT * FROM person WHERE username = ?", (username,))
                result2 = cursor.fetchone()
                if result2:
                    st.error("Already satisfied")
                else:
                    if password == password2 and username != "":
                        encrypted_username = hash.sha256(username.encode()).hexdigest()
                        encrypted_password = hash.sha256(password.encode()).hexdigest()
                        cursor.execute("INSERT INTO person(username, password) VALUES (?, ?)", (encrypted_username, encrypted_password))
                        st.success("Signup Successful you can login")
                        st.toast("Signup Successful !",icon="😊")
                    else:
                        st.error("Try Again")

            else:
                pass
else:
    st.sidebar.markdown("<h1 style='color:red;font-size:50px;'>WELCOME !</h1>",text_alignment="center",unsafe_allow_html=True)
    st.sidebar.markdown("---")
    page = st.sidebar.selectbox("Navigate to ->", ["Home🏠", "About📃","Contact📞","Store🛒"], index=0)
    log_out = st.sidebar.button("Log Out:house:")
    st.sidebar.markdown("#Daily Thoughts")
    st.sidebar.markdown("<h2 style='font-style:italic;align-content:justify;'>Any fool can write code that a computer can understand. Good programmers write code that humans can understand. — Martin Fowler</h2>",unsafe_allow_html=True)
    # Custom CSS for a clean profile card in the sidebar
    st.markdown(
        """
        <style>
            .profile-card {
                border: 1px solid black;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                border-left: 8px solid red;
                color: white;
            }
            .profile-name {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
                color: white;
            }
            .profile-detail {
                font-size: 16px;
                color: white;
                font-weight: bold;
                margin-bottom: 3px;
                line-height: 1.4;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
    # Render inside the Sidebar
    st.sidebar.markdown("---")
    with st.sidebar:
        st.markdown(
            """
              <div class="profile-card">
                  <div class="profile-name">👤 A.M. Hasith Samodya Bandara</div>
                  <div class="profile-detail">📍 Nittambuwa, Gampaha District, Sri Lanka</div>
                  <div class="profile-detail">📞 +94 70 379 1674</div>
              </div>
          """,
            unsafe_allow_html=True,
        )
        # Rest of your sidebar elements (logout button, settings, etc.)
    if log_out:
        st.session_state.logged_in = False
    else:
        pass
    if page == "Home🏠": # home page
        st.title(f"Hello {st.session_state.username.capitalize()} ! :streamlit:", text_alignment="center")
        col = st.columns(3)
        with col[0]:
            with st.container(border=True):
                st.metric(label="Account Status",value="Active",delta="Verified")
        with col[1]:
            with st.container(border=True):
                st.metric(label="Projects Loaded", value="12", delta="2%")
        with col[2]:
            with st.container(border=True):
                st.metric(label="System Usage", value="98%", delta="-1%")
        st.markdown("---")
        from streamlit_carousel import carousel

        # Define your slide objects
        slides = [
            {
                "title": "Slide 1",
                "text": "A beautiful view of nature",
                "img": "bailey-zindel-NRQV-hBF10M-unsplash.jpg"

            },
            {
                "title": "Slide 2",
                "text": "A close-up of local flora",
                "img":"C:\\Users\\Hasith\\Downloads\\bailey-zindel-NRQV-hBF10M-unsplash.jpg"
            }
        ]


        carousel(items=slides)

    elif page == "About📃":
        st.title(f"This is about page")
        st.warning("Under development !")
    elif page == "Contact📞":
        st.title(f"This is contact page")
        st.warning("Under development !")
    else:
        st.title(f"This is store page")
        st.warning("Under development !")


#end
connection.commit()
connection.close()

