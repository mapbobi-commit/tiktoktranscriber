import asyncio

import gradio as gr

from transcriber import (convert_videos_to_audio_files, download_videos,
                         transcribe_audio)


def transcribe(urls):
    v_ids = download_videos(urls)
    v_ids = convert_videos_to_audio_files(v_ids)
    transcriptions = transcribe_audio(v_ids)
    
    result = ""
    for id, tr in zip(v_ids, transcriptions):
        result += f"Transcription for {id}: {tr}\n"
    
    return result

with gr.Blocks() as demo:
    gr.Markdown(
    """
    Enter TikTok URLs seprated by commas to transcribe the videos!
    """)
    inp = gr.Textbox(placeholder="URLs")
    button = gr.Button(value="Transcribe")
    out = gr.Textbox()
    button.click(fn=transcribe, inputs=inp, outputs=out)

if __name__ == "__main__":
    demo.launch()