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

# 2. إعداد اللغتين واختيار البورصة في القائمة الجانبية
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
    "Zipmend Express": {"bg": "#FF3B30", "text": "#FFFFFF"}, # أحمر
    "Clicktrans": {"bg": "#FF9500", "text": "#FFFFFF"},      # برتقالي
    "Trans.eu": {"bg": "#004080", "text": "#FFFFFF"},        # أزرق غامق
    "Shiply": {"bg": "#CC9900", "text": "#FFFFFF"},          # أصفر غامق
    "uShip": {"bg": "#34AADC", "text": "#FFFFFF"}            # أزرق فاتح
}
brand = color_map[platform]

css_style = f"<style>.stButton>button {{background-color: {brand['bg']} !important; color: {brand['text']} !important; border-radius: 8px; width: 100%; font-weight: bold; padding: 12px;}} .platform-card {{background-color: {brand['bg']}; color: {brand['text']}; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center;}}</style>"
st.markdown(css_style, unsafe_allow_html=True)

if lang == "Deutsch":
    title_text = "F EX Freight Control Hub"
    subtitle_text = f"Berechnung kalibriert für: {platform}"
else:
    title_text = "مركز F EX لرقابة الشحن"
    subtitle_text = f"الحسابات الحالية مبرمجة ومطابقة لمنصة: {platform}"

