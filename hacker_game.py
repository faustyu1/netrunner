#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NETRUNNER - Advanced Network Intrusion Simulator
Realistic hacking simulation with procedural generation and persistent world
Version 2.0 - Extended Edition
"""

import random
import time
import os
import sys
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from enum import Enum


# ============================================================================
# GAME CONSTANTS - All magic numbers in one place for easy balancing
# ============================================================================
class GameConstants:
    """Central configuration for all game balance values"""
    
    # Player starting values
    STARTING_CREDITS = 1000
    STARTING_LEVEL = 1
    MAX_SKILL_LEVEL = 10
    
    # Experience & Leveling
    EXP_PER_LEVEL_MULTIPLIER = 100  # exp_needed = level * this
    EXP_SCAN_MULTIPLIER = 5         # exp = security_rating * this
    EXP_COMPROMISE_MULTIPLIER = 50  # exp = security_rating * this
    EXP_BACKDOOR_MULTIPLIER = 20    # exp = security_rating * this
    
    # Combat & Exploitation
    BASE_EXPLOIT_SUCCESS_RATE = 0.05   # Minimum success rate
    MAX_EXPLOIT_SUCCESS_RATE = 0.98    # Maximum success rate
    SKILL_SUCCESS_BONUS = 0.05         # Per skill level
    TOOL_SUCCESS_BONUS = 0.1           # Per tool effectiveness
    PATCH_PENALTY = 0.03               # Per patch level
    
    # Trace & Heat
    TRACE_COMPLETE_THRESHOLD = 100
    TRACE_HEAT_INCREASE = 15
    TRACE_IDENTITY_HEAT_INCREASE = 10
    TRACE_PENALTY_MIN = 100
    TRACE_PENALTY_MAX = 500
    INVESTIGATION_START_THRESHOLD = 50  # identity_heat > this
    INVESTIGATION_START_CHANCE = 0.3
    
    # Stealth bonuses
    STEALTH_SKILL_BONUS = 0.05         # Per skill level
    PROXY_CHAIN_BONUS = 0.1            # Per proxy chain
    BOUNCE_NODE_BONUS = 0.12           # Per bounce node
    MAX_STEALTH_REDUCTION = 0.9        # Cap at 90% reduction
    
    # DDoS
    DDOS_TRACE_INCREASE = 25
    DDOS_HEAT_INCREASE = 3
    
    # Botnet
    BOTNET_BUILD_COST = 2000
    BOTNET_BASE_SIZE_MIN = 50
    BOTNET_BASE_SIZE_MAX = 200
    BOTNET_SIZE_PER_SKILL = 20
    BOTNET_BASE_QUALITY = 0.5
    BOTNET_QUALITY_PER_SKILL = 0.05
    
    # Proxy chains
    PROXY_BASE_COST = 1000
    PROXY_COST_INCREMENT = 500
    
    # Social Engineering
    PHISHING_SKILL_BONUS = 0.08
    PHISHING_SUCCESS_TRACE = 5
    PHISHING_FAIL_TRACE = 15
    PHISHING_FAIL_HEAT = 2
    
    # Investigation
    INVESTIGATION_ASSET_LOSS_PERCENT = 0.7
    INVESTIGATION_REP_LOSS = 100
    INVESTIGATION_TOOLS_LOST = 3
    INVESTIGATION_RESET_HEAT = 20
    
    # Money Laundering
    LAUNDER_COST = 2000
    LAUNDER_IDENTITY_REDUCTION = 15
    LAUNDER_INVESTIGATION_REDUCTION = 5
    
    # Rival Hackers
    RIVAL_ACTIVITY_CHANCE = 0.1
    RIVAL_COMPROMISE_CHANCE = 0.05
    RIVAL_HACK_BASE_SUCCESS = 0.3
    
    # Admin Response
    ADMIN_PATCH_CHANCE = 0.05
    ADMIN_ACTIVATE_THRESHOLD = 40      # trace_progress > this
    ADMIN_ACTIVATE_CHANCE = 0.3
    ADMIN_TRACE_MULTIPLIER = 1.3
    
    # Network Generation
    MIN_SERVICES_PER_NODE = 3
    MAX_SERVICES_PER_NODE = 8
    MIN_EMPLOYEES_PER_NODE = 5
    MAX_EMPLOYEES_PER_NODE = 30
    ENCRYPTION_CHANCE = 0.4
    HONEYPOT_SECURITY_THRESHOLD = 5
    
    # Contracts
    INITIAL_CONTRACTS = 5
    MIN_ACTIVE_CONTRACTS = 3
    CONTRACT_DEADLINE_MIN_HOURS = 24
    CONTRACT_DEADLINE_MAX_HOURS = 168
    
    # Events
    MAX_ACTIVE_EVENTS = 2
    EVENT_TRIGGER_CHANCE = 0.05
    
    # UI Delays (seconds)
    DELAY_TYPING = 0.02
    DELAY_SHORT = 0.3
    DELAY_MEDIUM = 1.0
    DELAY_LONG = 2.0


# Terminal colors
class Color:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def log(text: str, color: str = Color.WHITE, delay: float = 0.02):
    """Terminal output with optional typing effect"""
    for char in text:
        sys.stdout.write(color + char + Color.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

class NetworkType(Enum):
    CORPORATE = "corporate"
    GOVERNMENT = "government"
    FINANCIAL = "financial"
    RESEARCH = "research"
    CRIMINAL = "criminal"
    MILITARY = "military"
    INFRASTRUCTURE = "infrastructure"

class ExploitType(Enum):
    SQL_INJECTION = "sql_injection"
    BUFFER_OVERFLOW = "buffer_overflow"
    XSS = "cross_site_scripting"
    RCE = "remote_code_execution"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    ZERO_DAY = "zero_day"
    SOCIAL_ENGINEERING = "social_engineering"
    MAN_IN_MIDDLE = "man_in_the_middle"
    PHISHING = "phishing"
    SUPPLY_CHAIN = "supply_chain"
    CRYPTOGRAPHIC = "cryptographic_weakness"

class ToolType(Enum):
    SCANNER = "scanner"
    EXPLOIT_FRAMEWORK = "exploit_framework"
    PROXY_CHAIN = "proxy_chain"
    CRYPTANALYSIS = "cryptanalysis"
    BOTNET_CONTROLLER = "botnet_controller"
    KEYLOGGER = "keylogger"
    ROOTKIT = "rootkit"

class EncryptionType(Enum):
    AES_128 = "aes_128"
    AES_256 = "aes_256"
    RSA_1024 = "rsa_1024"
    RSA_2048 = "rsa_2048"
    RSA_4096 = "rsa_4096"
    WEAK_HASH = "weak_hash"

class HardwareType(Enum):
    CPU = "processor"
    RAM = "memory"
    STORAGE = "storage"
    COOLING = "cooling"

class EventType(Enum):
    GLOBAL_PATCH = "global_patch"
    POLICE_CRACKDOWN = "police_crackdown"
    ZERO_DAY_LEAK = "zero_day_leak"
    NETWORK_WORM = "network_worm"

@dataclass
class HardwareComponent:
    name: str
    htype: HardwareType
    level: int
    cost: int
    bonus: float
    description: str

@dataclass
class WorldEvent:
    name: str
    etype: EventType
    duration: int  # in game "ticks" or hours
    multiplier: float
    description: str
    target_faction: Optional[str] = None
    target_network: Optional[NetworkType] = None

@dataclass
class Vulnerability:
    name: str
    exploit_type: ExploitType
    severity: float  # 0.0 to 1.0
    patch_level: int
    discovery_difficulty: float
    firewall_damage: Tuple[int, int]
    trace_cost: int
    success_rate_base: float
    requires_tool: Optional[str] = None

@dataclass
class EncryptedData:
    encryption_type: EncryptionType
    data_size: int
    value: int
    difficulty: float
    cracked: bool = False

@dataclass
class Employee:
    name: str
    email: str
    department: str
    access_level: int
    social_media_activity: float  # How much info available online
    phishing_susceptibility: float
    compromised: bool = False

@dataclass
class Service:
    name: str
    version: str
    port: int
    state: str
    vulnerabilities: List[Vulnerability]
    encryption: Optional[EncryptedData] = None
    employees_with_access: List[Employee] = field(default_factory=list)

@dataclass
class Honeypot:
    port: int
    fake_service: str
    detection_chance: float
    trace_increase: int

@dataclass
class Tool:
    name: str
    tool_type: ToolType
    cost: int
    effectiveness: float
    description: str
    level_requirement: int
    stealth_penalty: float = 0.0

@dataclass
class Botnet:
    size: int
    quality: float  # 0.0 to 1.0
    maintenance_cost: int
    ddos_power: int
    detected_nodes: int = 0

@dataclass
class NetworkNode:
    uid: str
    name: str
    ip_address: str
    network_type: NetworkType
    security_rating: int
    firewall_strength: int
    max_firewall: int
    ice_level: int
    services: List[Service]
    discovered_services: Set[int]
    discovered_vulns: Set[str]
    compromised: bool
    data_value: int
    trace_progress: float
    trace_speed: float
    last_attack_time: Optional[datetime]
    connections: List[str]
    honeypots: List[Honeypot] = field(default_factory=list)
    has_siem: bool = False
    has_incident_response: bool = False
    admin_active: bool = False
    admin_skill: int = 1
    backdoor_installed: bool = False
    network_segment: str = "DMZ"  # DMZ, INTERNAL, SECURE
    employees: List[Employee] = field(default_factory=list)
    encrypted_traffic: List[EncryptedData] = field(default_factory=list)

@dataclass
class PlayerSkills:
    scanning: int = 1
    exploitation: int = 1
    stealth: int = 1
    cryptanalysis: int = 1
    social_engineering: int = 1
    reverse_engineering: int = 1
    botnet_management: int = 1

@dataclass
class Faction:
    name: str
    reputation: int
    hostile: bool

@dataclass
class PlayerState:
    handle: str
    level: int
    experience: int
    credits: int
    reputation: int
    heat_level: int
    skills: PlayerSkills
    discovered_nodes: Set[str]
    compromised_nodes: Set[str]
    current_location: str
    inventory: List[Tool]
    active_contracts: List[str]
    completed_contracts: Set[str]
    game_time: datetime
    total_playtime: float
    botnets: List[Botnet] = field(default_factory=list)
    factions: Dict[str, Faction] = field(default_factory=dict)
    identity_heat: int = 0  # Separate from general heat
    known_exploits: Set[str] = field(default_factory=set)
    proxy_chains: int = 0
    safe_houses: List[str] = field(default_factory=list)
    under_investigation: bool = False
    investigation_progress: float = 0.0
    hardware: Dict[str, HardwareComponent] = field(default_factory=dict)
    active_events: List[WorldEvent] = field(default_factory=list)
    bounced_nodes: List[str] = field(default_factory=list)  # Proxy bouncing chain


@dataclass
class Contract:
    uid: str
    title: str
    description: str
    target_node_uid: str
    objective: str
    reward: int
    reputation_change: int
    time_limit: Optional[timedelta]
    difficulty: int
    contractor: str
    faction: Optional[str] = None
    completed: bool = False
    failed: bool = False
    deadline: Optional[datetime] = None

class SaveManager:
    SAVE_FILE = "netrunner_save.json.gz"  # Now using gzip compression
    
    @staticmethod
    def save_game(game_state: 'GameState') -> bool:
        import gzip
        try:
            data = {
                'player': asdict(game_state.player),
                'nodes': [asdict(node) for node in game_state.network.nodes.values()],
                'contracts': [asdict(c) for c in game_state.contracts],
                'rivals': [asdict(r) for r in game_state.rival_hackers],
                'world_seed': game_state.network.seed,
                'game_events': game_state.event_log[-100:],
                'black_market': [asdict(t) for t in game_state.black_market_tools]
            }
            
            def convert(obj):
                if isinstance(obj, set):
                    return list(obj)
                if isinstance(obj, Enum):
                    return obj.value
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, timedelta):
                    return obj.total_seconds()
                if isinstance(obj, (PlayerSkills, Tool, Botnet, Faction)):
                    return asdict(obj)
                return obj
            
            def deep_convert(d):
                if isinstance(d, dict):
                    return {k: deep_convert(v) for k, v in d.items()}
                if isinstance(d, list):
                    return [deep_convert(item) for item in d]
                return convert(d)
            
            serializable_data = deep_convert(data)
            
            # Compress with gzip, no indent (smaller file)
            json_bytes = json.dumps(serializable_data, separators=(',', ':')).encode('utf-8')
            with gzip.open(SaveManager.SAVE_FILE, 'wb') as f:
                f.write(json_bytes)
            
            return True
        except Exception as e:
            print(f"{Color.RED}Save failed: {e}{Color.RESET}")
            return False
    
    @staticmethod
    def load_game() -> Optional[Dict]:
        import gzip
        try:
            # Try new compressed format first
            if os.path.exists(SaveManager.SAVE_FILE):
                with gzip.open(SaveManager.SAVE_FILE, 'rb') as f:
                    return json.loads(f.read().decode('utf-8'))
            
            # Fallback: try old uncompressed format for backwards compatibility
            old_file = "netrunner_save.json"
            if os.path.exists(old_file):
                with open(old_file, 'r') as f:
                    return json.load(f)
            
            return None
        except Exception as e:
            print(f"{Color.RED}Load failed: {e}{Color.RESET}")
            return None

class EmployeeGenerator:
    FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                   "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas"]
    DEPARTMENTS = ["IT", "HR", "Finance", "Operations", "Marketing", "R&D", "Legal", "Executive"]
    
    @staticmethod
    def generate_employees(count: int, company_name: str) -> List[Employee]:
        employees = []
        domain = company_name.lower().replace(" ", "")[:15] + ".com"
        
        for _ in range(count):
            first = random.choice(EmployeeGenerator.FIRST_NAMES)
            last = random.choice(EmployeeGenerator.LAST_NAMES)
            dept = random.choice(EmployeeGenerator.DEPARTMENTS)
            
            employee = Employee(
                name=f"{first} {last}",
                email=f"{first.lower()}.{last.lower()}@{domain}",
                department=dept,
                access_level=random.randint(1, 5),
                social_media_activity=random.uniform(0.3, 0.9),
                phishing_susceptibility=random.uniform(0.2, 0.8)
            )
            employees.append(employee)
        
        return employees

class VulnerabilityDatabase:
    @staticmethod
    def generate_vulnerabilities(service_name: str, version: str, count: int) -> List[Vulnerability]:
        vulns = []
        
        templates = [
            ("SQL Injection in login form", ExploitType.SQL_INJECTION, 0.7, 2, 0.3, (15, 30), 8, 0.65, None),
            ("Buffer overflow in packet handler", ExploitType.BUFFER_OVERFLOW, 0.9, 5, 0.7, (25, 50), 15, 0.45, "exploit_framework"),
            ("Reflected XSS in search", ExploitType.XSS, 0.5, 1, 0.2, (10, 20), 5, 0.75, None),
            ("Remote code execution via deserialization", ExploitType.RCE, 0.95, 7, 0.8, (40, 80), 20, 0.35, "exploit_framework"),
            ("Privilege escalation via SUID binary", ExploitType.PRIVILEGE_ESCALATION, 0.8, 4, 0.6, (20, 40), 12, 0.55, None),
            ("Unpatched zero-day exploit", ExploitType.ZERO_DAY, 1.0, 10, 0.9, (50, 100), 25, 0.25, "exploit_framework"),
            ("Weak credentials susceptible to brute force", ExploitType.SOCIAL_ENGINEERING, 0.6, 1, 0.1, (15, 25), 10, 0.70, None),
            ("SSL stripping vulnerability", ExploitType.MAN_IN_MIDDLE, 0.75, 3, 0.5, (18, 35), 14, 0.50, "proxy_chain"),
            ("Phishing vector via email", ExploitType.PHISHING, 0.65, 2, 0.4, (20, 30), 7, 0.60, None),
            ("Supply chain backdoor", ExploitType.SUPPLY_CHAIN, 0.85, 6, 0.75, (35, 70), 18, 0.40, None),
            ("Weak cryptographic implementation", ExploitType.CRYPTOGRAPHIC, 0.7, 4, 0.6, (25, 45), 13, 0.50, "cryptanalysis"),
        ]
        
        selected = random.sample(templates, min(count, len(templates)))
        
        for name, exploit_type, severity, patch, discovery, damage, trace, success, tool in selected:
            vuln = Vulnerability(
                name=f"{name} ({service_name})",
                exploit_type=exploit_type,
                severity=severity + random.uniform(-0.1, 0.1),
                patch_level=patch + random.randint(-1, 1),
                discovery_difficulty=discovery,
                firewall_damage=damage,
                trace_cost=trace,
                success_rate_base=success,
                requires_tool=tool
            )
            vulns.append(vuln)
        
        return vulns

class ProceduralNetwork:
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.nodes: Dict[str, NetworkNode] = {}
        self.generate_network()
    
    def generate_network(self):
        service_templates = [
            ("Apache HTTP Server", "2.4.41", 80),
            ("nginx", "1.18.0", 80),
            ("OpenSSH", "7.9p1", 22),
            ("MySQL", "5.7.31", 3306),
            ("PostgreSQL", "12.4", 5432),
            ("ProFTPD", "1.3.6", 21),
            ("Microsoft IIS", "10.0", 80),
            ("Tomcat", "9.0.37", 8080),
            ("Redis", "6.0.9", 6379),
            ("MongoDB", "4.4.1", 27017),
            ("Elasticsearch", "7.9.2", 9200),
            ("Exchange Server", "2019", 25),
            ("Active Directory", "2019", 389),
            ("VPN Gateway", "5.6", 1194),
        ]
        
        node_configs = [
            (NetworkType.CORPORATE, random.randint(20, 30), 1, 4),
            (NetworkType.FINANCIAL, random.randint(12, 20), 3, 6),
            (NetworkType.GOVERNMENT, random.randint(10, 18), 4, 7),
            (NetworkType.RESEARCH, random.randint(8, 15), 2, 5),
            (NetworkType.CRIMINAL, random.randint(6, 12), 5, 8),
            (NetworkType.MILITARY, random.randint(4, 8), 6, 10),
            (NetworkType.INFRASTRUCTURE, random.randint(5, 10), 3, 6),
        ]
        
        all_nodes = []
        
        for network_type, count, min_security, max_security in node_configs:
            for i in range(count):
                node = self._create_node(network_type, min_security, max_security, service_templates)
                all_nodes.append(node)
                self.nodes[node.uid] = node
        
        self._establish_connections(all_nodes)
    
    def _create_node(self, network_type: NetworkType, min_sec: int, max_sec: int, service_templates: List) -> NetworkNode:
        uid = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:12]
        
        security = random.randint(min_sec, max_sec)
        ice_level = max(1, security - random.randint(0, 2))
        
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
        
        service_count = random.randint(3, 8)
        services = []
        used_ports = set()
        
        for _ in range(service_count):
            template = random.choice(service_templates)
            sname, sversion, sport = template
            
            if sport in used_ports:
                sport += random.randint(1, 1000)
            used_ports.add(sport)
            
            state = random.choice(["open", "open", "filtered", "closed"])
            
            vuln_count = random.randint(1, 5) if state == "open" else random.randint(0, 2)
            vulns = VulnerabilityDatabase.generate_vulnerabilities(sname, sversion, vuln_count)
            
            # Add encryption to some services
            encryption = None
            if random.random() < 0.4:
                enc_types = list(EncryptionType)
                encryption = EncryptedData(
                    encryption_type=random.choice(enc_types),
                    data_size=random.randint(100, 10000),
                    value=random.randint(500, 5000),
                    difficulty=random.uniform(0.3, 0.9)
                )
            
            service = Service(
                name=sname,
                version=sversion,
                port=sport,
                state=state,
                vulnerabilities=vulns,
                encryption=encryption
            )
            services.append(service)
        
        prefixes = ["TechCorp", "DataSys", "SecureNet", "GlobalTech", "CyberDyne", 
                   "NexGen", "Quantum", "Infinity", "Apex", "Zenith", "Vertex", "Axiom"]
        suffixes = ["Industries", "Systems", "Solutions", "Enterprises", "Group",
                   "Corporation", "Technologies", "Networks", "Services", "Digital"]
        
        if network_type == NetworkType.GOVERNMENT:
            org_name = f"{random.choice(['Federal', 'State', 'National', 'Regional'])} {random.choice(['Bureau', 'Agency', 'Department', 'Office'])}"
        elif network_type == NetworkType.MILITARY:
            org_name = f"{random.choice(['NORTHCOM', 'CYBERCOM', 'STRATCOM', 'Defense', 'SIGINT'])} Node {random.randint(1, 99)}"
        elif network_type == NetworkType.CRIMINAL:
            org_name = f"Dark{random.choice(['Net', 'Web', 'Site', 'Market'])} {random.randint(1, 999)}"
        elif network_type == NetworkType.INFRASTRUCTURE:
            org_name = f"{random.choice(['Power', 'Water', 'Telecom', 'Transit'])} {random.choice(['Grid', 'Network', 'System'])} {random.randint(1, 50)}"
        else:
            org_name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        
        max_firewall = security * random.randint(80, 150)
        data_value = security * random.randint(100, 500)
        trace_speed = 0.5 + (security * 0.3)
        
        # Generate honeypots for higher security nodes
        honeypots = []
        if security >= 5:
            honeypot_count = random.randint(1, 3)
            for _ in range(honeypot_count):
                honeypots.append(Honeypot(
                    port=random.randint(1024, 65535),
                    fake_service=random.choice(["FTP", "Telnet", "SMB", "RDP"]),
                    detection_chance=random.uniform(0.6, 0.9),
                    trace_increase=random.randint(20, 40)
                ))
        
        # Generate employees
        employee_count = random.randint(5, 30)
        employees = EmployeeGenerator.generate_employees(employee_count, org_name)
        
        # Network segmentation
        segments = ["DMZ", "INTERNAL", "SECURE"]
        segment = segments[min(2, security // 4)]
        
        # Generate encrypted traffic
        encrypted_traffic = []
        if random.random() < 0.5:
            traffic_count = random.randint(1, 5)
            for _ in range(traffic_count):
                encrypted_traffic.append(EncryptedData(
                    encryption_type=random.choice(list(EncryptionType)),
                    data_size=random.randint(1000, 50000),
                    value=random.randint(200, 3000),
                    difficulty=random.uniform(0.4, 0.95)
                ))
        
        return NetworkNode(
            uid=uid,
            name=org_name,
            ip_address=ip,
            network_type=network_type,
            security_rating=security,
            firewall_strength=max_firewall,
            max_firewall=max_firewall,
            ice_level=ice_level,
            services=services,
            discovered_services=set(),
            discovered_vulns=set(),
            compromised=False,
            data_value=data_value,
            trace_progress=0.0,
            trace_speed=trace_speed,
            last_attack_time=None,
            connections=[],
            honeypots=honeypots,
            has_siem=security >= 6,
            has_incident_response=security >= 7,
            admin_active=False,
            admin_skill=max(1, security - 3),
            network_segment=segment,
            employees=employees,
            encrypted_traffic=encrypted_traffic
        )
    
    def _establish_connections(self, nodes: List[NetworkNode]):
        by_type = {}
        for node in nodes:
            if node.network_type not in by_type:
                by_type[node.network_type] = []
            by_type[node.network_type].append(node)
        
        for node_list in by_type.values():
            for i, node in enumerate(node_list):
                connection_count = random.randint(2, 5)
                potential = [n for n in node_list if n.uid != node.uid and n.uid not in node.connections]
                connections = random.sample(potential, min(connection_count, len(potential)))
                
                for conn in connections:
                    if conn.uid not in node.connections:
                        node.connections.append(conn.uid)
                    if node.uid not in conn.connections:
                        conn.connections.append(node.uid)
        
        all_types = list(by_type.keys())
        for i in range(len(all_types)):
            for j in range(i + 1, len(all_types)):
                type_a = by_type[all_types[i]]
                type_b = by_type[all_types[j]]
                
                for _ in range(random.randint(2, 4)):
                    node_a = random.choice(type_a)
                    node_b = random.choice(type_b)
                    
                    if node_b.uid not in node_a.connections:
                        node_a.connections.append(node_b.uid)
                    if node_a.uid not in node_b.connections:
                        node_b.connections.append(node_a.uid)

class BlackMarket:
    @staticmethod
    def generate_tools() -> List[Tool]:
        tools = [
            Tool("PortScanner Pro", ToolType.SCANNER, 500, 1.5, "Advanced network scanner with stealth mode", 1, 0.0),
            Tool("MassiveMap", ToolType.SCANNER, 1500, 2.0, "Ultra-fast network mapper", 3, 0.1),
            Tool("ExploitKit v3", ToolType.EXPLOIT_FRAMEWORK, 2000, 1.8, "Automated exploitation framework", 2, 0.2),
            Tool("MetaSploit Pro", ToolType.EXPLOIT_FRAMEWORK, 5000, 2.5, "Professional penetration testing suite", 5, 0.15),
            Tool("ProxyChain Advanced", ToolType.PROXY_CHAIN, 1000, 1.0, "Multi-hop proxy network", 2, -0.3),
            Tool("TOR Router Pro", ToolType.PROXY_CHAIN, 3000, 1.0, "Enhanced anonymity routing", 4, -0.5),
            Tool("CryptoBreaker", ToolType.CRYPTANALYSIS, 4000, 2.0, "Advanced cryptanalysis tool", 4, 0.1),
            Tool("QuantumCrack", ToolType.CRYPTANALYSIS, 10000, 3.0, "Quantum-assisted decryption", 7, 0.2),
            Tool("BotCommander", ToolType.BOTNET_CONTROLLER, 3000, 1.5, "Manage distributed botnets", 3, 0.3),
            Tool("StealthLogger", ToolType.KEYLOGGER, 1500, 1.3, "Undetectable keylogging software", 2, 0.0),
            Tool("DeepRootkit", ToolType.ROOTKIT, 5000, 2.0, "Persistent system-level access", 5, 0.1),
        ]
        return tools
    
    @staticmethod
    def generate_hardware(player_level: int) -> List[HardwareComponent]:
        hardware = []
        bases = [
            ("Core-i7 Hacker Edition", HardwareType.CPU, 2.0, 5000, "High-performance CPU for faster exploit execution"),
            ("Quantum Processor V1", HardwareType.CPU, 4.0, 25000, "Experimental quantum chip"),
            ("32GB DDR5 RAM", HardwareType.RAM, 1.5, 3000, "Increases processing time window in mini-games"),
            ("64GB DDR5 X-Pro", HardwareType.RAM, 2.2, 8000, "Professional grade memory"),
            ("2TB NVMe SSD", HardwareType.STORAGE, 1.5, 4000, "Faster data extraction and storage"),
            ("Liquid Cooling System", HardwareType.COOLING, 1.3, 3500, "Reduces trace accumulation speed"),
            ("Nitro Cooling Rig", HardwareType.COOLING, 2.0, 12000, "Extreme cooling for elite hackers")
        ]
        
        for name, htype, bonus, cost, desc in bases:
            lvl_req = int(cost / 2000)
            if lvl_req <= player_level + 2:
                hardware.append(HardwareComponent(name, htype, lvl_req, cost, bonus, desc))
        return hardware

    @staticmethod
    def generate_exploits(player_level: int) -> List[Dict]:
        exploits = []
        
        exploit_names = [
            "EternalBlue", "BlueKeep", "Heartbleed", "Shellshock", "Dirty COW",
            "KRACK", "Meltdown", "Spectre", "PrintNightmare", "Log4Shell",
            "ProxyLogon", "ProxyShell", "ZeroLogon", "SolarFlare", "Ghost"
        ]
        
        for _ in range(random.randint(3, 7)):
            level_req = random.randint(max(1, player_level - 2), player_level + 3)
            exploits.append({
                "name": random.choice(exploit_names) + f" v{random.randint(1,5)}",
                "type": random.choice(list(ExploitType)).value,
                "cost": level_req * random.randint(500, 2000),
                "effectiveness": 0.6 + (level_req * 0.05),
                "level_req": level_req
            })
        
        return exploits

class DynamicEventManager:
    """Manages world events that affect gameplay"""
    
    @staticmethod
    def generate_event() -> WorldEvent:
        events = [
            ("Global Security Patch", EventType.GLOBAL_PATCH, random.randint(12, 48), 0.7,
             "Major software vendors released critical patches, reducing exploit effectiveness."),
            ("Police Crackdown", EventType.POLICE_CRACKDOWN, random.randint(24, 72), 1.5,
             "Law enforcement is actively hunting hackers. Trace accumulation increased."),
            ("Zero-Day Leak", EventType.ZERO_DAY_LEAK, random.randint(6, 24), 1.3,
             "New vulnerabilities leaked online. Exploitation effectiveness increased."),
            ("Network Worm Outbreak", EventType.NETWORK_WORM, random.randint(12, 36), 0.8,
             "A network worm is causing chaos. Security teams are distracted."),
        ]
        
        name, etype, duration, mult, desc = random.choice(events)
        
        return WorldEvent(
            name=name,
            etype=etype,
            duration=duration,
            multiplier=mult,
            description=desc
        )

@dataclass
class RivalHacker:
    name: str
    skill_level: int
    specialization: str
    active_targets: List[str]
    last_seen: datetime
    hostile: bool = False

class RivalGenerator:
    HACKER_HANDLES = [
        "DarkPhantom", "ZeroCool", "CrashOverride", "AcidBurn", "ThePlague",
        "Cypher", "Neo", "Morpheus", "Trinity", "Ghost", "Reaper", "Viper",
        "Shadow", "Nexus", "Void", "Raven", "Cipher", "Spectre", "Wraith"
    ]
    
    @staticmethod
    def generate_rival(player_level: int) -> RivalHacker:
        skill_variance = random.randint(-2, 3)
        skill = max(1, player_level + skill_variance)
        
        specializations = ["Exploitation", "Social Engineering", "Cryptanalysis", 
                          "Network Infiltration", "Botnet Operations"]
        
        return RivalHacker(
            name=random.choice(RivalGenerator.HACKER_HANDLES),
            skill_level=skill,
            specialization=random.choice(specializations),
            active_targets=[],
            last_seen=datetime.now() - timedelta(hours=random.randint(1, 72))
        )

class ContractGenerator:
    @staticmethod
    def generate_contract(network: ProceduralNetwork, player_level: int, factions: Dict[str, Faction]) -> Contract:
        suitable_nodes = [
            n for n in network.nodes.values()
            if not n.compromised and n.security_rating <= player_level + 3
        ]
        
        if not suitable_nodes:
            suitable_nodes = [n for n in network.nodes.values() if not n.compromised]
        
        if not suitable_nodes:
            return None
        
        target = random.choice(suitable_nodes)
        
        objectives = ["steal_data", "install_backdoor", "sabotage", "reconnaissance", 
                     "destroy_evidence", "plant_evidence", "exfiltrate_employee_data"]
        objective = random.choice(objectives)
        
        contractors = ["Anonymous Client", "Dark Web Broker", "Corporate Rival", 
                      "Intelligence Agency", "Hacktivist Group", "Crime Syndicate",
                      "Whistleblower", "Competitor Corporation", "Foreign Government"]
        
        faction_name = random.choice(list(factions.keys())) if factions and random.random() < 0.3 else None
        
        titles = {
            "steal_data": f"Data Extraction: {target.name}",
            "install_backdoor": f"Persistent Access: {target.name}",
            "sabotage": f"System Disruption: {target.name}",
            "reconnaissance": f"Network Mapping: {target.name}",
            "destroy_evidence": f"Evidence Destruction: {target.name}",
            "plant_evidence": f"Plant incriminating evidence on {target.name} systems to frame them.",
            "exfiltrate_employee_data": f"Steal complete employee database from {target.name} HR systems."
        }
        
        reward_mult = {
            "steal_data": 1.2, 
            "install_backdoor": 1.5, 
            "sabotage": 1.3, 
            "reconnaissance": 0.8,
            "destroy_evidence": 1.6,
            "plant_evidence": 1.7,
            "exfiltrate_employee_data": 1.4
        }
        
        descriptions = {
            "steal_data": f"Extract sensitive data from {target.name} servers. Payment on delivery.",
            "install_backdoor": f"Establish persistent access to {target.name} infrastructure for future operations.",
            "sabotage": f"Disrupt operations at {target.name}. Must appear like system failure.",
            "reconnaissance": f"Map internal network structure of {target.name}. Stealth is priority.",
            "destroy_evidence": f"Permanently delete specific files from {target.name} without detection.",
            "plant_evidence": f"Infiltrate {target.name} systems and plant incriminating evidence to frame the target.",
            "exfiltrate_employee_data": f"Access HR systems of {target.name} and exfiltrate the complete employee database."
        }
        
        uid = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8]
        
        has_deadline = random.random() > 0.4
        deadline = None
        if has_deadline:
            deadline = datetime.now() + timedelta(hours=random.randint(24, 168))
        
        return Contract(
            uid=uid,
            title=titles[objective],
            description=descriptions[objective],
            target_node_uid=target.uid,
            objective=objective,
            reward=int(target.data_value * reward_mult[objective]),
            reputation_change=target.security_rating * 5,
            time_limit=timedelta(hours=random.randint(24, 168)) if has_deadline else None,
            difficulty=target.security_rating,
            contractor=random.choice(contractors),
            faction=faction_name,
            deadline=deadline
        )

class GameState:
    def __init__(self):
        self.player = PlayerState(
            handle="ghost",
            level=GameConstants.STARTING_LEVEL,
            experience=0,
            credits=GameConstants.STARTING_CREDITS,
            reputation=0,
            heat_level=0,
            skills=PlayerSkills(),
            discovered_nodes=set(),
            compromised_nodes=set(),
            current_location="",
            inventory=[],
            active_contracts=[],
            completed_contracts=set(),
            game_time=datetime.now(),
            total_playtime=0.0
        )
        
        # Initialize basic hardware
        self.player.hardware = {
            "CPU": HardwareComponent("Basic Processor", HardwareType.CPU, 1, 0, 1.0, "Standard 4-core CPU"),
            "RAM": HardwareComponent("8GB Memory", HardwareType.RAM, 1, 0, 1.0, "Standard DDR3 RAM"),
            "Storage": HardwareComponent("500GB HDD", HardwareType.STORAGE, 1, 0, 1.0, "Mechanical hard drive"),
            "Cooling": HardwareComponent("Stock Cooler", HardwareType.COOLING, 1, 0, 1.0, "Basic air cooling")
        }
        
        # Initialize factions
        self.player.factions = {
            "White Hat Alliance": Faction("White Hat Alliance", 0, False),
            "Black Hat Syndicate": Faction("Black Hat Syndicate", 0, False),
            "Grey Market Traders": Faction("Grey Market Traders", 0, False),
            "Corporate Security": Faction("Corporate Security", -20, True),
            "Law Enforcement": Faction("Law Enforcement", -50, True),
        }
        
        self.network = ProceduralNetwork()
        self.contracts: List[Contract] = []
        self.event_log: List[str] = []
        self.black_market_tools = BlackMarket.generate_tools()
        self.black_market_exploits = []
        self.rival_hackers: List[RivalHacker] = []
        
        # Generate rivals
        for _ in range(random.randint(3, 7)):
            self.rival_hackers.append(RivalGenerator.generate_rival(self.player.level))
        
        # Start location
        entry_nodes = [n for n in self.network.nodes.values() if n.security_rating <= 2]
        if entry_nodes:
            start_node = random.choice(entry_nodes)
            self.player.current_location = start_node.uid
            self.player.discovered_nodes.add(start_node.uid)
        
        # Generate initial contracts
        for _ in range(GameConstants.INITIAL_CONTRACTS):
            contract = ContractGenerator.generate_contract(self.network, self.player.level, self.player.factions)
            if contract:
                self.contracts.append(contract)
        
        # Refresh black market
        self.black_market_exploits = BlackMarket.generate_exploits(self.player.level)
        self.black_market_hardware = BlackMarket.generate_hardware(self.player.level)
    
    def update_dynamic_events(self):
        """Update active world events"""
        # Progress existing events
        expired = []
        for i, event in enumerate(self.player.active_events):
            event.duration -= 1
            if event.duration <= 0:
                expired.append(i)
        
        for idx in reversed(expired):
            self.log_event(f"EVENT EXPIRED: {self.player.active_events[idx].name}")
            self.player.active_events.pop(idx)
        
        # Chance to trigger new event
        if len(self.player.active_events) < GameConstants.MAX_ACTIVE_EVENTS and random.random() < GameConstants.EVENT_TRIGGER_CHANCE:
            new_event = DynamicEventManager.generate_event()
            self.player.active_events.append(new_event)
            self.log_event(f"NEW WORLD EVENT: {new_event.name} - {new_event.description}")

    @classmethod
    def load_from_dict(cls, data: Dict) -> 'GameState':
        """Reconstructs the entire game state from a dictionary"""
        state = cls.__new__(cls)
        
        # Restore world seed and basic structures
        world_seed = data.get('world_seed', random.randint(0, 999999))
        state.network = ProceduralNetwork.__new__(ProceduralNetwork)
        state.network.seed = world_seed
        state.network.nodes = {}
        
        # Reconstruct network nodes
        for n_data in data['nodes']:
            # Convert simple lists back to sets and handle Enums
            n_data['network_type'] = NetworkType(n_data['network_type'])
            n_data['discovered_services'] = set(n_data['discovered_services'])
            n_data['discovered_vulns'] = set(n_data['discovered_vulns'])
            if n_data.get('last_attack_time'):
                n_data['last_attack_time'] = datetime.fromisoformat(n_data['last_attack_time'])
            
            # Reconstruct Services and their vulnerabilities
            services = []
            for s_data in n_data['services']:
                vulns = []
                for v_data in s_data['vulnerabilities']:
                    v_data['exploit_type'] = ExploitType(v_data['exploit_type'])
                    vulns.append(Vulnerability(**v_data))
                s_data['vulnerabilities'] = vulns
                
                if s_data.get('encryption'):
                    e_data = s_data['encryption']
                    e_data['encryption_type'] = EncryptionType(e_data['encryption_type'])
                    s_data['encryption'] = EncryptedData(**e_data)
                
                s_data['employees_with_access'] = [Employee(**e) for e in s_data.get('employees_with_access', [])]
                services.append(Service(**s_data))
            n_data['services'] = services
            
            n_data['honeypots'] = [Honeypot(**h) for h in n_data.get('honeypots', [])]
            n_data['employees'] = [Employee(**e) for e in n_data.get('employees', [])]
            
            traffic = []
            for t_data in n_data.get('encrypted_traffic', []):
                t_data['encryption_type'] = EncryptionType(t_data['encryption_type'])
                traffic.append(EncryptedData(**t_data))
            n_data['encrypted_traffic'] = traffic
            
            node = NetworkNode(**n_data)
            state.network.nodes[node.uid] = node
            
        # Reconstruct Player State
        p_data = data['player']
        p_data['skills'] = PlayerSkills(**p_data['skills'])
        p_data['discovered_nodes'] = set(p_data['discovered_nodes'])
        p_data['compromised_nodes'] = set(p_data['compromised_nodes'])
        p_data['completed_contracts'] = set(p_data['completed_contracts'])
        p_data['known_exploits'] = set(p_data['known_exploits'])
        p_data['game_time'] = datetime.fromisoformat(p_data['game_time'])
        
        p_data['botnets'] = [Botnet(**b) for b in p_data.get('botnets', [])]
        
        factions = {}
        for name, f_data in p_data.get('factions', {}).items():
            factions[name] = Faction(**f_data)
        p_data['factions'] = factions
        
        inventory = []
        for t_data in p_data.get('inventory', []):
            t_data['tool_type'] = ToolType(t_data['tool_type'])
            inventory.append(Tool(**t_data))
        p_data['inventory'] = inventory
        
        # Hardware
        hardware = {}
        for key, h_data in p_data.get('hardware', {}).items():
            h_data['htype'] = HardwareType(h_data['htype'])
            hardware[key] = HardwareComponent(**h_data)
        p_data['hardware'] = hardware
        
        # Events
        events = []
        for e_data in p_data.get('active_events', []):
            e_data['etype'] = EventType(e_data['etype'])
            events.append(WorldEvent(**e_data))
        p_data['active_events'] = events
        
        state.player = PlayerState(**p_data)
        
        # Reconstruct Contracts
        state.contracts = []
        for c_data in data.get('contracts', []):
            if c_data.get('deadline'):
                c_data['deadline'] = datetime.fromisoformat(c_data['deadline'])
            if c_data.get('time_limit') is not None:
                c_data['time_limit'] = timedelta(seconds=c_data['time_limit'])
            state.contracts.append(Contract(**c_data))
            
        # Reconstruct Rivals
        state.rival_hackers = []
        for r_data in data.get('rivals', []):
            r_data['last_seen'] = datetime.fromisoformat(r_data['last_seen'])
            state.rival_hackers.append(RivalHacker(**r_data))
            
        state.event_log = data.get('game_events', [])
        
        # Market tools
        market_tools = []
        for t_data in data.get('black_market', []):
            t_data['tool_type'] = ToolType(t_data['tool_type'])
            market_tools.append(Tool(**t_data))
        state.black_market_tools = market_tools
        state.black_market_exploits = BlackMarket.generate_exploits(state.player.level)
        state.black_market_hardware = BlackMarket.generate_hardware(state.player.level)
        
        return state
    
    def log_event(self, message: str):
        timestamp = self.player.game_time.strftime("%Y-%m-%d %H:%M:%S")
        self.event_log.append(f"[{timestamp}] {message}")
    
    def update_rival_activity(self):
        """Rivals compete for targets"""
        for rival in self.rival_hackers:
            if random.random() < GameConstants.RIVAL_ACTIVITY_CHANCE:
                available_nodes = [n for n in self.network.nodes.values() 
                                 if not n.compromised and n.security_rating <= rival.skill_level + 2]
                if available_nodes:
                    target = random.choice(available_nodes)
                    rival.active_targets.append(target.uid)
                    rival.last_seen = datetime.now()
                    
                    # Rival might compromise node
                    if random.random() < GameConstants.RIVAL_COMPROMISE_CHANCE:
                        target.compromised = True
                        self.log_event(f"Rival {rival.name} compromised {target.name}")
    
    def update_admin_response(self):
        """Admins patch vulnerabilities and respond to intrusions"""
        for node in self.network.nodes.values():
            if node.admin_active and not node.compromised:
                # Admin patches vulnerabilities
                for service in node.services:
                    for vuln in service.vulnerabilities:
                        if random.random() < GameConstants.ADMIN_PATCH_CHANCE:
                            vuln.patch_level += 1
                            self.log_event(f"Admin patched vulnerability at {node.name}")
                
                # Admin might detect ongoing attacks
                if node.trace_progress > 30 and random.random() < GameConstants.ADMIN_ACTIVATE_CHANCE:
                    node.trace_speed *= 1.5
                    self.log_event(f"Incident response activated at {node.name}"))

class GameInterface:
    def __init__(self, state: GameState):
        self.state = state
    
    def show_header(self):
        print(f"\n{Color.CYAN}{'='*70}{Color.RESET}")
        player_tools = len(self.state.player.inventory)
        botnets = len(self.state.player.botnets)
        print(f"{Color.BOLD}NETRUNNER{Color.RESET} | {self.state.player.handle} | "
              f"L{self.state.player.level} | {self.state.player.credits}BTC | "
              f"Tools:{player_tools} | Botnets:{botnets}")
        
        heat_color = Color.RED if self.state.player.heat_level > 70 else Color.YELLOW if self.state.player.heat_level > 40 else Color.GREEN
        print(f"Rep: {self.state.player.reputation} | "
              f"Heat: {heat_color}{self.state.player.heat_level}%{Color.RESET} | "
              f"Investigation: {int(self.state.player.investigation_progress)}%")
              
        if self.state.player.active_events:
            print(f"{Color.YELLOW}ACTV EVENTS:{Color.RESET} " + " | ".join([e.name for e in self.state.player.active_events]))

        print(f"{Color.CYAN}{'='*70}{Color.RESET}\n")
    
    def main_menu(self):
        while True:
            clear()
            self.show_header()
            
            current_node = self.state.network.nodes.get(self.state.player.current_location)
            if current_node:
                status = f"{Color.GREEN}COMPROMISED{Color.RESET}" if current_node.compromised else f"{Color.RED}SECURE{Color.RESET}"
                backdoor = f" {Color.MAGENTA}[BACKDOOR]{Color.RESET}" if current_node.backdoor_installed else ""
                print(f"Location: {current_node.name} ({current_node.ip_address}) [{status}]{backdoor}")
                print(f"Segment: {current_node.network_segment} | Security: {current_node.security_rating}/10\n")
            
            # Update game state
            self.state.update_rival_activity()
            self.state.update_admin_response()
            self.state.update_dynamic_events()
            
            # Check investigations
            if self.state.player.under_investigation:
                self.state.player.investigation_progress += random.uniform(0.1, 0.5)
                if self.state.player.investigation_progress >= GameConstants.TRACE_COMPLETE_THRESHOLD:
                    self.handle_investigation_complete()
            
            print("1. Network Operations")
            print("2. Contract Board")
            print("3. Black Market")
            print("4. Social Engineering")
            print("5. Cryptanalysis Lab")
            print("6. Botnet Management")
            print("7. Intelligence")
            print("8. Character & Skills")
            print("9. System Status")
            print("10. Save Game")
            print("11. Disconnect")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "1":
                self.network_menu()
            elif choice == "2":
                self.contract_menu()
            elif choice == "3":
                self.black_market_menu()
            elif choice == "4":
                self.social_engineering_menu()
            elif choice == "5":
                self.cryptanalysis_menu()
            elif choice == "6":
                self.botnet_menu()
            elif choice == "7":
                self.intelligence_menu()
            elif choice == "8":
                self.character_menu()
            elif choice == "9":
                self.system_status()
            elif choice == "10":
                if SaveManager.save_game(self.state):
                    print(f"{Color.GREEN}Game saved successfully{Color.RESET}")
                time.sleep(1)
            elif choice == "11":
                print(f"\n{Color.YELLOW}Disconnecting...{Color.RESET}")
                time.sleep(0.5)
                break
    
    def handle_investigation_complete(self):
        clear()
        print(f"\n{Color.RED}{'='*70}{Color.RESET}")
        print(f"{Color.RED}{Color.BOLD}INVESTIGATION COMPLETE - IDENTITY COMPROMISED{Color.RESET}")
        print(f"{Color.RED}{'='*70}{Color.RESET}\n")
        
        print("Law enforcement has identified your location.")
        print("Your assets are being seized...")
        
        # Heavy penalties
        asset_loss = int(self.state.player.credits * GameConstants.INVESTIGATION_ASSET_LOSS_PERCENT)
        self.state.player.credits = max(100, self.state.player.credits - asset_loss)
        self.state.player.reputation = max(0, self.state.player.reputation - GameConstants.INVESTIGATION_REP_LOSS)
        
        # Lose some tools
        if self.state.player.inventory:
            lost_tools = random.sample(self.state.player.inventory, 
                                      min(len(self.state.player.inventory), GameConstants.INVESTIGATION_TOOLS_LOST))
            for tool in lost_tools:
                self.state.player.inventory.remove(tool)
        
        # Lose botnets
        self.state.player.botnets = []
        
        print(f"\nAssets seized: {asset_loss}BTC")
        print(f"Reputation lost: 100")
        print(f"Tools confiscated: {len(lost_tools) if self.state.player.inventory else 0}")
        print(f"All botnets destroyed")
        
        # Reset investigation
        self.state.player.under_investigation = False
        self.state.player.investigation_progress = 0
        self.state.player.heat_level = GameConstants.INVESTIGATION_RESET_HEAT
        
        self.state.log_event("IDENTITY COMPROMISED - Major assets lost")
        
        print(f"\n{Color.YELLOW}You must rebuild from scratch...{Color.RESET}")
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def network_menu(self):
        while True:
            clear()
            self.show_header()
            
            current_node = self.state.network.nodes[self.state.player.current_location]
            print(f"Location: {current_node.name}\n")
            
            print("1. Scan current node")
            print("2. Attack current node")
            print("3. Install backdoor")
            print("4. Navigate to connected node")
            print("5. Discover new nodes")
            print("6. Connection Bouncing (Stealth)")
            print("7. Clear traces")
            print("8. Back")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "1":
                self.scan_node(current_node)
            elif choice == "2":
                self.attack_node(current_node)
            elif choice == "3":
                self.install_backdoor(current_node)
            elif choice == "4":
                self.navigate_network()
            elif choice == "5":
                self.discover_nodes()
            elif choice == "6":
                self.navigate_bounces()
            elif choice == "7":
                self.clear_traces_menu(current_node)
            elif choice == "8":
                break
    
    def scan_node(self, node: NetworkNode):
        clear()
        
        # Check for scanner tools
        scanner_bonus = 0.0
        for tool in self.state.player.inventory:
            if tool.tool_type == ToolType.SCANNER:
                scanner_bonus += tool.effectiveness
        
        print(f"\n{Color.YELLOW}Initiating port scan on {node.ip_address}...{Color.RESET}\n")
        time.sleep(0.5)
        
        discovery_chance = 0.3 + (self.state.player.skills.scanning * 0.1) + (scanner_bonus * 0.1)
        
        # Check for honeypots
        for honeypot in node.honeypots:
            if random.random() < honeypot.detection_chance * (1.0 - self.state.player.skills.stealth * 0.05):
                print(f"{Color.RED}[WARNING] Honeypot detected on port {honeypot.port}!{Color.RESET}")
                print(f"{Color.RED}Trace increased significantly!{Color.RESET}")
                node.trace_progress += honeypot.trace_increase
                self.state.player.heat_level += 5
                time.sleep(1)
        
        for i, service in enumerate(node.services):
            if random.random() < discovery_chance or i in node.discovered_services:
                node.discovered_services.add(i)
                print(f"Port {service.port}/tcp  {service.state.upper():<10} {service.name} {service.version}")
                
                # Show encryption if present
                if service.encryption:
                    enc_type = service.encryption.encryption_type.value
                    print(f"  [ENC] {enc_type} encryption detected")
                
                # Discover vulnerabilities
                if service.vulnerabilities and random.random() < discovery_chance * 0.7:
                    for vuln in service.vulnerabilities:
                        vuln_id = f"{node.uid}_{i}_{vuln.name}"
                        if vuln_id not in node.discovered_vulns:
                            if random.random() < (1.0 - vuln.discovery_difficulty + self.state.player.skills.scanning * 0.05):
                                node.discovered_vulns.add(vuln_id)
                                severity_color = Color.RED if vuln.severity > 0.8 else Color.YELLOW
                                print(f"  [{severity_color}!{Color.RESET}] {vuln.name}")
                                if vuln.requires_tool:
                                    print(f"      Requires: {vuln.requires_tool}")
        
        # Show employees with access
        if node.employees and random.random() < discovery_chance:
            print(f"\n{Color.CYAN}Employees with system access:{Color.RESET}")
            sample_employees = random.sample(node.employees, min(3, len(node.employees)))
            for emp in sample_employees:
                print(f"  {emp.name} ({emp.email}) - {emp.department}")
        
        self.state.player.experience += 5 * node.security_rating
        self.check_level_up()
        
        input(f"\n{Color.DIM}Press Enter to continue...{Color.RESET}")
    
    def attack_node(self, node: NetworkNode):
        if node.compromised and not node.backdoor_installed:
            print(f"\n{Color.YELLOW}Node already compromised. Install backdoor for persistent access.{Color.RESET}")
            time.sleep(1)
            return
        
        while node.firewall_strength > 0 and node.trace_progress < 100:
            clear()
            self.show_header()
            
            print(f"Target: {node.name} | Segment: {node.network_segment}")
            fw_bar = '█' * int(node.firewall_strength / node.max_firewall * 30)
            trace_bar = '█' * int(node.trace_progress / 100 * 30)
            print(f"Firewall: {Color.RED}{fw_bar:<30}{Color.RESET} {node.firewall_strength}/{node.max_firewall}")
            print(f"Trace: {Color.YELLOW}{trace_bar:<30}{Color.RESET} {int(node.trace_progress)}%")
            print(f"ICE Level: {node.ice_level}")
            
            if node.has_siem:
                print(f"{Color.RED}[SIEM ACTIVE] - Enhanced monitoring{Color.RESET}")
            if node.admin_active:
                print(f"{Color.YELLOW}[ADMIN ONLINE] - Active defense{Color.RESET}")
            
            print()
            
            # Available exploits
            if node.discovered_vulns:
                print("Available exploits:")
                vulns_list = []
                for i, service in enumerate(node.services):
                    if i in node.discovered_services:
                        for vuln in service.vulnerabilities:
                            vuln_id = f"{node.uid}_{i}_{vuln.name}"
                            if vuln_id in node.discovered_vulns:
                                vulns_list.append((service, vuln))
                
                for idx, (service, vuln) in enumerate(vulns_list, 1):
                    success_rate = self.calculate_success_rate(vuln)
                    tool_status = ""
                    if vuln.requires_tool:
                        has_tool = any(t.tool_type.value == vuln.requires_tool for t in self.state.player.inventory)
                        tool_status = f" {Color.GREEN}[TOOL OK]{Color.RESET}" if has_tool else f" {Color.RED}[NEED: {vuln.requires_tool}]{Color.RESET}"
                    print(f"{idx}. {vuln.name} ({int(success_rate*100)}%){tool_status}")
                
                print(f"\n{len(vulns_list) + 1}. Use botnet for DDoS")
                print(f"{len(vulns_list) + 2}. Clear traces")
                print(f"{len(vulns_list) + 3}. Abort attack")
                
                choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
                
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(vulns_list):
                        service, vuln = vulns_list[choice_num - 1]
                        
                        # Check tool requirement
                        if vuln.requires_tool:
                            has_tool = any(t.tool_type.value == vuln.requires_tool for t in self.state.player.inventory)
                            if not has_tool:
                                print(f"{Color.RED}Missing required tool: {vuln.requires_tool}{Color.RESET}")
                                time.sleep(1)
                                continue
                        
                        self.execute_exploit(node, vuln)
                    elif choice_num == len(vulns_list) + 1:
                        self.use_botnet_ddos(node)
                    elif choice_num == len(vulns_list) + 2:
                        self.clear_traces(node)
                    elif choice_num == len(vulns_list) + 3:
                        break
                except ValueError:
                    pass
            else:
                print(f"{Color.YELLOW}No exploits available. Run a scan first.{Color.RESET}")
                input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
                break
            
            # Calculate trace increase
            trace_increase = node.trace_speed
            
            # Hardware & Event multipliers
            trace_increase /= self.state.player.hardware["Cooling"].bonus
            
            for event in self.state.player.active_events:
                if event.etype == EventType.POLICE_CRACKDOWN:
                    trace_increase *= event.multiplier
                elif event.etype == EventType.NETWORK_WORM:
                    trace_increase *= event.multiplier

            # SIEM multiplier
            if node.has_siem:
                trace_increase *= 1.5
            
            # Stealth reduction
            stealth_bonus = self.state.player.skills.stealth * GameConstants.STEALTH_SKILL_BONUS
            
            # Proxy chain bonus
            if self.state.player.proxy_chains > 0:
                stealth_bonus += self.state.player.proxy_chains * GameConstants.PROXY_CHAIN_BONUS
                
            # Bounce bonus
            if self.state.player.bounced_nodes:
                stealth_bonus += len(self.state.player.bounced_nodes) * GameConstants.BOUNCE_NODE_BONUS
            
            trace_increase *= (1.0 - min(GameConstants.MAX_STEALTH_REDUCTION, stealth_bonus))
            
            node.trace_progress += trace_increase
            
            # Admin might activate
            if not node.admin_active and node.trace_progress > GameConstants.ADMIN_ACTIVATE_THRESHOLD and random.random() < GameConstants.ADMIN_ACTIVATE_CHANCE:
                node.admin_active = True
                node.trace_speed *= GameConstants.ADMIN_TRACE_MULTIPLIER
                print(f"\n{Color.RED}[ALERT] System administrator has been notified!{Color.RESET}")
                time.sleep(1)
            
            if node.trace_progress >= GameConstants.TRACE_COMPLETE_THRESHOLD:
                self.handle_trace_complete(node)
                break
        
        if node.firewall_strength <= 0:
            self.compromise_node(node)
    
    def calculate_success_rate(self, vuln: Vulnerability) -> float:
        base = vuln.success_rate_base
        skill_bonus = self.state.player.skills.exploitation * GameConstants.SKILL_SUCCESS_BONUS
        patch_penalty = vuln.patch_level * GameConstants.PATCH_PENALTY
        
        # Tool bonuses
        tool_bonus = 0.0
        for tool in self.state.player.inventory:
            if tool.tool_type == ToolType.EXPLOIT_FRAMEWORK:
                tool_bonus += tool.effectiveness * GameConstants.TOOL_SUCCESS_BONUS
        
        # Hardware bonuses
        cpu_bonus = (self.state.player.hardware["CPU"].bonus - 1.0) * 0.2
        ram_bonus = (self.state.player.hardware["RAM"].bonus - 1.0) * 0.1
        
        # Event multipliers
        event_mult = 1.0
        for event in self.state.player.active_events:
            if event.etype == EventType.GLOBAL_PATCH:
                event_mult *= event.multiplier
            elif event.etype == EventType.ZERO_DAY_LEAK:
                event_mult *= event.multiplier

        return max(GameConstants.BASE_EXPLOIT_SUCCESS_RATE, min(GameConstants.MAX_EXPLOIT_SUCCESS_RATE, (base + skill_bonus + tool_bonus + cpu_bonus + ram_bonus) * event_mult - patch_penalty))
    
    def execute_exploit(self, node: NetworkNode, vuln: Vulnerability):
        print(f"\n{Color.YELLOW}Executing {vuln.exploit_type.value}...{Color.RESET}")
        time.sleep(1)
        
        success_rate = self.calculate_success_rate(vuln)
        
        if random.random() < success_rate:
            # Mini-game challenge for critical vulnerabilities
            if vuln.severity > 0.7:
                if not self.run_hacking_minigame(vuln.discovery_difficulty):
                    print(f"{Color.RED}Security bypass failed!{Color.RESET}")
                    node.trace_progress += 10
                    time.sleep(1)
                    return

            damage = random.randint(*vuln.firewall_damage)
            
            # Apply skill multiplier
            damage = int(damage * (1 + self.state.player.skills.exploitation * 0.1))
            
            # Apply CPU damage bonus
            damage = int(damage * self.state.player.hardware["CPU"].bonus)
            
            node.firewall_strength -= damage
            print(f"{Color.GREEN}Success! Firewall damage: -{damage}{Color.RESET}")
            self.state.player.experience += int(10 * vuln.severity)
            self.check_level_up()
        else:
            print(f"{Color.RED}Exploit failed{Color.RESET}")
            node.trace_progress += vuln.trace_cost
            
            # Admin might patch this vulnerability
            if node.admin_active and random.random() < 0.2:
                vuln.patch_level += 1
                print(f"{Color.YELLOW}Admin patched the vulnerability!{Color.RESET}")
        
        time.sleep(1)
    
    def use_botnet_ddos(self, node: NetworkNode):
        if not self.state.player.botnets:
            print(f"\n{Color.RED}No botnets available{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.CYAN}Available botnets:{Color.RESET}")
        for i, botnet in enumerate(self.state.player.botnets, 1):
            print(f"{i}. Size: {botnet.size} nodes | Power: {botnet.ddos_power} | Quality: {botnet.quality:.2f}")
        
        choice = input(f"\n{Color.CYAN}Select botnet (0 to cancel)>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.player.botnets):
                botnet = self.state.player.botnets[idx]
                
                print(f"\n{Color.YELLOW}Launching DDoS attack...{Color.RESET}")
                time.sleep(1.5)
                
                damage = int(botnet.ddos_power * botnet.quality)
                node.firewall_strength -= damage
                
                # DDoS is very noisy
                node.trace_progress += GameConstants.DDOS_TRACE_INCREASE
                self.state.player.heat_level += GameConstants.DDOS_HEAT_INCREASE
                
                print(f"{Color.GREEN}DDoS successful! Damage: -{damage}{Color.RESET}")
                print(f"{Color.YELLOW}Warning: High trace increase from DDoS{Color.RESET}")
                
                self.state.player.experience += 15
                self.check_level_up()
                
                time.sleep(2)
        except ValueError:
            pass
    
    def clear_traces(self, node: NetworkNode):
        print(f"\n{Color.YELLOW}Clearing system logs...{Color.RESET}")
        time.sleep(1)
        
        effectiveness = 15 + self.state.player.skills.stealth * 5
        
        # Tool bonuses
        for tool in self.state.player.inventory:
            if tool.tool_type == ToolType.ROOTKIT:
                effectiveness += tool.effectiveness * 10
        
        node.trace_progress = max(0, node.trace_progress - effectiveness)
        
        print(f"{Color.GREEN}Trace reduced by {int(effectiveness)}%{Color.RESET}")
        time.sleep(1)
    
    def clear_traces_menu(self, node: NetworkNode):
        """Dedicated menu for trace clearing"""
        self.clear_traces(node)
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def run_hacking_minigame(self, difficulty: float) -> bool:
        """Simple text-based mini-game for hacking"""
        print(f"\n{Color.CYAN}--- BYPASSING SECURITY LAYER ---{Color.RESET}")
        
        # Simple math challenge
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        op = random.choice(['+', '-'])
        result = a + b if op == '+' else a - b
        
        print(f"Solve to bypass ICE: {a} {op} {b} = ?")
        
        start_time = time.time()
        # Adjusted by RAM level (better memory helps processing)
        timeout = (10.0 - (difficulty * 5)) * self.state.player.hardware["RAM"].bonus
        
        try:
            user_input = input(f"{Color.YELLOW}Enter bypass code (timeout: {timeout:.1f}s)>{Color.RESET} ").strip()
            
            end_time = time.time()
            if end_time - start_time > timeout:
                print(f"\n{Color.RED}TIMEOUT - Bypass failed{Color.RESET}")
                return False
                
            if user_input == str(result):
                print(f"{Color.GREEN}ACCESS GRANTED{Color.RESET}")
                return True
            else:
                print(f"{Color.RED}INCORRECT CODE{Color.RESET}")
                return False
        except:
            return False

    def navigate_bounces(self):
        """Set up connection bouncing through compromised nodes for stealth"""
        clear()
        self.show_header()
        
        print(f"{Color.CYAN}Connection Bouncing (Stealth Mode){Color.RESET}\n")
        print(f"Current bounce chain: {len(self.state.player.bounced_nodes)} nodes")
        print(f"Stealth bonus: -{len(self.state.player.bounced_nodes) * 12}% trace accumulation\n")
        
        compromised = [self.state.network.nodes[uid] for uid in self.state.player.compromised_nodes
                      if uid not in self.state.player.bounced_nodes]
        
        if not compromised:
            print(f"{Color.YELLOW}No available nodes for bouncing.{Color.RESET}")
            print(f"Compromise more nodes to use them as bounce points.")
            input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
            return
        
        print("Available nodes for bouncing:")
        for i, node in enumerate(compromised[:10], 1):
            print(f"{i}. {node.name} ({node.ip_address}) - Security: {node.security_rating}/10")
        
        print(f"\n{len(compromised[:10]) + 1}. Clear bounce chain")
        print(f"0. Back")
        
        choice = input(f"\n{Color.CYAN}Add to bounce chain>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if idx == len(compromised[:10]):
                self.state.player.bounced_nodes = []
                print(f"\n{Color.GREEN}Bounce chain cleared{Color.RESET}")
                time.sleep(1)
            elif 0 <= idx < len(compromised[:10]):
                node = compromised[idx]
                self.state.player.bounced_nodes.append(node.uid)
                print(f"\n{Color.GREEN}Added {node.name} to bounce chain{Color.RESET}")
                print(f"New stealth bonus: -{len(self.state.player.bounced_nodes) * 12}% trace")
                time.sleep(1)
        except ValueError:
            pass
    
    def install_backdoor(self, node: NetworkNode):
        if not node.compromised:
            print(f"\n{Color.RED}Node must be compromised first{Color.RESET}")
            time.sleep(1)
            return
        
        if node.backdoor_installed:
            print(f"\n{Color.YELLOW}Backdoor already installed{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.YELLOW}Installing persistent backdoor...{Color.RESET}")
        time.sleep(2)
        
        success_chance = 0.7 + (self.state.player.skills.reverse_engineering * 0.05)
        
        # Rootkit helps
        for tool in self.state.player.inventory:
            if tool.tool_type == ToolType.ROOTKIT:
                success_chance += tool.effectiveness * 0.1
        
        if random.random() < success_chance:
            node.backdoor_installed = True
            print(f"{Color.GREEN}Backdoor installed successfully{Color.RESET}")
            print(f"You can now access this node anytime without detection")
            self.state.player.experience += node.security_rating * 20
            self.check_level_up()
        else:
            print(f"{Color.RED}Backdoor installation failed{Color.RESET}")
            node.trace_progress += 20
        
        time.sleep(2)
    
    def handle_trace_complete(self, node: NetworkNode):
        print(f"\n{Color.RED}{'='*70}{Color.RESET}")
        print(f"{Color.RED}{Color.BOLD}TRACE COMPLETE - LOCATION COMPROMISED{Color.RESET}")
        print(f"{Color.RED}{'='*70}{Color.RESET}\n")
        
        self.state.player.heat_level += GameConstants.TRACE_HEAT_INCREASE
        self.state.player.identity_heat += GameConstants.TRACE_IDENTITY_HEAT_INCREASE
        penalty = random.randint(GameConstants.TRACE_PENALTY_MIN, GameConstants.TRACE_PENALTY_MAX)
        self.state.player.credits = max(0, self.state.player.credits - penalty)
        
        print(f"Heat level increased to {self.state.player.heat_level}%")
        print(f"Identity heat: {self.state.player.identity_heat}%")
        print(f"Credits lost: {penalty}BTC")
        
        # Chance of investigation
        if self.state.player.identity_heat > GameConstants.INVESTIGATION_START_THRESHOLD and not self.state.player.under_investigation:
            if random.random() < GameConstants.INVESTIGATION_START_CHANCE:
                self.state.player.under_investigation = True
                print(f"\n{Color.RED}[CRITICAL] Law enforcement investigation initiated!{Color.RESET}")
        
        self.state.log_event(f"TRACED at {node.name}")
        
        time.sleep(3)
    
    def compromise_node(self, node: NetworkNode):
        node.compromised = True
        self.state.player.compromised_nodes.add(node.uid)
        
        print(f"\n{Color.GREEN}{'='*70}{Color.RESET}")
        print(f"{Color.GREEN}{Color.BOLD}NODE COMPROMISED{Color.RESET}")
        print(f"{Color.GREEN}{'='*70}{Color.RESET}\n")
        
        print(f"Target: {node.name}")
        extracted_value = int(node.data_value * self.state.player.hardware["Storage"].bonus)
        print(f"Data extracted: {extracted_value}BTC worth")
        print(f"Experience gained: {node.security_rating * 50}XP")
        print(f"Reputation: +{node.security_rating * 10}")
        
        self.state.player.credits += extracted_value
        self.state.player.experience += node.security_rating * 50
        self.state.player.reputation += node.security_rating * 10
        
        # Discover connected nodes
        for conn_uid in node.connections:
            self.state.player.discovered_nodes.add(conn_uid)
        
        # Check for encrypted data
        if node.encrypted_traffic:
            print(f"\n{Color.CYAN}Found {len(node.encrypted_traffic)} encrypted data packages{Color.RESET}")
        
        # Check contract completion
        for contract in self.state.contracts:
            if contract.target_node_uid == node.uid and not contract.completed:
                if contract.objective in ["steal_data", "install_backdoor", "sabotage"]:
                    contract.completed = True
                    self.state.player.credits += contract.reward
                    self.state.player.reputation += contract.reputation_change
                    print(f"\n{Color.MAGENTA}Contract completed! Bonus: {contract.reward}BTC{Color.RESET}")
        
        self.state.log_event(f"Compromised {node.name}")
        self.check_level_up()
        
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def navigate_network(self):
        current_node = self.state.network.nodes[self.state.player.current_location]
        
        if not current_node.connections:
            print(f"\n{Color.YELLOW}No network connections available{Color.RESET}")
            time.sleep(1)
            return
        
        clear()
        print(f"\n{Color.CYAN}Connected nodes:{Color.RESET}\n")
        
        available = []
        for conn_uid in current_node.connections:
            if conn_uid in self.state.player.discovered_nodes:
                conn_node = self.state.network.nodes[conn_uid]
                available.append(conn_node)
        
        if not available:
            print(f"{Color.YELLOW}No discovered connections. Compromise this node first.{Color.RESET}")
            time.sleep(1)
            return
        
        for i, conn_node in enumerate(available, 1):
            status = f"{Color.GREEN}[COMP]{Color.RESET}" if conn_node.compromised else f"{Color.RED}[SEC]{Color.RESET}"
            backdoor = f" {Color.MAGENTA}[BD]{Color.RESET}" if conn_node.backdoor_installed else ""
            print(f"{i}. {status}{backdoor} {conn_node.name} - Sec:{conn_node.security_rating}/10 - {conn_node.network_segment}")
        
        print(f"\n0. Cancel")
        
        choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                self.state.player.current_location = available[idx].uid
                print(f"\n{Color.GREEN}Connected to {available[idx].name}{Color.RESET}")
                time.sleep(1)
        except ValueError:
            pass
    
    def discover_nodes(self):
        print(f"\n{Color.YELLOW}Scanning network topology...{Color.RESET}")
        time.sleep(1)
        
        current_node = self.state.network.nodes[self.state.player.current_location]
        
        discovered = 0
        for conn_uid in current_node.connections:
            if conn_uid not in self.state.player.discovered_nodes:
                if random.random() < 0.5 + self.state.player.skills.scanning * 0.1:
                    self.state.player.discovered_nodes.add(conn_uid)
                    conn_node = self.state.network.nodes[conn_uid]
                    print(f"{Color.GREEN}Found: {conn_node.name} ({conn_node.ip_address}) - {conn_node.network_type.value}{Color.RESET}")
                    discovered += 1
        
        if discovered == 0:
            print(f"{Color.YELLOW}No new nodes discovered{Color.RESET}")
        
        time.sleep(2)
    
    def social_engineering_menu(self):
        while True:
            clear()
            self.show_header()
            
            current_node = self.state.network.nodes.get(self.state.player.current_location)
            
            print("Social Engineering Operations:\n")
            print("1. Phishing campaign")
            print("2. Search OSINT databases")
            print("3. Social media reconnaissance")
            print("4. Compromise employee account")
            print("5. Back")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "1":
                self.phishing_campaign(current_node)
            elif choice == "2":
                self.osint_search(current_node)
            elif choice == "3":
                self.social_media_recon(current_node)
            elif choice == "4":
                self.compromise_employee(current_node)
            elif choice == "5":
                break
    
    def phishing_campaign(self, node: NetworkNode):
        if not node or not node.employees:
            print(f"\n{Color.RED}No employee data available for this node{Color.RESET}")
            time.sleep(1)
            return
        
        clear()
        print(f"\n{Color.CYAN}Launching phishing campaign against {node.name}...{Color.RESET}\n")
        time.sleep(1)
        
        targets = [emp for emp in node.employees if not emp.compromised]
        if not targets:
            print(f"{Color.YELLOW}All employees already compromised{Color.RESET}")
            time.sleep(1)
            return
        
        target = random.choice(targets)
        
        print(f"Target: {target.name} ({target.email})")
        print(f"Department: {target.department}")
        print(f"Access level: {target.access_level}/5")
        print(f"Susceptibility: {int(target.phishing_susceptibility * 100)}%\n")
        
        print("Crafting phishing email...")
        time.sleep(1.5)
        
        success_rate = target.phishing_susceptibility + (self.state.player.skills.social_engineering * GameConstants.PHISHING_SKILL_BONUS)
        
        if random.random() < success_rate:
            target.compromised = True
            print(f"\n{Color.GREEN}Success! {target.name} clicked the phishing link{Color.RESET}")
            print(f"Gained access credentials and session tokens")
            
            # Reduce firewall based on access level
            damage = target.access_level * 30
            node.firewall_strength -= damage
            
            # Lower trace cost
            node.trace_progress += GameConstants.PHISHING_SUCCESS_TRACE
            
            self.state.player.experience += target.access_level * 15
            self.check_level_up()
        else:
            print(f"\n{Color.RED}Phishing attempt failed{Color.RESET}")
            print(f"Target reported the email to IT security")
            node.trace_progress += GameConstants.PHISHING_FAIL_TRACE
            self.state.player.heat_level += GameConstants.PHISHING_FAIL_HEAT
        
        time.sleep(2)
    
    def osint_search(self, node: NetworkNode):
        if not node or not node.employees:
            print(f"\n{Color.RED}No employee data available{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.YELLOW}Searching open-source intelligence databases...{Color.RESET}\n")
        time.sleep(1.5)
        
        targets = random.sample(node.employees, min(5, len(node.employees)))
        
        for emp in targets:
            info_found = random.random() < emp.social_media_activity
            if info_found:
                print(f"{Color.GREEN}{emp.name}:{Color.RESET}")
                print(f"  Email: {emp.email}")
                print(f"  LinkedIn: Active in {emp.department}")
                if random.random() < 0.3:
                    print(f"  Personal email pattern detected")
                if random.random() < 0.2:
                    print(f"  Security question hints found")
                print()
        
        self.state.player.experience += 10
        time.sleep(2)
    
    def social_media_recon(self, node: NetworkNode):
        if not node or not node.employees:
            print(f"\n{Color.RED}No employee data available{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.YELLOW}Analyzing social media profiles...{Color.RESET}\n")
        time.sleep(1)
        
        high_activity = [emp for emp in node.employees if emp.social_media_activity > 0.6]
        
        if high_activity:
            target = random.choice(high_activity)
            print(f"Profile analysis: {target.name}")
            print(f"Activity level: {int(target.social_media_activity * 100)}%")
            print(f"\nIntelligence gathered:")
            print(f"  - Works at {node.name} in {target.department}")
            print(f"  - Recent posts about work projects")
            
            if random.random() < 0.4:
                print(f"  - Mentioned using specific software: {random.choice(['Slack', 'Jira', 'Salesforce'])}")
            if random.random() < 0.3:
                print(f"  - Shared photo with security badge visible")
            
            # Small phishing susceptibility increase
            target.phishing_susceptibility = min(1.0, target.phishing_susceptibility + 0.1)
            
            self.state.player.experience += 15
        else:
            print(f"{Color.YELLOW}No high-activity profiles found{Color.RESET}")
        
        time.sleep(2)
    
    def compromise_employee(self, node: NetworkNode):
        if not node or not node.employees:
            print(f"\n{Color.RED}No employee data available{Color.RESET}")
            time.sleep(1)
            return
        
        compromised = [emp for emp in node.employees if emp.compromised]
        
        if not compromised:
            print(f"\n{Color.RED}No compromised employees yet. Run phishing campaigns first.{Color.RESET}")
            time.sleep(1)
            return
        
        clear()
        print(f"\n{Color.CYAN}Compromised employees at {node.name}:{Color.RESET}\n")
        
        for i, emp in enumerate(compromised, 1):
            print(f"{i}. {emp.name} - {emp.department} - Access Level {emp.access_level}/5")
        
        print(f"\n0. Back")
        
        choice = input(f"\n{Color.CYAN}Select employee>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(compromised):
                emp = compromised[idx]
                
                print(f"\nUsing {emp.name}'s credentials...")
                time.sleep(1)
                
                print(f"Access level {emp.access_level} provides:")
                print(f"  - Reduced firewall strength")
                print(f"  - Lower trace accumulation")
                print(f"  - Bypass some security measures")
                
                # Provide benefits
                damage = emp.access_level * 25
                node.firewall_strength -= damage
                node.trace_speed *= 0.8
                
                print(f"\n{Color.GREEN}Firewall weakened by {damage} points{Color.RESET}")
                
                self.state.player.experience += emp.access_level * 10
                self.check_level_up()
                
                time.sleep(2)
        except ValueError:
            pass
    
    def cryptanalysis_menu(self):
        while True:
            clear()
            self.show_header()
            
            current_node = self.state.network.nodes.get(self.state.player.current_location)
            
            print("Cryptanalysis Laboratory:\n")
            print("1. Analyze encrypted traffic")
            print("2. Crack encryption")
            print("3. Decrypt intercepted data")
            print("4. Back")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "1":
                self.analyze_encrypted_traffic(current_node)
            elif choice == "2":
                self.crack_encryption(current_node)
            elif choice == "3":
                self.decrypt_data(current_node)
            elif choice == "4":
                break
    
    def analyze_encrypted_traffic(self, node: NetworkNode):
        if not node or not node.encrypted_traffic:
            print(f"\n{Color.RED}No encrypted traffic detected{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.YELLOW}Analyzing encrypted traffic patterns...{Color.RESET}\n")
        time.sleep(1.5)
        
        for i, data in enumerate(node.encrypted_traffic):
            status = f"{Color.GREEN}[CRACKED]{Color.RESET}" if data.cracked else f"{Color.RED}[ENCRYPTED]{Color.RESET}"
            print(f"{i+1}. {status} {data.encryption_type.value} - Size: {data.data_size}KB - Value: {data.value}BTC")
            print(f"   Difficulty: {int(data.difficulty * 100)}%")
        
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def crack_encryption(self, node: NetworkNode):
        if not node or not node.encrypted_traffic:
            print(f"\n{Color.RED}No encrypted data available{Color.RESET}")
            time.sleep(1)
            return
        
        uncracked = [d for d in node.encrypted_traffic if not d.cracked]
        if not uncracked:
            print(f"\n{Color.GREEN}All data already decrypted{Color.RESET}")
            time.sleep(1)
            return
        
        clear()
        print(f"\n{Color.CYAN}Select data package to decrypt:{Color.RESET}\n")
        
        for i, data in enumerate(uncracked, 1):
            print(f"{i}. {data.encryption_type.value} - Difficulty: {int(data.difficulty * 100)}% - Value: {data.value}BTC")
        
        print(f"\n0. Cancel")
        
        choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(uncracked):
                data = uncracked[idx]
                
                print(f"\n{Color.YELLOW}Attempting to crack {data.encryption_type.value}...{Color.RESET}")
                time.sleep(2)
                
                success_rate = 0.4 + (self.state.player.skills.cryptanalysis * 0.08) - (data.difficulty * 0.3)
                
                # Tool bonuses
                for tool in self.state.player.inventory:
                    if tool.tool_type == ToolType.CRYPTANALYSIS:
                        success_rate += tool.effectiveness * 0.15
                
                if random.random() < success_rate:
                    data.cracked = True
                    print(f"{Color.GREEN}Decryption successful!{Color.RESET}")
                    print(f"Gained: {data.value}BTC")
                    self.state.player.credits += data.value
                    self.state.player.experience += int(data.difficulty * 50)
                    self.check_level_up()
                else:
                    print(f"{Color.RED}Decryption failed{Color.RESET}")
                    print(f"The encryption is too strong or you lack the necessary tools")
                
                time.sleep(2)
        except ValueError:
            pass
    
    def decrypt_data(self, node: NetworkNode):
        # Show summary of cracked data
        if not node or not node.encrypted_traffic:
            print(f"\n{Color.RED}No data available{Color.RESET}")
            time.sleep(1)
            return
        
        cracked = [d for d in node.encrypted_traffic if d.cracked]
        
        if not cracked:
            print(f"\n{Color.YELLOW}No decrypted data yet{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.GREEN}Decrypted data packages:{Color.RESET}\n")
        total_value = sum(d.value for d in cracked)
        
        for data in cracked:
            print(f"  {data.encryption_type.value} - {data.data_size}KB - {data.value}BTC")
        
        print(f"\nTotal value extracted: {total_value}BTC")
        
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def botnet_menu(self):
        while True:
            clear()
            self.show_header()
            
            print("Botnet Management:\n")
            
            if self.state.player.botnets:
                for i, botnet in enumerate(self.state.player.botnets, 1):
                    health = int((1.0 - botnet.detected_nodes / max(1, botnet.size)) * 100)
                    print(f"{i}. Size: {botnet.size} nodes | Quality: {botnet.quality:.2f} | DDoS: {botnet.ddos_power}")
                    print(f"   Health: {health}% | Maintenance: {botnet.maintenance_cost}BTC/operation")
                print()
            else:
                print("No active botnets\n")
            
            print("1. Build new botnet")
            print("2. Maintain botnet")
            print("3. Expand botnet")
            print("4. Dismantle botnet")
            print("5. Back")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "1":
                self.build_botnet()
            elif choice == "2":
                self.maintain_botnet()
            elif choice == "3":
                self.expand_botnet()
            elif choice == "4":
                self.dismantle_botnet()
            elif choice == "5":
                break
    
    def build_botnet(self):
        cost = GameConstants.BOTNET_BUILD_COST
        
        if self.state.player.credits < cost:
            print(f"\n{Color.RED}Insufficient credits. Need: {cost}BTC{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.YELLOW}Building botnet... Cost: {cost}BTC{Color.RESET}")
        time.sleep(2)
        
        size = random.randint(GameConstants.BOTNET_BASE_SIZE_MIN, GameConstants.BOTNET_BASE_SIZE_MAX) + (self.state.player.skills.botnet_management * GameConstants.BOTNET_SIZE_PER_SKILL)
        quality = GameConstants.BOTNET_BASE_QUALITY + (self.state.player.skills.botnet_management * GameConstants.BOTNET_QUALITY_PER_SKILL)
        ddos_power = int(size * quality * 0.5)
        maintenance = int(size * 2)
        
        botnet = Botnet(
            size=size,
            quality=quality,
            maintenance_cost=maintenance,
            ddos_power=ddos_power
        )
        
        self.state.player.botnets.append(botnet)
        self.state.player.credits -= cost
        
        print(f"{Color.GREEN}Botnet created!{Color.RESET}")
        print(f"Size: {size} nodes")
        print(f"DDoS Power: {ddos_power}")
        
        time.sleep(2)
    
    def maintain_botnet(self):
        if not self.state.player.botnets:
            print(f"\n{Color.RED}No botnets to maintain{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.CYAN}Select botnet to maintain:{Color.RESET}\n")
        
        for i, botnet in enumerate(self.state.player.botnets, 1):
            print(f"{i}. Size: {botnet.size} | Cost: {botnet.maintenance_cost}BTC")
        
        choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.player.botnets):
                botnet = self.state.player.botnets[idx]
                
                if self.state.player.credits < botnet.maintenance_cost:
                    print(f"\n{Color.RED}Insufficient credits{Color.RESET}")
                    time.sleep(1)
                    return
                
                print(f"\n{Color.YELLOW}Maintaining botnet...{Color.RESET}")
                time.sleep(1)
                
                self.state.player.credits -= botnet.maintenance_cost
                botnet.detected_nodes = max(0, botnet.detected_nodes - int(botnet.size * 0.3))
                botnet.quality = min(1.0, botnet.quality + 0.05)
                
                print(f"{Color.GREEN}Botnet health restored{Color.RESET}")
                time.sleep(1)
        except ValueError:
            pass
    
    def expand_botnet(self):
        if not self.state.player.botnets:
            print(f"\n{Color.RED}No botnets available{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.CYAN}Select botnet to expand:{Color.RESET}\n")
        
        for i, botnet in enumerate(self.state.player.botnets, 1):
            expansion_cost = int(botnet.size * 10)
            print(f"{i}. Size: {botnet.size} | Expansion cost: {expansion_cost}BTC")
        
        choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.player.botnets):
                botnet = self.state.player.botnets[idx]
                expansion_cost = int(botnet.size * 10)
                
                if self.state.player.credits < expansion_cost:
                    print(f"\n{Color.RED}Insufficient credits{Color.RESET}")
                    time.sleep(1)
                    return
                
                print(f"\n{Color.YELLOW}Expanding botnet...{Color.RESET}")
                time.sleep(1.5)
                
                new_nodes = random.randint(20, 50) + (self.state.player.skills.botnet_management * 5)
                botnet.size += new_nodes
                botnet.ddos_power = int(botnet.size * botnet.quality * 0.5)
                botnet.maintenance_cost = int(botnet.size * 2)
                
                self.state.player.credits -= expansion_cost
                
                print(f"{Color.GREEN}Added {new_nodes} nodes to botnet{Color.RESET}")
                print(f"New size: {botnet.size}")
                time.sleep(1)
        except ValueError:
            pass
    
    def dismantle_botnet(self):
        if not self.state.player.botnets:
            print(f"\n{Color.RED}No botnets to dismantle{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.CYAN}Select botnet to dismantle:{Color.RESET}\n")
        
        for i, botnet in enumerate(self.state.player.botnets, 1):
            print(f"{i}. Size: {botnet.size} nodes")
        
        choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.player.botnets):
                print(f"\n{Color.YELLOW}Dismantling botnet...{Color.RESET}")
                time.sleep(1)
                
                self.state.player.botnets.pop(idx)
                
                print(f"{Color.GREEN}Botnet dismantled{Color.RESET}")
                time.sleep(1)
        except ValueError:
            pass
    
    def intelligence_menu(self):
        clear()
        self.show_header()
        
        print("Intelligence Report:\n")
        
        # Rival activity
        print(f"{Color.CYAN}Known Rival Hackers:{Color.RESET}")
        for rival in self.state.rival_hackers[:5]:
            status = f"{Color.RED}[HOSTILE]{Color.RESET}" if rival.hostile else ""
            print(f"  {rival.name} - Level {rival.skill_level} - {rival.specialization} {status}")
            if rival.active_targets:
                target_node = self.state.network.nodes.get(rival.active_targets[0])
                if target_node:
                    print(f"    Currently targeting: {target_node.name}")
        
        # Faction standings
        print(f"\n{Color.CYAN}Faction Relationships:{Color.RESET}")
        for faction_name, faction in self.state.player.factions.items():
            rep_color = Color.RED if faction.reputation < 0 else Color.GREEN if faction.reputation > 50 else Color.YELLOW
            status = "Hostile" if faction.hostile else "Neutral" if faction.reputation < 50 else "Friendly"
            print(f"  {faction_name}: {rep_color}{faction.reputation}{Color.RESET} ({status})")
        
        # Heat level analysis
        print(f"\n{Color.CYAN}Threat Assessment:{Color.RESET}")
        if self.state.player.heat_level < 30:
            print(f"  {Color.GREEN}Low profile - Operating safely{Color.RESET}")
        elif self.state.player.heat_level < 60:
            print(f"  {Color.YELLOW}Moderate attention - Exercise caution{Color.RESET}")
        else:
            print(f"  {Color.RED}High priority target - Extreme risk{Color.RESET}")
        
        if self.state.player.under_investigation:
            print(f"\n{Color.RED}ACTIVE INVESTIGATION: {int(self.state.player.investigation_progress)}% complete{Color.RESET}")
            
        print(f"\n1. Hack Rival")
        print(f"2. Back")
        
        choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
        
        if choice == "1":
            self.hack_rival_menu()
        
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")

    def hack_rival_menu(self):
        clear()
        self.show_header()
        print(f"{Color.CYAN}Rival Infiltration:{Color.RESET}\n")
        
        for i, rival in enumerate(self.state.rival_hackers[:5], 1):
            print(f"{i}. {rival.name} (Level {rival.skill_level})")
            
        choice = input(f"\n{Color.CYAN}Select target (0 to cancel)>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < 5:
                rival = self.state.rival_hackers[idx]
                print(f"\n{Color.YELLOW}Attempting to infiltrate {rival.name}'s system...{Color.RESET}")
                time.sleep(2)
                
                success_rate = GameConstants.RIVAL_HACK_BASE_SUCCESS + (self.state.player.skills.exploitation * GameConstants.SKILL_SUCCESS_BONUS) - (rival.skill_level * 0.04)
                
                if random.random() < success_rate:
                    reward = rival.skill_level * 500
                    self.state.player.credits += reward
                    print(f"{Color.GREEN}Infiltration successful!{Color.RESET}")
                    print(f"Stole encrypted wallet: {reward}BTC")
                    rival.hostile = True
                else:
                    print(f"{Color.RED}Detected! {rival.name} is counter-attacking...{Color.RESET}")
                    self.state.player.heat_level += 10
                    rival.hostile = True
                time.sleep(2)
        except: pass
    
    def contract_menu(self):
        while True:
            clear()
            self.show_header()
            
            print("Contract Board:\n")
            
            # Refresh contracts if needed
            if len(self.state.contracts) < GameConstants.MIN_ACTIVE_CONTRACTS:
                for _ in range(GameConstants.INITIAL_CONTRACTS):
                    contract = ContractGenerator.generate_contract(
                        self.state.network, 
                        self.state.player.level, 
                        self.state.player.factions
                    )
                    if contract:
                        self.state.contracts.append(contract)
            
            active = [c for c in self.state.contracts if not c.completed and not c.failed]
            
            if not active:
                print(f"{Color.YELLOW}No contracts available. Check back later.{Color.RESET}\n")
            else:
                for i, contract in enumerate(active, 1):
                    target = self.state.network.nodes.get(contract.target_node_uid)
                    if target:
                        print(f"{i}. {contract.title}")
                        print(f"   Contractor: {contract.contractor}")
                        if contract.faction:
                            print(f"   Faction: {contract.faction}")
                        print(f"   Target: {target.name} (Security: {target.security_rating}/10)")
                        print(f"   Objective: {contract.objective}")
                        print(f"   Reward: {contract.reward}BTC | Rep: +{contract.reputation_change}")
                        if contract.deadline:
                            time_left = contract.deadline - datetime.now()
                            print(f"   Deadline: {time_left.days}d {time_left.seconds//3600}h remaining")
                        print()
            
            print("0. Back")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "0":
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(active):
                    contract = active[idx]
                    target = self.state.network.nodes[contract.target_node_uid]
                    
                    print(f"\n{Color.CYAN}{contract.description}{Color.RESET}")
                    print(f"\nAccept contract? (y/n)")
                    
                    accept = input(f"{Color.CYAN}>{Color.RESET} ").strip().lower()
                    
                    if accept == 'y':
                        if contract.uid not in self.state.player.active_contracts:
                            self.state.player.active_contracts.append(contract.uid)
                        self.state.player.discovered_nodes.add(contract.target_node_uid)
                        print(f"\n{Color.GREEN}Contract accepted{Color.RESET}")
                        
                        # Faction reputation impact
                        if contract.faction and contract.faction in self.state.player.factions:
                            self.state.player.factions[contract.faction].reputation += 5
                        
                        time.sleep(1)
            except ValueError:
                pass
    
    def black_market_menu(self):
        while True:
            clear()
            self.show_header()
            
            print(f"{Color.MAGENTA}Black Market - Dark Web Trading Hub{Color.RESET}\n")
            
            print("1. Browse tools")
            print("2. Browse exploits")
            print("3. Upgrade hardware")
            print("4. Purchase proxy chains")
            print("5. Money Laundering")
            print("6. Sell stolen data")
            print("7. Back")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            if choice == "1":
                self.browse_tools()
            elif choice == "2":
                self.browse_exploits()
            elif choice == "3":
                self.browse_hardware()
            elif choice == "4":
                self.purchase_proxy()
            elif choice == "5":
                self.launder_money_menu()
            elif choice == "6":
                self.sell_data()
            elif choice == "7":
                break
    
    def browse_tools(self):
        clear()
        print(f"\n{Color.CYAN}Available Tools:{Color.RESET}\n")
        
        for i, tool in enumerate(self.state.black_market_tools, 1):
            owned = tool in self.state.player.inventory
            status = f"{Color.GREEN}[OWNED]{Color.RESET}" if owned else ""
            level_req = f"{Color.RED}[REQ: L{tool.level_requirement}]{Color.RESET}" if tool.level_requirement > self.state.player.level else ""
            print(f"{i}. {tool.name} - {tool.cost}BTC {status}{level_req}")
            print(f"   {tool.description}")
            print(f"   Effectiveness: {tool.effectiveness} | Stealth penalty: {tool.stealth_penalty}")
            print()
        
        print("0. Back")
        
        choice = input(f"\n{Color.CYAN}Purchase tool>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.black_market_tools):
                tool = self.state.black_market_tools[idx]
                
                if tool in self.state.player.inventory:
                    print(f"\n{Color.YELLOW}Already owned{Color.RESET}")
                    time.sleep(1)
                    return
                
                if tool.level_requirement > self.state.player.level:
                    print(f"\n{Color.RED}Level {tool.level_requirement} required{Color.RESET}")
                    time.sleep(1)
                    return
                
                if self.state.player.credits < tool.cost:
                    print(f"\n{Color.RED}Insufficient credits{Color.RESET}")
                    time.sleep(1)
                    return
                
                self.state.player.credits -= tool.cost
                self.state.player.inventory.append(tool)
                
                print(f"\n{Color.GREEN}Purchased {tool.name}{Color.RESET}")
                time.sleep(1)
        except ValueError:
            pass
    
    def browse_exploits(self):
        clear()
        print(f"\n{Color.CYAN}Available Exploits:{Color.RESET}\n")
        
        # Refresh exploits occasionally
        if random.random() < 0.3:
            self.state.black_market_exploits = BlackMarket.generate_exploits(self.state.player.level)
        
        for i, exploit in enumerate(self.state.black_market_exploits, 1):
            owned = exploit['name'] in self.state.player.known_exploits
            status = f"{Color.GREEN}[OWNED]{Color.RESET}" if owned else ""
            level_req = f"{Color.RED}[REQ: L{exploit['level_req']}]{Color.RESET}" if exploit['level_req'] > self.state.player.level else ""
            
            print(f"{i}. {exploit['name']} - {exploit['cost']}BTC {status}{level_req}")
            print(f"   Type: {exploit['type']} | Effectiveness: {exploit['effectiveness']:.2f}")
            print()
        
        print("0. Back")
        
        choice = input(f"\n{Color.CYAN}Purchase exploit>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.black_market_exploits):
                exploit = self.state.black_market_exploits[idx]
                
                if exploit['name'] in self.state.player.known_exploits:
                    print(f"\n{Color.YELLOW}Already known{Color.RESET}")
                    time.sleep(1)
                    return
                
                if exploit['level_req'] > self.state.player.level:
                    print(f"\n{Color.RED}Level {exploit['level_req']} required{Color.RESET}")
                    time.sleep(1)
                    return
                
                if self.state.player.credits < exploit['cost']:
                    print(f"\n{Color.RED}Insufficient credits{Color.RESET}")
                    time.sleep(1)
                    return
                
                self.state.player.credits -= exploit['cost']
                self.state.player.known_exploits.add(exploit['name'])
                
                print(f"\n{Color.GREEN}Learned {exploit['name']}{Color.RESET}")
                time.sleep(1)
        except ValueError:
            pass

    def browse_hardware(self):
        clear()
        print(f"\n{Color.CYAN}Hardware Upgrades:{Color.RESET}\n")
        
        for i, item in enumerate(self.state.black_market_hardware, 1):
            current = self.state.player.hardware.get(item.htype.name.capitalize())
            status = f"{Color.GREEN}[INSTALLED]{Color.RESET}" if current and current.name == item.name else ""
            level_req = f"{Color.RED}[REQ: L{item.level}]{Color.RESET}" if item.level > self.state.player.level else ""
            
            print(f"{i}. {item.name} ({item.htype.value}) - {item.cost}BTC {status}{level_req}")
            print(f"   {item.description}")
            print(f"   Bonus: x{item.bonus:.2f}")
            print()
            
        print("0. Back")
        
        choice = input(f"\n{Color.CYAN}Purchase hardware>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.state.black_market_hardware):
                item = self.state.black_market_hardware[idx]
                key = item.htype.name.capitalize()
                
                if self.state.player.hardware.get(key) and self.state.player.hardware[key].name == item.name:
                    print(f"\n{Color.YELLOW}Already installed{Color.RESET}")
                    time.sleep(1)
                    return
                    
                if item.level > self.state.player.level:
                    print(f"\n{Color.RED}Level {item.level} required{Color.RESET}")
                    time.sleep(1)
                    return
                    
                if self.state.player.credits < item.cost:
                    print(f"\n{Color.RED}Insufficient credits{Color.RESET}")
                    time.sleep(1)
                    return
                    
                self.state.player.credits -= item.cost
                self.state.player.hardware[key] = item
                
                print(f"\n{Color.GREEN}Installed {item.name}{Color.RESET}")
                time.sleep(1)
        except ValueError:
            pass
    
    def purchase_proxy(self):
        cost = GameConstants.PROXY_BASE_COST + (self.state.player.proxy_chains * GameConstants.PROXY_COST_INCREMENT)
        
        print(f"\n{Color.CYAN}Proxy Chain Purchase{Color.RESET}")
        print(f"Current chains: {self.state.player.proxy_chains}")
        print(f"Cost for next chain: {cost}BTC")
        print(f"Benefit: -{(self.state.player.proxy_chains + 1) * 10}% trace accumulation")
        
        if self.state.player.credits < cost:
            print(f"\n{Color.RED}Insufficient credits{Color.RESET}")
            input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
            return
        
        print(f"\nPurchase? (y/n)")
        choice = input(f"{Color.CYAN}>{Color.RESET} ").strip().lower()
        
        if choice == 'y':
            self.state.player.credits -= cost
            self.state.player.proxy_chains += 1
            
            print(f"\n{Color.GREEN}Proxy chain established{Color.RESET}")
            time.sleep(1)
    
    def sell_data(self):
        # Sell data from compromised nodes
        compromised_nodes = [self.state.network.nodes[uid] for uid in self.state.player.compromised_nodes]
        
        if not compromised_nodes:
            print(f"\n{Color.RED}No compromised nodes to sell data from{Color.RESET}")
            time.sleep(1)
            return
        
        print(f"\n{Color.CYAN}Compromised nodes with sellable data:{Color.RESET}\n")
        
        sellable = [n for n in compromised_nodes if n.data_value > 0]
        
        if not sellable:
            print(f"{Color.YELLOW}No sellable data available{Color.RESET}")
            time.sleep(1)
            return
        
        for i, node in enumerate(sellable, 1):
            print(f"{i}. {node.name} - {node.data_value}BTC worth of data")
        
        print(f"\n0. Back")
        
        choice = input(f"\n{Color.CYAN}Sell data from node>{Color.RESET} ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sellable):
                node = sellable[idx]
                
                value = node.data_value
                self.state.player.credits += value
                node.data_value = 0  # Data sold
                
                # Reputation gain
                self.state.player.reputation += 5
                
                # Heat increase
                self.state.player.heat_level += 3
                
                print(f"\n{Color.GREEN}Data sold for {value}BTC{Color.RESET}")
                print(f"{Color.YELLOW}Heat level increased slightly{Color.RESET}")
                
                time.sleep(2)
        except ValueError:
            pass

    def launder_money_menu(self):
        clear()
        self.show_header()
        print(f"{Color.MAGENTA}Money Laundering Service{Color.RESET}")
        print("Exchange BTC for a cleaner identity profile.\n")
        
        print(f"Identity Heat: {self.state.player.identity_heat}%")
        print(f"Investigation Progress: {int(self.state.player.investigation_progress)}%")
        
        cost = GameConstants.LAUNDER_COST
        print(f"\nLaunder {GameConstants.LAUNDER_COST}BTC to reduce identity heat by {GameConstants.LAUNDER_IDENTITY_REDUCTION}%? (y/n)")
        
        choice = input(f"{Color.CYAN}>{Color.RESET} ").strip().lower()
        
        if choice == 'y':
            if self.state.player.credits < cost:
                print(f"{Color.RED}Insufficient credits{Color.RESET}")
                time.sleep(1)
                return
                
            self.state.player.credits -= cost
            self.state.player.identity_heat = max(0, self.state.player.identity_heat - GameConstants.LAUNDER_IDENTITY_REDUCTION)
            self.state.player.investigation_progress = max(0, self.state.player.investigation_progress - GameConstants.LAUNDER_INVESTIGATION_REDUCTION)
            
            print(f"\n{Color.GREEN}Money laundered. Identity traces reduced.{Color.RESET}")
            time.sleep(1.5)

    def character_menu(self):
        clear()
        self.show_header()
        
        print("Character Profile:\n")
        
        # Skills
        print(f"{Color.CYAN}Skills:{Color.RESET}")
        skills_dict = asdict(self.state.player.skills)
        
        for skill_name, level in skills_dict.items():
            bar = '█' * level + '░' * (10 - level)
            print(f"  {skill_name.capitalize():<25} [{Color.CYAN}{bar}{Color.RESET}] {level}/10")
        
        # Experience
        exp_needed = self.state.player.level * GameConstants.EXP_PER_LEVEL_MULTIPLIER
        exp_bar = '█' * int((self.state.player.experience / exp_needed) * 20)
        print(f"\nExperience: [{Color.MAGENTA}{exp_bar:<20}{Color.RESET}] {self.state.player.experience}/{exp_needed}")
        
        # Inventory
        print(f"\n{Color.CYAN}Inventory ({len(self.state.player.inventory)} items):{Color.RESET}")
        for tool in self.state.player.inventory[:5]:
            print(f"  - {tool.name} ({tool.tool_type.value})")
        
        if len(self.state.player.inventory) > 5:
            print(f"  ... and {len(self.state.player.inventory) - 5} more")
        
        # Stats
        print(f"\n{Color.CYAN}Statistics:{Color.RESET}")
        print(f"  Nodes discovered: {len(self.state.player.discovered_nodes)}")
        print(f"  Nodes compromised: {len(self.state.player.compromised_nodes)}")
        print(f"  Contracts completed: {len(self.state.player.completed_contracts)}")
        print(f"  Known exploits: {len(self.state.player.known_exploits)}")
        
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def system_status(self):
        clear()
        self.show_header()
        
        print("System Status:\n")
        
        # Network stats
        total_nodes = len(self.state.network.nodes)
        discovered = len(self.state.player.discovered_nodes)
        compromised = len(self.state.player.compromised_nodes)
        
        print(f"{Color.CYAN}Network Progress:{Color.RESET}")
        print(f"  Discovered: {discovered}/{total_nodes} ({int(discovered/total_nodes*100)}%)")
        print(f"  Compromised: {compromised}/{total_nodes} ({int(compromised/total_nodes*100)}%)")
        
        # Contracts
        active_contracts = [c for c in self.state.contracts if not c.completed and not c.failed]
        completed_contracts = len(self.state.player.completed_contracts)
        
        print(f"\n{Color.CYAN}Contracts:{Color.RESET}")
        print(f"  Active: {len(active_contracts)}")
        print(f"  Completed: {completed_contracts}")
        
        # Threats
        print(f"\n{Color.CYAN}Threat Level:{Color.RESET}")
        heat_color = Color.RED if self.state.player.heat_level > 70 else Color.YELLOW if self.state.player.heat_level > 40 else Color.GREEN
        print(f"  Heat: {heat_color}{self.state.player.heat_level}%{Color.RESET}")
        print(f"  Identity heat: {self.state.player.identity_heat}%")
        
        if self.state.player.under_investigation:
            print(f"\n{Color.RED}  ACTIVE INVESTIGATION: {int(self.state.player.investigation_progress)}%{Color.RESET}")
            print(f"  {Color.RED}  Take action to reduce heat level!{Color.RESET}")
        
        # Recent events
        print(f"\n{Color.CYAN}Recent Activity:{Color.RESET}")
        for event in self.state.event_log[-10:]:
            print(f"  {Color.DIM}{event}{Color.RESET}")
        
        input(f"\n{Color.DIM}Press Enter...{Color.RESET}")
    
    def check_level_up(self):
        exp_needed = self.state.player.level * GameConstants.EXP_PER_LEVEL_MULTIPLIER
        
        while self.state.player.experience >= exp_needed:
            self.state.player.experience -= exp_needed
            self.state.player.level += 1
            exp_needed = self.state.player.level * GameConstants.EXP_PER_LEVEL_MULTIPLIER
            
            print(f"\n{Color.GREEN}═══════════════════════════════════════════════════════{Color.RESET}")
            print(f"{Color.GREEN}{Color.BOLD}              LEVEL UP - NOW LEVEL {self.state.player.level}{Color.RESET}")
            print(f"{Color.GREEN}═══════════════════════════════════════════════════════{Color.RESET}")
            
            print("\nChoose skill to upgrade:")
            
            skills = ['scanning', 'exploitation', 'stealth', 'cryptanalysis', 
                     'social_engineering', 'reverse_engineering', 'botnet_management']
            for i, skill in enumerate(skills, 1):
                current = getattr(self.state.player.skills, skill)
                print(f"{i}. {skill.capitalize()} (current: {current}/{GameConstants.MAX_SKILL_LEVEL})")
            
            choice = input(f"\n{Color.CYAN}>{Color.RESET} ").strip()
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(skills):
                    skill_name = skills[idx]
                    current_val = getattr(self.state.player.skills, skill_name)
                    if current_val < GameConstants.MAX_SKILL_LEVEL:
                        setattr(self.state.player.skills, skill_name, current_val + 1)
                        print(f"\n{Color.GREEN}{skill_name.capitalize()} improved to {current_val + 1}!{Color.RESET}")
                        time.sleep(1.5)
            except ValueError:
                pass

def intro_sequence():
    clear()
    log("Initializing secure connection...", Color.GREEN, 0.03)
    time.sleep(0.3)
    log("Loading neural interface...", Color.GREEN, 0.03)
    time.sleep(0.3)
    log("Establishing encrypted tunnel...", Color.GREEN, 0.03)
    time.sleep(0.3)
    log("Bypassing firewall...", Color.YELLOW, 0.03)
    time.sleep(0.5)
    log("Connection established.", Color.CYAN, 0.03)
    time.sleep(0.5)
    log("\nNETRUNNER v2.0", Color.CYAN, 0.03)
    log("Advanced Network Intrusion Simulator\n", Color.DIM, 0.02)
    time.sleep(1)

def main():
    save_data = SaveManager.load_game()
    
    if save_data:
        print(f"{Color.CYAN}Save file detected. Load game? (y/n){Color.RESET}")
        choice = input(f"{Color.CYAN}>{Color.RESET} ").strip().lower()
        
        if choice == 'y':
            print(f"{Color.YELLOW}Loading saved game...{Color.RESET}")
            time.sleep(1)
            state = GameState.load_from_dict(save_data)
            print(f"{Color.GREEN}Game loaded successfully! Welcome back, {state.player.handle}.{Color.RESET}")
            time.sleep(1.5)
        else:
            intro_sequence()
            state = GameState()
    else:
        intro_sequence()
        state = GameState()
    
    interface = GameInterface(state)
    
    try:
        interface.main_menu()
        
        # Save on exit
        print(f"\n{Color.YELLOW}Saving game...{Color.RESET}")
        SaveManager.save_game(state)
        print(f"{Color.GREEN}Game saved{Color.RESET}")
        time.sleep(0.5)
        
    except KeyboardInterrupt:
        print(f"\n\n{Color.RED}Emergency disconnect{Color.RESET}")
        print(f"{Color.YELLOW}Saving game...{Color.RESET}")
        SaveManager.save_game(state)
        print(f"{Color.GREEN}Game saved{Color.RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()