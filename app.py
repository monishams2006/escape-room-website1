import random
import streamlit as st

if "points" not in st.session_state:
    st.session_state.points = 0
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "tries" not in st.session_state:
    st.session_state.tries = []
if "random_state" not in st.session_state:
    st.session_state.random_state = {}

def slow(msg):
    st.write(msg)

def ask(label, key):
    return st.text_input(label, key=key)

def challenge1():
    slow("RIDDLE: I speak without a mouth and hear without ears. What am I?")
    answer = ask("Your answer", key="challenge1")
    if answer:
        return "echo" in answer.lower()
    return None

def challenge2():
    if "num2" not in st.session_state.random_state:
        st.session_state.random_state["num2"] = random.randint(1, 10)
        st.session_state.tries.append(3)
    tries = st.session_state.tries[0]
    slow(f"Guess a number between 1–10. You get {tries} tries.")
    guess = ask("Enter your guess", key="challenge2")
    if guess:
        try:
            guess_num = int(guess)
            if guess_num == st.session_state.random_state["num2"]:
                return True
            else:
                st.session_state.tries[0] -= 1
                if st.session_state.tries[0] < 1:
                    return False
                if guess_num < st.session_state.random_state["num2"]:
                    slow("Too low!")
                else:
                    slow("Too high!")
        except:
            slow("Enter a valid number.")
    return None

def challenge3():
    if "word3" not in st.session_state.random_state:
        words = ["python", "escape", "portal", "mystery"]
        st.session_state.random_state["word3"] = random.choice(words)
        st.session_state.random_state["scr3"] = ''.join(random.sample(st.session_state.random_state["word3"], len(st.session_state.random_state["word3"])))
    slow(f"Unscramble this word: {st.session_state.random_state['scr3']}")
    user = ask("Your answer", key="challenge3")
    if user:
        return user.lower() == st.session_state.random_state["word3"]
    return None

def challenge4():
    if "a4" not in st.session_state.random_state:
        st.session_state.random_state["a4"] = random.randint(5, 10)
        st.session_state.random_state["b4"] = random.randint(2, 5)
        st.session_state.random_state["correct4"] = st.session_state.random_state["a4"] * st.session_state.random_state["b4"] + st.session_state.random_state["b4"]
    slow(f"Solve: (a * b) + b where a={st.session_state.random_state['a4']}, b={st.session_state.random_state['b4']}")
    user = ask("Your answer", key="challenge4")
    if user:
        try:
            return int(user) == st.session_state.random_state["correct4"]
        except:
            slow("Enter a number.")
    return None

def challenge5():
    slow("Which is NOT a programming language?")
    slow("A) Python\nB) Java\nC) HTML\nD) C++")
    user = ask("Your choice (A/B/C/D)", key="challenge5")
    if user:
        return user.upper() == "C"
    return None

def play_level(name, fn):
    slow(f"\n---- {name} ----")
    result = fn()
    if result is None:
        return False
    if result:
        slow("✔ Correct! +10 points!")
        st.session_state.points += 10
        st.session_state.stage += 1
        return True
    else:
        slow("✖ Wrong! You must complete HARD MODE to escape! (Demo version skips hard mode, moves to next level.)")
        st.session_state.stage += 1
        return True
    slow("-----------------------------")
    return False

def main():
    st.title("✨ Escape Room Multiverse ✨")
    slow(f"Total Points: {st.session_state.points}\n")
    stages = [
        ("WORLD 1: Cave of Riddles", challenge1),
        ("WORLD 2: Forest of Numbers", challenge2),
        ("WORLD 3: Lava of Words", challenge3),
        ("WORLD 4: River of Logic", challenge4),
        ("WORLD 5: Final Gate", challenge5)
    ]
    for i in range(st.session_state.stage, len(stages)):
        name, fn = stages[i]
        if not play_level(name, fn):
            st.stop()
    st.success(f"🏁 FINAL SCORE: {st.session_state.points}")
    if st.session_state.points >= 40:
        st.balloons()
        st.success("🌟 GREAT ESCAPE! You mastered the escape worlds!")
    elif st.session_state.points >= 20:
        st.info("👍 GOOD ESCAPE! You escaped with decent skill.")
    else:
        st.warning("😅 ROUGH ESCAPE... But you still made it home.")
    st.write("🏠 You have returned home safely! 🎉 GAME COMPLETE 🎉")

main()
