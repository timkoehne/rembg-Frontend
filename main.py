from base64 import b64encode
import io
import json
import os
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
)
from rembg import remove
from PIL import Image

app = Flask(__name__)
upload_folder = "static/IMG/"


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.png",
        mimetype="image/vnd.microsoft.icon",
    )

@app.route("/")
def test():
    unedited_images = os.listdir(os.path.join(app.root_path, "static", "IMG"))
    finished = os.listdir(os.path.join(app.root_path, "static", "without_background"))
    edited_images = []

    for image in unedited_images:
        image_name = image.split(".")[0] + ".png"
        if image_name in finished:
            edited_images.append(image_name)
        else:
            edited_images.append("")
        print(image_name)

    unedited_images = ["/static/IMG/" + i for i in unedited_images]
    edited_images = ["/static/without_background/" + i for i in edited_images]

    return render_template(
        "image_list.html",
        num_images=len(unedited_images),
        unedited_images=unedited_images,
        edited_images=edited_images,
    )


@app.route("/images/<image_num>")
def images(image_num):
    image_num = int(image_num)
    IMG_LIST = os.listdir(os.path.join(app.root_path, "static", "IMG"))

    if len(IMG_LIST) == 0:
        img = ""
    else:
        IMG_LIST = ["IMG/" + i for i in IMG_LIST]
        if image_num >= len(IMG_LIST):
            return redirect("/images/" + str(image_num % len(IMG_LIST)))
        img = "/static/" + IMG_LIST[image_num]
    return render_template("test.html", image=img)


@app.route("/download_multiple", methods=["GET", "POST"])
def download_multiple():
    IMG_LIST = os.listdir(os.path.join(app.root_path, "static", "IMG"))

    if request.method == "POST":
        if request.json and request.json["ids"]:
            ids = request.json["ids"]
            for id in ids:
                file_type = IMG_LIST[id][IMG_LIST[id].index(".") + 1 :]
                input_path = os.path.join(app.root_path, "static", "IMG") + IMG_LIST[id]
                if file_type != "png":
                    IMG_LIST[id] = IMG_LIST[id].replace(file_type, "png")
                output_path = (
                    os.path.join(app.root_path, "static", "without_background")
                    + IMG_LIST[id]
                )
                input = Image.open(input_path)
                output = remove(input)
                output.save(output_path)  # type: ignore
    return ""


@app.route("/remove_background/<image_num>")
def remove_background(image_num):
    print("removing background")
    image_num = int(image_num)
    IMG_LIST = os.listdir(os.path.join(app.root_path, "static", "IMG"))
    input_path = os.path.join(app.root_path, "static", "IMG", IMG_LIST[image_num])
    output_path = (
        os.path.join(app.root_path, "static", "without_background", IMG_LIST[image_num])
    )

    input = Image.open(input_path)
    output = remove(input)

    file_type = IMG_LIST[image_num][IMG_LIST[image_num].index(".") + 1 :]
    input_path = os.path.join(app.root_path, "static", "IMG", IMG_LIST[image_num])
    output_filename = output_path
    if file_type != "png":
        output_filename = output_path.replace(file_type, "png")
    print(f"saving to {output_filename}")
    output.save(output_filename)  # type: ignore

    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, "png")  # type: ignore
    print(img_byte_arr)

    content = b64encode(img_byte_arr.getvalue()).decode("utf-8")
    return json.dumps({"content": content, "filename": IMG_LIST[image_num]})


@app.route("/delete_image/", methods=["GET", "POST"])
def delete_image():
    if request.method == "POST":
        if request.json and request.json["path"]:
            deletePath = request.json["path"]
            filename: str = deletePath.split("/")[-1]
            filetype = filename[filename.rindex(".") :]
            print(f"filetype {filetype}")

            IMG_LIST = os.listdir(os.path.join(app.root_path, "static", "IMG"))
            if filename in IMG_LIST:
                print("is in img_list")
                full_path = os.path.join(app.root_path, "static", "IMG", filename)
                os.remove(full_path)

            IMG_LIST = os.listdir(
                os.path.join(app.root_path, "static", "without_background")
            )
            filename = filename.replace(filetype, ".png")
            if filename in IMG_LIST:
                print("is in without_background")
                full_path = os.path.join(
                    app.root_path, "static", "without_background", filename
                )
                os.remove(full_path)
    return ""


@app.route("/upload/", methods=["GET", "POST"])  # type: ignore
def upload_file():
    print(request)
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        files = request.files.getlist("file")
        for file in files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            if file and file.filename:
                filename = file.filename
                file.save(upload_folder + filename)
        return redirect(request.referrer)


#TODO show images big when clicked on
#TODO show messages other than alert to report success
#TODO make top stay at the top of the screen
#TODO show progess
#TODO auto refresh after upload or dynamically load entries