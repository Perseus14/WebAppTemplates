import os
from flask import Flask, render_template, request, redirect
import glob
#from sightengine.client import SightengineClient

app = Flask(__name__)

#client = SightengineClient('{api_user}', '{api_secret}') # don't forget to add your credentials
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join('static','uploads')
IMAGE_DB = os.path.join('static','image_db')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_DB'] = IMAGE_DB

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global attributes, classes
    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    file.save(filename)

    files = glob.glob(os.path.join(IMAGE_DB,'*'))
    classes = [('.orig','Original')]
    attributes = [('.orig','-1','Uploaded Frontal Chest X-Ray Scan','Original',filename)]
    map_names = {'Atelectasis':'.atel','Cardiomegaly':'.cardio','Mass':'.mass','Nodule':'.nodule','Pneumonia':'.pneum', 'Infiltration':'.infil', 'Effusion':'.effusion', 'Pneumothorax':'.pneumo'}
    prob_map = {'Atelectasis':'93%','Cardiomegaly':'56%','Mass':'75%','Nodule':'7%','Pneumonia':'3%', 'Infiltration':'.infil', 'Effusion':'.effusion', 'Pneumothorax':'.pneumo'}
    text_map = {'Atelectasis':'Atelectasis is the collapse or closure of a lung resulting in reduced or absent gas exchange. It may affect part or all of a lung. It is usually unilateral. It is a condition where the alveoli are deflated down to little or no volume, as distinct from pulmonary consolidation, in which they are filled with liquid.','Cardiomegaly':'Cardiomegaly is a medical condition in which the heart is enlarged. It is more commonly referred to as an enlarged heart. The causes of cardiomegaly may vary. Many times this condition results from high blood pressure (hypertension) or coronary artery disease. An enlarged heart may not pump blood effectively, resulting in congestive heart failure. ','Mass':'A lung mass is defined as an abnormal spot or area in the lungs that is more than 3 cm in size. If a spot (or spots) is less than 3 cm in diameter, it is instead called a lung nodule. The most common causes of a lung mass differ from that of a lung nodule, as well as the chance that the abnormality may be cancer.','Nodule':'A nodule is a spot on the lung, seen on an X-ray or computed tomography (CT) scan. Normal lung tissue surrounds this small round or oval solid overgrowth of tissue. It may be a single or solitary pulmonary nodule.','Pneumonia':'Pneumonia is an infection in one or both lungs. It can be caused by bacteria, viruses, or fungi. Bacterial pneumonia is the most common type in adults. Pneumonia causes inflammation in the air sacs in your lungs, which are called alveoli.', 'Infiltration':'.infil', 'Effusion':'.effusion', 'Pneumothorax':'.pneumo'}
    
    for filename in files:
    	class_name = filename.split('/')[-1].split('.')[0]
    	classes.append((map_names[class_name],class_name))
    	attributes.append((map_names[class_name], prob_map[class_name], text_map[class_name], class_name, filename))
    print(attributes)	
    return redirect('/success')

@app.route('/success')    
def success():
    global attributes, classes    
    return render_template('success_dynamic.html', attributes=attributes, classes=classes)

if __name__ == "__main__":
	app.debug = True
	app.run()
