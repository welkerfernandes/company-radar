FROM eclipse-temurin:21-jdk AS native
WORKDIR /native
COPY engines/registry/RegistryPolicy.java .
RUN javac -d build RegistryPolicy.java
FROM eclipse-temurin:21-jre AS jre

FROM node:24-slim AS web
WORKDIR /web
COPY web/package*.json ./
RUN npm ci
COPY web .
RUN npm run build

FROM python:3.12-slim
WORKDIR /service
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home service && chown service /service
COPY --chown=service:service app ./app
COPY --from=web --chown=service:service /app/frontend ./app/frontend
COPY --from=jre /opt/java/openjdk /opt/java/openjdk
COPY --from=native /native/build /service/native
ENV NATIVE_ENGINE='["/opt/java/openjdk/bin/java","-cp","/service/native","RegistryPolicy"]'
USER service
EXPOSE 8202
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8202"]
