import streamlit as st
import random
import time

st.set_page_config(layout="wide")


# ---------------- PARTY CSS ----------------
st.markdown("""
<style>

html, body, [class*="css"] {
    overflow: hidden;
}

.title {
    text-align:center;
    font-size:40px;
    color:#00ffe5;
    font-weight:bold;
}

.big-number {
    font-size:150px;
    text-align:center;
    color:#00ff00;
    font-weight:bold;
    text-shadow:0 0 40px #00ff00;
    margin-top:20px;
}

.board {
    display:grid;
    grid-template-columns: repeat(10, 1fr);
    gap:6px;
    padding:10px;
}

.cell {
    background:#111;
    color:#444;
    font-size:24px;
    text-align:center;
    padding:12px;
    border-radius:8px;
}

.called {
    background:#ff0055;
    color:white;
    box-shadow:0 0 10px red;
}

.current {
    background:#00ff00;
    color:black;
    box-shadow:0 0 20px lime;
    transform:scale(1.15);
}

.stButton button {
    width:100%;
    height:60px;
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- Funny lines ----------------
funny = {
1:"Start begun",2:"One more",3:"Cup of tea",4:"Knock knock",5:"High five",
6:"Half dozen",7:"Lucky seven",8:"Garden gate",9:"Doctor time",10:"Perfect ten",
11:"Football team",12:"One dozen",13:"Unlucky teen",14:"Valentine number",15:"Young energy",
16:"Sweet sixteen",17:"Dancing queen",18:"Voting age",19:"Goodbye teens",20:"Blind twenty",
21:"Key age",22:"Two ducks",23:"You and me",24:"Two dozen",25:"Silver jubilee",
26:"Republic day",27:"Gateway India",28:"Moon night",29:"Almost thirty",30:"Dirty thirty",
31:"Baskin Robbins",32:"Buckle shoe",33:"Double three",34:"Ask more",35:"Jump alive",
36:"Popular number",37:"Lucky vibes",38:"Ladies number",39:"Watch time",40:"Naughty forty",
41:"One more fun",42:"Hitchhiker number",43:"Down on knees",44:"Double four",45:"Half century near",
46:"Up to tricks",47:"Four seven heaven",48:"Four dozen",49:"Almost fifty",50:"Half century",
51:"Royal entry",52:"Deck cards",53:"Stuck in tree",54:"Clean floor",55:"Double nickel",
56:"Shot ready",57:"Heinz variety",58:"Make them wait",59:"Just missed",60:"Old retired",
61:"Reverse lucky",62:"Turn around",63:"Old tricks",64:"Chess board",65:"Retirement near",
66:"Double trouble",67:"Made in heaven",68:"Saving more",69:"Funny position",70:"Lucky exit",
71:"Lucky bachelor",72:"Six dozen",73:"Queen bee",74:"Lucky door",75:"Diamond jubilee",
76:"Trombone sticks",77:"Double heaven",78:"Lucky vibes",79:"One more chance",80:"Blind eighty",
81:"Fat lady",82:"Straight away",83:"India wins",84:"Seven dozen",85:"Staying alive",
86:"Between sticks",87:"Almost heaven",88:"Two fat ladies",89:"Nearly there",90:"Top of world"
}

# ---------------- Session ----------------
if "numbers" not in st.session_state:
    st.session_state.numbers=[]

if "called" not in st.session_state:
    st.session_state.called=[]

if "current" not in st.session_state:
    st.session_state.current=None

if "auto" not in st.session_state:
    st.session_state.auto=False


# ---------------- Spell function ----------------
def spell(n):

    words=["zero","one","two","three","four","five","six","seven","eight","nine"]

    if n<10:
        return words[n]

    digits=" ".join(words[int(d)] for d in str(n))

    tens_words={
    10:"ten",20:"twenty",30:"thirty",40:"forty",50:"fifty",
    60:"sixty",70:"seventy",80:"eighty",90:"ninety"
    }

    if n in tens_words:
        return digits+" "+tens_words[n]

    tens=n//10*10
    ones=n%10

    return digits+" "+tens_words[tens]+" "+words[ones]


# ---------------- Female voice ----------------
import streamlit.components.v1 as components

def speak(n):

    funny_line = funny[n]
    spelling = spell(n)

    text = f"{funny_line} ... {spelling}"

    components.html(f"""
    <script>
    const synth = window.speechSynthesis;

    function speakNow() {{

        let voices = synth.getVoices();

        if (!voices.length) {{
            setTimeout(speakNow, 100);
            return;
        }}

        let female = voices.find(v =>
            v.name.includes("Samantha") ||
            v.name.includes("Google UK English Female") ||
            v.name.includes("Karen") ||
            v.name.includes("Victoria") ||
            v.name.includes("Female")
        ) || voices[0];

        let msg = new SpeechSynthesisUtterance("{text}");

        msg.voice = female;
        msg.rate = 0.9;
        msg.pitch = 1.2;
        msg.volume = 1;

        synth.cancel();
        synth.speak(msg);
    }}

    speakNow();

    </script>
    """, height=0)


# ---------------- Layout ----------------
left,right = st.columns([2,1])

# ---------------- LEFT BOARD ----------------
with left:

    board='<div class="board">'

    for i in range(1,91):

        cls="cell"

        if i in st.session_state.called:
            cls+=" called"

        if i==st.session_state.current:
            cls+=" current"

        board+=f'<div class="{cls}">{i}</div>'

    board+='</div>'

    st.markdown(board,unsafe_allow_html=True)


# ---------------- RIGHT CONTROL PANEL ----------------
with right:

    st.markdown('<div class="title">🎉 Tambola Party Mode</div>',unsafe_allow_html=True)

    if st.session_state.current:
        st.markdown(f'<div class="big-number">{st.session_state.current}</div>',unsafe_allow_html=True)


    if st.button("START GAME"):

        st.session_state.numbers=list(range(1,91))
        random.shuffle(st.session_state.numbers)
        st.session_state.called=[]
        st.session_state.current=None


    if st.button("NEXT NUMBER (SPACE)"):

        if st.session_state.numbers:

            n=st.session_state.numbers.pop(0)

            st.session_state.current=n

            st.session_state.called.append(n)

            speak(n)


    if st.button("AUTO MODE ON/OFF"):

        st.session_state.auto=not st.session_state.auto


    if st.button("RESET"):

        st.session_state.numbers=[]
        st.session_state.called=[]
        st.session_state.current=None


# ---------------- SPACEBAR SUPPORT ----------------
st.markdown("""
<script>

document.addEventListener('keydown', function(e) {

    if(e.code === 'Space') {

        window.parent.document.querySelector('button[kind="secondary"]').click();

    }

});

</script>
""", unsafe_allow_html=True)


# ---------------- AUTO MODE ----------------
if st.session_state.auto and st.session_state.numbers:

    time.sleep(5)

    n=st.session_state.numbers.pop(0)

    st.session_state.current=n

    st.session_state.called.append(n)

    speak(n)

    st.rerun()