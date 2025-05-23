from langchain_core.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate

examples = [
    {
        "user_input": "I want a Node.js service with 1 GB of memory, exposed on port 3000",
        "output": """
```yaml
version: "1.0"

services:
  web:
    image: node:latest
    expose:
      - port: 3000
        as: 3000
        to:
          - global: true
    env:
      - NODE_ENV=production

profiles:
  name: node-service
  mode: provider
  duration: 1h
  tier:
    - community
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 1Gi
        storage:
          size: 1Gi

  placement:
    default:
      attributes:
        region: us-east
      pricing:
        web:
          token: CST
          amount: 50

deployment:
  web:
    default:
      profile: web
      count: 1
```
""",
    },
    {
        "user_input": "Deploy a Node.js service with auto-scaling, starting with 2 instances and a maximum of 5, using 1.5 GB of memory each",
        "output": """
```yaml
version: "1.0"

services:
  web:
    image: node:latest
    expose:
      - port: 3000
        as: 3000
        to:
          - global: true
    env:
      - NODE_ENV=production

profiles:
  name: node-service-auto
  mode: provider
  duration: 1h
  tier:
    - community
  compute:
    web:
      resources:
        cpu:
          units: 1
        memory:
          size: 1.5Gi
        storage:
          size: 2Gi

  placement:
    scalable-region:
      attributes:
        region: us-east
      pricing:
        web:
          token: CST
          amount: 70

deployment:
  web:
    scalable-region:
      profile: web
      count: 2
```
""",
    },
    {
        "user_input": "Create a Node.js app with 2 GB of memory and 5 GB of persistent storage, running on port 8080.",
        "output": """
```yaml
version: "1.0"

services:
  web:
    image: node:latest
    expose:
      - port: 8080
        as: 8080
        to:
          - global: true
    env:
      - NODE_ENV=production

profiles:
  name: node-app-storage
  mode: provider
  duration: 1h
  tier:
    - community
  compute:
    web:
      resources:
        cpu:
          units: 1
        memory:
          size: 2Gi
        storage:
          size: 5Gi

  placement:
    storage-optimized:
      attributes:
        region: us-west
      pricing:
        web:
          token: cst
          amount: 100

deployment:
  web:
    storage-optimized:
      profile: web
      count: 1
```
""",
    },
    {
        "user_input": "Set up a high-performance Node.js API with 2 vCPUs, 4 GB of memory, and auto-scaling from 1 to 10 instances.",
        "output": """
```yaml
version: "1.0"

services:
  api:
    image: node:latest
    expose:
      - port: 4000
        as: 4000
        to:
          - global: true
    env:
      - NODE_ENV=production

profiles:
  name: high-performance-node
  mode: provider
  duration: 1h
  tier:
    - professional
  compute:
    api:
      resources:
        cpu:
          units: 2
        memory:
          size: 4Gi
        storage:
          size: 10Gi

  placement:
    performance-region:
      attributes:
        region: us-central
      pricing:
        api:
          token: CST
          amount: 200

deployment:
  api:
    performance-region:
      profile: api
      count: 5
```
""",
    },
    {
        "user_input": "Deploy a Node.js service with 1 GB of memory, 0.5 vCPU, and a pricing model using USDT at 20 per instance",
        "output": """
```yaml
version: "1.0"

services:
  web:
    image: node:latest
    expose:
      - port: 3000
        as: 3000
        to:
          - global: true
    env:
      - NODE_ENV=production

profiles:
  name: cost-optimized-node
  mode: provider
  duration: 1h
  tier:
    - community
  compute:
    web:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 1Gi
        storage:
          size: 1Gi

  placement:
    cost-effective:
      attributes:
        region: us-east
      pricing:
        web:
          token: USDT
          amount: 20

deployment:
  web:
    cost-effective:
      profile: web
      count: 1
```
""",
    },
    {
        "user_input": "Set up a Jupyter notebook service with 1 GB of memory and 0.5 vCPU",
        "output": """
```yaml
version: "1.0"

services:
  jupyter:
    image: jupyter/minimal-notebook:latest
    expose:
      - port: 8888
        as: 8888
        to:
          - global: true
    env:
      - JUPYTER_ENABLE_LAB=yes

profiles:
  name: jupyter-notebook
  mode: provider
  duration: 1h
  tier:
    - community
  compute:
    jupyter:
      resources:
        cpu:
          units: 0.5
        memory:
          size: 1Gi
        storage:
          size: 5Gi

  placement:
    default:
      attributes:
        region: us-east
      pricing:
        jupyter:
          token: CST
          amount: 50

deployment:
  jupyter:
    default:
      profile: jupyter
      count: 1
```
""",
    },
    {
        "user_input": "Deploy a Jupyter Notebook service with PyTorch 2.4.1 and CUDA on port 8888, using 8 vCPUs, 16 GB RAM, 200 GB storage, and an H100 GPU in the US West region for 30 min at 10 USDT per instance.",
        "output": """
```yaml
version: "1.0"

services:
  py-cuda:
    image: docker.io/pytorch/pytorch:2.4.1-cuda12.1-cudnn8-runtime
    expose:
      - port: 8888
        as: 8888
        to:
          - global: true
    env:
      - JUPYTER_TOKEN=sentient

profiles:
  name: py-cuda
  mode: provider
  duration: 30min
  tier:
    - community
  compute:
    py-cuda:
      resources:
        cpu:
          units: 8
        memory:
          size: 16Gi
        storage:
          - size: 200Gi
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
                - model: h100
  placement:
    westcoast:
      attributes:
        region: us-west
      pricing:
        py-cuda:
          token: CST
          amount: 10

deployment:
  py-cuda:
    westcoast:
      profile: py-cuda
      count: 1
```
""",
    },
]

prompt = ChatPromptTemplate.from_messages(
    [("user", "{user_input}"), ("ai", "{output}")],
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=prompt, examples=examples
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a chatbot helping users deploy service on spheron. Your task is to generatre config.yml files based on user input. Make sure the minimum duration must be 5 minutes.",
        ),
        few_shot_prompt,
        ("user", "{user_input}"),
    ]
)
