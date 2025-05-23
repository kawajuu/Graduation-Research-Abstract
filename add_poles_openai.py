import os
import openai
from pathlib import Path
from datetime import datetime
import requests

# === 設定 ===
client = openai.OpenAI(api_key="xxxx")

OUTPUT_DIR = Path("~/Desktop/卒研/画像収集/with_poles").expanduser()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_BASE = "A realistic Japanese street with electric poles and power lines, traditional buildings, sunny day, photo quality."
NUM_IMAGES = 2  # 作成する画像枚数

def generate_image_by_prompt(prompt, index):
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024"
        )


        # OpenAI Python 1.xでは response.data[0].url が存在
        image_url = response.data[0].url
        image_data = requests.get(image_url).content
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"generated_{index+1}_{timestamp}.png"
        out_path = OUTPUT_DIR / filename

        with open(out_path, "wb") as f:
            f.write(image_data)

        print(f"Saved: {out_path}")

    except Exception as e:
        print(f"Failed to generate image {index+1}: {e}")

# === 実行 ===
for i in range(NUM_IMAGES):
    generate_image_by_prompt(PROMPT_BASE, i)
