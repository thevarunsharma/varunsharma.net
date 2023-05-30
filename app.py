from flask import (
    Flask,
    render_template
)
from utils.cfg import (
    extract_post_meta,
    get_configs
)

app = Flask(__name__)
raw_configs = get_configs()


@app.route("/")
def index():
    configs = extract_post_meta(raw_configs)
    return render_template(
        "index.html",
        **configs
    )


if __name__ == '__main__':
    app.run()
