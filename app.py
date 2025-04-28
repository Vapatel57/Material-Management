import streamlit as st
import os
from pathlib import Path
from PIL import Image
import base64

# -------------------- SETTINGS --------------------
st.set_page_config(page_title="College Academic Hub", page_icon="🎓", layout="wide")

# -------------------- APP HEADER --------------------
st.title("🎓 College Students Academic Hub")
st.markdown("##### Find Question Banks, Papers, Solutions, and Short Notes 📚")
st.divider()

# -------------------- HELPER FUNCTIONS --------------------
def get_branches(data_path='data'):
    return [d.name for d in Path(data_path).iterdir() if d.is_dir()]

def get_semesters(branch, data_path='data'):
    sem_path = Path(data_path) / branch
    return [d.name for d in sem_path.iterdir() if d.is_dir()]

def get_subjects(branch, semester, data_path='data'):
    subj_path = Path(data_path) / branch / semester
    return [d.name for d in subj_path.iterdir() if d.is_dir()]

def get_years(branch, semester, subject, data_path='data'):
    year_path = Path(data_path) / branch / semester / subject
    return [d.name for d in year_path.iterdir() if d.is_dir()]

def list_materials(branch, semester, subject, year, data_path='data'):
    material_path = Path(data_path) / branch / semester / subject / year
    return [f for f in material_path.iterdir() if f.is_file()]

def get_display_name(file_name):
    name_map = {
        "midsem_paper": "📝 Mid Semester Paper",
        "endsem_paper": "📝 End Semester Paper",
        "question_bank": "📚 Question Bank",
        "solutions": "✅ Solutions",
        "short_notes": "🧠 Short Notes"
    }
    for key in name_map:
        if key in file_name.lower():
            return name_map[key]
    return "📄 Other Material"

