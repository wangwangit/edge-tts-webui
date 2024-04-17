import gradio as gr
import edge_tts
import asyncio
import os
import json
# https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
with open("voice.txt", "r", encoding="utf-8") as f:
    voice_data = json.load(f)

# Create a dictionary of supported voices
SUPPORTED_VOICES = {
    f"{voice['Gender']}-{voice['ShortName']}": voice['ShortName']
    for voice in voice_data
}

# 发音切换
def changeVoice(voices):
    example = SUPPORTED_VOICES[voices]
    # example_file = os.path.join(os.path.dirname(__file__), "example/"+example+".wav")
    # return example_file
    # 以上两行给注释掉了，因为我没制作相关的音频。
    return

# 文本转语音
async def textToSpeech(text, voices, rate, volume):
    output_file = "output.mp3"
    voices = SUPPORTED_VOICES[voices]
    if (rate >= 0):
        rates = rate = "+" + str(rate) + "%"
    else:
        rates = str(rate) + "%"
    if (volume >= 0):
        volumes = "+" + str(volume) + "%"
    else:
        volumes = str(volume) + "%"
    communicate = edge_tts.Communicate(text,
                                       voices,
                                       rate=rates,
                                       volume=volumes,
                                       proxy=None)
    await communicate.save(output_file)
    audio_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(audio_file)):
        return audio_file
    else:
        raise gr.Error("转换失败！")
        return FileNotFoundError


# 清除转换结果
def clearSpeech():
    output_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(output_file)):
        os.remove(output_file)
    return None, None


with gr.Blocks(css="style.css", title="文本转语音") as demo:
    gr.Markdown("""
    # 微软Edge文本转语音
    公众号: 一只会飞的旺旺
    博客: https://www.wangwangit.com
    """)
    with gr.Row():
        with gr.Column():
            text = gr.TextArea(label="文本", elem_classes="text-area", lines=15)
            btn = gr.Button("生成", elem_id="submit-btn")
        with gr.Column():
            voices = gr.Dropdown( choices=list(SUPPORTED_VOICES.keys()),  # Use the keys from SUPPORTED_VOICES
    value="Male-zh-CN-YunxiNeural",  # Set a default voice
    label="发音",
    info="请选择发音人",                                 interactive=True)

            example = gr.Audio(label="试听",
                              value="example/zh-CN-YunxiNeural.wav",
                              interactive=False,
                              elem_classes="example")

            voices.change(fn=changeVoice,inputs=voices,outputs=example)
            rate = gr.Slider(-100,
                             100,
                             step=1,
                             value=0,
                             label="语速增减",
                             info="加快或减慢语速",
                             interactive=True)

            volume = gr.Slider(-100,
                               100,
                               step=1,
                               value=0,
                               label="音调增减",
                               info="加大或减小音调",
                               interactive=True)
            audio = gr.Audio(label="输出",
                             interactive=False,
                             elem_classes="audio")
            clear = gr.Button("清除", elem_id="clear-btn")
            btn.click(fn=textToSpeech,
                      inputs=[text, voices, rate, volume],
                      outputs=[audio])
            clear.click(fn=clearSpeech, outputs=[text, audio])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7880)

