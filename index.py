import io, requests, json, re, time, base64
from PIL import Image
import google.generativeai as genai
import streamlit as st
from bs4 import BeautifulSoup
from jsonc_parser.parser import JsoncParser

# Load config.json file
def load_config():
	with open('./config.json', 'r', encoding="utf-8") as f:
		text = f.read()
		config_obj = JsoncParser.parse_str(text)
	return config_obj

# Load the .env file
import import_settings

# Set the Gemini API key
genai.configure(api_key=import_settings.gemini_api)

def vvox_test(text):
	# エンジン起動時に表示されているIP、portを指定
	host = import_settings.voicevox_host
	port = import_settings.voicevox_port

	# 音声化する文言と話者を指定(3で標準ずんだもんになる)
	params = (
		('text', text),
		('speaker', 3),
	)

	# 音声合成用のクエリ作成
	query = requests.post(
		f'http://{host}:{port}/audio_query',
		params=params
	)

	# 音声合成を実施
	synthesis = requests.post(
		f'http://{host}:{port}/synthesis',
		headers = {"Content-Type": "application/json"},
		params = params,
		data = json.dumps(query.json())
	)

	# 再生処理
	voice = synthesis.content
	return voice

def main():
	# Streamlit
	st.title("今週のおすすめ商品")

	config = load_config()
	res = requests.get(config["loading_page"])
	res.encoding = res.apparent_encoding
	soup = BeautifulSoup(res.text, 'html.parser')

	product_img = st.empty()
	st.text("※商品紹介の音声は、画像を元にAIを用いて生成されているため、すべてが正しい情報とは限りません。詳しい説明は店頭のスタッフにお尋ねください。")
	st.image(config["mobile_qr"])
	while True:
		for img_link in (soup.find('div', {'class': 'wsprd_row wsprd_row-2'}).find_all('img')):
			img_src = config["loading_page"] + img_link.get('src')[2:]
			img = Image.open(io.BytesIO(requests.get(img_src).content))
			model = genai.GenerativeModel("gemini-1.5-flash")
			update_config = load_config()
			prompt = update_config["prompt"]
			response = model.generate_content([prompt, img])
			time.sleep(2)
			# 画像認識、説明文生成、音声出力
			content = vvox_test(response.text)
			audio_str = "data:audio/ogg;base64,%s"%(base64.b64encode(content).decode())
			audio_html = """
				<audio autoplay=True>
				<source src="%s" type="audio/ogg" autoplay=True>
				Your browser does not support the audio element.
				</audio>
				"""%audio_str

			product_img.write(img)
			audio_placeholder = st.empty()
			audio_placeholder.empty()
			time.sleep(0.5)
			audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
			time.sleep(60)

	# for img in (soup.find('div', {'class': 'wsprd_row wsprd_row-2'}).find_all('img')):
	# 	img_src = config["loading_page"] + img.get('src')[2:]

	# 	print(img_src)
	# 	img = Image.open(io.BytesIO(requests.get(img_src).content))

	# 	model = genai.GenerativeModel("gemini-1.5-flash")
	# 	prompt = "あなたは商品の販売員です。この商品について、お客様に話すように説明してください。また、ポイント還元というのは商品の料金に合してポイントをお付けするというものです。TTS用に認識させやすい形式で出力してください。100文字以上、200文字以下でまとめてください。"
	# 	response = model.generate_content([prompt, img_src])
	# 	vvox_test(response.text)
	# 	print(response.text)

	# 	time.sleep(60)

if __name__ == "__main__":
	main()