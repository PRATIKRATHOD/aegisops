# 1️⃣ Build Stage (Node)
FROM node:18 AS build

# 2️⃣ Working dir inside container
WORKDIR /app

# 3️⃣ Copy package.json and install deps
COPY package*.json ./
RUN npm install

# 4️⃣ Copy full UI source
COPY . .

# 5️⃣ Build React App
RUN npm run build

# 6️⃣ Production Stage (nginx)
FROM nginx:alpine

# 7️⃣ Copy build output to nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

# 8️⃣ Expose port
EXPOSE 3000

# 9️⃣ Start nginx
CMD ["nginx", "-g", "daemon off;"]
