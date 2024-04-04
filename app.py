import sys
import gradio as gr
import logging
import logging.config
from pointer_generator.infer import Generate

logger = logging.getLogger(__name__)

title = "Vietnamese Spelling error correction sytem"

description = """
🔎 Vietnamese Spelling error correction system using Transformer"""

# init the chain for answering
def vote(data: gr.LikeData):
    if data.liked:
        logger.info(f"Liked answer: {data.value}")
        return
    else:
        return

chatbot = gr.Chatbot(bubble_full_width = True)
generate = Generate()

demo = gr.Interface(
    fn=generate.generate_correct_sentence,
    title=title, 
    description=description,
    inputs=["text"],
    outputs=["text"],
    examples=[
    ["Hôm nay tooi đi học."],
    ["TH là nhà máy sữa ở Vieet Nam."],
    ["Công nghệ Blockchain: Tasc động lớn đến các nền kinh tế mới nổi."]
    ]
)

if __name__ == "__main__":
    demo.queue(max_size=3).launch(share=False)