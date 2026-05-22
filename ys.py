import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Konfigurasi layout halaman web melebar (wide)
st.set_page_config(page_title="Sistem Kontrol Suhu Ruangan", layout="wide")


# 1. DEFINISI VARIABEL INPUT DAN OUTPUT 
suhu_luar = ctrl.Antecedent(np.arange(0, 11, 1), 'suhu_luar')
suhu_dalam = ctrl.Antecedent(np.arange(0, 11, 1), 'suhu_dalam')
kelembaban = ctrl.Antecedent(np.arange(0, 11, 1), 'kelembaban')

kipas_angin = ctrl.Consequent(np.arange(0, 26, 1), 'kipas_angin')
pendingin_udara = ctrl.Consequent(np.arange(0, 26, 1), 'pendingin_udara')
pemanas = ctrl.Consequent(np.arange(0, 26, 1), 'pemanas')

# 2. MEMBERSHIP FUNCTION 

# --- Input 1: Suhu Udara Luar (Segitiga Lancip Ada Garis Puncaknya) ---
suhu_luar['Dingin'] = fuzz.trimf(suhu_luar.universe, [0, 0, 5])
suhu_luar['Sejuk']  = fuzz.trimf(suhu_luar.universe, [0, 4, 10]) 
suhu_luar['Hangat'] = fuzz.trimf(suhu_luar.universe, [5, 10, 10])

# --- Input 2: Suhu Udara Dalam ---
suhu_dalam['Sejuk']  = fuzz.trimf(suhu_dalam.universe, [0, 0, 5])
suhu_dalam['Nyaman'] = fuzz.trimf(suhu_dalam.universe, [0, 3, 10]) 
suhu_dalam['Hangat'] = fuzz.trimf(suhu_dalam.universe, [5, 10, 10])

# --- Input 3: Kelembaban Udara ---
kelembaban['Kering'] = fuzz.trimf(kelembaban.universe, [0, 0, 5])
kelembaban['Sedang'] = fuzz.trimf(kelembaban.universe, [0, 4, 10]) 
kelembaban['Lembab'] = fuzz.trimf(kelembaban.universe, [5, 10, 10])

# --- Output: Menggunakan Fungsi Segitiga (trimf) ---
kipas_angin['Lambat'] = fuzz.trimf(kipas_angin.universe, [0, 0, 12])
kipas_angin['Sedang'] = fuzz.trimf(kipas_angin.universe, [0, 12, 25])
kipas_angin['Cepat']  = fuzz.trimf(kipas_angin.universe, [12, 25, 25])

pendingin_udara['Sedikit'] = fuzz.trimf(pendingin_udara.universe, [0, 0, 12])
pendingin_udara['Sedang']  = fuzz.trimf(pendingin_udara.universe, [0, 12, 25])
pendingin_udara['Banyak']  = fuzz.trimf(pendingin_udara.universe, [12, 25, 25])

pemanas['Rendah'] = fuzz.trimf(pemanas.universe, [0, 0, 12])
pemanas['Sedang'] = fuzz.trimf(pemanas.universe, [0, 12, 25])
pemanas['Tinggi'] = fuzz.trimf(pemanas.universe, [12, 25, 25])

# 3. ATURAN FUZZY (5 RULES)
rules = [
    ctrl.Rule(suhu_luar['Dingin'] & suhu_dalam['Sejuk'] & kelembaban['Kering'], (kipas_angin['Lambat'], pendingin_udara['Sedikit'], pemanas['Tinggi'])),
    ctrl.Rule(suhu_luar['Sejuk'] & suhu_dalam['Nyaman'] & kelembaban['Sedang'], (kipas_angin['Sedang'], pendingin_udara['Sedang'], pemanas['Rendah'])),
    ctrl.Rule(suhu_luar['Hangat'] & suhu_dalam['Hangat'] & kelembaban['Lembab'], (kipas_angin['Cepat'], pendingin_udara['Sedikit'], pemanas['Rendah'])),
    ctrl.Rule(suhu_luar['Sejuk'] & suhu_dalam['Sejuk'] & kelembaban['Sedang'], (kipas_angin['Lambat'], pendingin_udara['Banyak'], pemanas['Sedang'])),
    ctrl.Rule(suhu_luar['Hangat'] & suhu_dalam['Nyaman'] & kelembaban['Sedang'], (kipas_angin['Cepat'], pendingin_udara['Sedang'], pemanas['Rendah']))
]

sistem_kontrol = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(sistem_kontrol)


# 4. ANTARMUKA WEB STREAMLIT 
# Judul Utama Aplikasi
st.markdown("# **Sistem Kontrol Suhu Ruangan - Fuzzy Logic**")
st.markdown("<p style='color: gray; font-size: 14px; margin-top: -15px;'>Tugas 4 - Sistem Pendukung Keputusan</p>", unsafe_allow_html=True)

