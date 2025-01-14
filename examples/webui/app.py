import os

import gradio as gr
from notionai import (
    NotionAI,
    PromptTypeEnum,
    TopicEnum,
    TranslateLanguageEnum,
    ToneEnum,
)

TOKEN = os.getenv("NOTION_TOKEN")
ai = NotionAI(TOKEN)

TOPIC_MAPPING = {item.name: item for item in TopicEnum}
LANGUAGE_MAPPING = {item.name: item for item in TranslateLanguageEnum}
ACTION_TYPE_MAPPING = {item.name: item for item in PromptTypeEnum}
TONE_MAPPING = {item.name: item for item in ToneEnum}


def write_by_topic(topic, prompt):
    res = ai.writing_with_topic(TOPIC_MAPPING[topic], prompt)
    return res


def translate(language, text):
    return ai.translate(TranslateLanguageEnum[language], text)


def summarize(action_type, context, prompt):
    return ai.writing_with_prompt(ACTION_TYPE_MAPPING[action_type], context, prompt)


def change_tone(tone, text):
    return ai.change_tone(text, TONE_MAPPING[tone])


app = gr.Blocks()

with app:
    gr.Markdown("Notion AI is here to serve your every need and make your life easier.")
    with gr.Tabs():
        with gr.TabItem("Write with Tpoics"):
            with gr.Column():
                topic_type = gr.Dropdown(
                    choices=[item.name for item in TopicEnum],
                    value=TopicEnum.blog_post.name,
                    label="Topic",
                )
                topic_prompt = gr.Textbox(
                    lines=3,
                    placeholder="Let me help you write on the topic.",
                    label="Prompt",
                )
                topic_output = gr.Markdown(
                    label="AI response", visible=True, value="Notion AI Says..."
                )
            topic_button = gr.Button("Write", label="Write")
        with gr.TabItem("Translate"):
            with gr.Column():
                translate_language = gr.Dropdown(
                    choices=[item.value for item in TranslateLanguageEnum],
                    label="Target Language",
                    value=TranslateLanguageEnum.japanese.value,
                )
                translate_text = gr.Textbox(
                    lines=2, placeholder="Translate texts", label="Text"
                )
                translate_output = gr.Markdown(
                    label="Translate response", visible=True, value="Translating..."
                )
            translate_button = gr.Button("Translate", label="Translate")
        with gr.TabItem("ChangeTone"):
            with gr.Column():
                tone = gr.Dropdown(
                    choices=[item.value for item in ToneEnum],
                    label="Which tone do you want to change to?",
                    value=ToneEnum.professional.value,
                )
                tone_text = gr.Textbox(lines=2, placeholder="Your texts", label="Text")
                tone_output = gr.Markdown(
                    label="Tone Response", visible=True, value="processing..."
                )
            change_tone_button = gr.Button("ChangeTone", label="change_tone")
        with gr.TabItem("More..."):
            with gr.Column():
                summary_type = gr.Dropdown(
                    choices=[
                        item.name
                        for item in PromptTypeEnum
                        if item != PromptTypeEnum.translate
                        and item != PromptTypeEnum.change_tone
                    ],
                    label="Action Type",
                    value=PromptTypeEnum.improve_writing.value,
                )
                summarize_text = gr.Textbox(
                    lines=2, placeholder="How to process your text?", label="Texts"
                )
                summarize_rompt = gr.Textbox(
                    lines=2,
                    placeholder="Only for help_me_write and help_me_edit",
                    label="Prompt",
                    value="",
                )

                summarize_output = gr.Markdown(
                    label="Summarize response", visible=True, value="Processing..."
                )
            summarize_button = gr.Button("Summarize", label="Summarize")

    topic_button.click(
        write_by_topic, inputs=[topic_type, topic_prompt], outputs=topic_output
    )
    translate_button.click(
        translate, inputs=[translate_language, translate_text], outputs=translate_output
    )
    change_tone_button.click(change_tone, inputs=[tone, tone_text], outputs=tone_output)
    summarize_button.click(
        summarize,
        inputs=[summary_type, summarize_text, summarize_rompt],
        outputs=summarize_output,
    )

app.launch(debug=True)
