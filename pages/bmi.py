import streamlit as st

st.title("BMI Calculator")
imgshow = st.empty()
bmishow = st.empty()
categoryshow = st.empty()

bmi_categories = {
    18.5: "Underweight",
    24.9: "Healthy weight",
    29.9: "Overweight",
    float('inf'): "Obese"
}

Gender = st.radio("Select Gender:", options=["Male", "Female"], horizontal=True)
kg = st.slider("Weight (Kg)", 0, 500)
height = st.slider("Height (Cm)", 0, 500)

if kg > 0 and height > 0:
    imgnum = 0
    bmi = kg / ((height / 100) ** 2)
    bmi_str = f"{bmi:.2f}"

    for threshold, category in bmi_categories.items():
        imgnum += 1
        if bmi <= threshold:
            result = category
            break

    bmishow.write(f"BMI: {bmi_str}")
    categoryshow.write(f"Category: **{result}**")

    image_path = f"img/{Gender.lower()}{imgnum}.png"
    imgshow.image(image_path, width=250)

else:
    if kg == 0 and height > 0:
        st.header("Please enter valid weight.")
    elif kg > 0 and height == 0:
        st.header("Please enter valid height.")
    else:
        st.header("Please enter valid weight and height.")

st.markdown("---")
st.page_link("main.py",label="[⬅️ Back]")
