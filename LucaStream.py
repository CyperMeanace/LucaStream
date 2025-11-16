from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>LucaTube Downloader</title>
    <style>
        body {
            background-color: #0d0d0d;
            color: #00ffea;
            font-family: 'Consolas', 'Courier New', monospace;
            text-align: center;
            padding-top: 80px;
        }

        h1 {
            font-size: 50px;
            text-shadow: 0 0 10px #00ffe5, 0 0 20px #00ffe5;
            animation: glow 4s infinite alternate;
        }

        @keyframes glow {
            from { text-shadow: 0 0 10px #00ffe5; }
            to { text-shadow: 0 0 25px #00ffe5; }
        }

        .input-box {
            width: 450px;
            padding: 15px;
            border: 2px solid #00ffe5;
            border-radius: 10px;
            background-color: #1a1a1a;
            color: #00ffe5;
            outline: none;
            font-size: 18px;
            box-shadow: 0 0 10px #00ffe5;
        }

        .download-btn {
            margin-top: 20px;
            padding: 12px 30px;
            font-size: 20px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            background-color: #00ffe5;
            color: black;
            transition: 0.2s;
            font-weight: bold;
            box-shadow: 0 0 20px #00ffe5;
        }

        .download-btn:hover {
            background-color: #0affc1;
            box-shadow: 0 0 35px #00ffe5;
            transform: scale(1.05);
        }

        footer {
            margin-top: 40px;
            font-size: 14px;
            opacity: 0.7;
        }
    </style>
</head>
<body>

    <h1>LUCA<span style="color:#0affc1">STREAM</span></h1>
    <p>⚡ Cyber-AI Powered YouTube Downloader ⚡</p>

    <form method="POST" action="/download">
        <input class="input-box" type="text" name="url" placeholder="Paste YouTube link here..." required>
        <br>
        <button class="download-btn" type="submit">Download</button>
    </form>

    <footer>
        Designed by LucaAI • Cyber Intelligence Module v1.0
    </footer>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")

    video_id = str(uuid.uuid4())
    output_path = f"{video_id}.mp4"

    ydl_opts = {
        "outtmpl": output_path,
        "format": "mp4/best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = send_file(
            output_path,
            as_attachment=True,
            download_name="LucaTube_video.mp4"
        )

        os.remove(output_path)
        return response

    except Exception as e:
        return f"<h2 style='color:red;'>Error: {e}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
