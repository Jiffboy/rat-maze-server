sudo systemctl stop ratmaze.service

cd ..
git pull

cd frontend
npm install
npm run build

sudo systemctl start ratmaze.service