import re
import ipaddress

class StaticValidator:
    def __init__(self):

        self.dangerous_commands = [
            r"\breload\b", r"\bwrite\s+erase\b", r"\bformat\b",
            r"\berase\b", r"\bdelete\b", r"\bdebug\s+all\b"
        ]

    def validate(self, config: str, dsl: dict) -> dict:

        results = {
            "syntax": self._check_syntax(config),
            "dangerous": self._check_dangerous(config),
            "address_mask": self._check_address_mask(config, dsl),
            "gateway_vlan": self._check_gateway_vlan(config, dsl)
        }

        results["passed"] = all(r["passed"] for r in results.values())
        return results

    def _check_syntax(self, config: str) -> dict:

        errors = []
        for i, line in enumerate(config.split("\n"), 1):
            line = line.strip()
            if not line or line.startswith("!") or line.startswith("hostname"):
                continue
            if line.startswith("interface") and len(line.split()) < 2:
                errors.append(f"行{i}: 接口名缺失")
            if "ip address" in line:
                parts = line.split()
                if len(parts) < 4:
                    errors.append(f"行{i}: IP地址格式不完整")
                elif not re.match(r"^\d+\.\d+\.\d+\.\d+$", parts[2]):
                    errors.append(f"行{i}: 无效的IP格式 {parts[2]}")
        return {"passed": len(errors) == 0, "errors": errors}

    def _check_dangerous(self, config: str) -> dict:

        found = []
        for pattern in self.dangerous_commands:
            if re.search(pattern, config, re.IGNORECASE):
                found.append(f"检测到危险命令: {pattern}")
        return {"passed": len(found) == 0, "errors": found}

    def _check_address_mask(self, config: str, dsl: dict) -> dict:

        errors = []
        for dev in dsl.get("devices", []):
            for intf in dev.get("interfaces", []):
                ip = intf.get("ip")
                mask = intf.get("mask")
                if not ip or ip == "dhcp":
                    continue
                try:

                    iface = ipaddress.ip_interface(f"{ip}/{mask}")
                    if iface.ip == iface.network.network_address:
                        errors.append(f"{dev['name']}.{intf['name']}: {ip} 是网络地址，不能配给接口")
                    if iface.ip == iface.network.broadcast_address:
                        errors.append(f"{dev['name']}.{intf['name']}: {ip} 是广播地址，不能配给接口")
                except ValueError as e:
                    errors.append(f"{dev['name']}.{intf['name']}: IP或掩码无效 ({e})")
        return {"passed": len(errors) == 0, "errors": errors}

    def _check_gateway_vlan(self, config: str, dsl: dict) -> dict:

        errors = []
        for dev in dsl.get("devices", []):

            dev_vlans = {v["id"] for v in dev.get("vlans", []) if isinstance(v, dict) and "id" in v}
            
            for intf in dev.get("interfaces", []):
                vlan = intf.get("vlan")

                if isinstance(vlan, int) and vlan not in dev_vlans:
                    errors.append(f"{dev['name']}.{intf['name']}: 引用了未定义的 VLAN {vlan}")
                

                if dev["type"] == "pc" and intf.get("gateway"):
                    gw = intf["gateway"]
                    if not re.match(r"^\d+\.\d+\.\d+\.\d+$", gw):
                        errors.append(f"{dev['name']}.{intf['name']}: 网关地址格式错误 {gw}")
        return {"passed": len(errors) == 0, "errors": errors}