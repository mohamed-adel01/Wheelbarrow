import streamlit as st
from num2words import num2words
import math # For rounding fractional parts correctly

# --- The core conversion logic ---
def amount_to_arabic_text(amount, currency_code='SAR', add_only_prefix_suffix=True):
    if not isinstance(amount, (int, float)):
        return "خطأ: المدخل يجب أن يكون رقماً."
    if amount < 0:
        return "خطأ: المبلغ يجب أن يكون موجباً."
    try:
        arabic_text = num2words(amount, to='currency', lang='ar', currency=currency_code)
        if add_only_prefix_suffix:
            return f"فقط {arabic_text} لا غير"
        else:
            return arabic_text
    except NotImplementedError:
        st.warning(f"تحذير: العملة '{currency_code}' قد لا تكون مدعومة بالكامل. يتم استخدام تحويل أساسي.")
        integer_part = int(amount)
        decimals = 3 if currency_code in ['KWD', 'BHD', 'OMR', 'LYD', 'TND'] else 2
        fractional_part = int(round((amount - integer_part) * (10**decimals)))
        major_name_default, minor_name_default = get_currency_names_fallback(currency_code)
        text_parts = []
        if integer_part == 0 and fractional_part == 0:
            text_parts.append(num2words(0, lang='ar'))
            text_parts.append(major_name_default)
        else:
            if integer_part > 0:
                text_parts.append(num2words(integer_part, lang='ar'))
                text_parts.append(major_name_default)
            if fractional_part > 0:
                if integer_part > 0: text_parts.append("و")
                text_parts.append(num2words(fractional_part, lang='ar'))
                text_parts.append(minor_name_default)
        arabic_text_fallback = " ".join(text_parts)
        if add_only_prefix_suffix: return f"فقط {arabic_text_fallback} لا غير"
        return arabic_text_fallback
    except Exception as e:
        return f"حدث خطأ غير متوقع: {str(e)}"

def get_currency_names_fallback(currency_code):
    currencies = {
        'SAR': ('ريال سعودي', 'هللة'), 'EGP': ('جنيه مصري', 'قرش'),
        'USD': ('دولار أمريكي', 'سنت'), 'AED': ('درهم إماراتي', 'فلس'),
        'KWD': ('دينار كويتي', 'فلس'), 'QAR': ('ريال قطري', 'درهم'),
        'BHD': ('دينار بحريني', 'فلس'), 'OMR': ('ريال عماني', 'بيسة'),
        'EUR': ('يورو', 'سنت يورو'), 'JOD': ('دينار أردني', 'قرش'),
        'LYD': ('دينار ليبي', 'درهم'), 'TND': ('دينار تونسي', 'مليم'),
        'DZD': ('دينار جزائري', 'سنتيم'), 'MAD': ('درهم مغربي', 'سنتيم'),
    }
    return currencies.get(currency_code.upper(), (currency_code, 'وحدة فرعية'))

# --- Streamlit App Interface ---
st.set_page_config(layout="wide", page_title="تحويل المبلغ إلى نص عربي (تفقيط)")
st.title("💰 تحويل المبلغ إلى نص عربي (تفقيط)")
st.markdown("أداة لتحويل المبالغ الرقمية إلى نص عربي (تفقيط).")

CURRENCIES = {
    "SAR": {"name": "ريال سعودي", "decimals": 2}, "EGP": {"name": "جنيه مصري", "decimals": 2},
    "USD": {"name": "دولار أمريكي", "decimals": 2}, "AED": {"name": "درهم إماراتي", "decimals": 2},
    "KWD": {"name": "دينار كويتي", "decimals": 3}, "QAR": {"name": "ريال قطري", "decimals": 2},
    "BHD": {"name": "دينار بحريني", "decimals": 3}, "OMR": {"name": "ريال عماني", "decimals": 3},
    "EUR": {"name": "يورو", "decimals": 2}, "JOD": {"name": "دينار أردني", "decimals": 2},
    "LYD": {"name": "دينار ليبي", "decimals": 3}, "TND": {"name": "دينار تونسي", "decimals": 3},
    "DZD": {"name": "دينار جزائري", "decimals": 2}, "MAD": {"name": "درهم مغربي", "decimals": 2},
}

col1, col2 = st.columns([2,3])
with col1:
    st.subheader("إعدادات التحويل")
    selected_currency_code = st.selectbox(
        "اختر العملة:", options=list(CURRENCIES.keys()),
        format_func=lambda code: f"{CURRENCIES[code]['name']} ({code})"
    )
    currency_details = CURRENCIES[selected_currency_code]
    num_decimals = currency_details["decimals"]
    step_value = 1 / (10**num_decimals)
    amount_input = st.number_input(
        f"أدخل المبلغ (حتى {num_decimals} خانات عشرية):", min_value=0.0,
        value=123.45 if num_decimals == 2 else 123.456,
        step=step_value, format=f"%.{num_decimals}f"
    )
    add_prefix_suffix = st.checkbox("إضافة 'فقط' و 'لا غير'", value=True)
    convert_button = st.button("✨ تحويل إلى نص", type="primary", use_container_width=True)

with col2:
    st.subheader("النتيجة النصية")
    if convert_button:
        if amount_input is not None:
            arabic_text_output = amount_to_arabic_text(
                amount_input, selected_currency_code, add_prefix_suffix
            )
            st.session_state.arabic_text_output = arabic_text_output
        else:
            st.session_state.arabic_text_output = "الرجاء إدخال مبلغ صحيح."

    if 'arabic_text_output' in st.session_state:
        st.text_area(
            "النص باللغة العربية:", value=st.session_state.arabic_text_output,
            height=150, key="output_text_area"
        )
st.markdown("---")
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub details
github_username = "YOUR_USERNAME" # Change this
repo_name = "YOUR_REPO_NAME"     # Change this
st.markdown(f"الكود المصدري على [GitHub](https://github.com/{github_username}/{repo_name})")
