import streamlit as st
import datetime
import os
import pandas as pd

# 1. إعدادات الصفحة الأساسية وتهيئة ملف السجل الآمن
st.set_page_config(page_title="F EX Freight Hub", layout="centered")
LOGBOOK_FILE = "f_ex_logbook.csv"

def load_logbook():
    if os.path.exists(LOGBOOK_FILE):
        try:
            return pd.read_csv(LOGBOOK_FILE)
        except:
            pass
    return pd.DataFrame(columns=["Datum", "Plattform", "Gesamtdistanz_KM", "Kosten_Euro", "Gebot_Euro", "Netto_Profit_Euro", "Status"])

# 2. إعداد نظام اللغتين الثابت واختيار البورصة في القائمة الجانبية
st.sidebar.markdown("# F EX Freight Hub")
lang = st.sidebar.radio("🌐 Language / اللغة", ["Deutsch", "العربية"])

if lang == "Deutsch":
    platform_label = "🔌 Wählen Sie die Frachtenbörse:"
    platforms = ["Zipmend Express", "Clicktrans", "Trans.eu", "Shiply", "uShip"]
    enter_btn_text = "🚀 In die Plattform einloggen & Befehle öffnen"
    sidebar_header = "🛠️ Ihre Kosteneinstellungen"
    monthly_rent_label = "Monatliche Lkw-Miete (€):"
    insurance_tax_label = "Versicherung & Steuern monatlich (€):"
    diesel_price_label = "Aktueller Dieselpreis pro Liter (€):"
    consumption_label = "Lkw-Verbrauch (Liter pro 100 km):"
    chart_title = "📊 Kumulierter Netto-Profit nach Plattformen (€)"
    save_success = "Auftrag erfolgreich im Logbook gesichert!"
    save_btn_txt = "💾 Als GEWONNEN im Logbook speichern"
    
    order_header = "📋 Auftragsdaten eingeben"
    base_offer_lbl = "Startangebot / Richtpreis der Plattform (€):"
    trip_distance_lbl = "Transportstrecke (km) von A nach B:"
    anfahrt_distance_lbl = "Anfahrtsstrecke zum Ladeort (km) [Anfahrt]:"
    time_hour_lbl = "Stunde des Auftrags (0-23):"
    time_minute_lbl = "Minute des Auftrags (0-59):"
    actual_cost_lbl = "📊 Tatsächliche Betriebskosten für diesen Transport: {:.2f} €"
    min_bid_lbl = "📉 Mindestgebot"
    rec_bid_lbl = "💡 Empfohlen"
    max_bid_lbl = "🚀 Maximal"
    profit_header = "💰 F EX Netto-Profit-Kalkulator"
    user_bid_lbl = "Ihr Gebot (€):"
    net_profit_pos = "📊 Erwarteter Netto-Gewinn: {:.2f} €"
    net_profit_neg = "🚨 Erwarteter Verlust: {:.2f} €"
    diesel_monitor_title = "⛽ F EX Taktischer Diesel-Monitor (Dortmund/NRW)"
    diesel_expensive = "🚨 WARNUNG: Die Kraftstoffpreise sind aktuell auf dem Tageshöchststand. Tanken vermeiden!"
    diesel_cheap = "✅ OPTIMALER ZEITPUNKT: Die Kraftstoffpreise in NRW sind jetzt am günstigsten. Jetzt volltanken!"
    diesel_normal = "⏱️ STABIL: Die Kraftstoffpreise sind stabil. Tanken zu Normalbedingungen möglich."
    ai_advice_lbl = "🤖 Taktischer F EX Assistenten-Tipp:"
    zipmend_advice = "Zimpend Express schätzt Direktfahrten. Achten Sie darauf, dass der Mindestpreis über 179€ für Hebebühnen-Fahrten liegt."
    marketplace_advice = "Clicktrans/Shiply/uShip basieren auf offenem Bieten. Nutzen Sie die Strategie, 5€ unter dem niedrigsten Konkurrenten zu bieten, solange Sie über Ihrem Mindestgebot bleiben."
    transeu_advice = "Trans.eu ist B2B-fokussiert. Da Zahlungsziele oft 30-60 Tage betragen, schlägt F EX automatisch 7% Liquiditäts-Aufschlag auf das Mindestgebot auf."
