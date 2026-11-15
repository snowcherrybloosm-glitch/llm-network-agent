import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from core.config_generator import ConfigGenerator

class PTManualGuide:
    def __init__(self):
        self.generator = ConfigGenerator()

    def generate_markdown(self, dsl_path: str, output_path="report/PT部署手册.md"):
        # 1. 读取完美 DSL
        with open(dsl_path, "r", encoding="utf-8") as f:
            dsl = yaml.safe_load(f)

        # 2. 生成配置
        configs = self.generator.generate(dsl)

        # 3. 拼接 Markdown
        lines = [
            f"# Packet Tracer 部署手册 - {dsl.get('name', '拓扑')}\n",
            "> 本手册由系统自动生成，请按设备逐台粘贴到 PT 的 CLI 中。\n",
            "## 通用粘贴步骤\n",
            "1. 在 PT 中双击对应设备 → 进入 `CLI` 标签页。",
            "2. 按回车进入命令行，输入 `enable`，然后输入 `configure terminal`。",
            "3. 逐段复制下方配置，粘贴到终端中。",
            "4. 粘贴完毕输入 `end` 和 `write memory` 保存。\n"
        ]

        for dev_name, cfg in configs.items():
            lines.append(f"---\n## 💻 设备：{dev_name}\n")
            lines.append("```cisco\n" + cfg + "\n```\n")
            
            # 针对 PC 的特殊说明
            if "PC" in dev_name:
                lines.append(f"**🖥️ 注意**：如果是 PC，请双击 PC → Desktop → IP Configuration，手动填入 IP 和网关。\n")

        # 4. 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"✅ PT 部署手册已生成：{output_path}")
        print("请在左侧双击打开该文件，按步骤在 Packet Tracer 中操作即可。")

if __name__ == "__main__":
    guide = PTManualGuide()
    guide.generate_markdown("dsl/examples/uc01_startup.yaml")