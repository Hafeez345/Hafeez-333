import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Page Configuration
st.set_page_config(page_title="AI Data Analyst Pro", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .answer-box {
        background: linear-gradient(135deg, #6a11cb 0%, #9d50bb 100%);
        color: #ffffff; padding: 30px; border-radius: 20px;
        font-size: 26px !important; font-weight: bold; text-align: center;
        margin: 20px 0px; box-shadow: 0px 10px 30px rgba(157, 80, 187, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# File Path (Aapka original path)
FILE_PATH = r"C:\Users\sys\Desktop\Ai agent 1.csv"

@st.cache_data
def load_data(file_source):
    try:
        # Check if file_source is a path string or an uploaded file object
        if isinstance(file_source, str):
            if not os.path.exists(file_source):
                return None
            df = pd.read_csv(file_source)
        else:
            df = pd.read_csv(file_source)

        # Basic Cleaning (Aapke features)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = [c.strip() for c in df.columns]
        
        # Mapping search columns
        df['Name_Search'] = df['Name'].astype(str).str.strip().str.lower()
        df['State_Search'] = df['State'].astype(str).str.strip().str.lower()
        
        # Numeric conversions
        df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce').fillna(0)
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- FILE LOADING LOGIC ---
df = load_data(FILE_PATH)

# Agar Desktop par nahi mili, to uploader dikhao
if df is None:
    st.warning(f"Desktop par file nahi mili: {FILE_PATH}")
    uploaded_file = st.file_uploader("Manual upload karein ya file ko Desktop par 'Ai agent 1.csv' naam se rakhein", type="csv")
    if uploaded_file:
        df = load_data(uploaded_file)

def display_styled_answer(text):
    st.markdown(f'<div class="answer-box">{text}</div>', unsafe_allow_html=True)

# --- YOUR EXACT 155 QUESTIONS ---
all_questions = [
    "1. What is the salary of ali ahmed ?", "2. What is the contact number of ali ahmed?",
    "3. Which state does rank 3 employee belong to?", "4. What is the rank of ali ahmed?",
    "5. What is the ID of ali ahmed?", "6. Who has the highest salary?",
    "7. Who has the lowest salary?", "8. Who has the highest rank?",
    "9. Who has the lowest rank?", "10. List top 5 highest paid employees.",
    "11. List top 5 lowest paid employees.", "12. List top 5 highest ranked employees.",
    "13. List bottom 5 lowest ranked employees.", "14. What is the average salary in each state?",
    "15. Which state has the highest average salary?", "16. Which state has the lowest average salary?",
    "17. How many employees are there in each state?", "18. Which state has the highest number of employees?",
    "19. Which state has the lowest number of employees?", "20. What is the average salary for each rank?",
    "21. Which employee is ranked number 1?", "22. Which employee is ranked last?",
    "23. How many employees earn more than 100,000?", "24. How many employees earn less than 50,000?",
    "25. List employees earning above average salary.", "26. List employees earning below average salary.",
    "27. Provide a list of all employee contact numbers.", "28. Find the contact number of the employee with the highest salary.",
    "29. Find the employee with highest salary in each state.", "30. Find the employee with lowest salary in each state.",
    "31. Find the top 3 employees with highest salary in Islamabad.", "32. Find the top 3 employees with lowest salary in Sindh.",
    "33. List employees from KPK earning more than 100,000.", "34. List all employees from Islamabad.",
    "35. Average salary of employees in Islamabad.", "36. Highest paid employee in Islamabad.",
    "37. Lowest paid employee in Islamabad.", "38. Number of employees in Islamabad.",
    "39. List employees in Islamabad earning above 50,000.", "40. List employees in Islamabad earning below 100,000.",
    "41. List all employees from Sindh.", "42. Average salary of employees in Sindh.",
    "43. Highest paid employee in Sindh.", "44. Lowest paid employee in Sindh.",
    "45. Number of employees in Sindh.", "46. List employees in Sindh earning above 50,000.",
    "47. List employees in Sindh earning below 100,000.", "48. List all employees from KPK.",
    "49. Average salary of employees in KPK.", "50. Highest paid employee in KPK.",
    "51. Lowest paid employee in KPK.", "52. Number of employees in KPK.",
    "53. List employees in KPK earning above 50,000.", "54. List employees in KPK earning below 100,000.",
    "55. Who is the employee with rank 1?", "56. What is the salary of the employee with rank 1?",
    "57. Who is the employee with rank 2?", "58. What is the salary of the employee with rank 2?",
    "59. Who is the employee with rank 3?", "60. What is the salary of the employee with rank 3?",
    "61. Who is the employee with rank 4?", "62. What is the salary of the employee with rank 4?",
    "63. Who is the employee with rank 5?", "64. What is the salary of the employee with rank 5?",
    "65. Who is the employee with rank 6?", "66. What is the salary of the employee with rank 6?",
    "67. Who is the employee with rank 7?", "68. What is the salary of the employee with rank 7?",
    "69. Who is the employee with rank 8?", "70. What is the salary of the employee with rank 8?",
    "71. Who is the employee with rank 9?", "72. What is the salary of the employee with rank 9?",
    "73. Who is the employee with rank 10?", "74. What is the salary of the employee with rank 10?",
    "75. What is the salary of Ali Ahmed?", "76. What is the rank of Ali Ahmed?",
    "77. Which state does Ali Ahmed belong to?", "78. What is the contact number of Ali Ahmed?",
    "79. What is the salary of Ahmed Ali?", "80. What is the rank of Ahmed Ali?",
    "81. Which state does Ahmed Ali belong to?", "82. What is the contact number of Ahmed Ali?",
    "83. What is the salary of Usman Farooq?", "84. What is the rank of Usman Farooq?",
    "85. Which state does Usman Farooq belong to?", "86. What is the contact number of Usman Farooq?",
    "87. What is the salary of Zain Ali?", "88. What is the rank of Zain Ali?",
    "89. Which state does Zain Ali belong to?", "90. What is the contact number of Zain Ali?",
    "91. What is the salary of Usman Shah?", "92. What is the rank of Usman Shah?",
    "93. Which state does Usman Shah belong to?", "94. What is the contact number of Usman Shah?",
    "95. Which employee has the median salary?", "96. Which employee has the median rank?",
    "97. What is the total salary of all employees?", "98. Which employees have the same salary?",
    "99. Which employees have the same rank?", "100. List employees sorted by salary ascending.",
    "101. List employees sorted by salary descending.", "102. List employees sorted by rank ascending.",
    "103. List employees sorted by rank descending.", "104. Provide a chart of salary distribution.",
    "105. Provide a chart of employee count per state.", "106. Provide a chart of average salary per state.",
    "107. Find employees whose name contains 'Ali'.", "108. Find employees whose name contains 'Usman'.",
    "109. Find employees whose ID starts with 'ID00'.", "110. Which employees earn exactly 100,000?",
    "111. List employees earning between 50,000 and 100,000.", "112. Find the employee with the second highest salary.",
    "113. Find the employee with the second lowest salary.", "114. List employees whose contact number starts with '3'.",
    "115. List employees earning above 75,000.", "116. List employees earning below 75,000.",
    "117. What is the total number of employees?", "118. Which employee has the maximum contact number?",
    "119. Which employee has the minimum contact number?", "120. List employees with even-numbered ranks.",
    "121. List employees with odd-numbered ranks.", "122. Find all employees with salary divisible by 10,000.",
    "123. Find all employees with rank less than 5.", "124. Find all employees with rank greater than 5.",
    "125. List employees sorted alphabetically by name.", "126. List employees sorted alphabetically by state.",
    "127. Which state has the maximum salary?", "128. Which state has the minimum salary?",
    "129. List employees with name starting with 'A'.", "130. List employees with name starting with 'U'.",
    "131. List employees with ID ending in '1'.", "132. List employees with ID ending in '2'.",
    "133. List employees whose contact number ends with '7'.", "134. List employees whose contact number ends with '3'.",
    "135. Count of employees in Islamabad earning above 80,000.", "136. Count of employees in Sindh earning above 80,000.",
    "137. Count of employees in KPK earning above 80,000.", "138. Average rank of employees in Islamabad.",
    "139. Average rank of employees in Sindh.", "140. Average rank of employees in KPK.",
    "141. Highest rank employee in Islamabad.", "142. Highest rank employee in Sindh.",
    "143. Highest rank employee in KPK.", "144. Lowest rank employee in Islamabad.",
    "145. Lowest rank employee in Sindh.", "146. Lowest rank employee in KPK.",
    "147. Total salary of employees in Islamabad.", "148. Total salary of employees in Sindh.",
    "149. Total salary of employees in KPK.", "150. List employees with salary equal to rank multiplied by 10,000.",
    "151. Employees whose contact number contains '33'.", "152. List employees whose ID contains '003'.",
    "153. Employees earning above average salary in Islamabad.", "154. Employees earning below average salary in Sindh.",
    "155. Employees earning average salary in KPK."
]

# --- IMPROVED LOGIC ENGINE ---
def process_logic(query, df):
    q = query.lower()
    
    # CHARTS LOGIC
    if "chart" in q or "distribution" in q:
        fig, ax = plt.subplots(figsize=(10, 5))
        if "salary" in q:
            sns.histplot(df['Salary'], kde=True, color='#9d50bb', ax=ax)
            ax.set_title("Salary Distribution Chart")
        elif "count" in q or "state" in q:
            df['State'].value_counts().plot(kind='bar', color='#6a11cb', ax=ax)
            ax.set_title("Employee Count per State")
        st.pyplot(fig)
        return "📊 Chart Generated Successfully!"

    # RANK SPECIFIC LOGIC
    rank_match = re.search(r'rank (\d+)', q)
    if rank_match:
        r_val = int(rank_match.group(1))
        res = df[df['Rank'] == r_val]
        if not res.empty:
            if "state" in q: return f"📍 Rank {r_val} is from {res.iloc[0]['State']}"
            if "salary" in q: return f"💰 Rank {r_val} Salary: Rs. {res.iloc[0]['Salary']:,}"
            return res
        return "Rank value not found."

    # NAME SEARCH
    for name in df['Name'].unique():
        if str(name).lower() in q:
            row = df[df['Name_Search'] == str(name).lower()].iloc[0]
            if "salary" in q: return f"💰 {name}'s Salary: Rs. {row['Salary']:,}"
            if "contact" in q: return f"📞 {name}'s Number: {row['Contact Number']}"
            if "rank" in q: return f"🎖️ {name}'s Rank: {row['Rank']}"
            if "state" in q: return f"📍 {name} is from {row['State']}"
            return df[df['Name_Search'] == str(name).lower()]

    # STATE SEARCH
    for state in ["islamabad", "sindh", "kpk", "punjab", "balochistan"]:
        if state in q:
            s_df = df[df['State_Search'] == state]
            if "average salary" in q: return f"📊 {state.upper()} Avg Salary: Rs. {s_df['Salary'].mean():,.0f}"
            if "highest" in q: return s_df.nlargest(1, 'Salary')
            if "lowest" in q: return s_df.nsmallest(1, 'Salary')
            if "count" in q or "number of" in q: return f"👥 {state.upper()} has {len(s_df)} employees."
            return s_df

    # AGGREGATIONS
    if "highest salary" in q: return df.nlargest(1, 'Salary')
    if "lowest salary" in q: return df.nsmallest(1, 'Salary')
    if "top 5 highest paid" in q: return df.nlargest(5, 'Salary')
    if "total salary" in q: return f"💵 Total Payroll: Rs. {df['Salary'].sum():,}"
    if "average salary" in q: return f"💵 Global Average: Rs. {df['Salary'].mean():,.0f}"

    return "Processing... (Please ensure names/states match your CSV exactly)"

# --- MAIN APP ---
st.title("💜 AI Data Analyst (Pro Engine)")

if df is not None:
    # Sidebar
    selected_q = st.sidebar.selectbox("📋 155 Questions:", ["Select..."] + all_questions)
    
    # Input
    user_query = st.text_input("💬 Ask your own or edit the question:")
    final_query = user_query if user_query else (selected_q if selected_q != "Select..." else None)

    if final_query:
        clean_q = re.sub(r'^\d+\.\s*', '', final_query)
        st.write(f"**Query:** {clean_q}")
        
        result = process_logic(clean_q, df)
        
        if isinstance(result, pd.DataFrame):
            st.success("Targeted Data Found:")
            st.dataframe(result, use_container_width=True)
        else:
            display_styled_answer(result)
            
    st.divider()
    st.subheader("📋 Dataset Overview")
    st.dataframe(df.head(15), use_container_width=True)
else:
    st.error("CSV File missing! Please place 'Ai agent 1.csv' on Desktop or Upload manually.")