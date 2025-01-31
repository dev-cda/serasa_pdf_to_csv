import os
import PyPDF2

from flask import (
    Blueprint,
    current_app as app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from fileupload.utils.upload import (
    create_csv
)

from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pdf"


@bp.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            pdf_filename = secure_filename(file.filename)
            filename = pdf_filename.split('.')[0]
            
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename))

            csv_filename = f"{filename}.csv"

            create_csv(
                csv_filename,
                app.config["CSV_FOLDER"]
            )

            return redirect(url_for("upload.download_file", name=csv_filename))
    return render_template("upload/index.html")


@bp.route("/uploads/<name>")
def download_file(name):
    return send_from_directory(app.config["CSV_FOLDER"], name)
