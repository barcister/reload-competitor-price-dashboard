FROM node:22-alpine
WORKDIR /app
COPY package.json tsconfig.json next-env.d.ts ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]
