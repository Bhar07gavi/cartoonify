import streamlit as st

def inject_styles():
    st.markdown(
        """
<style>
#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

:root{
  --bg1:#070a14;
  --bg2:#0a0f22;
  --card: rgba(255,255,255,0.07);
  --border: rgba(255,255,255,0.12);
  --text: #ECF2FF;
  --muted: rgba(236,242,255,0.72);
}

.stApp{
  background:
    radial-gradient(1100px 600px at 10% 15%, rgba(255,92,222,0.18), transparent 55%),
    radial-gradient(1100px 650px at 90% 10%, rgba(0,229,255,0.14), transparent 55%),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 55%, var(--bg1) 100%);
  color: var(--text);
}

.block-container{
  max-width: 1200px;
  padding-top: 1rem;
}

.card{
  border-radius: 18px;
  padding: 16px;
  background: var(--card);
  border: 1px solid var(--border);
  box-shadow: 0 18px 55px rgba(0,0,0,0.35);
  backdrop-filter: blur(10px);
}

.hr{height:1px;background:rgba(255,255,255,0.12);margin: 12px 0;}
.muted{color:var(--muted);font-size:0.92rem;}

.stButton>button, .stDownloadButton>button{
  width:100%;
  border-radius: 14px;
  border: 0;
  padding: 0.85rem 1rem;
  font-weight: 900;
  color: #071018;
  background: linear-gradient(90deg, #ff5cde, #00e5ff);
  box-shadow: 0 14px 28px rgba(0,229,255,0.10);
}

img{ border-radius:16px !important; box-shadow: 0 18px 60px rgba(0,0,0,0.35); }
video{ border-radius:16px !important; overflow:hidden; }
</style>
""",
        unsafe_allow_html=True,
    )