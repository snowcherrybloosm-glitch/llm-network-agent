from core.config_generator import ConfigGenerator
from core.validators import StaticValidator


dsl = {
    "name": "Test",
    "devices": [
        {
            "name": "R0",
            "type": "router",
            "interfaces": [{"name": "Gig0/0", "ip": "192.168.1.1", "mask": 24}]
        }
    ],
    "links": []
}

generator = ConfigGenerator()
validator = StaticValidator()


configs = generator.generate(dsl)
normal_config = configs["R0"]
print("=== 正常配置的检查结果 ===")
res1 = validator.validate(normal_config, dsl)
print(f"是否通过: {res1['passed']}")


bad_config = """
hostname R0
interface Gig0/0
 ip address 192.168.1.0 255.255.255.128
 shutdown
reload
"""
print("\n=== 错误配置的检查结果 ===")
res2 = validator.validate(bad_config, dsl)
print(f"是否通过: {res2['passed']}")
for check_name, result in res2.items():
    if check_name != "passed" and not result["passed"]:
        print(f"  [{check_name}] 发现错误: {result['errors']}")