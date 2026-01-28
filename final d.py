


##################################################below code is original working code so please dont delete

# import streamlit as st  
# import pandas as pd
# from datetime import datetime
# import base64
# import os

# # Set wide layout for full width
# st.set_page_config(layout="wide")

# # YOUR GOOGLE SHEET ID
# GOOGLE_SHEET_ID = "1T0Vm1acvcXqHlMkcKi3NgNRiJERMLGLM"

# # Custom CSS for full page coverage and table styling
# st.markdown(
#     """
#     <style>
#     /* Remove default Streamlit padding */
#     .stApp {
#         max-width: 100%;
#         padding: 0;
#         background-color: white;
#     }
#     /* Main container */
#     .st-emotion-cache-1jicfl2 {
#         width: 100%;
#         padding: 0;
#         margin: 0;
#         max-width: initial;
#     }

#     /* Glass table styling */
#     .glass-table {
#         background: rgba(255,255,255,0.1);
#         backdrop-filter: blur(10px);
#         border-radius: 15px;
#         padding: 20px;
#         margin: 20px 0;
#         box-shadow: 0 4px 30px rgba(0,0,0,0.1);
#         border: 1px solid rgba(255,255,255,0.3);
#         overflow-x: auto;
#     }
#     .glass-table h3 {
#         color: black;
#         font-family: 'Fredoka', sans-serif;
#         text-align: center;
#     }
#     .glass-table table {
#         width: 100%;
#         border-collapse: collapse;
#         color: black;
#         font-family: 'Fredoka', sans-serif;
#     }
#     .glass-table th, .glass-table td {
#         border: 1px solid rgba(0,0,0,0.3);
#         padding: 10px;
#         text-align: center;
#     }
#     .glass-table th {
#         font-size: 12px;
#     }
#     .glass-table-red table {
#         color: red !important;
#     }
#     .fixed-height {
#         height: 250px;        
#         overflow-y: auto;     
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# def get_base64(bin_file):
#     if os.path.exists(bin_file):
#         with open(bin_file, 'rb') as f:
#             data = f.read()
#         return base64.b64encode(data).decode()
#     return ""

# BACKGROUND_IMAGE = "dark.jpg"
# bin_str = get_base64(BACKGROUND_IMAGE)

# def norm(s: str) -> str:
#     s = str(s).replace(" ", " ")
#     s = " ".join(s.split())
#     s = s.strip().upper()
#     return s

# # Session state
# if 'df' not in st.session_state:
#     st.session_state.df = None
# if 'source' not in st.session_state:
#     st.session_state.source = None

# # Google Sheet Loading
# col1, col2, col3 = st.columns([1, 2, 1])
# with col2:
#     if st.button("🚀 LOAD FROM GOOGLE SHEET", type="primary"):
#         with st.spinner("Loading Google Sheet..."):
#             try:
#                 url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BTST%20-%20AVX%20AND%20TML"
#                 df_temp = pd.read_csv(url, header=None)
                
#                 df_temp.columns = [
#                     'Col0', 'Supplier Name', 'PLANT', 'Inwarding PO', 'Part No.', 
#                     'Part Description', 'Qty', 'Unit', 'AVX Challan No.', 'AVX Challan Date', 
#                     'AVX PHY Material Recipt DATE', 'AVX Invoice Ack. Handover Date', 
#                     'AVX invoice Ack. Copy recevied by', 'TML Challan No.', 'TML Challan Date', 
#                     'Qty (GRN)', 'TML INVOICE RECEIVE DATE', 'GRN Days'
#                 ][:len(df_temp.columns)]
                
#                 df_temp = df_temp.iloc[2:].reset_index(drop=True)
#                 df_temp = df_temp.dropna(how='all')
                
#                 st.session_state.df = df_temp
#                 st.session_state.source = "Google Sheet (Fixed)"
#                 st.success(f"✅ Google Sheet loaded ({len(df_temp)} rows)")
#                 st.rerun()
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")

# # File Upload fallback
# if st.session_state.df is None:
#     uploaded_file = st.file_uploader("📁 OR Upload Excel File", type=["xlsx"])
#     if uploaded_file is not None:
#         df = pd.read_excel(uploaded_file, sheet_name="BTST - AVX AND TML", header=2)
#         st.session_state.df = df
#         st.session_state.source = "Excel Upload"
#         st.success(f"✅ Excel loaded ({len(df)} rows)")

