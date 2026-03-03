import streamlit as st
from datetime import datetime

st.set_page_config(page_title="A.K.L.A.T", page_icon="📚", layout="wide")

# ================== STATE ==================
if "page" not in st.session_state:
    st.session_state.page = "Bahay"

if "grades" not in st.session_state:
    st.session_state.grades = {}

if "reading_progress" not in st.session_state:
    st.session_state.reading_progress = 0

if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "modules_status" not in st.session_state:
    st.session_state.modules_status = {"Aralin 1":"Hindi pa nasimulan", "Aralin 2":"Hindi pa nasimulan", "Aralin 3":"Hindi pa nasimulan"}

if "assignments" not in st.session_state:
    st.session_state.assignments = []

# ================== STYLES ==================
st.markdown("""
<style>
.stApp { background-color: #ffffff; }

html, body, p, span, label, div, h1, h2, h3, h4, h5 { color: black !important; }

.header {
    text-align:center; padding:45px; border-radius:20px;
    background: linear-gradient(135deg, #f5e6d3, #c19a6b);
    border:2px solid black; margin-bottom:35px;
}

.card {
    padding:25px; border-radius:20px; border:2px solid black;
    box-shadow:0 6px 18px rgba(0,0,0,0.08); margin-bottom:20px;
}

.stButton>button { background:#8b5e3c; color:white !important; border-radius:10px; }
.stButton>button:hover { background:#5c4033; }

[data-testid="stSidebar"] { background-color:#f8f1e5; border-right:2px solid black; }

            /* Card style for Modules and Quizzes */
.card {
    background: linear-gradient(to right, #d9b38c, #8b5e3c);
    color: black !important;
    padding: 15px;
    margin: 10px 0px;
    border-radius: 12px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
}

/* Buttons */
.stButton>button {
    background-color: #8b5e3c;
    color: white;
    border-radius: 8px;
    padding: 8px 15px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #a6784c;
}

/* Sidebar container */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #f7f2ee, #e0d4c3);
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #d4c0a1;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
}

/* Sidebar buttons as cards */
.stButton>button {
    background-color: #d9b38c;
    color: black;
    border-radius: 10px;
    padding: 10px 15px;
    margin: 5px 0;
    width: 100%;
    font-weight: bold;
    text-align: left;
    transition: all 0.2s ease;
}

/* Hover effect for buttons */
.stButton>button:hover {
    background-color: #b5815b;
    color: white;
    transform: scale(1.02);
}

/* Active page button */
.stButton>button:focus {
    background-color: #8b5e3c;
    color: white;
}

/* Optional icon spacing */
.stButton>button img {
    margin-right: 8px;
    vertical-align: middle;

/* Progress tracker card */
.progress-card {
    background: #fff2e6;
    color: black;
    padding: 15px;
    margin: 10px 0px;
    border-radius: 12px;
    border: 2px solid #d4c0a1;
</style>
""", unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("""
<div class="header">
<h1>📚 A.K.L.A.T.</h1>
<h4>Aplikasyong Katuwang sa Literasiya at Aktibong Pagbasa ng Teksto</h4>
<p><i>Isang makabuluhang plataporma upang mapaunlad ang kakayahan sa pagbasa ng mga Pilipino</i></p>
</div>
""", unsafe_allow_html=True)

# ================== SIDEBAR ==================
st.sidebar.title("🧭 Navigation")

pages = ["Bahay", "Mga Aralin", "Mga Pagsusulit", "Mga Takdang-Aralin", "Mga Marka", "Pagsubaybay sa Pagbasa"]
for p in pages:
    if st.sidebar.button(p):
        st.session_state.page = p

# ================== FUNCTIONS ==================

# ---------- Bahay ----------
def bahay():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Dashboard Overview")

    avg = sum(st.session_state.grades.values())/len(st.session_state.grades) if st.session_state.grades else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Average na Marka", f"{avg:.1f}")
    col2.metric("Nakuha na Pagsusulit", len(st.session_state.quiz_history))
    col3.metric("Reading Streak 🔥", st.session_state.streak)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏆 Mga Nakamit")
    if avg >= 90:
        st.success("🌟 Ganap na Mambabasa")
    elif avg >= 75:
        st.info("📘 Mahusay na Mambabasa")
    else:
        st.write("Magpatuloy sa pagsasanay upang makamit ang mga badge!")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Mga Aralin (Modules) ----------
def aralin():
    st.subheader("📖 Mga Aralin sa Pagbasa")

    modules = {
        "Aralin 1 — Pag-unawa sa Teksto": "https://www.depedcar.ph/sites/default/files/ALS%20English%20Handbook%20-%20Pagbasa%20at%20Pagsulat%20Tungo%20sa%20Pananaliksik%20(Part%20I).pdf",
        "Aralin 2 — Kritikal na Pagbasa": "https://bpb-us-e1.wpmucdn.com/sites.wayne.edu/dist/0/21/files/2016/05/Critical-Reading-Guide-1up.pdf",
        "Aralin 3 — Pagsusuri at Pag-aanalisa ng Impormasyon": "https://eric.ed.gov/?id=ED410518"
    }

    for module, pdf_link in modules.items():
        status = st.session_state.modules_status.get(module, "Hindi pa nasimulan")
        st.markdown(f'<div class="card"><b>{module}</b><br>Status: {status}<br>🔗 <a href="{pdf_link}" target="_blank">I-download ang PDF</a></div>', unsafe_allow_html=True)
        if st.button(f"Mark as Completed - {module}", key=f"complete_{module}"):
            st.session_state.modules_status[module] = "Natapos na"
            # Update reading progress +20% per module
            st.session_state.reading_progress = min(100, st.session_state.reading_progress + 20)
            st.success(f"{module} ay natapos na! 📈 Reading progress tumaas ng 20%")

            # ---------- Mga Pagsusulit (Quizzes) ----------
def pagsusulit():
    st.subheader("📝 Mga Pagsusulit sa Pagbasa")

    quizzes = [
        {
            "title": "Aralin 1 Quiz – Pag-unawa sa Teksto",
            "link": "https://resources.quizalize.com/view/quiz/pagbasa-989629bb-e4a0-4ac7-b3d7-855771ef5816"
        },
        {
            "title": "Aralin 2 Quiz – Kritikal na Pagbasa",
            "link": "https://wayground.com/admin/quiz/62c7a1af187640001d9f95d7/pagbasa"
        },
        {
            "title": "Aralin 3 Quiz – Pagsusuri at Pag-aanalisa",
            "link": "https://wayground.com/admin/quiz/60758ba05b887a001bfdd55b/kritikal-na-pagbasa"
        }
    ]

    for q in quizzes:
        st.markdown(f'<div class="card"><b>{q["title"]}</b><br>🔗 <a href="{q["link"]}" target="_blank">Buksan ang Quiz</a></div>', unsafe_allow_html=True)

    st.markdown("#### I-update ang iyong score upang tumaas ang reading progress")
    score_input = st.number_input("Ilagay ang nakuha mong score (0-100):", min_value=0, max_value=100, step=1, key="quiz_score_input")

    if st.button("I-submit ang score", key="submit_quiz_score"):
        quiz_name = f"User Quiz {len(st.session_state.quiz_history)+1}"
        st.session_state.grades[quiz_name] = score_input
        st.session_state.quiz_history.append(score_input)

        # Update reading progress automatically (score * 0.1%)
        increment = score_input * 0.1
        st.session_state.reading_progress = min(100, st.session_state.reading_progress + increment)
        st.session_state.streak += 1

        st.success(f"Score {score_input}/100 na na-save! 📈 Reading progress tumaas ng {increment:.1f}%")
        # Corrected progress bar for Streamlit
        st.progress(st.session_state.reading_progress / 100)

        # Encouragement
        if st.session_state.reading_progress < 50:
            st.info("Simulan pa lang ang pagbasa...")
        elif st.session_state.reading_progress < 90:
            st.info("Magpatuloy sa pagbabasa!")
        else:
            st.success("🎉 Halos kumpleto na ang pagbasa!")

# ---------- Mga Takdang-Aralin ----------
def takdang_aralin():
    st.subheader("📂 Pagsumite ng Takdang-Aralin")
    file = st.file_uploader("I-upload ang iyong takdang-aralin dito")
    if file:
        st.session_state.assignments.append({"file": file.name, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")})
        st.success("Matagumpay na na-upload ang takdang-aralin!")
    if st.session_state.assignments:
        st.write("📋 Listahan ng Na-submit na Takdang-Aralin:")
        for a in st.session_state.assignments:
            st.write(f"{a['file']} (Uploaded: {a['timestamp']})")

# ---------- Mga Marka ----------
def marka():
    st.subheader("📊 Mga Marka")
    if st.session_state.grades:
        for k, v in st.session_state.grades.items():
            color = "green" if v>=75 else "orange" if v>=50 else "red"
            st.markdown(f'<div class="card" style="border-color:{color}"><b>{k}:</b> {v}/100</div>', unsafe_allow_html=True)
        avg = sum(st.session_state.grades.values())/len(st.session_state.grades)
        st.write(f"Average: {avg:.1f}")
    else:
        st.info("Wala pang nakuhang marka.")

# ---------- Pagsubaybay sa Pagbasa ----------
def pagbasa():
    st.subheader("📈 Pagsubaybay sa Pagbasa (Auto-Updated)")

    progress = st.session_state.reading_progress  # e.g., 70
    st.progress(progress / 100)  # ✅ divide by 100
    st.write(f"Current Progress: {progress:.1f}%")
    
    if progress < 50:
        st.info("Simulan pa lang ang pagbasa...")
    elif progress < 90:
        st.info("Magpatuloy sa pagbabasa!")
    else:
        st.success("🎉 Halos kumpleto na ang pagbasa!")

page_funcs = {
    "Bahay": bahay,
    "Mga Aralin": aralin,         # ✅ Use the Modules function
    "Mga Pagsusulit": pagsusulit, # ✅ Use the Quizzes function
    "Mga Takdang-Aralin": takdang_aralin,
    "Mga Marka": marka,
    "Pagsubaybay sa Pagbasa": pagbasa
}

# Then display the selected page
page_funcs[st.session_state.page]()