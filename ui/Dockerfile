# 1️⃣ Build Stage (Node 20)
FROM node:20-alpine AS build

# 2️⃣ Working directory
WORKDIR /app

# 3️⃣ Copy package files
COPY package*.json ./

# 4️⃣ Install dependencies
RUN npm install

# 5️⃣ Copy everything
COPY . .

# 6️⃣ Build Vite
RUN npm run build

# 7️⃣ Nginx runtime for production
FROM nginx:alpine

# 8️⃣ Copy build output → nginx
COPY --from=build /app/dist /usr/share/nginx/html

# 9️⃣ Expose port 80 (container) → app mapped in compose
EXPOSE 80

# ️⃣ Run nginx
CMD ["nginx", "-g", "daemon off;"]
