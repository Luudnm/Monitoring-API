# Monitoring-API

Om dit werkende te krijgen heb je nodig
* minikube
* docker
* helm

# Rest-API
Een eenvoudige python app die alleen een status terug geeft op de /health endpoint.

Te deployen op het cluster door het image te bouwen aan de hand van de Dockerfile en uit te rollen op cluster via de kustomization.yaml

# Postgress database 
Op het minikube cluster te krijgen met de volgende commando's

    helm repo add bitnami https://charts.bitnami.com/bitnami

    helm install postgres bitnami/postgresql \
      --set auth.username=admin \
      --set auth.password=admin \
      --set auth.database=appdb

# Monitor-API
De python applicatie die de status opvraagd van een rest api en een postgresSQL database

