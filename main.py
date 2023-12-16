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
from rembg.session_factory import new_session

app = Flask(__name__)
unedited_files_folder = "static/IMG/".split("/")
edited_files_folder = "static/without_background/".split("/")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.png",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/")
def test():
    unedited_images = os.listdir(os.path.join(app.root_path, *unedited_files_folder))
    finished = os.listdir(os.path.join(app.root_path, *edited_files_folder))
    edited_images = []

    for image in unedited_images:
        image_name = image.split(".")[0] + ".png"
        if image_name in finished:
            edited_images.append(image_name)
        else:
            edited_images.append("")
        print(image_name)

    unedited_images = [os.path.join(*unedited_files_folder, i) for i in unedited_images]
    edited_images = [os.path.join(*edited_files_folder, i) for i in edited_images]

    # unedited_images = ["/static/IMG/" + i for i in unedited_images]
    # edited_images = ["/static/without_background/" + i for i in edited_images]

    return render_template(
        "image_list.html",
        separator=os.sep,
        num_images=len(unedited_images),
        unedited_images=unedited_images,
        edited_images=edited_images,
    )


@app.route("/remove_background", methods=["GET", "POST"])
def remove_background():
    if request.method == "POST":
        if request.json:
            request_content = request.json
            print(request_content)

            IMG_LIST = os.listdir(os.path.join(app.root_path, *unedited_files_folder))
            input_path = os.path.join(
                app.root_path, *unedited_files_folder, request_content["filename"]
            )
            output_filename = request_content["filename"]

            file_type = request_content["filename"][
                request_content["filename"].index(".") + 1 :
            ]
            if file_type != "png":
                output_filename = request_content["filename"].replace(file_type, "png")
            output_path = os.path.join(
                app.root_path, *edited_files_folder, output_filename
            )

            print(f"input_path {input_path}")
            print(f"output_path {output_path}")

            image = Image.open(input_path)
            image = remove(
                image,
                alpha_matting=request_content["enable_alpha_matting"],
                alpha_matting_foreground_threshold=request_content[
                    "alpha_matting_foreground_threshold"
                ],
                alpha_matting_background_threshold=request_content[
                    "alpha_matting_background_threshold"
                ],
                session=new_session(request_content["model"]),
            )

            image.save(output_path)  # type: ignore

            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, "png")  # type: ignore

            content = b64encode(img_byte_arr.getvalue()).decode("utf-8")
            return json.dumps(
                {"content": content, "filename": request_content["filename"]}
            )

    return ""


@app.route("/delete_image/", methods=["GET", "POST"])
def delete_image():
    if request.method == "POST":
        if request.json and request.json["path"]:
            deletePath = request.json["path"]
            filename: str = deletePath.split(os.sep)[-1]
            filetype = filename[filename.rindex(".") :]
            print(filename)
            print(f"filetype {filetype}")

            IMG_LIST = os.listdir(os.path.join(app.root_path, *unedited_files_folder))
            if filename in IMG_LIST:
                print("is in img")
                full_path = os.path.join(
                    app.root_path, *unedited_files_folder, filename
                )
                print(f"deleting {full_path}")
                os.remove(full_path)

            IMG_LIST = os.listdir(os.path.join(app.root_path, *edited_files_folder))
            filename = filename.replace(filetype, ".png")
            if filename in IMG_LIST:
                print("is in without_background")
                full_path = os.path.join(app.root_path, *edited_files_folder, filename)
                print(f"deleting {full_path}")
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
                file.save(os.path.join(app.root_path, *unedited_files_folder, filename))
        return redirect(request.referrer)


# TODO show images big when clicked on
# TODO show messages other than alert to report success
# TODO show progess
