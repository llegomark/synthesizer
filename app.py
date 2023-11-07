import gradio as grd
import os
import tempfile
from openai import OpenAI

# Initialize OpenAI client with API key
api_key = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = api_key

openai_client = OpenAI()

def synthesize_speech(input_text, selected_model, selected_voice):
    audio_response = openai_client.audio.speech.create(
        model=selected_model,
        voice=selected_voice,
        input=input_text,
    )

    # Save the synthesized speech to a temporary audio file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_temp:
        audio_temp.write(audio_response.content)
        audio_file_path = audio_temp.name

    return audio_file_path

# Define the Gradio interface
with grd.Blocks() as speech_synthesizer_interface:
    grd.Markdown("# <center> Text-to-Speech Synthesizer </center>")
    with grd.Row():
        model_selector = grd.Dropdown(choices=['tts-1', 'tts-1-hd'], label='Choose Model', value='tts-1')
        voice_selector = grd.Dropdown(choices=['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'], label='Select Voice', value='alloy')

    input_field = grd.Textbox(label="Enter your text here", placeholder="Type here and convert to speech.")
    synthesis_button = grd.Button("Convert to Speech")
    audio_result = grd.Audio(label="Generated Speech")

    input_field.submit(fn=synthesize_speech, inputs=[input_field, model_selector, voice_selector], outputs=audio_result)
    synthesis_button.click(fn=synthesize_speech, inputs=[input_field, model_selector, voice_selector], outputs=audio_result)

# Launch the interface
speech_synthesizer_interface.launch()