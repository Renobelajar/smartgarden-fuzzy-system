import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Konfigurasi layout halaman web melebar (wide)
st.set_page_config(page_title="Sistem Kontrol Suhu Ruangan", layout="wide")


# 1. DEFINISI VARIABEL INPUT DAN OUTPUT 
suhu_tanah = ctrl.Antecedent(np.arange(0, 11, 1), 'suhu_tanah')
kelembaban_tanah = ctrl.Antecedent(np.arange(0, 11, 1), 'kelembaban_tanah')
intensitas_cahaya = ctrl.Antecedent(np.arange(0, 11, 1), 'intensitas_cahaya')

katup_air = ctrl.Consequent(np.arange(0, 51, 1), 'katup_air')
pompa_nutrisi = ctrl.Consequent(np.arange(0, 51, 1), 'pompa_nutrisi')
peneduh_elektrik = ctrl.Consequent(np.arange(0, 51, 1), 'peneduh_elektrik')

# 2. MEMBERSHIP FUNCTION 

# --- Input 1: Suhu Udara Luar ---
suhu_tanah['Dingin'] = fuzz.trimf(suhu_tanah.universe, [0, 0, 5])
suhu_tanah['Normal']  = fuzz.trimf(suhu_tanah.universe, [0, 4, 10]) 
suhu_tanah['Panas'] = fuzz.trimf(suhu_tanah.universe, [5, 10, 10])

# --- Input 2: Suhu Udara Dalam ---
kelembaban_tanah['Kering']  = fuzz.trimf(kelembaban_tanah.universe, [0, 0, 5])
kelembaban_tanah['Sedang'] = fuzz.trimf(kelembaban_tanah.universe, [0, 3, 10]) 
kelembaban_tanah['Basah'] = fuzz.trimf(kelembaban_tanah.universe, [5, 10, 10])

# --- Input 3: intensitas_cahaya Udara ---
intensitas_cahaya['Redup'] = fuzz.trimf(intensitas_cahaya.universe, [0, 0, 5])
intensitas_cahaya['Sedang'] = fuzz.trimf(intensitas_cahaya.universe, [0, 4, 10]) 
intensitas_cahaya['Terik'] = fuzz.trimf(intensitas_cahaya.universe, [5, 10, 10])

# --- Output: Menggunakan Fungsi Segitiga (trimf) ---
katup_air['Sedikit'] = fuzz.trimf(katup_air.universe, [0, 0, 12])
katup_air['Sedang'] = fuzz.trimf(katup_air.universe, [0, 12, 25])
katup_air['Banyak']  = fuzz.trimf(katup_air.universe, [12, 25, 25])

pompa_nutrisi['Rendah'] = fuzz.trimf(pompa_nutrisi.universe, [0, 0, 12])
pompa_nutrisi['Sedang']  = fuzz.trimf(pompa_nutrisi.universe, [0, 12, 25])
pompa_nutrisi['Tinggi']  = fuzz.trimf(pompa_nutrisi.universe, [12, 25, 25])

peneduh_elektrik['Tutup'] = fuzz.trimf(peneduh_elektrik.universe, [0, 0, 12])
peneduh_elektrik['Setengah'] = fuzz.trimf(peneduh_elektrik.universe, [0, 12, 25])
peneduh_elektrik['Buka'] = fuzz.trimf(peneduh_elektrik.universe, [12, 25, 25])

# 3. ATURAN FUZZY 
rules = [
    ctrl.Rule(suhu_tanah['Dingin'] & kelembaban_tanah['Basah'] & intensitas_cahaya['Redup'], (katup_air['Sedikit'], pompa_nutrisi['Rendah'], peneduh_elektrik['Tutup'])),
    ctrl.Rule(suhu_tanah['Normal'] & kelembaban_tanah['Sedang'] & intensitas_cahaya['Sedang'], (katup_air['Sedang'], pompa_nutrisi['Sedang'], peneduh_elektrik['Setengah'])),
    ctrl.Rule(suhu_tanah['Panas'] & kelembaban_tanah['Kering'] & intensitas_cahaya['Terik'], (katup_air['Banyak'], pompa_nutrisi['Rendah'], peneduh_elektrik['Buka']))
]

sistem_kontrol = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(sistem_kontrol)


# 4. ANTARMUKA WEB STREAMLIT 
# Judul Utama Aplikasi
st.markdown("# **Sistem Smart Garden - Fuzzy Logic**")
st.markdown("<p style='color: gray; font-size: 14px; margin-top: -15px;'> Sistem Pendukung Keputusan</p>", unsafe_allow_html=True)

st.write("")

