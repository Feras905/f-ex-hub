import streamlit as st
import datetime

st.set_page_config(page_title="مساعد المزايدة الذكي لشاحنات النقل", layout="centered")
st.title("🚚 مساعد المزايدة الذكي لـ zipmend")
st.write("ادخل بياناتك الحالية لحساب أفضل سعر للمزايدة ونسبة القبول المتوقعة.")

st.sidebar.header("🛠️ إعدادات التكاليف الخاصة بك")
monthly_rent = st.sidebar.number_input("إيجار الشاحنة الشهري (يورو):", value=1200)
insurance_tax = st.sidebar.number_input("التأمين والضرائب شهرياً (يورو):", value=300)
diesel_price = st.sidebar.number_input("سعر لتر الديزل الحالي (يورو):", value=1.70)
consumption = st.sidebar.number_input("استهلاك الشاحنة (لتر لكل 100 كم):", value=10.0)

fixed_cost_per_day = (monthly_rent + insurance_tax) / 30
diesel_cost_per_km = (consumption / 100) * diesel_price

st.header("📋 بيانات الطلب الحالي")
base_offer = st.number_input("العرض الافتتاحي من المنصة (يورو):", value=100.0)
trip_distance = st.number_input("مسافة الرحلة (كم) من (A إلى B):", value=50.0)
anfahrt_distance = st.number_input("مسافة الاقتراب للتحميل Anfahrt (كم):", value=15.0)

order_time = st.time_input("وقت استلام/تنفيذ الطلب:", datetime.time(8, 30))

total_distance = trip_distance + anfahrt_distance
actual_trip_cost = fixed_cost_per_day + (total_distance * diesel_cost_per_km)

is_peak_hour = (6 <= order_time.hour <= 9) or (17 <= order_time.hour <= 21)

if is_peak_hour:
    peak_multiplier = 1.30
    time_status = "🔥 وقت ذروة (سعر مرتفع وفرصة قبول أعلى للمزايدة)"
else:
    peak_multiplier = 1.15
    time_status = "⏱️ وقت عادي (المنافسة مستقرة)"

min_acceptable_bid = actual_trip_cost * 1.20
recommended_bid = base_offer * 1.10
max_possible_bid = base_offer * peak_multiplier

st.subheader("📊 تحليل الوقت والجدوى")
st.info(f"حالة الوقت الحالي: {time_status}")
st.warning(f"التكلفة الفعلية لتنفيذ هذه الرحلة عليك (شاملة الإيجار اليومي والديزل): {actual_trip_cost:.2f} يورو")

st.header("🎯 عروض المزايدة المقترحة")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📉 الحد الأدنى لربحك", value=f"{min_acceptable_bid:.2f} €", delta="لا تنزل عن هذا")
with col2:
    st.metric(label="💡 السعر الموصى به", value=f"{recommended_bid:.2f} €", delta="فرصة قبول 85%")
with col3:
    st.metric(label="🚀 الحد الأقصى للمزايدة", value=f"{max_possible_bid:.2f} €", delta="فرصة قبول مشروطة بالطوارئ")

st.subheader("🤖 نصيحة المساعد الذكي:")
if min_acceptable_bid > (base_offer * 1.25):
    st.error("🚨 تحذير: هذا الطلب غير مجدي اقتصادياً لشاحنتك لأن مسافة الاقتراب أو تكلفة التشغيل أعلى من العرض المعروض!")
elif is_peak_hour:
    st.success("💪 هذا وقت ممتاز للمزايدة بالحد الأقصى! المنصة مستعجلة وغالباً ستوافق على سعرك المرتفع لعدم وجود بدلاء.")
else:
    st.success("✅ الطلب جيد. نقترح تقديم 'السعر الموصى به' لضمان الفوز بالطلب أمام المنافسين الآخرين.")