html_header = f"<div class='platform-card'><h2 style='margin:0;'>{title_text}</h2><p style='margin:5px 0 0 0; font-weight: bold;'>{subtitle_text}</p></div>"
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
    st.subheader(f"📋 لوحة التحكم والأوامر الخاصة بـ {platform}" if lang == "Deutsch" else f"📋 لوحة التحكم والأوامر الخاصة بـ {platform}")
    
    base_offer = st.number_input("Startangebot (€):" if lang == "Deutsch" else "العرض الافتتاحي أو السعر الاسترشادي للمنصة (€):", value=100.0, step=1.0)
    trip_distance = st.number_input("Transportstrecke (km):" if lang == "Deutsch" else "مسافة النقل الصافية (كم) من A إلى B:", value=25.0, step=1.0)
    anfahrt_distance = st.number_input("Anfahrtsstrecke zum Ladeort (km):" if lang == "Deutsch" else "مسافة الاقتراب لموقع التحميل (كم) [Anfahrt]:", value=10.0, step=1.0)
    
    h_input = st.number_input("Stunde des Auftrags (0-23):" if lang == "Deutsch" else "ساعة استلام/تنفيذ الطلب (0-23):", min_value=0, max_value=23, value=14, step=1)
    m_input = st.number_input("Minute des Auftrags (0-59):" if lang == "Deutsch" else "دقيقة استلام/تنفيذ الطلب (0-59):", min_value=0, max_value=59, value=30, step=1)
    
    total_dist = trip_distance + anfahrt_distance
    actual_cost = fixed_cost_day + (total_dist * diesel_cost_km)
    
    is_peak = (6 <= h_input <= 9) or (17 <= h_input <= 21)
    mult = 1.35 if is_peak else 1.15
    
    # [خوارزمية العطاءات المخصصة لكل منصة]
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
    st.warning(f"📊 Tatsächliche Betriebskosten: {actual_cost:.2f} €" if lang == "Deutsch" else f"📊 التكلفة التشغيلية الفعلية لتنفيذ هذه الرحلة بالكامل: {actual_cost:.2f} يورو")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📉 Mindestgebot" if lang == "Deutsch" else "📉 الحد الأدنى لعرضك", f"{min_bid:.2f} €")
    col2.metric("💡 Empfohlen" if lang == "Deutsch" else "💡 السعر الموصى به", f"{rec_bid:.2f} €")
    col3.metric("🚀 Maximal" if lang == "Deutsch" else "🚀 الحد الأقصى الآمن", f"{max_bid:.2f} €")
    
    # حاسبة الأرباح الصافية الفورية (Net Profit Calculator)
    st.write("---")
    st.markdown("### 💰 Netto-Profit-Kalkulator" if lang == "Deutsch" else "### 💰 حاسبة الأرباح الصافية الفورية")
    user_bid = st.number_input("Ihr Gebot (€):" if lang == "Deutsch" else "أدخل السعر الذي تنوي المزايدة به الآن (€):", value=round(rec_bid, 2), step=1.0)
    net_profit = user_bid - actual_cost
    
    if net_profit > 0:
        st.success(f"Erwarteter Netto-Gewinn: {net_profit:.2f} €" if lang == "Deutsch" else f"صافي الربح المتوقع الذي ستضعه في جيبك: {net_profit:.2f} يورو")
    else:
        st.error(f"Netto-Gewinn: {net_profit:.2f} € (Verlust!)" if lang == "Deutsch" else f"صافي الربح المتوقع: {net_profit:.2f} يورو (رحلة خاسرة!)")
        
    # [ميزة الحفظ الأوتوماتيكي الصامت - Auto Save] لحماية بياناتك من الضياع
    log_df = load_logbook()
    auto_row = {"Datum": datetime.date.today().strftime("%Y-%m-%d"), "Plattform": platform, "Gesamtdistanz_KM": total_dist, "Kosten_Euro": round(actual_cost, 2), "Gebot_Euro": round(user_bid, 2), "Netto_Profit_Euro": round(net_profit, 2), "Status": "Auto-Saved"}
    log_df = log_df[log_df["Status"] != "Auto-Saved"]
    log_df = pd.concat([log_df, pd.DataFrame([auto_row])], ignore_index=True)
    log_df.to_csv(LOGBOOK_FILE, index=False)
        
    # [مراقب ديزل F EX التكتيكي لأسواق دورتموند / NRW]
    st.write("---")
    st.markdown("### ⛽ Diesel-Monitor" if lang == "Deutsch" else "### ⛽ مراقب ديزل F EX التكتيكي (Dortmund/NRW)")
    if 5 <= h_input <= 8:
        st.error("🚨 WARNUNG: Kraftstoffpreise hoch!" if lang == "Deutsch" else "🚨 تحذير: أسعار الديزل in المحطات الآن في أعلى ذروتها اليومية! تجنب التعبئة الآن.")
    elif 18 <= h_input <= 22:
        st.success("✅ OPTIMAL: Jetzt volltanken!" if lang == "Deutsch" else "✅ وقت مثالي: أسعار الديزل في دورتموند الآن في أدنى مستوياتها البنائية اليومية. املأ الخزان فوراً!")
    else:
        st.info("⏱️ STABIL: Kraftstoffpreise normal." if lang == "Deutsch" else "⏱️ وضع مستقر: أسعار الديزل طبيعية ومتوازنة حالياً في المحطات الألمانية.")

    # زر الحفظ اليدوي الفعلي لتثبيت الرحلات الفائزة في الرسم البياني
    st.write("---")
    if st.button(save_btn_txt):
        log_df = load_logbook()
        auto_row["Status"] = "Gewonnen"
        log_df = pd.concat([log_df, pd.DataFrame([auto_row])], ignore_index=True)
        log_df.to_csv(LOGBOOK_FILE, index=False)
        st.success(save_success)
        st.rerun()

# 7. لوحة التحكم البيانية المدمجة والملونة شهرياً (Merged Chart Dashboard)
st.write("---")
st.subheader(chart_title)
history_df = load_logbook()

if not history_df.empty and len(history_df[history_df["Status"] == "Gewonnen"]) > 0:
    active_history = history_df[history_df["Status"] == "Gewonnen"]
    chart_data = active_history.groupby("Plattform")["Netto_Profit_Euro"].sum().reset_index()
    st.bar_chart(data=chart_data, x="Plattform", y="Netto_Profit_Euro", use_container_width=True)
else:
    dummy_data = pd.DataFrame({
        "Plattform": ["Zipmend Express", "Clicktrans", "Trans.eu", "Shiply", "uShip"],
        "Netto_Profit_Euro": [0.0, 0.0, 0.0, 0.0, 0.0]
    })
