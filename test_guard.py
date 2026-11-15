from core.safety_guard import SafetyGuard

guard = SafetyGuard()


commands = [
    "interface Gig0/0",
    "ip address 192.168.1.1 255.255.255.0",
    "no shutdown",
    "reload",                   
    "ip route 0.0.0.0 0.0.0.0", 
    "write erase"               
]

print("=== 开始安全过滤 ===")
allowed, blocked = guard.filter_commands(commands, context="R0_test")

print("\n✅ 允许执行的命令:")
for cmd in allowed:
    print(f"  {cmd}")

print("\n🚫 被拦截的命令:")
for b in blocked:
    print(f"  {b['cmd']} (原因: {b['reason']})")


print("\n=== 测试确认门 ===")
guard.confirm_deploy("R0", len(allowed))
print("测试结束，请查看根目录的 audit_log.jsonl 文件")