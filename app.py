import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Semester Result Management System", layout="wide"
)

st.title("📚 Semester Result & Attendance Management System")
st.write(
    "Enter obtained and total marks. The table will show exact weighted marks"
    " for each component and the final total score out of 100."
)

# Sidebar for Weightages (Directly out of 100)
st.sidebar.header("⚙️ Component Weightages (%)")
att_w = st.sidebar.slider("Attendance Weightage (%)", 0, 100, 10)
quiz_w = st.sidebar.slider("Quizzes Weightage (%)", 0, 100, 15)
asg_w = st.sidebar.slider("Assignments Weightage (%)", 0, 100, 15)
mid_w = st.sidebar.slider("Mid Exam Weightage (%)", 0, 100, 20)
final_w = st.sidebar.slider("Final Exam Weightage (%)", 0, 100, 40)

total_w = att_w + quiz_w + asg_w + mid_w + final_w
if total_w != 100:
  st.sidebar.warning(
      f"⚠️ Total Weightage is {total_w}%. Please adjust it to make it exactly"
      " 100%."
  )

if "students" not in st.session_state:
  st.session_state.students = []

st.subheader("📝 Add Student Record (Obtained / Total Marks)")
with st.form("student_form", clear_on_submit=True):
  col1, col2 = st.columns(2)
  with col1:
    name = st.text_input("Student Name")
  with col2:
    roll_no = st.text_input("Roll Number (e.g., BSCS-2023-01)")

  st.markdown("---")

  # Attendance Inputs
  c1, c2 = st.columns(2)
  with c1:
    att_obt = st.number_input(
        "Attendance Obtained Marks", 0.0, 1000.0, 8.0, key="att_o"
    )
  with c2:
    att_tot = st.number_input(
        "Attendance Total Marks", 1.0, 1000.0, 10.0, key="att_t"
    )

  # Quiz Inputs
  c3, c4 = st.columns(2)
  with c3:
    quiz_obt = st.number_input(
        "Quizzes Obtained Marks", 0.0, 1000.0, 15.0, key="q_o"
    )
  with c4:
    quiz_tot = st.number_input(
        "Quizzes Total Marks", 1.0, 1000.0, 20.0, key="q_t"
    )

  # Assignment Inputs
  c5, c6 = st.columns(2)
  with c5:
    asg_obt = st.number_input(
        "Assignments Obtained Marks", 0.0, 1000.0, 18.0, key="asg_o"
    )
  with c6:
    asg_tot = st.number_input(
        "Assignments Total Marks", 1.0, 1000.0, 20.0, key="asg_t"
    )

  # Mid Exam Inputs
  c7, c8 = st.columns(2)
  with c7:
    mid_obt = st.number_input(
        "Mid Exam Obtained Marks", 0.0, 1000.0, 25.0, key="mid_o"
    )
  with c8:
    mid_tot = st.number_input(
        "Mid Exam Total Marks", 1.0, 1000.0, 30.0, key="mid_t"
    )

  # Final Exam Inputs
  c9, c10 = st.columns(2)
  with c9:
    final_obt = st.number_input(
        "Final Exam Obtained Marks", 0.0, 1000.0, 42.0, key="fin_o"
    )
  with c10:
    final_tot = st.number_input(
        "Final Exam Total Marks", 1.0, 1000.0, 50.0, key="fin_t"
    )

  submit_btn = st.form_submit_button("Add Student & Calculate Result")

  if submit_btn:
    if name.strip() and roll_no.strip():
      if total_w == 100:
        # Calculate exact weighted points for each component
        att_score = (att_obt / att_tot) * att_w if att_tot > 0 else 0
        quiz_score = (quiz_obt / quiz_tot) * quiz_w if quiz_tot > 0 else 0
        asg_score = (asg_obt / asg_tot) * asg_w if asg_tot > 0 else 0
        mid_score = (mid_obt / mid_tot) * mid_w if mid_tot > 0 else 0
        final_score = (final_obt / final_tot) * final_w if final_tot > 0 else 0

        # Final Total Score out of 100
        final_total = (
            att_score + quiz_score + asg_score + mid_score + final_score
        )

        # Assign Grade based on total percentage
        if final_total >= 85:
          grade = "A"
        elif final_total >= 70:
          grade = "B"
        elif final_total >= 55:
          grade = "C"
        elif final_total >= 40:
          grade = "D"
        else:
          grade = "F"

        # Append structured data to session state
        st.session_state.students.append({
            "Roll Number": roll_no,
            "Student Name": name,
            "Attendance": round(att_score, 2),
            "Quizzes": round(quiz_score, 2),
            "Assignments": round(asg_score, 2),
            "Mid Exam": round(mid_score, 2),
            "Final Exam": round(final_score, 2),
            "Total Score (%)": round(final_total, 2),
            "Grade": grade,
        })
        st.success(f"Added {name} ({roll_no}) successfully!")
      else:
        st.error("Please ensure total weightage equals 100% in the sidebar.")
    else:
      st.error("Please provide both Student Name and Roll Number.")

# Display Result Table & Excel Download Option
if st.session_state.students:
  st.markdown("---")
  st.subheader("📊 Class Result Sheet")
  df = pd.DataFrame(st.session_state.students)
  st.dataframe(df, use_container_width=True)


  def convert_df_to_excel(dataframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      dataframe.to_excel(writer, index=False, sheet_name="Semester Results")
    return output.getvalue()


  excel_data = convert_df_to_excel(df)

  st.download_button(
      label="📥 Download Complete Result as Excel",
      data=excel_data,
      file_name="semester_results.xlsx",
      mime=(
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ),
  )

  if st.button("Clear All Records"):
    st.session_state.students = []
    st.rerun()