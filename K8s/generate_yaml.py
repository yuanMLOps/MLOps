# Creating mongodb-bundle.yaml with all Kubernetes manifests for mongo-db namespace
import os

# Ensure output directory exists
output_dir = "/mnt/data"
os.makedirs(output_dir, exist_ok=True)

# Define the YAML content
yaml_content = """# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mongo-db

---
# mongodb-headless-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  namespace: mongo-db
spec:
  clusterIP: None
  selector:
    app: mongodb
  ports:
    - port: 27017
      targetPort: 27017

---
# mongodb-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
  namespace: mongo-db
spec:
  serviceName: mongodb
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo:6.0
          ports:
            - containerPort: 27017
          env:
            - name: MONGO_INITDB_ROOT_USERNAME
              value: admin
            - name: MONGO_INITDB_ROOT_PASSWORD
              value: admin
          volumeMounts:
            - name: mongo-storage
              mountPath: /data/db
  volumeClaimTemplates:
    - metadata:
        name: mongo-storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 5Gi

---
# mongodb-0-nodeport.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-0-svc
  namespace: mongo-db
spec:
  type: NodePort
  selector:
    statefulset.kubernetes.io/pod-name: mongodb-0
  ports:
    - port: 27017
      targetPort: 27017
      nodePort: 32001

---
# mongodb-1-nodeport.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-1-svc
  namespace: mongo-db
spec:
  type: NodePort
  selector:
    statefulset.kubernetes.io/pod-name: mongodb-1
  ports:
    - port: 27017
      targetPort: 27017
      nodePort: 32002

---
# mongodb-2-nodeport.yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-2-svc
  namespace: mongo-db
spec:
  type: NodePort
  selector:
    statefulset.kubernetes.io/pod-name: mongodb-2
  ports:
    - port: 27017
      targetPort: 27017
      nodePort: 32003
"""

# Write to file
file_path = os.path.join(output_dir, "mongodb-bundle.yaml")
with open(file_path, "w") as f:
    f.write(yaml_content)

print("Generated 'mongodb-bundle.yaml' with all Kubernetes manifests for the 'mongo-db' namespace.")
