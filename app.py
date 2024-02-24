import google.generativeai as genai
from pathlib import Path
import gradio as gr
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Configure the GenerativeAI API key using the loaded environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# Initialize the GenerativeModel with the specified model name, configuration, and safety settings
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
# Function to read image data from a file path
def read_image_data(file_path):
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Could not find image: {image_path}")
    return {"mime_type": "image/jpeg", "data": image_path.read_bytes()}

# Function to generate a response based on a prompt and an image path
def generate_gemini_response(prompt, image_path):
    image_data = read_image_data(image_path)
    response = model.generate_content([prompt, image_data])
    return response.text

# Initial input prompt for the plant pathologist
input_prompt = """
You should analyze the image very carefully and thoroughly and then you should make the decision because  it is crucial that you understand.
If user insert the photo other than xray you should not analyze the image .Please make you sure that the image which you analyze is xray only. If it is not xray then you should answer that I am a health care analyzer.The uploaded image is not of human health related.
Your role as a Xray analyst is crucial in assessing whether xray fall within normal ranges or if there are deviations that require attention. Guide the model to analyze health reports and determine the status of various health parameters. Follow the structured guidelines below for a comprehensive evaluation:

Issue Identification: Examine the provided X-ray images to identify and characterize potential problems accurately.If you encounter pneumonia then you are not sure then you should answer to concern a doctor.If there is any dislocation of bone then you should analyze that also.

Detailed Findings: Provide detailed insights into the nature and extent of the issues identified in the X-ray images. Include specific observations, affected areas, and potential causes.

Next Steps: Outline the recommended course of action for addressing the issues detected in the X-ray images. This may involve treatment options, corrective measures, or further diagnostic procedures.

Recommendations: Offer informed recommendations for maintaining optimal conditions, preventing future issues, and optimizing overall health based on the X-ray analysis.

Important Note: As an expert in X-ray analysis for plant health, your insights are crucial for making informed decisions in healtcare domain. This analysis is a valuable tool but should not replace professional advice. Consult with qualified experts before implementing any strategies or treatments based on the X-ray findings.
"""
def process_uploaded_files(files):
    file_path = files[0].name if files else None
    response = generate_gemini_response(input_prompt, file_path) if file_path else None
    return file_path, response

# Gradio interface setup
with gr.Blocks() as demo:
    file_output = gr.Textbox()
    image_output = gr.Image()
    combined_output = [image_output, file_output]

    # Upload button for user to provide images
    upload_button = gr.UploadButton(
        "Click to Upload an Image",
        file_types=["image"],
        file_count="multiple",
    )
     # Set up the upload button to trigger the processing function
    upload_button.upload(process_uploaded_files, upload_button, combined_output)

# Launch the Gradio interface with debug mode enabled
demo.launch(debug=True)
