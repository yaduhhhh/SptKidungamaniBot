apt update && apt upgrade -y
apt install git -y           
pip install -U pip

git clone https://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@github.com/yaduhhhh/SptKidungamaniBot kidu                     
cd kidu
pip install -U -r requirements.txt
python3 bot.py