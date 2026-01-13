FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Vite dev server with host flag
CMD ["npm", "run", "dev", "--", "--host"]
