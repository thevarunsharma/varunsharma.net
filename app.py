from flask import (
    Flask,
    render_template
)
from utils.cfg import (
    extract_post_meta,
    get_configs
)


app = Flask(__name__)
configs = extract_post_meta(get_configs())


@app.route("/")
def index():
    return render_template(
        "index.html",
        **configs
    )