else:
    platform_label = "🔌 اختر بورصة أو منصة الشحن:"
    platforms = ["Zipmend Express", "Clicktrans", "Trans.eu", "Shiply", "uShip"]
    enter_btn_text = "🚀 دخول إلى أوامر المنصة واستعراض الحاسبة التكتيكية"
    sidebar_header = "🛠️ إعدادات التكاليف الخاصة بك"
    monthly_rent_label = "إيجار الشاحنة الشهري (يورو):"
    insurance_tax_label = "التأمين والضرائب شهرياً (يورو):"
    diesel_price_label = "سعر لتر الديزل الحالي (يورو):"
    consumption_label = "استهلاك الشاحنة (لتر لكل 100 كم):"
    chart_title = "📊 إجمالي أرباحك الصافية الشهرية المدمجة لكل منصة بلونها الخاص (€)"
    save_success = "تم حفظ وتثبيت الرحلة بنجاح في سجلات F EX الدائمة!"
    save_btn_txt = "💾 حفظ هذه الرحلة رسمياً كـ (رحلة فائزة) في السجل"
    
    order_header = "📋 أدخل بيانات الطلب الحالي"
    base_offer_lbl = "العرض الافتتاحي أو السعر الاسترشادي للمنصة (€):"
    trip_distance_lbl = "مسافة النقل الصافية (كم) من A إلى B:"
    anfahrt_distance_lbl = "مسافة الاقتراب لموقع التحميل (كم) [Anfahrt]:"
    time_hour_lbl = "ساعة استلام/تنفيذ الطلب (0-23):"
    time_minute_lbl = "دقيقة استلام/تنفيذ الطلب (0-59):"
    actual_cost_lbl = "📊 التكلفة التشغيلية الفعلية لتنفيذ هذه الرحلة بالكامل: {:.2f} يورو"
    min_bid_lbl = "📉 الحد الأدنى لعرضك"
    rec_bid_lbl = "💡 السعر الموصى به"
    max_bid_lbl = "🚀 الحد الأقصى الآمن"
    profit_header = "### 💰 حاسبة الأرباح الصافية الفورية"
    user_bid_lbl = "أدخل السعر الذي تنوي المزايدة به الآن (€):"
    net_profit_pos = "صافي الربح المتوقع الذي ستضعه في جيبك: {:.2f} يورو"
    net_profit_neg = "صافي الربح المتوقع: {:.2f} يورو (رحلة خاسرة!)"
    diesel_monitor_title = "### ⛽ مراقب ديزل F EX التكتيكي (Dortmund/NRW)"
    diesel_expensive = "🚨 تحذير: أسعار الديزل في المحطات الآن في أعلى ذروتها اليومية! تجنب التعبئة الآن."
    diesel_cheap = "✅ وقت مثالي: أسعار الديزل في دورتموند الآن في أدنى مستوياتها البنائية اليومية. املأ الخزان فوراً!"
    diesel_normal = "⏱️ وضع مستقر: أسعار الديزل طبيعية ومتوازنة حالياً في المحطات الألمانية."
    ai_advice_lbl = "### 🤖 نصيحة مساعد F EX التكتيكي الذكي:"
    zipmend_advice = "منصة زيبمند تفضل السرعة والالتزام. تأكد تماماً أن السعر النهائي لا يقل عن 179 يورو لأن شاحنتك تحتوي على مرفاع هيدروليكي (Hebebühne)."
    marketplace_advice = "منصات المزايدة المفتوحة تعتمد على المنافسة العلنية. خوارزمية F EX تنصحك بتقديم سعر يقل بـ 5 يورو عن أقل منافس لك، بشرط ألا تنزل عن حدك الأدنى التكتيكي."
    transeu_advice = "بورصة Trans.eu تجارية وموجهة للشركات. بما أن شروط الدفع فيها قد تتأخر لـ 30 أو 60 يوماً، قامت خوارزمية F EX بإضافة هامش أمان 7% تلقائياً للتعويض عن السيولة."

platform = st.sidebar.selectbox(platform_label, platforms)

# 3. إظهار إعدادات التكاليف مع قفزات التحكم المعدلة (+ و -)
st.sidebar.write("---")
st.sidebar.header(sidebar_header)
monthly_rent = st.sidebar.number_input(monthly_rent_label, value=1650.0, step=1.0)
insurance_tax = st.sidebar.number_input(insurance_tax_label, value=300.0, step=1.0)
diesel_price = st.sidebar.number_input(diesel_price_label, value=2.15, step=0.05)
consumption = st.sidebar.number_input(consumption_label, value=14.0, step=1.0)