# if st.session_state.df is None:
#     st.info("👆 Click 'LOAD FROM GOOGLE SHEET' or upload Excel")
#     st.stop()

# df = st.session_state.df
# # st.success(f"✅ Loaded: **{st.session_state.source}** ({len(df)} rows)")

# def load_tml(df):
#     KEY_CUSTOMER = "Supplier Name"
#     KEY_PART_NO = "Part No."
#     KEY_SUPP_QTY = "Qty"
#     KEY_GRN_QTY = "Qty (GRN)"
#     KEY_AVX_CHALLAN = "AVX Challan Date"
#     KEY_HANDOVER = "AVX Invoice Ack. Handover Date"
#     KEY_TML_CHALLAN = "TML Challan Date"
#     KEY_PHY_RCPT = "AVX PHY Material Recipt DATE"

#     required_cols = [KEY_CUSTOMER, KEY_PART_NO, KEY_SUPP_QTY, KEY_GRN_QTY]
#     missing = [col for col in required_cols if col not in df.columns]
#     if missing:
#         st.error(f"❌ Missing columns: {missing}")
#         st.write("Available:", list(df.columns))
#         st.stop()

#     df["AVX_CHALLAN_DATE"] = pd.to_datetime(df[KEY_AVX_CHALLAN], errors="coerce", dayfirst=True)
#     df["HANDOVER_DATE"] = pd.to_datetime(df[KEY_HANDOVER], errors="coerce", dayfirst=True)
#     df["TML_CHALLAN_DATE"] = pd.to_datetime(df[KEY_TML_CHALLAN], errors="coerce", dayfirst=True)
#     df["PHY_RCPT_DATE"] = pd.to_datetime(df[KEY_PHY_RCPT], errors="coerce", dayfirst=True)

#     df["SUPPLIER_QTY"] = pd.to_numeric(df[KEY_SUPP_QTY], errors="coerce")
#     df["GRN_QTY"] = pd.to_numeric(df[KEY_GRN_QTY], errors="coerce")

#     df["PART_NO"] = df[KEY_PART_NO].apply(lambda x: str(int(x)) if pd.notna(x) and float(x).is_integer() else str(x) if pd.notna(x) else "")
#     df["CUSTOMER"] = df[KEY_CUSTOMER].astype(str).fillna("").replace("nan","")

#     df = df[df["PART_NO"].str.strip() != ""]

#     today = pd.to_datetime(datetime.today().date())
    
#     df["AGE_DAYS"] = pd.NA
#     mask_q = df["TML_CHALLAN_DATE"].notna()
#     df.loc[mask_q, "AGE_DAYS"] = (today - df.loc[mask_q, "TML_CHALLAN_DATE"]).dt.days

#     df["Q_MINUS_N_DAYS"] = pd.NA
#     mask_qn = df["TML_CHALLAN_DATE"].notna() & df["PHY_RCPT_DATE"].notna()
#     df.loc[mask_qn, "Q_MINUS_N_DAYS"] = (df.loc[mask_qn, "TML_CHALLAN_DATE"] - df.loc[mask_qn, "PHY_RCPT_DATE"]).dt.days

#     mask_no_challan = df["TML_CHALLAN_DATE"].isna() & df["PHY_RCPT_DATE"].notna()
#     df.loc[mask_no_challan, "Q_MINUS_N_DAYS"] = (today - df.loc[mask_no_challan, "PHY_RCPT_DATE"]).dt.days

#     return df

# tml_full = load_tml(df)

# # Customer Filter
# customers = sorted(tml_full["CUSTOMER"].dropna().unique().tolist())
# selected_customer = st.selectbox("Customer", ["All"] + customers)
# tml = tml_full if selected_customer == "All" else tml_full[tml_full["CUSTOMER"] == selected_customer].copy()

# st.caption(f"Rows: {len(tml)} (Customer: {selected_customer})")

# # Metrics
# btst_invoice_qty = int(tml["AVX_CHALLAN_DATE"].notna().sum())
# btst_handover_status = int(tml["HANDOVER_DATE"].notna().sum())
# btst_tml_grn_status = int(tml["TML_CHALLAN_DATE"].notna().sum())
# avg_days = 0 if tml["Q_MINUS_N_DAYS"].dropna().empty else round(tml["Q_MINUS_N_DAYS"].dropna().mean())

