from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloader</title>
    <style>
        body { font-family: Arial; padding: 40px; }
        input { width: 400px; padding: 10px; }
        button { padding: 10px 20px; }
    </style>
</head>
<body>
    <h2>YouTube Video Downloader</h2>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="Paste YouTube link here" required/>
        <button type="submit">Download</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")

    # Generate a random filename to avoid clashes
    video_id = str(uuid.uuid4())
    output_path = f"{video_id}.mp4"

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4/best",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Send the file to user
        response = send_file(
            output_path,
            as_attachment=True,
            download_name="video.mp4"
        )

        # Delete file after sending
        os.remove(output_path)
        return response

    except Exception as e:
        return f"Error: {e}"
    

if __name__ == "__main__":
    app.run(debug=True)
