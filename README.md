🎓 Material Management Web App

This is a simple and clean web app built with Streamlit to manage study materials like question banks, notes, and papers. Admins can upload, delete, and modify materials based on Branch, Semester, Subject, and Year.

---

🚀 Features

- Add/Delete Branches, Semesters, Subjects, and Years
- Upload new materials (question banks, notes, papers)
- Replace or delete uploaded materials
- Organized folder structure for easy access
- Admin login/logout functionality

---

📂 Folder Structure

Uploaded files are saved inside the `data/` directory automatically:

```
data/Branch/Semester/Subject/Year/MaterialType/File
```

Example:

```
data/Computer_Science/Sem1/Maths/2023/question_bank/sample.pdf
```

---

✅ How to Run the Project

1.Clone the repository
   ```bash
   git clone [https://github.com/Vapatel57/ma.git](https://github.com/Vapatel57/academic.git)
   cd material-management-app
   ```

2. Run the app
   ```bash
   streamlit run app.py
   ```

---

## 🔐 Admin Login

A simple admin login is implemented in `app.py`.  
You can edit admin username and password directly in that file.

---

📦 Requirements

The main requirement is Streamlit:
streamlit
---

🛠 Future Improvements

- Add material search and filter functionality
- User role management (Admin, Student access)
- Upload activity history logs
- More stylish UI design

---

📜 License

MIT License.  
Feel free to use, modify, and distribute this project.

---
🙌 Author

Made with ❤️ by Vaidik Makasana

✅ That's it!  
You can **directly use** this in your GitHub repo.  
You only need to replace **Vaidik Makasana** and your **GitHub link** where needed.

---