def show_pdf(file_path):
    with open(str(file_path), "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
def preview_file(file):
    file_suffix = file.suffix.lower()
    if file_suffix == '.pdf':
        with st.expander("👀 Preview PDF"):
            show_pdf(file)
    elif file_suffix in ['.jpg', '.jpeg', '.png']:
        with st.expander("👀 Preview Image"):
            img = Image.open(file)
            st.image(img, use_column_width=True)
    else:
        with st.expander("ℹ️ Preview Not Available"):
            st.info("⚡ Preview not supported for this file type. Please download to view.")

def create_folder_structure(branch, semester, subject, year, data_path='data'):
    folder_path = Path(data_path) / branch / semester / subject / year
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

# -------------------- ADMIN PANEL --------------------
def admin_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.header("🔐 Admin Login")
        username = st.text_input("Username", "")
        password = st.text_input("Password", "", type="password")
        
        if st.button("Login"):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.success("Login successful! Welcome to the Admin Panel.")
            else:
                st.error("Invalid username or password. Please try again.")
    
    if st.session_state.logged_in:
        st.sidebar.success("You are logged in as Admin")

def admin_logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.success("You have been logged out successfully!")
        st.stop()

def upload_file(branch, semester, subject, year, file_type, data_path='data'):
    folder = create_folder_structure(branch, semester, subject, year, data_path)
    uploaded_file = st.file_uploader("Upload your file", type=['pdf', 'jpg', 'jpeg', 'png', 'pptx'])
    if uploaded_file:
        # Retain the original file name and extension
        file_name = uploaded_file.name  # Use the original name of the file

        # Save the uploaded file with the original name in the folder
        with open(folder / file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{file_name}' uploaded successfully!")

def delete_file(branch, semester, subject, year, file_name, data_path='data'):
    file_path = Path(data_path) / branch / semester / subject / year / file_name
    if file_path.exists():
        file_path.unlink()  # Delete the file
        st.success(f"File '{file_name}' deleted successfully!")
    else:
        st.error(f"File '{file_name}' not found!")

def replace_file(branch, semester, subject, year, file_type, data_path='data'):
    folder = create_folder_structure(branch, semester, subject, year, data_path)
    uploaded_file = st.file_uploader("Upload the new file to replace the old one", type=['pdf', 'jpg', 'jpeg', 'png', 'pptx'])
    if uploaded_file:
        # Retain the original file name and format when replacing
        file_name = uploaded_file.name  # Use the original name of the file
        
        # Save the uploaded file with the same name as the old one
        with open(folder / file_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File '{file_name}' replaced successfully!")

def add_branch(data_path='data'):
    branch_name = st.text_input("Enter New Branch Name:")
    if st.button("Add Branch"):
        branch_path = Path(data_path) / branch_name
        branch_path.mkdir(parents=True, exist_ok=True)
        st.success(f"Branch '{branch_name}' added successfully!")

def add_semester(branch, data_path='data'):
    semester_name = st.text_input("Enter New Semester Name:")
    if st.button("Add Semester"):
        semester_path = Path(data_path) / branch / semester_name
        semester_path.mkdir(parents=True, exist_ok=True)
        st.success(f"Semester '{semester_name}' added successfully under '{branch}'!")

def add_subject(branch, semester, data_path='data'):
    subject_name = st.text_input("Enter New Subject Name:")
    if st.button("Add Subject"):
        subject_path = Path(data_path) / branch / semester / subject_name
        subject_path.mkdir(parents=True, exist_ok=True)
        st.success(f"Subject '{subject_name}' added successfully under '{branch} ➔ {semester}'!")

def add_year(branch, semester, subject, data_path='data'):
    year_name = st.text_input("Enter New Year Name:")
    if st.button("Add Year"):
        year_path = Path(data_path) / branch / semester / subject / year_name
        year_path.mkdir(parents=True, exist_ok=True)
        st.success(f"Year '{year_name}' added successfully under '{branch} ➔ {semester} ➔ {subject}'!")

# -------------------- MAIN APP --------------------
admin_login()

if "logged_in" in st.session_state and st.session_state.logged_in:
    st.sidebar.checkbox("🛠️ Admin Panel", True)

    st.header("📂 Admin Panel - Manage Materials")
    
    st.subheader("➕ Add New Entries")
    choice = st.selectbox("What do you want to add?", ["Branch", "Semester", "Subject", "Year", "Materials"])

    if choice == "Branch":
        add_branch()
        admin_logout()

    elif choice == "Semester":
        branches = get_branches('data')
        branch = st.selectbox("Select Branch", options=branches)
        if branch:
            add_semester(branch)
        admin_logout()

    elif choice == "Subject":
        branches = get_branches('data')
        branch = st.selectbox("Select Branch", options=branches)
        if branch:
            semesters = get_semesters(branch, 'data')
            semester = st.selectbox("Select Semester", options=semesters)
            if semester:
                add_subject(branch, semester)
        admin_logout()

    elif choice == "Year":
        branches = get_branches('data')
        branch = st.selectbox("Select Branch", options=branches)
        if branch:
            semesters = get_semesters(branch, 'data')
            semester = st.selectbox("Select Semester", options=semesters)
            if semester:
                subjects = get_subjects(branch, semester, 'data')
                subject = st.selectbox("Select Subject", options=subjects)
                if subject:
                    add_year(branch, semester, subject)
        admin_logout()

    elif choice == "Materials":
        branches = get_branches('data')
        branch = st.selectbox("Select Branch", options=branches)
        if branch:
            semesters = get_semesters(branch, 'data')
            semester = st.selectbox("Select Semester", options=semesters)
            if semester:
                subjects = get_subjects(branch, semester, 'data')
                subject = st.selectbox("Select Subject", options=subjects)
                if subject:
                    years = get_years(branch, semester, subject, 'data')
                    year = st.selectbox("Select Year", options=years)
                    if year:
                        file_type = st.selectbox(
                            "Select File Type", 
                            ["question_bank", "midsem_paper", "endsem_paper", "solutions", "short_notes"]
                        )
                        action = st.radio("Select Action", ["Upload New File", "Delete File", "Replace Existing File"])

                        if action == "Upload New File":
                            upload_file(branch, semester, subject, year, file_type)
                        elif action == "Delete File":
                            files = list_materials(branch, semester, subject, year, 'data')
                            file_to_delete = st.selectbox("Select File to Delete", options=[f.name for f in files])
                            if file_to_delete and st.button(f"Delete {file_to_delete}"):
                                delete_file(branch, semester, subject, year, file_to_delete, 'data')
                        elif action == "Replace Existing File":
                            files = list_materials(branch, semester, subject, year, 'data')
                            file_to_replace = st.selectbox("Select File to Replace", options=[f.name for f in files])
                            if file_to_replace:
                                replace_file(branch, semester, subject, year, file_type)
        admin_logout()

else:
    # -------------------- STUDENT VIEW --------------------
    st.header("📚 Materials for Students")
    
    branches = get_branches('data')
    branch = st.selectbox("Select Your Branch", options=branches)

    if branch:
        semesters = get_semesters(branch, 'data')
        semester = st.selectbox("Select Your Semester", options=semesters)
        
        if semester:
            subjects = get_subjects(branch, semester, 'data')
            subject = st.selectbox("Select Subject", options=subjects)

            if subject:
                years = get_years(branch, semester, subject, 'data')
                year = st.selectbox("Select the Year of Papers", options=years)

                if year:
                    st.success(f"Showing materials for **{branch} ➔ {semester} ➔ {subject} ➔ {year}** 🎯")

                    files = list_materials(branch, semester, subject, year, 'data')

                if files:
                        for file in files:
                            material_type = get_display_name(file.name)
                            col1, col2 = st.columns([7, 3])
                            with col1:
                                st.subheader(material_type)
                            with col2:
                                with open(file, "rb") as f:
                                    file_data = f.read()
                                    st.download_button(
                                        label="📥 Download",
                                        data=file_data,
                                        file_name=file.name,
                                        mime="application/pdf", 
                                        key=file.name
                                    )
                            preview_file(file)
                else:
                    st.warning("⚠️ No materials found for selected combination!")
