import os
import subprocess
from flask import Flask,request,send_file
from flask_restful import reqparse, Api,Resource
from controllers.image_download1 import Labelled_Image1
app = Flask(__name__)
api = Api(app)


#----------------------------------------------------------------------------------------------------

class Labelled_Image1(Resource):
    def post(self):
        try:
            home_path = os.getcwd()
            #print("//: ",home_path)
            image = request.files['image']
            image_upload = str(home_path) + '/' + 'labelled_image'
            if not os.path.exists(image_upload):
                os.makedirs(image_upload)
            upload_folder = os.path.basename('labelled_image')
            f = os.path.join(upload_folder, image.filename)
            image.save(f)
            image_path = image_upload + '/' + image.filename
            test = subprocess.run('cd ..;cd darknet;./darknet detector test cfg/obj.data cfg/yolo-obj.cfg backup/yolo-voc_13000.weights '+image_path, shell=True)
            if test:
                filename = '/home/ganesh/learning/server/labelled_image/1.jpg'
                return send_file(filename,mimetype='image/jpg')
        except Exception as e:
            return e
#-----------------------------------------------------------------------------------------------------

api.add_resource(Labelled_Image1, '/labelled_image1')
#--------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
