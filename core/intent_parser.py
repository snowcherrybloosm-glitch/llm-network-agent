import json
import yaml
import requests
from jsonschema import validate

class OllamaClient:
    def __init__(self, model="qwen2.5:7b", url="http://127.0.0.1:11434"):
        self.model = model
        self.url = url

    def generate(self, prompt: str) -> str:
        
        r = requests.post(f"{self.url}/api/generate", json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        return r.json()["response"]

class IntentParser:
    def __init__(self, llm_client, schema_path="dsl/topology_schema.json"):
        self.llm = llm_client
        self.schema = json.load(open(schema_path, encoding='utf-8'))

    def parse(self, natural_language: str) -> dict:
        prompt = f"""你是网络拓扑专家。请将以下需求转换为符合JSON Schema的YAML DSL。
你必须严格遵守以下规则：
1. 顶层必须只包含 name, devices, links 三个字段，不要加其他的。
2. ip 和 mask 必须分开写。例如：ip: "192.168.1.1", mask: 24 （不能写成 CIDR 格式）。
3. links 必须用 a, b, a_intf, b_intf 格式。
4. 严格只输出 YAML，不要输出任何解释文字，不要带 ```yaml 标记。

以下是格式示例：
name: "示例网络"
devices:
  - name: R0
    type: router
    interfaces:
      - name: Gig0/0
        ip: "10.0.0.1"
        mask: 30
links:
  - a: R0
    b: R1
    a_intf: Gig0/0
    b_intf: Gig0/0

需求: {natural_language}

请严格按照上述示例格式输出 YAML:"""

        response = self.llm.generate(prompt)
        

        response = response.replace("```yaml", "").replace("```", "").strip()


        try:
            dsl = yaml.safe_load(response)
        except Exception as e:
            raise ValueError(f"YAML解析失败，LLM原始输出：\n{response}\n错误：{e}")


        validate(instance=dsl, schema=self.schema)
        return dsl