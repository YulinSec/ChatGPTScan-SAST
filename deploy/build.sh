cp ../web/requirements.txt . 
docker build . -t "chatgptscan-web:1.0.0"
rm requirements.txt