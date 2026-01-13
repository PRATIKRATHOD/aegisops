# 1️⃣ Use Java 17 base image
FROM eclipse-temurin:17-jdk-alpine

# 2️⃣ Install Maven (because your project does not include mvnw wrapper)
RUN apk update && apk add --no-cache maven

# 3️⃣ Set work directory
WORKDIR /app

# 4️⃣ Copy backend source code
COPY . .

# 5️⃣ Build Spring Boot JAR
RUN mvn -q -e -DskipTests package

# 6️⃣ Run the correct JAR (your actual jar file)
CMD ["java", "-jar", "target/aegisops-backend-1.0.0.jar"]
