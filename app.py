import json
import sys
import urllib
from urllib import parse

# Package import
from flask import Flask, render_template, request

# initialise app
app = Flask(__name__)


# decorator for homepage
@app.route('/')
def home():
    f = open('templates/results.html', 'w')
    f.close()
    f = open('static/collage.js', 'w')
    f.close()
    return render_template('index.html')


@app.route('/', methods=["POST"])
def search():
    search = request.form["gif"]
    print(search)
    url = "http://api.giphy.com/v1/gifs/search"

    params = parse.urlencode({
        "q": search,
        "api_key": "s3wjS43tb003Ho0tZUHH9fMC0pHR7vrv"
    })

    with urllib.request.urlopen("".join((url, "?", params))) as response:
        data = json.loads(response.read())

    data = json.dumps(data, sort_keys=True, indent=4)
    data = json.loads(data)

    data = data["data"]

    f = open('templates/results.html', 'w')

    html_template = """<!DOCTYPE html>
<head>
    <title>Giphy Playground</title>
    <script type="text/javascript" src="jquery-2.0.0.min.js"></script>
    <link rel="stylesheet" href='/static/style.css' />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet"  type='text/css'>
</head>
      <body>
<div class="text-center">
    <h1><i class="fas fa-clone"></i> GIPHY Playground</h1>
    <h4>Powered By GIPHY</h4>
    <p>By: Vincent Song</p>
    <form name="search" action="." method="post">
        <label>Search Gifs: </label>
        <input type="text" name="gif">
        <input type="submit" value="Submit">
    </form>
</div>     
      """
    html_template += "\n"
    html_template += "<h2>Results for: " + search + "</h2>"
    gif_urls = []
    for gif in data:
        #   html_template += "\n"
        #   html_template += "<img src = \"" + gif['images']["original"]["url"] + "\"/>"
        gif_urls.append(gif['images']["original"]["url"])

    print(gif_urls)

    html_template += "\n"

    html_template += """
      <script type="text/javascript" src="static/collage.js"></script>

      </body>
      </html>
      """

    # writing the code into the file
    f.write(html_template)

    # close the file
    f.close()

    sys.stdout = open('static/collage.js', 'w')
    f = open('static/collage.js', 'w')
    f.write("const images = [")
    i = 0
    while i < len(gif_urls):
        if i != len(gif_urls) - 1:
            f.write("\"" + gif_urls[i] + "\"" + ", ")
        else:
            f.write("\"" + gif_urls[i] + "\"")
        i += 1
    f.write("]")
    f.write("""
    let i = 0

    function placeImage(x,y) {
        const nextImage = images[i]
        const img = document.createElement("img")
        img.setAttribute("src", nextImage)
        img.style.left = x + "px"
        img.style.top = y + "px"
        img.style.transform = "translate(-50%, -50%) scale(0.5) rotate(" + (Math.random() * 20 - 10) + "deg)"

        document.body.appendChild(img)
        i = i + 1

        if (i >= images.length){
            i = 0
        }
    }
    
    let mouse = 0
    
    document.addEventListener("mousemove", function(event) {
      mouse = mouse + 1
      if (mouse % 20 == 0){
        placeImage(event.pageX,event.pageY)
      }
    })
    """)
    f.close()

    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)
