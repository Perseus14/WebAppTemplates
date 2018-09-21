from flask import Flask, request, redirect, render_template
import datetime
import os,glob
import sys
from PIL import Image
import json

import skin_lesion

app = Flask(__name__)
now = datetime.datetime.now()
IMG_DB = os.path.join('static','image_db')

################################

if not os.path.exists(IMG_DB):
	os.makedirs(IMG_DB)

@app.route('/')
def hello_world():
    return render_template('index_single.html')

@app.route("/upload", methods=["GET","POST"])
def upload():
    global attributes, text_map, name_map

    img = Image.open(request.files['image'])
    now = datetime.datetime.now()
    path_name = os.path.join(IMG_DB, "sdd-test_"+now.isoformat()+".png")
    img.save(path_name)

    prediction = skin_lesion.test(path_name)
    attributes = [(prediction[0]['image_path'], prediction[1]['Lesion Detected'], prediction[2]['Top Predictions'])]
    name_map = {'Malignant melanoma':'mmel', 'Basal cell carcinoma':'bcc', 'Squamous cell carcinoma':'scc', 'Intraepithelial carcinoma':'iec',
            'Pyogenic granuloma':'pg', 'Seborrheic keratosis':'sk', 'Melanocytic nevus':'mn', 'Actinic keratosis':'ak', 'Dermatofibroma':'df',
            'Hemangioma':'hg', 'Wart':'wart', 'Lentigo':'lentigo'}
    text_map = {'Malignant melanoma':'A type of cancer that develops from the pigment-containing cells known as melanocytes, typically occur in the skin','Basal cell carcinoma':'A type of skin cancer that begins in the basal cells, often appears as a slightly transparent bump on the skin, occurs on areas of the skin that are exposed to the sun, such as your head and neck.','Squamous cell carcinoma':'A type of cancer usually found on areas of the body damaged by UV rays from the sun or tanning beds, includes the head, neck, ears, lips, arms, legs, and hands.', 'Intraepithelial carcinoma':'A type of squamous cell skin cancer but one that is confined only to the upper layer of skin (epidermis) and is therefore fairly easy to treat.','Pyogenic granuloma':'A vascular lesion that occurs on both mucosa and skin, and appears as an overgrowth of tissue due to irritation, physical trauma, or hormonal factors.', 'Seborrheic keratosis':'A non-cancerous (benign) skin tumour that originates from cells in the outer layer of the skin (keratinocytes).', 'Melanocytic nevus':'Benign neoplasms or hamartomas composed of melanocytes, the pigment-producing cells that constitutively colonize the epidermis', 'Actinic keratosis':'A crusty, scaly growth caused by damage from exposure to ultraviolet (UV) radiation.', 'Dermatofibroma': 'A common benign fibrous nodule that most often arises on the skin of the lower legs.', 'Hemangioma':'Noncancerous growths that form on your skin or liver. Most people develop them in the womb, and they\'re usually harmless.', 'Wart':'A small, fleshy bump on the skin or mucous membrane caused by a virus.', 'Lentigo':'Flat tan, brown or black spots on the skin common with age.'}
    
    return redirect('/success')

@app.route('/success')    
def success():
    global attributes, text_map, name_map   
    return render_template('skin_res.html', attributes=attributes, text_map=text_map, name_map=name_map)   
########################################

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5002, debug=True)

