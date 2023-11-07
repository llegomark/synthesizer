import gradio as grd
import os
import tempfile
from openai import OpenAI

# Initialize OpenAI client with API key
api_key = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = api_key

openai_client = OpenAI()


def synthesize_speech(input_text, selected_model, selected_voice, audio_format):
    # This is a new feature from OpenAI, so please check the documentation for the correct parameter to set the audio format.
    # See: https://platform.openai.com/docs/guides/text-to-speech
    audio_response = openai_client.audio.speech.create(
        model=selected_model,
        voice=selected_voice,
        input=input_text
        # Add the correct parameter for audio format here, if available
    )

    # Determine the file extension based on the selected audio format
    file_extension = f".{audio_format}" if audio_format in [
        'mp3', 'aac', 'flac'] else ".opus"

    # Save the synthesized speech to a temporary audio file
    with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as audio_temp:
        audio_temp.write(audio_response.content)
        audio_file_path = audio_temp.name

    return audio_file_path


# Define the Gradio interface
with grd.Blocks() as speech_synthesizer_interface:
    grd.Markdown("# <center> Text-to-Speech Synthesizer </center>")
    with grd.Row():
        model_selector = grd.Dropdown(
            choices=['tts-1', 'tts-1-hd'], label='Choose Model', value='tts-1')
        voice_selector = grd.Dropdown(choices=[
                                      'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'], label='Select Voice', value='alloy')
        format_selector = grd.Dropdown(
            choices=['mp3', 'opus', 'aac', 'flac'], label='Select Format', value='mp3')

    input_field = grd.Textbox(
        label="Enter your text here", placeholder="Type here and convert to speech.")
    synthesis_button = grd.Button("Convert to Speech")
    audio_result = grd.Audio(label="Generated Speech")

    input_field.submit(fn=synthesize_speech, inputs=[
                       input_field, model_selector, voice_selector, format_selector], outputs=audio_result)
    synthesis_button.click(fn=synthesize_speech, inputs=[
                           input_field, model_selector, voice_selector, format_selector], outputs=audio_result)

# Launch the interface
speech_synthesizer_interface.launch()
