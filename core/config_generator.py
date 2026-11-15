import ipaddress

class ConfigGenerator:
    def __init__(self):
        pass

    def generate(self, dsl: dict) -> dict:

        configs = {}
        for dev in dsl.get("devices", []):
            configs[dev["name"]] = self._generate_device_config(dev, dsl)
        return configs

    def _generate_device_config(self, dev: dict, dsl: dict) -> str:
        lines = [f"hostname {dev['name']}", "!"]


        for intf in dev.get("interfaces", []):
            lines.append(f"interface {intf['name']}")
            if intf.get("ip"):
                mask_dotted = str(ipaddress.IPv4Network(f"0.0.0.0/{intf.get('mask', 24)}").netmask)
                lines.append(f" ip address {intf['ip']} {mask_dotted}")
            if intf.get("shutdown"):
                lines.append(" shutdown")
            else:
                lines.append(" no shutdown")
            lines.append("!")


        routing = dev.get("routing", {})
        protocol = routing.get("protocol")
        if protocol == "rip":
            lines.extend([
                "router rip",
                " version 2",
                " no auto-summary"
            ])
            for net in routing.get("networks", []):
                lines.append(f" network {net}")
            lines.append("!")
        elif protocol == "ospf":
            pid = routing.get("process_id", 1)
            lines.append(f"router ospf {pid}")
            for net in routing.get("networks", []):
                
                lines.append(f" network {net}")
            lines.append("!")


        if "default_route" in dev:
            lines.append(f"ip route 0.0.0.0 0.0.0.0 {dev['default_route']}")
            lines.append("!")

        return "\n".join(lines)