st.write("")

# Sidebar Panel Masukan Nilai
st.sidebar.markdown("### **Masukkan Nilai Input**\n### **(Skala 0-10)**")
input_luar = st.sidebar.slider("Suhu Udara Luar", 0.0, 10.0, 6.0, 0.1)
input_dalam = st.sidebar.slider("Suhu Udara Dalam", 0.0, 10.0, 5.0, 0.1)
input_kelembaban = st.sidebar.slider("Kelembaban Udara", 0.0, 10.0, 7.0, 0.1)

# Sinkronisasi nilai slider ke simulator fuzzy
simulasi.input['suhu_luar'] = input_luar
simulasi.input['suhu_dalam'] = input_dalam
simulasi.input['kelembaban'] = input_kelembaban

# Hitung Defuzifikasi
simulasi.compute()

hasil_kipas = simulasi.output['kipas_angin']
hasil_ac = simulasi.output['pendingin_udara']
hasil_pemanas = simulasi.output['pemanas']

# Bagian Cetak Teks Hasil Output Crisp 
st.markdown("### **Hasil Perhitungan Sistem (Output Crisp)**")
col_txt1, col_txt2, col_txt3 = st.columns(3)

with col_txt1:
    st.markdown("<p style='font-size: 13px; color: gray; margin-bottom: -5px;'>Kecepatan Kipas Angin</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: -5px;'>{hasil_kipas:.2f}</h1>", unsafe_allow_html=True)

with col_txt2:
    st.markdown("<p style='font-size: 13px; color: gray; margin-bottom: -5px;'>Pendingin Udara (AC)</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: -5px;'>{hasil_ac:.2f}</h1>", unsafe_allow_html=True)

with col_txt3:
    st.markdown("<p style='font-size: 13px; color: gray; margin-bottom: -5px;'>Pemanas Ruangan</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: -5px;'>{hasil_pemanas:.2f}</h1>", unsafe_allow_html=True)

st.write("")
st.write("")

# 5. CANVAS GRAFIK FUNGSI KEANGGOTAAN 

# --- BARIS 1: INPUT ---
st.markdown("### **Canvas 1: Fungsi Keanggotaan Input**")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    st.markdown("<h4 style='text-align: center; margin-bottom: -10px;'>Suhu Udara Luar</h4>", unsafe_allow_html=True)
    suhu_luar.view(sim=simulasi)
    fig_luar = plt.gcf()
    plt.title("") 
    st.pyplot(fig_luar)
    plt.close(fig_luar)

with col_in2:
    st.markdown("<h4 style='text-align: center; margin-bottom: -10px;'>Suhu Udara Dalam</h4>", unsafe_allow_html=True)
    suhu_dalam.view(sim=simulasi)
    fig_dalam = plt.gcf()
    plt.title("")
    st.pyplot(fig_dalam)
    plt.close(fig_dalam)

with col_in3:
    st.markdown("<h4 style='text-align: center; margin-bottom: -10px;'>Kelembaban Udara</h4>", unsafe_allow_html=True)
    kelembaban.view(sim=simulasi)
    fig_kelembaban = plt.gcf()
    plt.title("")
    st.pyplot(fig_kelembaban)
    plt.close(fig_kelembaban)

st.write("")

# --- BARIS 2: OUTPUT ---
st.markdown("### **Canvas 2: Fungsi Keanggotaan Output**")
col_out1, col_out2, col_out3 = st.columns(3)

with col_out1:
    st.markdown(f"<h4 style='text-align: center; margin-bottom: -10px;'>Output Kipas (Hasil: {hasil_kipas:.1f})</h4>", unsafe_allow_html=True)
    kipas_angin.view(sim=simulasi)
    fig_kipas = plt.gcf()
    plt.title("")
    st.pyplot(fig_kipas)
    plt.close(fig_kipas)

with col_out2:
    st.markdown(f"<h4 style='text-align: center; margin-bottom: -10px;'>Output AC (Hasil: {hasil_ac:.1f})</h4>", unsafe_allow_html=True)
    pendingin_udara.view(sim=simulasi)
    fig_ac = plt.gcf()
    plt.title("")
    st.pyplot(fig_ac)
    plt.close(fig_ac)

with col_out3:
    st.markdown(f"<h4 style='text-align: center; margin-bottom: -10px;'>Output Pemanas (Hasil: {hasil_pemanas:.1f})</h4>", unsafe_allow_html=True)
    pemanas.view(sim=simulasi)
    fig_pemanas = plt.gcf()
    plt.title("")
    st.pyplot(fig_pemanas)
    plt.close(fig_pemanas)