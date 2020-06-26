import io
from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
from utils import get_img
from model import g
gen=g(1).cpu()


def serve_pil_image(pil_img):
    img_io = io.BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


#from model import gen_photo
app = Flask(__name__)

print('started')
@app.route('/',methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
  
  name = request.form.get('city')

  return serve_pil_image(get_img(name,gen))





if __name__ == "__main__":
    app.run(port='4567', host='0.0.0.0')
