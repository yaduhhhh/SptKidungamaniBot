apt update && apt upgrade -y
apt install git -y           
pip install -U pip

git clone https://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@github.com/yaduhhhh/SptKidungamaniBot kidu                     
cd kidu
pip install -U -r requirements.txt
python3 bot.py