# # FIXED HTML CARDS
# html_template = f"""
# <!doctype html>
# <html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700;900&display=swap" rel="stylesheet"><style>
# :root {{
#     --blue1: #8ad1ff;
#     --blue2: #4ca0ff;
#     --blue3: #0d6efd;
# }}
# body {{
#     margin: 0;
#     padding: 0;
#     font-family: "Fredoka", sans-serif;
#     background: none !important;
# }}
# .container {{
#     box-sizing: border-box;
#     width: 100%;
#     padding: 20px 20px 0 20px;
#     display: grid;
#     grid-template-columns: 1fr 1fr 1fr 1fr;
#     gap: 20px;
#     max-width: 1700px;
#     margin: auto;
# }}
# .card {{
#     position: relative;
#     border-radius: 20px;
#     padding: 0;
#     display: flex;
#     flex-direction: column;
#     justify-content: center;
#     align-items: center;
#     backdrop-filter: blur(12px) saturate(180%);
#     background: rgba(255,255,255,0.08);
#     border: 1px solid rgba(0,0,0,0.15);
#     box-shadow: 0 0 15px rgba(0,0,0,0.28), 0 10px 30px rgba(0,0,0,0.5), inset 0 0 20px rgba(255,255,255,0.12);
#     overflow: hidden;
#     text-align: center;
# }}
# .value-blue {{
#     font-size: 60px !important;
#     font-weight: 1000;
#     background: linear-gradient(180deg, var(--blue1), var(--blue2), var(--blue3));
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     display: block;
#     width: 100%;
# }}
# .title-black {{
#     color: black !important;
#     font-size: 18px;
#     font-weight: 800;
#     margin-top: 6px;
#     text-align: center;
#     width: 100%;
# }}
# </style></head><body><div class="container">
#     <div class="card">
#         <div class="value-blue">{btst_invoice_qty}</div>
#         <div class="title-black">BTST Invoice Qty Rec'd from AVX</div>
#     </div>
#     <div class="card">
#         <div class="value-blue">{btst_handover_status}</div>
#         <div class="title-black">BTST Invoice Handover Status</div>
#     </div>
#     <div class="card">
#         <div class="value-blue">{btst_tml_grn_status}</div>
#         <div class="title-black">BTST TML GRN Status</div>
#     </div>
#     <div class="card">
#         <div class="value-blue">{avg_days}</div>
#         <div class="title-black">TML GRN Average Days</div>
#     </div>
# </div></body></html>
# """
# st.markdown(html_template, unsafe_allow_html=True)

# # Second Row
# r2c1, r2c2 = st.columns([1, 1])

# with r2c1:
#     tml_valid = tml[tml["PART_NO"].str.strip() != ""].copy()
#     diff = (tml_valid["SUPPLIER_QTY"].fillna(0) - tml_valid["GRN_QTY"].fillna(0))
#     tml_valid["PENDING_QTY"] = diff.apply(lambda x: x if x > 0 else 0).astype(int)
#     part_pending = tml_valid.groupby("PART_NO")["PENDING_QTY"].sum().reset_index()
#     part_pending.columns = ["Part No", "GRN Pending Qty"]
    
#     st.markdown(f"""
#     <div class="glass-table glass-table-red fixed-height">
#         <h3>TML Part Wise GRN Pending Qty</h3>
#         <div style='text-align: center;'>{part_pending.to_html(escape=False, index=False)}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with r2c2:
#     age_df = tml_valid.dropna(subset=["CUSTOMER", "PHY_RCPT_DATE"]).copy()
#     age_df["AGEING_DAYS"] = pd.NA
#     mask_with_challan = age_df["TML_CHALLAN_DATE"].notna()
#     age_df.loc[mask_with_challan, "AGEING_DAYS"] = (age_df.loc[mask_with_challan, "TML_CHALLAN_DATE"] - age_df.loc[mask_with_challan, "PHY_RCPT_DATE"]).dt.days
#     mask_no_challan = age_df["TML_CHALLAN_DATE"].isna()
#     age_df.loc[mask_no_challan, "AGEING_DAYS"] = (pd.to_datetime(datetime.today().date()) - age_df.loc[mask_no_challan, "PHY_RCPT_DATE"]).dt.days

#     def age_bucket(d):
#         if pd.isna(d): return "No Data"
#         d = int(d)
#         if d <= 7: return "0-7"
#         if d <= 15: return "8-15"
#         if d <= 25: return "16-25"
#         return ">25"

