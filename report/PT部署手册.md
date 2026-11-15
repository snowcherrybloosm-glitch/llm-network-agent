# Packet Tracer 部署手册 - UC-01 创业公司组网完整版

> 本手册由系统自动生成，请按设备逐台粘贴到 PT 的 CLI 中。

## 通用粘贴步骤

1. 在 PT 中双击对应设备 → 进入 `CLI` 标签页。
2. 按回车进入命令行，输入 `enable`，然后输入 `configure terminal`。
3. 逐段复制下方配置，粘贴到终端中。
4. 粘贴完毕输入 `end` 和 `write memory` 保存。

---
## 💻 设备：R0

```cisco
hostname R0
!
interface Gig0/0
 ip address 192.168.16.126 255.255.255.128
 no shutdown
!
interface Gig0/1
 ip address 10.0.0.1 255.255.255.252
 no shutdown
!
interface Gig0/2
 ip address 20.0.0.1 255.255.255.252
 no shutdown
!
router rip
 version 2
 no auto-summary
 network 192.168.16.0
 network 10.0.0.0
 network 20.0.0.0
!
```

---
## 💻 设备：R1

```cisco
hostname R1
!
interface Gig0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
!
interface Gig0/1
 ip address 30.0.0.1 255.255.255.252
 no shutdown
!
interface Gig0/2
 ip address 20.0.0.2 255.255.255.252
 no shutdown
!
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 network 20.0.0.0
 network 30.0.0.0
!
```

---
## 💻 设备：R2

```cisco
hostname R2
!
interface Gig0/0
 ip address 192.168.16.190 255.255.255.192
 no shutdown
!
interface Gig0/1
 ip address 30.0.0.2 255.255.255.252
 no shutdown
!
router rip
 version 2
 no auto-summary
 network 192.168.16.128
 network 30.0.0.0
!
```

---
## 💻 设备：PC0

```cisco
hostname PC0
!
interface eth0
 ip address 192.168.16.1 255.255.255.128
 no shutdown
!
```

**🖥️ 注意**：如果是 PC，请双击 PC → Desktop → IP Configuration，手动填入 IP 和网关。

---
## 💻 设备：PC1

```cisco
hostname PC1
!
interface eth0
 ip address 192.168.16.189 255.255.255.192
 no shutdown
!
```

**🖥️ 注意**：如果是 PC，请双击 PC → Desktop → IP Configuration，手动填入 IP 和网关。
