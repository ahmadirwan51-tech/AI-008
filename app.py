import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Sparkles, 
  Trash2, 
  Save, 
  Bot, 
  Search, 
  Menu,
  BookOpen,
  Users,
  FileText,
  Calendar,
  ClipboardList,
  Lightbulb,
  FileQuestion,
  School,
  LogOut,
  UserCircle,
  CheckCircle2,
  Download,
  ChevronDown,
  Clock,
  ArrowLeft,
  PlusCircle,
  Edit,
  XCircle,
  TrendingUp,
  MoreHorizontal
} from 'lucide-react';

const App = () => {
  // --- STATE MANAGEMENT ---
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loadingAI, setLoadingAI] = useState(false);

  // --- PERSISTENT DATA STATE (LocalStorage) ---
  const [userProfile, setUserProfile] = useState({ name: '', nip: '', school: '' });
  const [documents, setDocuments] = useState([]);
  
  // Data Kelas
  const [classes, setClasses] = useState([]); 

  // --- INITIAL LOAD FROM STORAGE ---
  useEffect(() => {
    const savedUser = localStorage.getItem('ai008_user');
    const savedDocs = localStorage.getItem('ai008_docs');
    const savedClasses = localStorage.getItem('ai008_classes');

    if (savedUser) {
      setUserProfile(JSON.parse(savedUser));
      setIsLoggedIn(true);
    }
    if (savedDocs) setDocuments(JSON.parse(savedDocs));
    if (savedClasses) setClasses(JSON.parse(savedClasses));
  }, []);

  // --- SAVE TO STORAGE ON CHANGE ---
  useEffect(() => {
    if (isLoggedIn) localStorage.setItem('ai008_user', JSON.stringify(userProfile));
  }, [userProfile, isLoggedIn]);

  useEffect(() => {
    localStorage.setItem('ai008_docs', JSON.stringify(documents));
  }, [documents]);

  useEffect(() => {
    localStorage.setItem('ai008_classes', JSON.stringify(classes));
  }, [classes]);

  // Form State for Generators
  const [formData, setFormData] = useState({
    type: '',
    subject: '',
    phase: 'Fase A',
    grade: 'Kelas 1',
    topic: '',
    meetingCount: '1', // Jumlah Pertemuan
    jpDetails: { 1: '2' }, // Detail JP per pertemuan (default pert 1 = 2 JP)
    durationPerJP: '35',
    selectedDimensions: [],
    teachingSchedule: '',
    environmentDescription: '', // NEW: Deskripsi Lingkungan/Sarana/Prodi
    academicYear: '2024/2025',
    questionType: 'Tes Objektif',
    questionCount: '10',
    cognitiveLevel: 'HOTS',
    content: ''
  });

  // Options & Constants
  const dimensionOptions = [
    "Keimanan dan ketakwaan Terhadap Tuhan YME",
    "Kewargaan",
    "Penalaran Kritis",
    "Kreativitas",
    "Kolaborasi",
    "Kemandirian",
    "Kesehatan",
    "Komunikasi"
  ];

  const durationOptions = [
    { label: "PAUD (30 Menit)", value: "30" },
    { label: "SD (35 Menit)", value: "35" },
    { label: "SMP (40 Menit)", value: "40" },
    { label: "SMA / SMK (45 Menit)", value: "45" },
    { label: "Khusus (60 Menit)", value: "60" }
  ];

  const questionTypeOptions = ["Tes Objektif", "Tes Subjektif", "AKM"];
  const cognitiveLevelOptions = ["LOTS", "MOTS", "HOTS"];

  const phaseMap = {
    'Fase Fondasi': ['PAUD', 'TK A', 'TK B'],
    'Fase A': ['Kelas 1', 'Kelas 2'],
    'Fase B': ['Kelas 3', 'Kelas 4'],
    'Fase C': ['Kelas 5', 'Kelas 6'],
    'Fase D': ['Kelas 7', 'Kelas 8', 'Kelas 9'],
    'Fase E': ['Kelas 10'],
    'Fase F': ['Kelas 11', 'Kelas 12']
  };

  const menuGroups = [
    {
      title: "PERANGKAT AJAR (AI)",
      items: [
        { id: 'Modul Ajar', label: 'Modul Ajar', icon: <BookOpen size={20} /> },
        { id: 'Bank Soal', label: 'Bank Soal', icon: <FileQuestion size={20} /> },
        { id: 'Ide Kreatif', label: 'Ide Kreatif', icon: <Lightbulb size={20} /> },
      ]
    },
    {
      title: "MANAJEMEN KELAS",
      items: [
        { id: 'Manajemen Kelas', label: 'Kelas & Penilaian', icon: <Users size={20} /> },
      ]
    },
    {
      title: "PERENCANAAN (AI)",
      items: [
        { id: 'Perencanaan', label: 'Prota & Promes', icon: <Calendar size={20} /> },
      ]
    }
  ];

  const isGeneratorGroup = (type) => ['Modul Ajar', 'Bank Soal', 'Ide Kreatif', 'Perencanaan'].includes(type);
  const isClassGroup = (type) => ['Manajemen Kelas'].includes(type);

  // Effect to reset form when changing tabs
  useEffect(() => {
    if (activeTab !== 'Dashboard' && isGeneratorGroup(activeTab)) {
      setFormData(prev => ({
        ...prev,
        type: activeTab,
        content: '',
        topic: '',
        subject: prev.subject,
        selectedDimensions: [],
        questionType: 'Tes Objektif',
        questionCount: '10',
        cognitiveLevel: 'HOTS',
        // Reset specific fields
        meetingCount: '1',
        jpDetails: { 1: '2' },
        environmentDescription: ''
      }));
    }
  }, [activeTab]);

  // --- API KEY CONFIGURATION ---
  const apiKey = ""; 

  // --- HANDLERS ---
  const [loginInput, setLoginInput] = useState({ name: '', nip: '', school: '' });
  
  const handleLogin = (e) => {
    e.preventDefault();
    if (loginInput.name && loginInput.school) {
      setUserProfile(loginInput);
      setIsLoggedIn(true);
    } else {
      alert("Mohon lengkapi Nama dan Nama Sekolah.");
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserProfile({ name: '', nip: '', school: '' });
    setActiveTab('Dashboard');
    localStorage.removeItem('ai008_user');
  };

  const handleDimensionToggle = (dim) => {
    setFormData(prev => {
      const current = prev.selectedDimensions || [];
      if (current.includes(dim)) {
        return { ...prev, selectedDimensions: current.filter(d => d !== dim) };
      } else {
        return { ...prev, selectedDimensions: [...current, dim] };
      }
    });
  };

  const handlePhaseChange = (e) => {
    const selectedPhase = e.target.value;
    setFormData({ ...formData, phase: selectedPhase, grade: phaseMap[selectedPhase][0] });
  };

  const handleMeetingCountChange = (val) => {
    const count = parseInt(val) || 1;
    const safeCount = Math.max(1, Math.min(count, 20)); // Limit 1-20 meetings
    
    // Initialize default JP for new meetings if not present
    const newDetails = { ...formData.jpDetails };
    for (let i = 1; i <= safeCount; i++) {
        if (!newDetails[i]) newDetails[i] = '2'; // Default 2 JP
    }
    setFormData({ ...formData, meetingCount: safeCount.toString(), jpDetails: newDetails });
  };

  const handleJpDetailChange = (meeting, val) => {
      setFormData({
          ...formData,
          jpDetails: { ...formData.jpDetails, [meeting]: val }
      });
  };

  // Class Management Handlers
  const addClass = (name, subject) => {
    const newClass = { id: Date.now(), name, subject, students: [] };
    setClasses([...classes, newClass]);
  };

  const addStudent = (classId, studentName) => {
    setClasses(classes.map(c => {
      if (c.id === classId) {
        return { ...c, students: [...c.students, { id: Date.now(), name: studentName, attendance: {}, dailyGrades: {} }] };
      }
      return c;
    }));
  };

  const updateStudentData = (classId, studentId, date, field, value) => {
    setClasses(classes.map(c => {
      if (c.id === classId) {
        return {
          ...c,
          students: c.students.map(s => {
            if (s.id === studentId) {
              if (field === 'attendance') return { ...s, attendance: { ...s.attendance, [date]: value } };
              else if (field === 'grade') return { ...s, dailyGrades: { ...s.dailyGrades, [date]: value } };
            }
            return s;
          })
        };
      }
      return c;
    }));
  };

  const deleteClass = (id) => {
    if(confirm("Hapus kelas ini beserta semua data siswanya?")) {
      setClasses(classes.filter(c => c.id !== id));
    }
  };

  // Document Handlers
  const handleSaveDocument = () => {
    if (!formData.subject) return;
    const newDoc = {
      id: Date.now(),
      type: formData.type,
      title: `${formData.type}: ${formData.topic || formData.academicYear}`,
      subject: formData.subject,
      phase: formData.phase,
      grade: formData.grade,
      content: formData.content,
      status: "Draft",
      date: new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
    };
    setDocuments([newDoc, ...documents]);
    setActiveTab('Dashboard');
  };

  const handleDelete = (id) => {
    setDocuments(documents.filter(d => d.id !== id));
  };

  const handleDownloadWord = (doc) => {
    const header = `<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'><head><meta charset='utf-8'><title>${doc.title}</title><style>table{border-collapse:collapse;width:100%;margin-bottom:1em}th,td{border:1px solid black;padding:8px;text-align:left}th{background-color:#f2f2f2}</style></head><body>`;
    const bodyContent = `<h1 style="text-align:center;">${doc.title}</h1><p><strong>Mata Pelajaran:</strong> ${doc.subject}</p><p><strong>Fase / Kelas:</strong> ${doc.phase} / ${doc.grade}</p><p><strong>Tanggal Dibuat:</strong> ${doc.date}</p><hr/><div style="font-family: Arial, sans-serif; line-height: 1.5;">${doc.content}</div>`;
    const sourceHTML = header + bodyContent + "</body></html>";
    const source = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(sourceHTML);
    const fileDownload = document.createElement("a");
    document.body.appendChild(fileDownload);
    fileDownload.href = source;
    fileDownload.download = `${doc.title}.doc`;
    fileDownload.click();
    document.body.removeChild(fileDownload);
  };

  const generateContent = async () => {
    if (!formData.subject) { alert("Mohon isi Mata Pelajaran."); return; }
    setLoadingAI(true);
    
    const teacherContext = `Guru: ${userProfile.name}, NIP: ${userProfile.nip}, Sekolah: ${userProfile.school}`;
    const gradeContext = `${formData.grade} (${formData.phase})`;
    const tableInstruction = "PENTING: Jika membuat tabel, GUNAKAN FORMAT HTML TABLE STANDARD (<table border='1' style='border-collapse:collapse; width:100%'>...</table>) agar rapi saat dicopy ke Word. JANGAN gunakan markdown.";
    let promptContext = "";

    if (formData.type === "Modul Ajar") {
        const dimensions = formData.selectedDimensions.length > 0 ? formData.selectedDimensions.join(", ") : "Pilih dimensi yang relevan secara mandiri";
        
        // Build schedule detail string
        const count = parseInt(formData.meetingCount) || 1;
        let scheduleDetails = [];
        let totalJP = 0;
        for(let i=1; i<=count; i++) {
            const jp = parseInt(formData.jpDetails[i] || '2');
            scheduleDetails.push(`Pertemuan ${i} (${jp} JP)`);
            totalJP += jp;
        }
        const scheduleString = scheduleDetails.join(', ');

        promptContext = `Bertindaklah sebagai ahli kurikulum Indonesia. Buatkan **Modul Ajar Lengkap** untuk mapel ${formData.subject} tingkat ${gradeContext} topik "${formData.topic}". 
        
        DETAIL WAKTU:
        - Total Pertemuan: ${count} kali pertemuan
        - Total Jam Pelajaran (JP): ${totalJP} JP
        - Rincian Alokasi Waktu: ${scheduleString}
        - Durasi 1 JP: ${formData.durationPerJP || '35'} menit.
        
        INSTRUKSI KHUSUS PROFIL LULUSAN: Ganti "Profil Pelajar Pancasila" dengan "Dimensi Profil Lulusan": ${dimensions}. 
        Identitas: ${teacherContext}. 
        Rujukan: Keputusan Kepala BSKAP No. 046/H/KR/2025. 
        
        STRUKTUR MODUL (Output HTML Lengkap): 
        1. Informasi Umum
        2. Komponen Inti (Tujuan Pembelajaran, Pemahaman Bermakna, Pertanyaan Pemantik)
        3. Langkah Pembelajaran (Detailkan kegiatan Pembuka, Inti, Penutup untuk SETIAP PERTEMUAN (Pertemuan 1 sampai ${count}) sesuai alokasi JP masing-masing)
        4. Asesmen
        5. Lampiran (LKPD & Bahan Bacaan)
        
        ${tableInstruction}`;
    } else if (formData.type === "Bank Soal") {
        promptContext = `Buatkan Bank Soal untuk mapel ${formData.subject} tingkat ${gradeContext} topik "${formData.topic}". Detail: Jenis ${formData.questionType}, Jumlah ${formData.questionCount} butir, Kognitif ${formData.cognitiveLevel}. ${formData.questionType === 'AKM' ? 'Berbasis stimulus literasi/numerasi.' : ''} ${tableInstruction} Output: Tabel No, Soal, Kunci, Bobot.`;
    } else if (formData.type === "Ide Kreatif") {
        promptContext = `5 ide metode pembelajaran kreatif untuk topik "${formData.topic}" siswa ${gradeContext}. ${tableInstruction} jika diperlukan.`;
    } else if (formData.type === "Perencanaan") {
        promptContext = `Buatkan dokumen Perencanaan Pembelajaran Lengkap (Prota & Promes) untuk Tahun Ajaran ${formData.academicYear}. Mapel: ${formData.subject}, Tingkat: ${gradeContext}. 
        
        Jadwal Mengajar: ${formData.teachingSchedule}. 
        
        KONTEKS KHUSUS SEKOLAH/JURUSAN: ${formData.environmentDescription ? formData.environmentDescription : "Gunakan standar umum kurikulum merdeka."}
        Instruksi: Sesuaikan materi, studi kasus, atau alokasi waktu dengan konteks lingkungan/sarana/jurusan di atas jika relevan.

        ${tableInstruction} Pastikan tabel HTML rapi.`;
    }

    try {
      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ contents: [{ parts: [{ text: promptContext }] }] })
        }
      );
      const data = await response.json();
      const generatedText = data.candidates?.[0]?.content?.parts?.[0]?.text || "Gagal menghasilkan konten.";
      setFormData(prev => ({ ...prev, content: generatedText }));
    } catch (error) {
      console.error(error);
      alert("Terjadi kesalahan koneksi AI.");
    } finally {
      setLoadingAI(false);
    }
  };

  // --- RENDER ---

  if (!isLoggedIn) {
    return (
       <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans">
        <div className="bg-white max-w-md w-full rounded-3xl shadow-2xl overflow-hidden border border-slate-100">
          <div className="bg-gradient-to-br from-emerald-600 to-teal-700 p-10 text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
            <Bot className="w-16 h-16 text-white mx-auto mb-4 relative z-10 drop-shadow-md" />
            <h1 className="text-3xl font-extrabold text-white tracking-widest relative z-10">AI-008</h1>
            <p className="text-emerald-100 mt-2 text-sm font-medium relative z-10">Asisten Cerdas Guru Indonesia</p>
          </div>
          <div className="p-8">
            <h2 className="text-xl font-bold text-slate-800 mb-6 text-center">Selamat Datang, Pahlawan Pendidikan</h2>
            <form onSubmit={handleLogin} className="space-y-5">
              <input type="text" required className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 outline-none transition-all" placeholder="Nama Lengkap (Contoh: Budi, S.Pd)" value={loginInput.name} onChange={(e) => setLoginInput({...loginInput, name: e.target.value})} />
              <input type="text" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 outline-none transition-all" placeholder="NIP (Opsional)" value={loginInput.nip} onChange={(e) => setLoginInput({...loginInput, nip: e.target.value})} />
              <input type="text" required className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 outline-none transition-all" placeholder="Asal Sekolah" value={loginInput.school} onChange={(e) => setLoginInput({...loginInput, school: e.target.value})} />
              <button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3.5 rounded-2xl shadow-lg shadow-emerald-200 transition-all hover:-translate-y-0.5">Masuk Dashboard</button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-800 overflow-hidden">
      {/* SIDEBAR */}
      <aside className={`${sidebarOpen ? 'w-72' : 'w-20'} bg-gradient-to-b from-emerald-900 to-teal-900 text-white transition-all duration-300 flex flex-col shadow-2xl z-20`}>
        <div className="p-6 flex items-center justify-between border-b border-emerald-800/30">
          {sidebarOpen && <div className="flex items-center gap-3"><div className="bg-white/10 p-2 rounded-xl backdrop-blur-sm"><Bot className="w-6 h-6 text-white"/></div><h1 className="text-xl font-bold tracking-widest text-white">AI-008</h1></div>}
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-white/10 rounded-xl transition-colors"><Menu className="w-5 h-5 text-emerald-100" /></button>
        </div>
        <nav className="flex-1 overflow-y-auto py-6 px-4 space-y-8 scrollbar-hide">
          <button onClick={() => setActiveTab('Dashboard')} className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-2xl text-sm transition-all duration-200 group font-medium ${activeTab === 'Dashboard' ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-900/20' : 'text-emerald-100 hover:bg-white/5'}`}>
            <LayoutDashboard size={20} />{sidebarOpen && <span className="truncate">Dashboard Utama</span>}
          </button>
          {menuGroups.map((group, index) => (
            <div key={index} className={!sidebarOpen ? 'hidden md:block' : ''}>
              {sidebarOpen && <h4 className="px-4 mb-3 text-[10px] font-bold text-emerald-400 tracking-widest uppercase opacity-80">{group.title}</h4>}
              <div className="space-y-2">
                {group.items.map((item) => (
                  <button key={item.id} onClick={() => setActiveTab(item.id)} className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm transition-all duration-200 group font-medium ${activeTab === item.id ? 'bg-white/10 text-white border border-white/10 shadow-inner' : 'text-emerald-200 hover:bg-white/5 hover:text-white'}`}>
                    <div className={`${activeTab === item.id ? 'text-white' : 'text-emerald-400/80 group-hover:text-emerald-200'}`}>{item.icon}</div>{sidebarOpen && <span className="truncate">{item.label}</span>}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </nav>
        <div className="p-4 bg-emerald-950/30 backdrop-blur-md border-t border-emerald-800/30">
           <div className="flex items-center gap-3">
             <div className="w-10 h-10 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center font-bold text-white shadow-md border-2 border-white/20">{userProfile.name.charAt(0)}</div>
             {sidebarOpen && <div className="truncate flex-1"><p className="text-sm font-bold truncate text-white">{userProfile.name}</p><p className="text-[10px] text-emerald-300 truncate">{userProfile.school}</p></div>}
             {sidebarOpen && <button onClick={handleLogout} className="p-2 hover:bg-red-500/20 rounded-lg text-emerald-400 hover:text-red-300 transition-colors"><LogOut size={18}/></button>}
           </div>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col overflow-hidden relative bg-gradient-to-br from-slate-50 via-white to-emerald-50/30">
        
        {/* HEADER */}
        <header className="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200/60 flex items-center justify-between px-8 shadow-sm z-10">
          <div className="flex flex-col">
             <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
                {activeTab === 'Dashboard' ? <LayoutDashboard className="text-emerald-600"/> : <Sparkles className="text-emerald-600"/>}
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600">
                  {activeTab === 'Dashboard' ? 'DASHBOARD UTAMA' : activeTab.toUpperCase()}
                </span>
             </h2>
             <p className="text-xs text-slate-500 mt-1 font-medium">
               {activeTab === 'Dashboard' ? 'Selamat datang kembali! Siap menginspirasi siswa hari ini?' : 'Mari susun administrasi terbaik untuk kelas Anda.'}
             </p>
          </div>
          {activeTab === 'Dashboard' && (
             <div className="hidden md:flex items-center gap-2 bg-white px-4 py-2 rounded-full border border-slate-200 shadow-sm text-xs font-semibold text-slate-600">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                {documents.length} Dokumen Tersimpan
             </div>
          )}
        </header>

        <div className="flex-1 overflow-y-auto p-8 scroll-smooth">
          
          {/* VIEW 1: DASHBOARD */}
          {activeTab === 'Dashboard' && (
            <div className="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-500">
               {/* Welcome Banner */}
               <div className="bg-gradient-to-r from-emerald-600 to-teal-500 rounded-[2rem] p-8 mb-10 text-white shadow-xl shadow-emerald-900/10 relative overflow-hidden group transition-all hover:shadow-2xl hover:shadow-emerald-900/20">
                  <div className="relative z-10 max-w-2xl">
                    <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/20 backdrop-blur-md rounded-full text-xs font-medium mb-4 border border-white/20">
                      <School size={12} /> {userProfile.school || 'Sekolah Impian'}
                    </div>
                    <h3 className="text-3xl font-bold mb-3 tracking-tight">Halo, {userProfile.name || 'Bapak/Ibu Guru'}! 👋</h3>
                    <p className="text-emerald-50 text-lg leading-relaxed font-light">
                      Setiap langkah kecil dalam perencanaan adalah lompatan besar bagi masa depan siswa Anda. Mari mulai berkarya hari ini.
                    </p>
                  </div>
                  <Bot className="absolute -right-8 -bottom-12 w-48 h-48 text-white opacity-10 rotate-12 group-hover:scale-110 group-hover:rotate-6 transition-all duration-700 ease-out" />
                  <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
               </div>

               <div className="flex items-center justify-between mb-6">
                  <h3 className="font-bold text-slate-700 text-lg flex items-center gap-2">
                    <FileText className="text-emerald-500" size={20}/> Dokumen Terakhir
                  </h3>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-12">
                {documents.length > 0 ? (
                  documents.map((doc) => <DocumentCard key={doc.id} doc={doc} onDelete={handleDelete} onDownload={handleDownloadWord} />)
                ) : (
                  <div className="col-span-full py-24 text-center bg-white/60 backdrop-blur-sm rounded-[2rem] border-2 border-dashed border-slate-300 flex flex-col items-center justify-center hover:border-emerald-300 transition-colors group cursor-pointer" onClick={() => setActiveTab('Modul Ajar')}>
                    <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-sm border border-slate-100">
                       <PlusCircle className="w-10 h-10 text-slate-300 group-hover:text-emerald-500 transition-colors" />
                    </div>
                    <h4 className="text-slate-700 font-bold text-lg">Ruang kerja Anda masih kosong</h4>
                    <p className="text-slate-500 text-sm mt-2 max-w-md mx-auto">
                      Belum ada dokumen yang dibuat. Pilih menu di samping untuk mulai menyusun Modul Ajar, Soal, atau Administrasi Kelas.
                    </p>
                    <button className="mt-6 px-6 py-2.5 bg-emerald-600 text-white rounded-full font-bold text-sm shadow-lg shadow-emerald-200 hover:shadow-emerald-300 hover:-translate-y-1 transition-all">
                      Buat Dokumen Pertama
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* VIEW 2: GENERATOR FORM */}
          {isGeneratorGroup(activeTab) && (
            <div className="max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-300">
              <div className="bg-white rounded-[2rem] shadow-xl shadow-slate-200/50 border border-slate-100 overflow-hidden flex flex-col min-h-[600px]">
                
                {/* Form Header */}
                <div className="relative bg-slate-50/50 border-b border-slate-100 p-8 flex justify-between items-start overflow-hidden">
                   <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>
                   <div className="relative z-10">
                      <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-bold mb-3 uppercase tracking-wider border border-emerald-200">
                         <Sparkles size={12}/> AI Generator
                      </div>
                      <h3 className="font-bold text-3xl text-slate-800 mb-2 tracking-tight">{activeTab}</h3>
                      <p className="text-slate-500 max-w-xl leading-relaxed text-sm">
                         Lengkapi formulir di bawah ini dengan santai. AI kami akan membantu merangkai kata-kata pendidikan yang tepat dan profesional untuk kebutuhan kelas Anda.
                      </p>
                   </div>
                   <button onClick={() => setActiveTab('Dashboard')} className="group flex items-center justify-center w-10 h-10 rounded-full bg-white border border-slate-200 shadow-sm text-slate-400 hover:text-emerald-600 hover:border-emerald-200 transition-all z-10">
                      <ArrowLeft size={20} className="group-hover:-translate-x-0.5 transition-transform"/>
                   </button>
                </div>

                <div className="p-10 flex-1 overflow-y-auto">
                   <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6 mb-10">
                      
                      {/* Common Input: Subject */}
                      <div className="col-span-full md:col-span-2 group">
                         <label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Mata Pelajaran</label>
                         <input type="text" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none text-slate-700 font-medium placeholder:text-slate-400" placeholder="Contoh: Matematika / IPAS" value={formData.subject} onChange={(e) => setFormData({...formData, subject: e.target.value})} />
                      </div>

                      {/* Common Selects */}
                      <div className="group">
                        <label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Pilih Fase</label>
                        <div className="relative">
                          <select className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none text-slate-700 font-medium appearance-none cursor-pointer" value={formData.phase} onChange={handlePhaseChange}>{Object.keys(phaseMap).map(phase => <option key={phase} value={phase}>{phase}</option>)}</select>
                          <ChevronDown className="absolute right-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                        </div>
                      </div>
                      <div className="group">
                        <label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Pilih Kelas</label>
                        <div className="relative">
                          <select className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none text-slate-700 font-medium appearance-none cursor-pointer" value={formData.grade} onChange={(e) => setFormData({...formData, grade: e.target.value})}>{phaseMap[formData.phase].map(grade => <option key={grade} value={grade}>{grade}</option>)}</select>
                          <ChevronDown className="absolute right-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                        </div>
                      </div>
                      
                      {/* --- Dynamic Inputs based on Type --- */}
                      {formData.type === 'Modul Ajar' && (
                        <>
                          <div className="col-span-full group"><label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Topik / Materi Pokok</label><input type="text" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" value={formData.topic} onChange={(e) => setFormData({...formData, topic: e.target.value})} placeholder="Contoh: Pecahan Senilai" /></div>
                          
                          {/* Jml Pertemuan & Durasi */}
                          <div className="grid grid-cols-2 gap-4 col-span-full">
                              <div className="group">
                                  <label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Jumlah Pertemuan</label>
                                  <input 
                                    type="number" 
                                    min="1" 
                                    max="20"
                                    className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" 
                                    value={formData.meetingCount} 
                                    onChange={(e) => handleMeetingCountChange(e.target.value)} 
                                    placeholder="1" 
                                  />
                              </div>
                              <div className="group">
                                  <label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Durasi 1 JP (Menit)</label>
                                  <div className="relative">
                                      <select className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none appearance-none cursor-pointer" value={formData.durationPerJP} onChange={(e) => setFormData({...formData, durationPerJP: e.target.value})}>
                                          {durationOptions.map((opt, i) => <option key={i} value={opt.value}>{opt.label}</option>)}
                                      </select>
                                      <ChevronDown className="absolute right-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                                  </div>
                              </div>
                          </div>

                          {/* Dynamic JP Input Grid */}
                          <div className="col-span-full bg-slate-50 p-4 rounded-2xl border border-slate-200">
                             <label className="block text-xs font-bold text-slate-500 mb-3 uppercase tracking-wider flex items-center gap-2">
                                <Clock size={14}/> Atur JP Per Pertemuan
                             </label>
                             <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3">
                                {Array.from({ length: Math.min(parseInt(formData.meetingCount) || 1, 20) }).map((_, idx) => {
                                    const meetingNum = idx + 1;
                                    return (
                                        <div key={meetingNum} className="flex flex-col">
                                            <span className="text-[10px] font-bold text-slate-500 mb-1 ml-1">Pertemuan {meetingNum}</span>
                                            <div className="relative group/jp">
                                                <input 
                                                    type="number" 
                                                    min="1"
                                                    className="w-full pl-3 pr-8 py-2 border border-slate-300 rounded-xl text-sm focus:border-emerald-500 focus:ring-2 focus:ring-emerald-200 outline-none text-center font-bold text-slate-700" 
                                                    value={formData.jpDetails[meetingNum] || ''} 
                                                    onChange={(e) => handleJpDetailChange(meetingNum, e.target.value)}
                                                />
                                                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-slate-400 font-bold group-focus-within/jp:text-emerald-600">JP</span>
                                            </div>
                                        </div>
                                    );
                                })}
                             </div>
                             <p className="text-[10px] text-slate-400 mt-2 text-center italic">Sesuaikan jumlah JP jika beban materi tiap pertemuan berbeda.</p>
                          </div>

                          <div className="col-span-full"><label className="block text-sm font-bold text-slate-700 mb-4">Dimensi Profil Lulusan (Wajib Dipilih)</label><div className="grid grid-cols-1 md:grid-cols-2 gap-3">{dimensionOptions.map((dim, idx) => (<label key={idx} className={`flex items-start gap-3 p-4 rounded-xl border transition-all cursor-pointer ${formData.selectedDimensions.includes(dim) ? 'bg-emerald-50 border-emerald-300 shadow-sm' : 'bg-white border-slate-200 hover:bg-slate-50'}`}><div className={`mt-0.5 w-5 h-5 rounded border flex items-center justify-center transition-colors ${formData.selectedDimensions.includes(dim) ? 'bg-emerald-500 border-emerald-500' : 'border-slate-300 bg-white'}`}>{formData.selectedDimensions.includes(dim) && <CheckCircle2 size={14} className="text-white"/>}</div><input type="checkbox" className="hidden" checked={formData.selectedDimensions.includes(dim)} onChange={() => handleDimensionToggle(dim)} /><span className={`text-sm font-medium leading-snug ${formData.selectedDimensions.includes(dim) ? 'text-emerald-800' : 'text-slate-600'}`}>{dim}</span></label>))}</div></div>
                        </>
                      )}

                      {/* Bank Soal Fields */}
                      {formData.type === 'Bank Soal' && (
                         <>
                          <div className="col-span-full group"><label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Topik / Materi Pokok</label><input type="text" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" value={formData.topic} onChange={(e) => setFormData({...formData, topic: e.target.value})} /></div>
                          <div className="group">
                            <label className="block text-sm font-bold text-slate-700 mb-2">Jenis Soal</label>
                            <div className="relative">
                              <select className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none appearance-none" value={formData.questionType} onChange={(e) => setFormData({...formData, questionType: e.target.value})}>
                                {questionTypeOptions.map((opt, i) => <option key={i} value={opt}>{opt}</option>)}
                              </select>
                              <ChevronDown className="absolute right-5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
                            </div>
                          </div>
                          <div className="group">
                            <label className="block text-sm font-bold text-slate-700 mb-2">Jumlah Soal</label>
                            <input type="number" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" value={formData.questionCount} onChange={(e) => setFormData({...formData, questionCount: e.target.value})} />
                          </div>
                          <div className="col-span-full">
                             <label className="block text-sm font-bold text-slate-700 mb-4">Tingkat Berpikir (Kognitif)</label>
                             <div className="flex flex-wrap gap-4">
                                {cognitiveLevelOptions.map(level => (
                                   <label key={level} className={`flex items-center gap-3 px-5 py-3 rounded-xl border cursor-pointer transition-all ${formData.cognitiveLevel === level ? 'bg-emerald-50 border-emerald-300 shadow-sm' : 'bg-white border-slate-200 hover:bg-slate-50'}`}>
                                      <div className={`w-5 h-5 rounded-full border flex items-center justify-center ${formData.cognitiveLevel === level ? 'border-emerald-500' : 'border-slate-300'}`}>
                                        {formData.cognitiveLevel === level && <div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>}
                                      </div>
                                      <input type="radio" name="cognitiveLevel" className="hidden" checked={formData.cognitiveLevel === level} onChange={() => setFormData({...formData, cognitiveLevel: level})}/>
                                      <span className={`text-sm font-bold ${formData.cognitiveLevel === level ? 'text-emerald-800' : 'text-slate-600'}`}>{level}</span>
                                   </label>
                                ))}
                             </div>
                          </div>
                         </>
                      )}

                      {/* Ide Kreatif Field */}
                      {formData.type === 'Ide Kreatif' && <div className="col-span-full group"><label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Topik / Materi Pokok</label><input type="text" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" value={formData.topic} onChange={(e) => setFormData({...formData, topic: e.target.value})} /></div>}
                      
                      {/* Perencanaan Fields */}
                      {formData.type === 'Perencanaan' && (
                         <>
                          <div className="col-span-full group"><label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Tahun Ajaran</label><input type="text" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" value={formData.academicYear} onChange={(e) => setFormData({...formData, academicYear: e.target.value})} /></div>
                          <div className="col-span-full group"><label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Jadwal Mengajar</label><textarea rows="2" className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" value={formData.teachingSchedule} onChange={(e) => setFormData({...formData, teachingSchedule: e.target.value})} placeholder="Contoh: Senin: 07.00 - 09.00 (2 JP)..." /></div>
                          
                          {/* New Field */}
                          <div className="col-span-full group">
                            <label className="block text-sm font-bold text-slate-700 mb-2 group-focus-within:text-emerald-600 transition-colors">Konteks Lingkungan / Sarana / Program Studi (SMK)</label>
                            <textarea 
                              rows="3" 
                              className="w-full px-5 py-3.5 border border-slate-200 rounded-2xl bg-slate-50/50 focus:bg-white focus:ring-4 focus:ring-emerald-100 focus:border-emerald-500 transition-all outline-none" 
                              value={formData.environmentDescription} 
                              onChange={(e) => setFormData({...formData, environmentDescription: e.target.value})} 
                              placeholder="Contoh: Sekolah di daerah pesisir, tersedia lab komputer, atau Program Keahlian Teknik Komputer Jaringan..." 
                            />
                            <p className="text-xs text-slate-400 mt-2">Info ini membantu AI menyesuaikan materi dengan kondisi nyata sekolah Anda.</p>
                          </div>
                         </>
                      )}
                   </div>

                   {/* Action Buttons */}
                   <div className="flex justify-end pt-6 border-t border-slate-100">
                      <button 
                        onClick={generateContent}
                        disabled={loadingAI}
                        className={`px-8 py-4 rounded-2xl text-sm font-bold flex items-center gap-3 shadow-xl transition-all hover:-translate-y-1 ${
                          loadingAI ? 'bg-slate-100 text-slate-400 cursor-wait' : 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-emerald-200'
                        }`}
                      >
                        {loadingAI ? <><div className="w-5 h-5 border-3 border-current border-t-transparent rounded-full animate-spin"/> Sedang Meracik...</> : <><Sparkles className="w-5 h-5" /> GENERATE DOKUMEN</>}
                      </button>
                   </div>

                   {/* Generated Content View */}
                   {formData.content && (
                     <div className="mt-12 animate-in fade-in duration-500">
                        <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-5 mb-6 flex items-start gap-4">
                          <div className="p-2 bg-emerald-100 rounded-full text-emerald-600"><CheckCircle2 size={24}/></div>
                          <div>
                             <h4 className="font-bold text-lg text-emerald-900">Dokumen Berhasil Dibuat!</h4>
                             <p className="text-sm text-emerald-700 mt-1">Silakan review hasil di bawah ini. Anda bisa menyimpannya atau membuatnya ulang jika belum sesuai.</p>
                          </div>
                        </div>
                        <div className="border border-slate-200 rounded-[2rem] p-8 bg-white min-h-[400px] prose prose-slate prose-headings:font-bold prose-a:text-emerald-600 max-w-none shadow-sm" dangerouslySetInnerHTML={{ __html: formData.content }}></div>
                        <div className="flex justify-end gap-4 mt-8">
                           <button onClick={() => setFormData({...formData, content: ''})} className="px-8 py-3 text-slate-500 hover:bg-slate-100 rounded-xl font-bold transition-colors">Buang & Ulangi</button>
                           <button onClick={handleSaveDocument} className="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold flex items-center gap-2 shadow-lg shadow-indigo-200 transition-all hover:-translate-y-1"><Save size={18}/> SIMPAN DOKUMEN</button>
                        </div>
                     </div>
                   )}
                </div>
              </div>
            </div>
          )}

          {/* --- CLASS MANAGEMENT VIEW --- */}
          {isClassGroup(activeTab) && (
            <ClassManager 
              classes={classes} 
              onAddClass={addClass} 
              onDeleteClass={deleteClass} 
              onAddStudent={addStudent}
              onUpdateStudentData={updateStudentData}
            />
          )}

        </div>
      </main>
    </div>
  );
};

// --- SUB-COMPONENT: MERGED CLASS MANAGER ---
const ClassManager = ({ classes, onAddClass, onDeleteClass, onAddStudent, onUpdateStudentData }) => {
  const [selectedClassId, setSelectedClassId] = useState(null);
  const [newClassName, setNewClassName] = useState('');
  const [newSubject, setNewSubject] = useState('');
  const [newStudentName, setNewStudentName] = useState('');
  
  const [activeDate, setActiveDate] = useState(new Date().toISOString().split('T')[0]);

  const handleCreateClass = () => {
    if(newClassName && newSubject) {
      onAddClass(newClassName, newSubject);
      setNewClassName('');
      setNewSubject('');
    }
  };

  const selectedClass = classes.find(c => c.id === selectedClassId);

  return (
    <div className="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-300">
      
      {/* 1. CLASS LIST HEADER */}
      {!selectedClass ? (
        <div className="bg-white rounded-[2rem] shadow-xl shadow-slate-200/50 border border-slate-100 p-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
             <div>
                <h3 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
                  <span className="p-2 bg-indigo-100 text-indigo-600 rounded-xl"><School size={24}/></span> Manajemen Kelas
                </h3>
                <p className="text-slate-500 mt-2 text-sm">Kelola absensi harian dan penilaian siswa dalam satu tempat yang terintegrasi.</p>
             </div>
             <div className="flex gap-3 bg-slate-50 p-2 rounded-2xl border border-slate-200">
                <input type="text" placeholder="Nama Kelas (7A)" className="px-4 py-2 border border-slate-200 rounded-xl text-sm outline-none focus:border-emerald-500" value={newClassName} onChange={e => setNewClassName(e.target.value)} />
                <input type="text" placeholder="Mapel (Math)" className="px-4 py-2 border border-slate-200 rounded-xl text-sm outline-none focus:border-emerald-500" value={newSubject} onChange={e => setNewSubject(e.target.value)} />
                <button onClick={handleCreateClass} className="bg-emerald-600 text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 hover:bg-emerald-700 text-sm shadow-md">
                  <PlusCircle size={16}/> Tambah
                </button>
             </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {classes.map(cls => (
              <div key={cls.id} onClick={() => setSelectedClassId(cls.id)} className="bg-white border border-slate-200 hover:border-emerald-400 hover:shadow-xl hover:-translate-y-1 cursor-pointer p-6 rounded-2xl transition-all group relative">
                <button onClick={(e) => {e.stopPropagation(); onDeleteClass(cls.id)}} className="absolute top-4 right-4 text-slate-300 hover:text-red-500 hover:bg-red-50 p-2 rounded-full transition-colors"><XCircle size={20}/></button>
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl mb-4 flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-blue-200">
                   {cls.name.substring(0,2)}
                </div>
                <h4 className="font-bold text-xl text-slate-800">{cls.name}</h4>
                <p className="text-sm text-slate-500 font-medium mb-4">{cls.subject}</p>
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg w-fit border border-emerald-100">
                  <Users size={14}/> {cls.students.length} Siswa
                </div>
              </div>
            ))}
            {classes.length === 0 && (
               <div className="col-span-full py-16 flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-3xl bg-slate-50/50">
                  <School size={48} className="mb-4 opacity-50"/>
                  <p>Belum ada kelas. Tambahkan kelas baru di atas.</p>
               </div>
            )}
          </div>
        </div>
      ) : (
        // 2. SELECTED CLASS VIEW
        <div className="bg-white rounded-[2rem] shadow-xl shadow-slate-200/50 border border-slate-100 overflow-hidden flex flex-col h-[calc(100vh-140px)]">
          {/* Header */}
          <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-white/50 backdrop-blur-sm sticky top-0 z-20">
            <div>
              <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
                <span className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-base px-3 py-1 rounded-xl shadow-md shadow-blue-200">{selectedClass.name}</span> {selectedClass.subject}
              </h2>
              <p className="text-sm text-slate-500 mt-1 font-medium">Jurnal Kegiatan & Penilaian Harian</p>
            </div>
            <button onClick={() => setSelectedClassId(null)} className="text-slate-500 hover:text-emerald-600 hover:bg-slate-50 px-4 py-2 rounded-xl flex items-center gap-2 text-sm font-bold transition-all">
              <ArrowLeft size={18}/> Kembali
            </button>
          </div>

          {/* Toolbar */}
          <div className="p-6 border-b border-slate-100 bg-slate-50/30 flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-3 bg-white px-4 py-2 rounded-xl border border-slate-200 shadow-sm">
              <div className="bg-indigo-100 p-1.5 rounded-lg"><Calendar size={18} className="text-indigo-600" /></div>
              <div className="flex flex-col">
                 <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Tanggal Pertemuan</label>
                 <input type="date" className="bg-transparent font-bold text-slate-700 outline-none text-sm cursor-pointer" value={activeDate} onChange={e => setActiveDate(e.target.value)} />
              </div>
            </div>

            <div className="flex gap-2 items-center ml-auto bg-white p-1.5 rounded-xl border border-slate-200 shadow-sm">
              <input type="text" placeholder="Nama Siswa Baru..." className="px-3 py-2 text-sm w-48 outline-none bg-transparent" value={newStudentName} onChange={e => setNewStudentName(e.target.value)} />
              <button onClick={() => { if(newStudentName) { onAddStudent(selectedClass.id, newStudentName); setNewStudentName(''); }}} className="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-slate-800 flex items-center gap-2 transition-colors"><PlusCircle size={16}/> Tambah</button>
            </div>
          </div>

          {/* TABLE */}
          <div className="flex-1 overflow-auto p-0">
            <table className="w-full text-sm text-left border-collapse">
              <thead className="text-xs text-slate-500 font-bold uppercase bg-slate-50 sticky top-0 shadow-sm z-10">
                <tr>
                  <th className="px-6 py-4 border-b border-slate-200 w-16 text-center">No</th>
                  <th className="px-6 py-4 border-b border-slate-200">Nama Siswa</th>
                  <th className="px-6 py-4 border-b border-slate-200 text-center w-48 bg-blue-50/30">Absensi</th>
                  <th className="px-6 py-4 border-b border-slate-200 text-center w-40 bg-emerald-50/30">Nilai Harian</th>
                  <th className="px-6 py-4 border-b border-slate-200 text-center w-40 text-slate-400">Rerata Nilai</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {selectedClass.students.map((student, index) => {
                  const grades = Object.values(student.dailyGrades || {});
                  const average = grades.length ? (grades.reduce((a, b) => a + b, 0) / grades.length).toFixed(1) : '-';
                  const currentAttendance = student.attendance?.[activeDate] || '';
                  const currentGrade = student.dailyGrades?.[activeDate] || '';

                  // Attendance Colors
                  const attStyle = 
                    currentAttendance === 'H' ? 'bg-emerald-100 text-emerald-700 border-emerald-200' :
                    currentAttendance === 'S' ? 'bg-blue-100 text-blue-700 border-blue-200' :
                    currentAttendance === 'I' ? 'bg-amber-100 text-amber-700 border-amber-200' :
                    currentAttendance === 'A' ? 'bg-red-100 text-red-700 border-red-200' : 'bg-white text-slate-400 border-slate-200';

                  return (
                    <tr key={student.id} className="bg-white hover:bg-slate-50/80 transition-colors group">
                      <td className="px-6 py-4 text-center font-mono text-slate-400 text-xs">{index + 1}</td>
                      <td className="px-6 py-4 font-bold text-slate-700">{student.name}</td>
                      
                      <td className="px-4 py-3 text-center bg-blue-50/5">
                        <select 
                          value={currentAttendance}
                          onChange={(e) => onUpdateStudentData(selectedClass.id, student.id, activeDate, 'attendance', e.target.value)}
                          className={`w-full px-3 py-2 rounded-xl border text-xs font-bold focus:ring-2 focus:ring-blue-500 outline-none cursor-pointer transition-all ${attStyle}`}
                        >
                          <option value="">- Status -</option>
                          <option value="H">Hadir</option>
                          <option value="S">Sakit</option>
                          <option value="I">Izin</option>
                          <option value="A">Alpa</option>
                        </select>
                      </td>

                      <td className="px-4 py-3 text-center bg-emerald-50/5">
                         <input 
                            type="number" 
                            className="w-20 text-center py-2 px-2 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none font-mono text-emerald-700 font-bold bg-white"
                            placeholder="-"
                            value={currentGrade}
                            onChange={(e) => onUpdateStudentData(selectedClass.id, student.id, activeDate, 'grade', parseFloat(e.target.value))}
                          />
                      </td>

                      <td className="px-6 py-4 text-center">
                        <span className="inline-block px-3 py-1 bg-slate-100 text-slate-600 rounded-lg font-mono text-xs font-bold">{average}</span>
                      </td>
                    </tr>
                  );
                })}
                {selectedClass.students.length === 0 && (
                  <tr><td colSpan="5" className="text-center py-20 text-slate-400 italic">Belum ada siswa di kelas ini.</td></tr>
                )}
              </tbody>
            </table>
          </div>
          <div className="p-4 bg-slate-50 border-t border-slate-200 text-xs font-medium text-slate-500 flex justify-between items-center">
             <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div> Tersimpan otomatis</span>
             <span>Total: {selectedClass.students.length} Siswa</span>
          </div>
        </div>
      )}
    </div>
  );
};

// --- SUB-COMPONENT: DOCUMENT CARD ---
const DocumentCard = ({ doc, onDelete, onDownload }) => {
  const previewText = doc.content.replace(/<[^>]+>/g, ' ').substring(0, 120) + '...';
  return (
    <div className="bg-white rounded-[1.5rem] border border-slate-100 p-6 shadow-lg shadow-slate-100 hover:shadow-xl hover:shadow-emerald-900/5 hover:border-emerald-200 transition-all duration-300 flex flex-col h-full group">
      <div className="flex justify-between items-start mb-4">
         <span className="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-100 group-hover:bg-emerald-100 transition-colors">{doc.type}</span>
         <button onClick={() => onDelete(doc.id)} className="text-slate-300 hover:text-red-500 hover:bg-red-50 p-1.5 rounded-full transition-colors opacity-0 group-hover:opacity-100"><Trash2 className="w-4 h-4" /></button>
      </div>
      
      <h3 className="font-bold text-slate-800 mb-1 leading-snug text-lg line-clamp-2 group-hover:text-emerald-700 transition-colors">{doc.subject}</h3>
      <p className="text-xs text-slate-500 mb-4 font-bold uppercase tracking-wide opacity-70">{doc.grade} • {doc.title}</p>
      
      <div className="bg-slate-50 rounded-2xl p-4 mb-6 flex-1 border border-slate-50 group-hover:bg-white group-hover:border-emerald-100 transition-colors">
        <p className="text-xs text-slate-600 font-medium leading-relaxed opacity-80">{previewText}</p>
      </div>

      <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-50">
        <button onClick={() => onDownload(doc)} className="text-xs font-bold text-slate-500 hover:text-indigo-600 flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-indigo-50 transition-all">
          <Download className="w-4 h-4" /> Download
        </button>
        <span className="text-[10px] font-bold text-slate-300 bg-slate-50 px-2 py-1 rounded-lg">{doc.date}</span>
      </div>
    </div>
  );
};

export default App;
