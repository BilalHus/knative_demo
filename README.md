# Installation guide:

## Install metrics

`helm upgrade --install metrics-server metrics-server/metrics-server --set args={--kubelet-insecure-tls}`

## Install Knative

### Serving

`kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-crds.yaml`

`kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-core.yaml`

`kubectl apply -f https://github.com/knative/net-kourier/releases/download/knative-v1.15.1/kourier.yaml`

`kubectl patch configmap/config-network --namespace knative-serving --type merge --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'`

`kubectl --namespace kourier-system get service kourier`

`kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.15.2/serving-default-domain.yaml`

### Eventing

`kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.15.2/eventing-crds.yaml`

`kubectl apply -f https://github.com/knative/eventing/releases/download/knative-v1.15.2/eventing-core.yaml`

`kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.15.5/eventing-kafka-controller.yaml`

`kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.15.5/eventing-kafka-channel.yaml`

`kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.15.5/eventing-kafka-broker.yaml`

`kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.15.5/eventing-kafka-sink.yaml`

`kubectl apply -f https://github.com/knative-extensions/eventing-kafka-broker/releases/download/knative-v1.15.5/eventing-kafka-source.yaml`


## Install Kafka

`kubectl create namespace kafka`

`helm install kafka oci://registry-1.docker.io/bitnamicharts/kafka -f values.yaml --namespace kafka`

`kubectl run kafka-client --restart='Never' --image docker.io/bitnami/kafka:3.8.0-debian-12-r5 --namespace kafka --command -- sleep infinity`

`kubectl exec --tty -i kafka-client --namespace kafka -- bash`

    PRODUCER:
        kafka-console-producer.sh \
            --broker-list kafka-controller-0.kafka-controller-headless.kafka.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.kafka.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.kafka.svc.cluster.local:9092 \
            --topic demo

    CONSUMER:
        kafka-console-consumer.sh \
            --bootstrap-server kafka.kafka.svc.cluster.local:9092 \
            --topic demo \
            --from-beginning
    
    TOPICS:
        kafka-topics.sh \
            --bootstrap-server kafka.kafka.svc.cluster.local:9092 \
            --create \
            --topic demo \
            --partitions 3 \
            --replication-factor 1

`Message format: '{"name": "Alice", "age": 30, "city": "New York"}'`

## Build image

`pip freeze > requirements.txt`
`docker build -t bilalhus/knative_demo .`
`docker tag bilalhus/knative_demo m1koto/knative_demo:v2`
`docker push m1koto/knative_demo:v2`
