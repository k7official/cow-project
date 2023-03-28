from flask import Blueprint, render_template, request, redirect, url_for
import base64
from ultralytics import YOLO
import os
import imghdr
from .models import Cow, Img
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")


@views.route('/identify', methods=["GET", "POST"])
def identify():
    return render_template("identify.html")


@views.route('/predict', methods=["GET", "POST"])
def predict():

    # Load a model
    model = YOLO('best_musa.pt')

    if request.method == "POST":
        # TODO: file is a byte string that represents the contents of the uploaded file.
        #  need to convert it back to image for the format required by the model
        # TODO: maybe create an API that will handle this task because its the second time doing it
        file = request.files['fileUpload'].read()
        print(type(file))
        from PIL import Image
        from io import BytesIO

        # assume `file` is the byte string containing binary data of the JPEG image
        img = Image.open(BytesIO(file))

        results = model(img, save=True)  # predict on an image....results not image
        # print(results)

        # set the path to the directory where the results will be saved
        results_dir = '/Users/musa.official/PycharmProjects/project-webapp/runs/detect'

        # run the object detection model and save the results to a file in the results_dir directory
        # ...

        # get the list of files in the results_dir directory
        files = os.listdir(results_dir)

        # filter the list of files to include only files starting with 'predict'
        predict_files = [f for f in files if f.startswith('predict')]

        # sort the list of predict_files based on modification time, in descending order
        predict_files.sort(key=lambda x: os.path.getmtime(os.path.join(results_dir, x)), reverse=True)

        # get the latest predict file
        latest_predict_file = predict_files[0]

        # get the full path of the latest predict file
        latest_predict_path = os.path.join(results_dir, latest_predict_file)

        # print the path of the latest predict file....
        # TODO: think about what to do with the predicted path(file), how to show it to non-technical stakeholders
        # print('Latest predict file:', latest_predict_path)

        image_file = None
        for file in os.listdir(latest_predict_path):
            file_path = os.path.join(latest_predict_path, file)
            if os.path.isfile(file_path):
                if imghdr.what(file_path) is not None:
                    # the file is an image file
                    image_file = file_path
                    break

        if image_file is not None:
            # an image file was found
            image_path = image_file
        else:
            print('Image file not found.')

        # find the image file in the directory
        image_file = None
        for file in os.listdir(latest_predict_path):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                # the file is an image file
                image_file = os.path.join(latest_predict_path, file)
                break
        print(image_file)
        # use the HTML code to display the image
        # if image_file is not None:
        #     html = f"<img src='data:image/jpg;base64,{image_file}' alt='Image'>"
        # else:
        #     html = "<p>Error: Failed to load image.</p>"
        #
        # # return the HTML code to the client
        # return html
        # import time
        # time.sleep(10)
         # from PIL import Image
        # img = Image.open(image_file)
        # img.show()
        import shutil
        src_path = image_file
        dest_dir = 'website/static'
        # copy the file from the source path to the destination directory
        shutil.copy(src_path, dest_dir)
        img_path = file
        # return send_from_directory(latest_predict_path, file)

        return render_template('predictions.html', img_path=img_path)
    return redirect(url_for('home'))


@views.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_cow = Cow(
            animal_id=request.form["animal_id"],
            ear_tag=request.form["ear_tag"],
            animal_type=request.form["animal_type"],
            breed=request.form["breed"],
            color=request.form["color"],
        )
        file = request.files['pic'].read()
        new_img = Img(id=request.form["animal_id"], pic=file)
        db.session.add(new_img)

        # Add record
        db.session.add(new_cow)
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error adding data to database: {e}")
            db.session.rollback()
        finally:
            db.session.close()

        return redirect(url_for('views.home'))

    return render_template("add_animal.html")


@views.route('/display_all', methods=["GET", "POST"])
def display_all():
    # with app.app_context():
    all_cows = db.session.query(Cow).all()
    return render_template('display_all.html', cows=all_cows)


@views.route('/edit', methods=["GET", "POST"])
def edit():
    # UPDATE RECORD
    cow_id = request.args['id']
    cow_to_update = Cow.query.get(cow_id)
    image_object = Img.query.get(cow_id)
    # print(type(image_object))
    image_to_update = image_object.pic
    # print(type(image_to_update))
    encoded_image = base64.b64encode(image_to_update)
    image = encoded_image.decode('UTF-8')
    # print(type(image))
    return render_template('edit.html', cow=cow_to_update, img=image)
