# microsoft/resnet-50 


- https://arxiv.org/abs/1512.03385
- https://huggingface.co/microsoft/resnet-50
- https://huggingface.co/docs/transformers/main/en/model_doc/resnet




#### Change directory to where the application lives.
```bash
cd microsoft-resnet-50
```

#### Launch the application locally.
```bash
fastapi dev microsoft-resnet-50/serve_model.py
```

#### Testing the application.
```bash
curl -X GET http://127.0.0.1:8000/
curl -X POST -L -F "file=@data/cats/cat.1.jpg" http://127.0.0.1:8000/predict
curl -X POST -L -F "file=@data/bikes/bike_001.bmp.jpeg" http://127.0.0.1:8000/predict
```


eval $(minikube docker-env)

#### Building the docker image.
```bash
docker build . --tag=local.models/microsoft-resnet-50:latest
```

#### Running the docker image.
```bash
docker run -p 8000:8000 local.models/microsoft-resnet-50:latest
```

#### Registering the image into minikube.

Minikube is required for simulating a real world environment deployment. See. https://minikube.sigs.k8s.io/docs/start 
```bash
minikube image load local.models/microsoft-resnet-50:latest
```

####  Ensure you are running the commands in the minikube cluster
```bash
kubectl config get-contexts
```

#### Deploy the service using kubernetes.

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

#### Set up autoscaling and expose the application.
```bash
kubectl autoscale deployment model-deployment --cpu-percent=50 --min=3 --max=10
kubectl expose deployment model-deployment --type=LoadBalancer --port=8080
```

#### Create a tunnel to access the application from minikube.
```bash
minikube tunnel
```

#### Check the pods are up and running.
```bash
kubectl get pods
```



####  Delete the service using kubernetes.
```bash
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/service.yaml
```

