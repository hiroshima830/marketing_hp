import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog_side.html')


@app.route('/send-email', methods=['POST'])
def send_email():
    sender_email = 'bullpen.hiroshima@gmail.com'  # 送信元のメールアドレス
    sender_password = settings.mailpass  # 送信元のメールアカウントのパス

    # メールの作成
    email = request.form['email']
    name = request.form['name']

    subject = f'お問い合わせありがとうございます。'
    body = f'{name}様\n' \
           f'ご連絡ありがとうございます。お手数ですが、以下の質問にお答えいただき返信をお願い致します。5番のみでも構いません。\n' \
           '\n' \
           f'1.貴社名\n' \
           '\n' \
           f'2.貴社ウェブサイトURL\n' \
           '\n' \
           f'3.事業について教えてください。具体的な商品やサービス、ターゲットなど。\n' \
           '\n' \
           f'4.集客のために既に試してみたことや、経験した成果について教えていただけますか？\n' \
           '\n' \
           f'5.その他お問合せ、ご相談したい内容はございますか？\n' \
           '\n' \
           f'上記の質問にお答えいただけましたら、より具体的なご提案や解決策をお伝えすることができます。\n' \
           f'※このメールに心当たりのない場合は、お手数ですが削除をお願い致します。\n' \
           '\n' \
           f'BULLPEN\n' \

    # メールの作成
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # メールの送信
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        # メールの送信に成功した場合には成功メッセージを返す
        return render_template('thanks.html')
    except smtplib.SMTPException:
        return "メールの送信に失敗しました"


if __name__ == '__main__':
    app.run(debug=False)
