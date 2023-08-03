# gpt3.5_docker

使用條件:
1. Python 3.9 以上版本
2. 安裝gpt_call.py所使用到的相關套件(依照提示依序pip install)
3. 將OpenAI的API Key輸入程式中或設為環境變數

使用方式:
python gpt_call.py  #可使用語音或文字模式
-------
or
-------
docker build -t gpt-3.5 . #Windows系統下映射麥克風裝置到Docker容器中較為複雜，因此目前在Docker中無法使用語音模式
bash start_gpt.sh
-------