fixed_cost_day = (monthly_rent + insurance_tax) / 30
diesel_cost_km = (consumption / 100) * diesel_price

# 4. نظام الهويات اللونية الحقيقية لكل منصة
color_map = {
    "Zipmend Express": {"bg": "#FF3B30", "text": "#FFFFFF"}, 
    "Clicktrans": {"bg": "#FF9500", "text": "#FFFFFF"},      
    "Trans.eu": {"bg": "#004080", "text": "#FFFFFF"},        
    "Shiply": {"bg": "#CC9900", "text": "#FFFFFF"},          
    "uShip": {"bg": "#34AADC", "text": "#FFFFFF"}            
}
brand = color_map[platform]

# (الحل الجذري القاطع لكروم والموبايل): إجبار المتصفح على إلغاء الأرقام الهندية وفرض الأرقام العالمية اللاتينية
css_style = f"""
<style>
@import url('https://googleapis.com');
* {{
    font-family: 'Roboto Mono', monospace !important;
    font-variant-numeric: lnum-spacing lining-nums !important;
    font-feature-settings: "lnum" 1, "tnum" 1 !important;
}}
.stButton>button {{
    background-color: {brand['bg']} !important;
    color: {brand['text']} !important;
    border-radius: 8px;
    width: 100%;
    font-weight: bold;
    padding: 12px;
}}
.platform-card {{
    background-color: {brand['bg']};
    color: {brand['text']};
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

if lang == "Deutsch":
    html_header = f"<div class='platform-card'><h2 style='margin:0;'>F EX Freight Control Hub</h2><p style='margin:5px 0 0 0; font-weight: bold;'>Berechnung kalibriert für: {platform}</p></div>"
else:
    html_header = f"<div class='platform-card'><h2 style='margin:0;'>مركز F EX لرقابة الشحن</h2><p style='margin:5px 0 0 0; font-weight: bold;'>الحسابات الحالية مبرمجة ومطابقة لمنصة: {platform}</p></div>"
st.markdown(html_header, unsafe_allow_html=True)

# 5. بوابات التحكم وذاكرة النظام الآمنة
if "gate_open" not in st.session_state:
    st.session_state.gate_open = False
if "last_p" not in st.session_state:
    st.session_state.last_p = platform

if st.session_state.last_p != platform:
    st.session_state.gate_open = False
    st.session_state.last_p = platform

# 6. إدارة بوابات الدخول للمنصات وعرض الحسابات والأوامر الخفية
if not st.session_state.gate_open:
    st.write("")
    if st.button(enter_btn_text, key="main_gate_btn"):
        st.session_state.gate_open = True
        st.rerun()
else:
    st.write("---")
    st.subheader(order_header)
    
    base_offer = st.number_input(base_offer_lbl, value=100.0, step=1.0)
    trip_distance = st.number_input(trip_distance_lbl, value=25.0, step=1.0)
    anfahrt_distance = st.number_input(anfahrt_distance_lbl, value=10.0, step=1.0)
    
    h_input = st.number_input(time_hour_lbl, min_value=0, max_value=23, value=14, step=1)
    m_input = st.number_input(time_minute_lbl, min_value=0, max_value=59, value=30, step=1)
    
    total_dist = trip_distance + anfahrt_distance
    actual_cost = fixed_cost_day + (total_dist * diesel_cost_km)
    
    is_peak = (6 <= h_input <= 9) or (17 <= h_input <= 21)
    mult = 1.35 if is_peak else 1.15
    
    if platform == "Zipmend Express":
        min_bid = actual_cost * 1.20
        rec_bid = max(base_offer * 1.10, 179.0)
        max_bid = max(base_offer * mult, 210.0)
    elif platform in ["Clicktrans", "Shiply", "uShip"]:
        min_bid = actual_cost * 1.15
        rec_bid = actual_cost * 1.35
        max_bid = actual_cost * 1.65
    else:
        min_bid = (actual_cost * 1.25) * 1.07
        rec_bid = base_offer * 1.15
        max_bid = base_offer * 1.35
        
    st.write("---")
    st.warning(actual_cost_lbl.format(actual_cost))
    
    col1, col2, col3 = st.columns(3)
    col1.metric(min_bid_lbl, f"{min_bid:.2f} €")
    col2.metric(rec_bid_lbl, f"{rec_bid:.2f} €")
