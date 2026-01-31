# 🕵️ NETRUNNER

> Advanced Network Intrusion Simulator
> 
> A text-based cyberpunk hacking game with procedural generation and persistent world

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## 📖 Description

NETRUNNER is a text-based hacking simulation game where you play as a cyberpunk hacker navigating through procedurally generated corporate networks. Execute exploits, manage botnets, complete contracts, and climb the ranks of the underground hacking community.

## ✨ Features

- **Procedural Network Generation** — Every playthrough features unique networks with different security levels
- **Multiple Exploitation Vectors** — SQL injection, buffer overflow, XSS, RCE, social engineering, and more
- **Deep Progression System** — 7 skills to develop, hardware upgrades, and reputation mechanics
- **Social Engineering** — Phishing campaigns, OSINT reconnaissance, and employee compromise
- **Cryptanalysis Lab** — Break encryption to steal valuable data
- **Botnet Management** — Build and maintain DDoS attack networks
- **Contract System** — Accept missions from anonymous clients
- **Rival Hackers** — Compete with AI hackers for the same targets
- **Heat & Investigation System** — Stay under the radar or face consequences
- **Dynamic World Events** — Global patches, police crackdowns, zero-day leaks
- **Save/Load System** — Persistant game state with JSON serialization

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- No external dependencies required (stdlib only)

### Installation

```bash
git clone https://github.com/faustyu1/netrunner.git
cd hacker-game
python hacker_game.py
```

## 🎮 How to Play

### Main Menu Options

| Option | Description |
|--------|-------------|
| **Network Operations** | Scan, attack, and navigate through network nodes |
| **Contract Board** | Accept missions with rewards and deadlines |
| **Black Market** | Purchase tools, exploits, and hardware upgrades |
| **Social Engineering** | Phishing, OSINT, and employee manipulation |
| **Cryptanalysis Lab** | Decrypt intercepted data packages |
| **Botnet Management** | Build and control zombie networks |
| **Intelligence** | View rival hackers and faction standings |

### Basic Gameplay Loop

1. **Scan** a network node to discover services and vulnerabilities
2. **Attack** using discovered exploits to weaken the firewall
3. **Compromise** the node once firewall reaches 0
4. **Install backdoors** for persistent access
5. **Extract data** and complete contracts for rewards
6. **Manage heat** to avoid law enforcement investigations

### Combat Mechanics

- **Firewall** — Target's defense strength; reduce to 0 to compromise
- **Trace** — Detection progress; reaching 100% triggers countermeasures
- **ICE Level** — Intrusion Countermeasures Electronics difficulty
- **SIEM** — Enhanced monitoring on high-security targets

### Skills

| Skill | Effect |
|-------|--------|
| Scanning | Improves node/vulnerability discovery |
| Exploitation | Increases exploit success rate and damage |
| Stealth | Reduces trace accumulation |
| Cryptanalysis | Better encryption cracking chances |
| Social Engineering | Improves phishing success |
| Reverse Engineering | Increases backdoor installation success |
| Botnet Management | Larger and higher quality botnets |

## 📁 Project Structure

```
hacker-game/
├── hacker_game.py      # Main game file
├── netrunner_save.json # Save file (auto-generated)
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

## 💾 Save System

The game automatically saves:
- On graceful exit via "Disconnect" menu
- On manual save via "Save Game" option
- On Ctrl+C interrupt

Save file location: `netrunner_save.json` (same directory as game)

## 🛠️ Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contribution

- [ ] Add more exploit types and vulnerabilities
- [ ] Implement multiplayer features
- [ ] Create ASCII art UI elements
- [ ] Add sound effects (optional)
- [ ] Build a curses-based TUI interface
- [ ] Add localization support

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This game is purely fictional and intended for entertainment purposes only. The hacking mechanics are simplified simulations and do not represent real-world techniques. Do not attempt any illegal activities.

## 🙏 Acknowledgments

- Inspired by classic cyberpunk literature and games
- Thanks to the Python community for amazing documentation

---

**Stay in the shadows. Trust no one. Happy hacking! 🖥️💀**
