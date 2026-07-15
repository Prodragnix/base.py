from groq import generate_response
import re
import streamlit as st
def looks_incomplete(text:str)->bool:
    if not text or len(text.strip())<10:
        return True
    t=text.strip()
    if t.endswith(("*", "*", "-", "—", ":", ",", "(", "[", "{")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):
        return True
    if not re.search(r"[.!?]\s*$", t):
        return True
    return False
def complete_answer(question:str,max_rounds:int=2)->str:
    base_prompt=(
        "Answer clearly."
        "Do not cut sentences, finish each point"
        f"Question :\n{question}\n"
    )
    ans=generate_response(base_prompt,temperature=0.5,max_tokens=1024)
    rounds=0
    while rounds<max_rounds and looks_incomplete(ans):
        cont_prompt=(
            "Continue EXACTTLY from where you stopped"
            "Do NOT repeat earlier text"
            "FINSH incomplete points and complete the answer\n"
            f"Question :\n{question}"
            f"Answer so far :\n{ans}\nContinue"
        )
        more=generate_response(cont_prompt,temperature=0.5,max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans=(ans.rstrip()+"\n"+more.lstrip()).strip() 
        rounds+=1
    return ans
def main():
    st.title('AI teaching assistant')
    st.write('Welcome! You can ask me anythng!')
    user_input=st.text_input("Enter your question!")
    if user_input:
        st.write(f"Your question:\n{user_input}")
        response=complete_answer(user_input)
        st.write("AI's answer:")
        st.markdown(response)
    else:
        st.info('Please enter a question!')
main()