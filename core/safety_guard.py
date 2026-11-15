import re
import json
from datetime import datetime

class SafetyGuard:
    def __init__(self):

        self.whitelist = [
            r"^hostname\s+\S+",
            r"^interface\s+\S+",
            r"^ip\s+address\s+\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+",
            r"^no\s+shutdown",
            r"^shutdown",
            r"^router\s+(rip|ospf|bgp)\s*\d*",
            r"^network\s+\S+",
            r"^version\s+2",
            r"^no\s+auto-summary",
            r"^vlan\s+\d+",
            r"^name\s+\S+",
            r"^encapsulation\s+dot1Q\s+\d+",
            r"^ip\s+nat\s+\S+",
            r"^access-list\s+\d+\s+\S+",
            r"^bgp\s+router-id",
            r"^neighbor\s+\S+\s+remote-as\s+\d+",
            r"^!",
            r"^end",
            r"^exit"
        ]

        self.blacklist = [
            (r"\breload\b", "设备重启命令被拦截"),
            (r"\bwrite\s+erase\b", "配置擦除命令被拦截"),
            (r"\bformat\b", "格式化命令被拦截"),
            (r"\berase\s+(startup|flash)", "擦除命令被拦截"),
        ]
        
        self.audit_log_file = "audit_log.jsonl"

    def filter_commands(self, commands: list, context: str = "") -> tuple:

        allowed, blocked = [], []
        for cmd in commands:
            cmd_clean = cmd.strip()
            if not cmd_clean:
                continue


            blacklisted = False
            for pattern, reason in self.blacklist:
                if re.search(pattern, cmd_clean, re.IGNORECASE):
                    blocked.append({"cmd": cmd_clean, "reason": reason})
                    self._audit("BLACKLIST_BLOCK", cmd_clean, reason, context)
                    blacklisted = True
                    break
            if blacklisted:
                continue


            whitelisted = any(re.match(p, cmd_clean) for p in self.whitelist)
            if whitelisted:
                allowed.append(cmd_clean)
                self._audit("WHITELIST_PASS", cmd_clean, "", context)
            else:

                blocked.append({"cmd": cmd_clean, "reason": "不在白名单"})
                self._audit("WHITELIST_BLOCK", cmd_clean, "不在白名单", context)
                
        return allowed, blocked

    def confirm_deploy(self, device_name: str, command_count: int) -> bool:

        print(f"\n{'='*50}")
        print(f"【确认门】设备: {device_name} | 准备下发命令数: {command_count}")
        response = input("确认部署? [yes/no]: ")
        confirmed = response.lower() == "yes"
        self._audit("MANUAL_CONFIRM", f"deploy to {device_name}", "confirmed" if confirmed else "rejected", "")
        return confirmed

    def _audit(self, action: str, content: str, result: str, context: str):

        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "content": content[:200],
            "result": result,
            "context": context
        }
        with open(self.audit_log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")