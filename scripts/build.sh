cd frontend
npm install -g pnpm
pnpm install
pnpm build
cd ..
cp -r frontend/dist/* backend/staticfiles/
cp frontend/dist/index.html backend/backend/templates/
