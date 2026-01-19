import streamlit as st
import json
import datetime
import google.generativeai as genai
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AI-008: Asisten Guru",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS KUSTOM UNTUK TAMPILAN ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #047857;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #334155;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #059669;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #047857;
        color: white;
    }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if 'user' not in st.session_state:
    st.session_state.user = None
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'classes' not in st.session_state:
    st.session_state.classes = []
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""

# --- FUNGSI UTILITAS ---
def get_download_link(doc):
    """Membuat konten HTML agar bisa didownload sebagai file .doc (Word)"""
    header = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'><head><meta charset='utf-8'><title>" + doc['title'] + "</title><style>table{border-collapse:collapse;width:100%;margin-bottom:1em}th,td{border:1px solid black;padding:8px;text-align:left}th{background-color:#f2f2f2}</style></head><body>"
    body = f"<h1 style='text-align:center;'>{doc['title']}</h1><p><strong>Mata Pelajaran:</strong> {doc['subject']}</p><p><strong>Fase / Kelas:</strong> {doc['phase']} / {doc['grade']}</p><p><strong>Tanggal Dibuat:</strong> {doc['date']}</p><hr/><div style='font-family: Arial, sans-serif; line-height: 1.5;'>{doc['content']}</div>"
    return header + body + "</body></html>"

# --- LOGIN PAGE ---
def login_page():
    st.markdown("<div style='text-align: center; padding: 50px;'>", unsafe_allow_html=True)
    st.title("🎓 AI-008")
    st.subheader("Asisten Cerdas Guru Indonesia")
    
    with st.form("login_form"):
        name = st.text_input("Nama Lengkap (Contoh: Budi, S.Pd)")
        nip = st.text_input("NIP (Opsional)")
        school = st.text_input("Asal Sekolah")
        
        submitted = st.form_submit_button("Masuk Dashboard")
        
        if submitted:
            if name and school:
                st.session_state.user = {"name": name, "nip": nip, "school": school}
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Mohon lengkapi Nama dan Nama Sekolah.")

