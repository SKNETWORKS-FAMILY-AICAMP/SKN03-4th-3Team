<<<<<<< HEAD
# import streamlit as st

# def reset_state():
#     if "question" not in st.session_state:
#         st.session_state["question"] = ""
#     if "recommended_question" not in st.session_state:
#         st.session_state["recommended_question"] = ""
#     if "answer_result" not in st.session_state:
#         st.session_state["answer_result"] = ""
#     if "show_answer" not in st.session_state:
#         st.session_state["show_answer"] = False

=======
>>>>>>> d43ed311a022636ec41ad44fb510511dd2a9ffed
import streamlit as st

def reset_state():
    for key in ["question", "recommended_question", "answer_result", "show_answer"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key != "show_answer" else False
