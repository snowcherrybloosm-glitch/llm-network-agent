import yaml
from core.intent_parser import IntentParser, OllamaClient


llm = OllamaClient(model="qwen2.5:7b")


parser = IntentParser(llm)


requirement = """
搭建一个包含三台路由器、两台 PC 的网络。左侧局域网从 192.168.16.0/24 中划出前一半给行政部（网关取本子网最后一个可用地址）；右侧局域网划出 192.168.16.128/26 给研发部（网关同样取最后一个可用地址）。路由器之间用三条 /30 串行链路互联（10.0.0.0/30、20.0.0.0/30、30.0.0.0/30）。全网运行 RIP 协议，要求使用支持 VLSM 的版本并关闭自动汇总。
"""

print("正在呼叫本地大模型（这可能需要几十秒，请稍候）...")
try:
    dsl = parser.parse(requirement)
    print("\n✅ 生成并校验成功！生成的 DSL 如下：\n")
    # 打印生成的 YAML 结果
    print(yaml.dump(dsl, allow_unicode=True, sort_keys=False))
except Exception as e:
    print(f"\n❌ 失败了：{e}")