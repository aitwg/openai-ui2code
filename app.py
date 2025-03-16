import base64
import os
import pathlib
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("API_KEY")
print(OPENAI_API_KEY)
_MODEL_NAME = os.getenv("MODEL_NAME")
print(_MODEL_NAME)
_BASE_URL = os.getenv("BASE_URL")
print(_BASE_URL)
client = OpenAI(api_key=OPENAI_API_KEY, base_url=_BASE_URL)

# Framework selection (e.g., Tailwind, Bootstrap, etc.)
# Change this to "Bootstrap" or any other framework as needed
framework = "Regular CSS use flex grid etc"


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def send_message_to_model(message, image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model=_MODEL_NAME,
        messages=[{
            "role":
            "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{message}",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }],
    )
    return response.choices[0].message.content


# Streamlit app
def main():
    st.title("OpenAI, UI to Code 👨‍💻 ")
    st.subheader('Made by yckao@aitwg')

    uploaded_file = st.file_uploader("Choose an image...",
                                     type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)

            # Convert image to RGB mode if it has an alpha channel
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Save the uploaded image temporarily
            temp_image_path = pathlib.Path("temp_image.jpg")
            image.save(temp_image_path, format="JPEG")

            # Generate UI description
            if st.button("Code UI"):
                st.write("🧑‍💻 Looking at your UI...")
                prompt = "Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)]. Also Describe the color of the elements."
                description = send_message_to_model(prompt, temp_image_path)
                st.write(description)

                # Refine the description
                st.write("🔍 Refining description with visual comparison...")
                refine_prompt = f"Compare the described UI elements with the provided image and identify any missing elements or inaccuracies. Also Describe the color of the elements. Provide a refined and accurate description of the UI elements based on this comparison. Here is the initial description: {description}"
                refined_description = send_message_to_model(
                    refine_prompt, temp_image_path)
                st.write(refined_description)

                # Generate HTML
                st.write("🛠️ Generating website...")
                html_prompt = f"Create an HTML file based on the following UI description, using the UI elements described in the previous response. Include {framework} CSS within the HTML file to style the elements. Make sure the colors used are the same as the original UI. The UI needs to be responsive and mobile-first, matching the original UI as closely as possible. Do not include any explanations or comments. Avoid using ```html. and ``` at the end. ONLY return the HTML code with inline CSS. Here is the refined description: {refined_description}"
                initial_html = send_message_to_model(html_prompt,
                                                     temp_image_path)
                st.code(initial_html, language='html')

                # Refine HTML
                st.write("🔧 Refining website...")
                refine_html_prompt = f"Validate the following HTML code based on the UI description and image and provide a refined version of the HTML code with {framework} CSS that improves accuracy, responsiveness, and adherence to the original design. ONLY return the refined HTML code with inline CSS. Avoid using ```html. and ``` at the end. Here is the initial HTML: {initial_html}"
                refined_html = send_message_to_model(refine_html_prompt,
                                                     temp_image_path)
                st.code(refined_html, language='html')

                # Save the refined HTML to a file
                with open("index.html", "w") as file:
                    file.write(refined_html)
                st.success("HTML file 'index.html' has been created.")

                # Provide download link for HTML
                st.download_button(label="Download HTML",
                                   data=refined_html,
                                   file_name="index.html",
                                   mime="text/html")
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
