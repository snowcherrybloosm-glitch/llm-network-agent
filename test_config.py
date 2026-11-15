import yaml
from core.config_generator import ConfigGenerator


dsl_yaml = """
name: 三路由器两PC网络
devices:
- name: R0
  type: router
  interfaces:
  - {name: Gig0/0, ip: 10.0.0.1, mask: 30}
  - {name: Gig0/1, ip: 192.168.16.1, mask: 24}
  - {name: Gig0/2, ip: 20.0.0.1, mask: 30}
  routing:
    protocol: rip
    networks: ["10.0.0.0", "192.168.16.0", "20.0.0.0"]
- name: R1
  type: router
  interfaces:
  - {name: Gig0/0, ip: 10.0.0.2, mask: 30}
  - {name: Gig0/1, ip: 192.168.16.64, mask: 26}
  - {name: Gig0/2, ip: 20.0.0.2, mask: 30}
  routing:
    protocol: rip
    networks: ["10.0.0.0", "192.168.16.0", "20.0.0.0"]
links: []
"""

dsl = yaml.safe_load(dsl_yaml)
generator = ConfigGenerator()
configs = generator.generate(dsl)

print("✅ 配置生成成功！\n")
for dev_name, config in configs.items():
    print(f"===== 设备 {dev_name} 的配置 =====")
    print(config)
    print("\n")