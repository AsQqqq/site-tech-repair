from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_url():
    """
    Основная страница
    """

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/letsencrypt/live/repair-31.ru/fullchain.pem', '/etc/letsencrypt/live/repair-31.ru/privkey.pem'))