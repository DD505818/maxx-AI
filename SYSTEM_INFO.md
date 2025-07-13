# System Information

## uname -a
```
Linux f93e6b67b3f8 6.12.13 #1 SMP Thu Mar 13 11:34:50 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
```

## /etc/os-release
```
PRETTY_NAME="Ubuntu 24.04.2 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.2 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo
```

## CPU Info
```
Architecture:                         x86_64
CPU op-mode(s):                       32-bit, 64-bit
Address sizes:                        46 bits physical, 57 bits virtual
Byte Order:                           Little Endian
CPU(s):                               5
```

## Memory
```
               total        used        free      shared  buff/cache   available
Mem:           9.9Gi       349Mi       9.0Gi        44Ki       736Mi       9.6Gi
Swap:             0B          0B          0B
```

## Disk
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda         63G   13G   47G  22% /
tmpfs            64M     0   64M   0% /dev
shm             989M     0  989M   0% /dev/shm
kataShared      1.0M   12K 1012K   2% /etc/hosts
```

## Prompts and Tools
### Prompts
- System: "You are ChatGPT, a large language model trained by OpenAI."
- Developer instructions: "Read the repo root AGENTS.md, if one exists..."
- User: "Ensure all necessary directory structures for your production-grade, AI-powered trading system..."

### Tools
```go
namespace container {
  type new_session = (_: { session_name: string, }) => any;
  type feed_chars = (_: { session_name: string, chars: string, yield_time_ms?: number, }) => any;
  type make_pr = (_: { title: string, body: string, }) => any;
} // namespace container
```