# Sidebar Panel Masukan Nilai
st.sidebar.markdown("### **Masukkan Nilai Input**\n### **(Skala 0-10)**")
input_suhu = st.sidebar.slider("Suhu Udara Luar", 0.0, 10.0, 6.0, 0.1)
input_kelembaban = st.sidebar.slider("Suhu Udara Dalam", 0.0, 10.0, 8.0, 0.1)
input_cahaya = st.sidebar.slider("intensitas_cahaya Udara", 0.0, 10.0, 7.0, 0.1)

# Sinkronisasi nilai slider ke simulator fuzzy
simulasi.input['suhu_tanah'] = input_suhu
simulasi.input['kelembaban_tanah'] = input_kelembaban
simulasi.input['intensitas_cahaya'] = input_cahaya

# Hitung Defuzifikasi
simulasi.compute()

hasil_katup = simulasi.output['katup_air']
hasil_pompa = simulasi.output['pompa_nutrisi']
hasil_peneduh = simulasi.output['peneduh_elektrik']

# Bagian Cetak Teks Hasil Output Crisp 
st.markdown("### **Hasil Perhitungan Sistem (Output Crisp)**")
col_txt1, col_txt2, col_txt3 = st.columns(3)

with col_txt1:
    st.markdown("<p style='font-size: 13px; color: gray; margin-bottom: -5px;'>Katup Air</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: -5px;'>{hasil_katup:.2f}</h1>", unsafe_allow_html=True)

with col_txt2:
    st.markdown("<p style='font-size: 13px; color: gray; margin-bottom: -5px;'>Pompa Nutrisi (AC)</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: -5px;'>{hasil_peneduh:.2f}</h1>", unsafe_allow_html=True)

with col_txt3:
    st.markdown("<p style='font-size: 13px; color: gray; margin-bottom: -5px;'>Peneduh Elektrik Ruangan</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-size: 42px; font-weight: bold; margin-top: -5px;'>{hasil_peneduh:.2f}</h1>", unsafe_allow_html=True)

st.write("")
st.write("")

# 5. CANVAS GRAFIK FUNGSI KEANGGOTAAN 

# INPUT
st.markdown("### **Canvas 1: Fungsi Keanggotaan Input**")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    st.markdown("<h4 style='text-align: center; margin-bottom: -10px;'>Suhu Tanah</h4>", unsafe_allow_html=True)
    suhu_tanah.view(sim=simulasi)
    fig_suhu = plt.gcf()
    plt.title("") 
    st.pyplot(fig_suhu)
    plt.close(fig_suhu)

with col_in2:
    st.markdown("<h4 style='text-align: center; margin-bottom: -10px;'>Kelembaban Tanah</h4>", unsafe_allow_html=True)
    kelembaban_tanah.view(sim=simulasi)
    fig_kelembaban = plt.gcf()
    plt.title("")
    st.pyplot(fig_kelembaban)
    plt.close(fig_kelembaban)

with col_in3:
    st.markdown("<h4 style='text-align: center; margin-bottom: -10px;'>IntensitasCahaya</h4>", unsafe_allow_html=True)
    intensitas_cahaya.view(sim=simulasi)
    fig_cahaya = plt.gcf()
    plt.title("")
    st.pyplot(fig_cahaya)
    plt.close(fig_cahaya)

st.write("")

#  OUTPUT 
st.markdown("### **Canvas 2: Fungsi Keanggotaan Output**")
col_out1, col_out2, col_out3 = st.columns(3)

with col_out1:
    st.markdown(f"<h4 style='text-align: center; margin-bottom: -10px;'>Output Kipas (Hasil: {hasil_katup:.1f})</h4>", unsafe_allow_html=True)
    katup_air.view(sim=simulasi)
    fig_katup = plt.gcf()
    plt.title("")
    st.pyplot(fig_katup)
    plt.close(fig_katup)

with col_out2:
    st.markdown(f"<h4 style='text-align: center; margin-bottom: -10px;'>Output AC (Hasil: {hasil_pompa:.1f})</h4>", unsafe_allow_html=True)
    pompa_nutrisi.view(sim=simulasi)
    fig_pompa = plt.gcf()
    plt.title("")
    st.pyplot(fig_pompa)
    plt.close(fig_pompa)

with col_out3:
    st.markdown(f"<h4 style='text-align: center; margin-bottom: -10px;'>Output peneduh_elektrik (Hasil: {hasil_peneduh:.1f})</h4>", unsafe_allow_html=True)
    peneduh_elektrik.view(sim=simulasi)
    fig_peneduh = plt.gcf()
    plt.title("")
    st.pyplot(fig_peneduh)
    plt.close(fig_peneduh)