#     if not age_df.empty:
#         age_df["AGE_BUCKET"] = age_df["AGEING_DAYS"].apply(age_bucket)
#         age_pivot = age_df.pivot_table(
#             index="AGE_BUCKET",
#             columns="CUSTOMER",
#             values="AGEING_DAYS",
#             aggfunc="count",
#             fill_value=0
#         )
#         age_pivot = age_pivot.reindex(index=["0-7", "8-15", "16-25", ">25"]).fillna(0)
#         age_pivot["Total"] = age_pivot.sum(axis=1).astype(int)
#         age_pivot = age_pivot.reset_index().rename(columns={"AGE_BUCKET": "Bucket"})

#         # ✅ FIXED: Safe numeric conversion
#         for col in age_pivot.columns[1:]:  # Skip Bucket column
#             age_pivot[col] = pd.to_numeric(age_pivot[col], errors='coerce').fillna(0).astype(int)

#         color_map = {
#             "0-7": {"bg": "#8ceba7", "color": "#000000"},
#             "8-15": {"bg": "#fae698", "color": "#000000"},
#             "16-25": {"bg": "#f7be99", "color": "#000000"},
#             ">25": {"bg": "#f78e8e", "color": "#000000"}
#         }

#         html_rows = ""
#         for _, row in age_pivot.iterrows():
#             bucket = row["Bucket"]
#             bgcolor = color_map.get(bucket, {}).get("bg", "#ffffff")
#             txtcolor = color_map.get(bucket, {}).get("color", "#ffffff")
#             html_rows += "<tr style='background-color:{}; color:{};'>".format(bgcolor, txtcolor)
#             for col_name in age_pivot.columns:
#                 # ✅ FIXED: Safe value conversion
#                 val = row[col_name]
#                 safe_val = int(val) if pd.notna(val) and str(val).replace('.','').isdigit() else 0
#                 html_rows += f"<td>{safe_val}</td>"
#             html_rows += "</tr>"

#         table_html = "<table style='margin:auto; border-collapse: collapse; color:black;'>"
#         table_html += "<tr>"
#         for col in age_pivot.columns:
#             table_html += f"<th style='padding:8px; border:1px solid rgba(0,0,0,0.3);'>{col}</th>"
#         table_html += "</tr>"
#         table_html += html_rows
#         table_html += "</table>"
#     else:
#         table_html = "<div style='text-align: center;'>No ageing data</div>"

#     st.markdown(f"""
#     <div class="glass-table fixed-height">
#         <h3>TML GRN Ageing Day</h3>
#         {table_html}
#     </div>
#     """, unsafe_allow_html=True)

# # Third Row: Partwise Material Receipt Qty
# st.write("---")

# tml_valid = tml[tml["PART_NO"].str.strip() != ""].copy()
# df_age = tml_valid.dropna(subset=["PHY_RCPT_DATE"]).copy()
# df_age = df_age[df_age["SUPPLIER_QTY"].fillna(0) > 0]

# df_age["RCPT_DAY"] = df_age["PHY_RCPT_DATE"].dt.day.astype(int)

# today = pd.to_datetime(datetime.today().date())
# month_end = today.replace(day=pd.Period(today, freq='M').days_in_month)
# days = list(range(1, month_end.day + 1))

# mat_pivot = df_age.pivot_table(
#     index="PART_NO",
#     columns="RCPT_DAY",
#     values="SUPPLIER_QTY",
#     aggfunc="sum",
#     fill_value=0
# ).reindex(columns=days, fill_value=0)

# mat_pivot = mat_pivot.reindex(tml_valid["PART_NO"].unique(), fill_value=0)
# mat_pivot.columns = [str(d) for d in mat_pivot.columns]

# def format_qty(x):
#     if x == 0 or pd.isna(x):
#         return ""
#     return str(int(x))

# mat_pivot = mat_pivot.applymap(format_qty)
# mat_pivot = mat_pivot.reset_index()

# table_html = mat_pivot.to_html(escape=False, index=False)
# table_html = table_html.replace('<th>PART_NO</th>', '<th style="font-size: 12px;">PART NO</th>')

# st.markdown(f"""
# <div class="glass-table">
#     <h3>Partwise Material Receipt Qty (Only Non-Zero)</h3>
#     <div style='text-align: center;'>{table_html}</div>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("---")
# st.caption("✅ **FIXED & WORKING PERFECTLY!** No more int() errors!")