# --- DASHBOARD PAGE ---
def dashboard_page():
    user = st.session_state.user
    
    # Welcome Banner
    st.markdown(f"""
    <div style="background: linear-gradient(to right, #059669, #0d9488); padding: 30px; border-radius: 20px; color: white; margin-bottom: 30px;">
        <h3>Halo, {user['name']}! 👋</h3>
        <p style="font-size: 1.1em;">{user['school']}</p>
        <p style="margin-top: 10px; opacity: 0.9;">Setiap langkah kecil dalam perencanaan adalah lompatan besar bagi masa depan siswa Anda.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_head, col_stat = st.columns([3, 1])
    with col_head:
        st.subheader("📂 Dokumen Tersimpan")
    with col_stat:
        st.metric("Total Dokumen", len(st.session_state.documents))
    
    if not st.session_state.documents:
        st.info("Belum ada dokumen. Gunakan menu di sidebar untuk membuat Modul Ajar atau Soal.")
    else:
        for idx, doc in enumerate(st.session_state.documents):
            with st.expander(f"{doc['type']} - {doc['subject']} ({doc['date']})"):
                st.markdown(f"**Judul:** {doc['title']}")
                st.markdown(f"**Kelas:** {doc['grade']} ({doc['phase']})")
                st.caption(doc['content'][:200] + "...")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.download_button(
                        label="⬇️ Download Word",
                        data=get_download_link(doc),
                        file_name=f"{doc['title']}.doc",
                        mime="application/msword",
                        key=f"dl_{idx}"
                    )
                with col2:
                    if st.button("🗑️ Hapus", key=f"del_{idx}"):
                        st.session_state.documents.pop(idx)
                        st.rerun()

# --- GENERATOR AI LOGIC ---
def generator_page(doc_type):
    st.title(f"✨ Generator {doc_type}")
    st.info("Lengkapi formulir di bawah ini, AI akan membantu menyusun dokumen Anda.")

    # --- API KEY INPUT (Penting untuk Streamlit Cloud) ---
    with st.expander("🔑 Pengaturan API Key (Google Gemini)", expanded=False):
        api_key = st.text_input("Masukkan Google Gemini API Key Anda", type="password", help="Dapatkan di aistudio.google.com")
        if not api_key:
            # Coba cek st.secrets jika user sudah setting di cloud
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
                st.success("API Key terdeteksi dari sistem.")
            else:
                st.warning("API Key diperlukan untuk menghasilkan konten.")

    # --- FORM INPUT ---
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Mata Pelajaran", placeholder="Contoh: Matematika")
        phase = st.selectbox("Fase", ["Fase Fondasi", "Fase A", "Fase B", "Fase C", "Fase D", "Fase E", "Fase F"])
    
    # Mapping Phase to Grade
    phase_map = {
        'Fase Fondasi': ['PAUD', 'TK A', 'TK B'],
        'Fase A': ['Kelas 1', 'Kelas 2'],
        'Fase B': ['Kelas 3', 'Kelas 4'],
        'Fase C': ['Kelas 5', 'Kelas 6'],
        'Fase D': ['Kelas 7', 'Kelas 8', 'Kelas 9'],
        'Fase E': ['Kelas 10'],
        'Fase F': ['Kelas 11', 'Kelas 12']
    }
    
    with col2:
        grade = st.selectbox("Kelas", phase_map[phase])
        topic = st.text_input("Topik / Materi Pokok", placeholder="Contoh: Pecahan Senilai")

    # --- INPUT KHUSUS BERDASARKAN TIPE ---
    extra_context = ""
    
    if doc_type == "Modul Ajar":
        col_meet, col_dur = st.columns(2)
        with col_meet:
            meeting_count = st.number_input("Jumlah Pertemuan", min_value=1, max_value=20, value=1)
        with col_dur:
            duration_jp = st.selectbox("Durasi 1 JP (Menit)", ["30", "35", "40", "45", "60"], index=1)
        
        st.markdown("<strong>Rincian JP per Pertemuan:</strong>", unsafe_allow_html=True)
        jp_cols = st.columns(min(meeting_count, 5)) # Membatasi kolom visual max 5 per baris
        jp_details = {}
        
        # Loop untuk input JP dinamis
        for i in range(1, meeting_count + 1):
            col_idx = (i - 1) % 5
            if col_idx == 0 and i > 1:
                jp_cols = st.columns(min(meeting_count - (i-1), 5))
            
            with jp_cols[col_idx]:
                jp_val = st.number_input(f"Pert {i} (JP)", min_value=1, value=2, key=f"jp_{i}")
                jp_details[i] = jp_val

        dimensions = st.multiselect("Dimensi Profil Lulusan", [
            "Beriman & Bertakwa", "Berkebinekaan Global", "Gotong Royong", 
            "Kreatif", "Bernalar Kritis", "Mandiri"
        ])
        
    elif doc_type == "Bank Soal":
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            q_type = st.selectbox("Jenis Soal", ["Tes Objektif", "Tes Subjektif", "AKM"])
        with col_q2:
            q_count = st.number_input("Jumlah Soal", min_value=1, value=10)
        with col_q3:
            cog_level = st.selectbox("Level Kognitif", ["LOTS", "MOTS", "HOTS"])
            
    elif doc_type == "Perencanaan":
        ac_year = st.text_input("Tahun Ajaran", value="2024/2025")
        schedule = st.text_area("Jadwal Mengajar", placeholder="Senin: 07.00 - 09.00 (2 JP)...")
        env_desc = st.text_area("Konteks Lingkungan / Sarana / Jurusan (SMK)", 
                               placeholder="Contoh: Lab komputer tersedia, Jurusan TKJ...")

    # --- TOMBOL GENERATE ---
    if st.button("✨ Generate Dokumen"):
        if not api_key:
            st.error("Mohon masukkan API Key Google Gemini terlebih dahulu.")
        elif not subject:
            st.error("Mohon isi Mata Pelajaran.")
        else:
            with st.spinner("Sedang meracik dokumen pendidikan..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # KONSTRUKSI PROMPT
                    teacher_info = f"Guru: {st.session_state.user['name']}, Sekolah: {st.session_state.user['school']}"
                    grade_ctx = f"{grade} ({phase})"
                    table_instruction = "Gunakan format HTML <table> dengan border=1 style='border-collapse:collapse; width:100%'. JANGAN gunakan markdown."
                    
                    prompt = ""
                    if doc_type == "Modul Ajar":
                        sched_str = ", ".join([f"Pertemuan {k} ({v} JP)" for k,v in jp_details.items()])
                        dim_str = ", ".join(dimensions) if dimensions else "Sesuaikan"
                        prompt = f"""
                        Bertindaklah sebagai ahli kurikulum. Buatkan Modul Ajar untuk {subject}, {grade_ctx}, Topik: {topic}.
                        Guru: {teacher_info}.
                        Waktu: {meeting_count} Pertemuan. Rincian: {sched_str}. Durasi 1 JP: {duration_jp} menit.
                        Profil Lulusan: {dim_str}.
                        Struktur HTML Lengkap: Informasi Umum, Komponen Inti, Langkah Pembelajaran (Per Pertemuan), Asesmen, Lampiran.
                        {table_instruction}
                        """
                    elif doc_type == "Bank Soal":
                        prompt = f"""
                        Buatkan Bank Soal {subject}, {grade_ctx}, Topik: {topic}.
                        Jenis: {q_type}, Jumlah: {q_count}, Level: {cog_level}.
                        {table_instruction} Output tabel: No, Soal, Kunci Jawaban, Bobot.
                        """
                    elif doc_type == "Ide Kreatif":
                        prompt = f"5 ide pembelajaran kreatif untuk {subject}, {grade_ctx}, Topik: {topic}. Gunakan HTML rapi."
                    elif doc_type == "Perencanaan":
                        prompt = f"""
                        Buat Prota & Promes Tahun Ajaran {ac_year}. Mapel: {subject}, {grade_ctx}.
                        Jadwal: {schedule}. Konteks Lingkungan: {env_desc}.
                        {table_instruction}
                        """
                    
                    response = model.generate_content(prompt)
                    st.session_state.generated_content = response.text
                    st.success("Selesai!")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

    # --- PREVIEW & SAVE AREA ---
    if st.session_state.generated_content:
        st.divider()
        st.subheader("📝 Preview & Edit")
        
        # Editor
        edited_content = st.text_area("Edit Konten (HTML Support)", 
                                      value=st.session_state.generated_content, 
                                      height=400)
        
        # HTML Preview
        with st.expander("Lihat Hasil Render"):
            st.markdown(edited_content, unsafe_allow_html=True)
        
        # Save Button
        if st.button("💾 Simpan ke Dashboard"):
            new_doc = {
                "id": datetime.datetime.now().isoformat(),
                "type": doc_type,
                "title": f"{doc_type}: {topic if topic else subject}",
                "subject": subject,
                "grade": grade,
                "phase": phase,
                "content": edited_content,
                "date": datetime.datetime.now().strftime("%d %b %Y")
            }
            st.session_state.documents.append(new_doc)
            st.success("Dokumen berhasil disimpan!")
            time.sleep(1)
            st.rerun()

# --- CLASS MANAGEMENT PAGE ---
def class_management_page():
    st.title("👥 Manajemen Kelas")
    
    # 1. Tambah Kelas
    with st.expander("➕ Tambah Kelas Baru"):
        c1, c2, c3 = st.columns([2, 2, 1])
        new_cls_name = c1.text_input("Nama Kelas (misal: 7A)")
        new_cls_subj = c2.text_input("Mapel")
        if c3.button("Buat Kelas"):
            if new_cls_name:
                st.session_state.classes.append({
                    "id": len(st.session_state.classes) + 1,
                    "name": new_cls_name,
                    "subject": new_cls_subj,
                    "students": []
                })
                st.success("Kelas dibuat!")
                st.rerun()

    # 2. Pilih Kelas
    if not st.session_state.classes:
        st.warning("Belum ada kelas.")
        return

    cls_names = [c["name"] for c in st.session_state.classes]
    selected_cls_name = st.selectbox("Pilih Kelas", cls_names)
    
    # Cari objek kelas yang dipilih
    selected_class = next(c for c in st.session_state.classes if c["name"] == selected_cls_name)
    
    st.divider()
    st.subheader(f"Data Kelas: {selected_class['name']} - {selected_class['subject']}")
    
    # 3. Tambah Siswa
    c_add, c_act = st.columns([3, 1])
    new_student = c_add.text_input("Nama Siswa Baru")
    if c_act.button("Tambah Siswa"):
        if new_student:
            selected_class["students"].append({
                "id": len(selected_class["students"]) + 1,
                "name": new_student,
                "attendance": {}, # Dict {date: status}
                "grades": {}      # Dict {date: score}
            })
            st.rerun()

    # 4. Tabel Absensi & Nilai Harian
    st.markdown("### 📅 Jurnal Harian")
    active_date = st.date_input("Tanggal", datetime.date.today()).strftime("%Y-%m-%d")
    
    if selected_class["students"]:
        # Header Tabel
        cols = st.columns([1, 4, 3, 2])
        cols[0].markdown("**No**")
        cols[1].markdown("**Nama**")
        cols[2].markdown("**Kehadiran**")
        cols[3].markdown("**Nilai**")
        
        for idx, student in enumerate(selected_class["students"]):
            cols = st.columns([1, 4, 3, 2])
            cols[0].write(idx + 1)
            cols[1].write(student["name"])
            
            # Attendance Input
            current_status = student["attendance"].get(active_date, "H")
            status_opts = ["H", "S", "I", "A"]
            try:
                idx_stat = status_opts.index(current_status)
            except:
                idx_stat = 0
                
            new_status = cols[2].selectbox(
                "Absen", 
                status_opts, 
                index=idx_stat, 
                key=f"att_{student['id']}_{active_date}", 
                label_visibility="collapsed"
            )
            student["attendance"][active_date] = new_status
            
            # Grade Input
            current_grade = student["grades"].get(active_date, 0.0)
            new_grade = cols[3].number_input(
                "Nilai", 
                value=float(current_grade), 
                key=f"grd_{student['id']}_{active_date}",
                label_visibility="collapsed"
            )
            student["grades"][active_date] = new_grade
            
        st.caption("Data tersimpan otomatis di sesi ini.")
    else:
        st.info("Belum ada siswa di kelas ini.")

# --- MAIN ROUTING ---
def main():
    if not st.session_state.user:
        login_page()
    else:
        with st.sidebar:
            st.title("Menu Navigasi")
            menu = st.radio("Pilih Menu", [
                "Dashboard", 
                "Modul Ajar", 
                "Bank Soal", 
                "Ide Kreatif", 
                "Perencanaan", 
                "Manajemen Kelas"
            ])
            st.divider()
            st.markdown(f"User: **{st.session_state.user['name']}**")
            if st.button("Log Out"):
                st.session_state.user = None
                st.rerun()

        if menu == "Dashboard":
            dashboard_page()
        elif menu in ["Modul Ajar", "Bank Soal", "Ide Kreatif", "Perencanaan"]:
            generator_page(menu)
        elif menu == "Manajemen Kelas":
            class_management_page()

if __name__ == "__main__":
    main()
