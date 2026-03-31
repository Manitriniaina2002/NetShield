# 📡 Guide: Commandes Wi-Fi Réelles en Mode Linux

## Vue d'ensemble

En mode réel Linux, NetShield peut exécuter 6 commandes critiques pour l'audit Wi-Fi.

Ci-dessous, tous les détails et exemples pour chaque commande.

---

## 1️⃣ `ifconfig` - Interfaces Réseau

### Description
Affiche la configuration de toutes les interfaces réseau (filaire et Wi-Fi).

### Permissions
- ✅ Peut s'exécuter sans root (affichage seulement)

### Syntaxe
```bash
# Afficher toutes les interfaces
ifconfig

# Afficher une interface spécifique
ifconfig wlan0

# Afficher seulement info utile
ifconfig | grep -E "inet|HWaddr"
```

### Exemples Réels

**Commande:** `ifconfig`
```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::1  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:26:30:c7  txqueuelen 1000  (Ethernet)
        RX packets 10245  bytes 5120000 (5.1 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 8192  bytes 2560000 (2.5 MB)
        TX errors 0  dropped 0 overruns 0 carrier 0  collisions 0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.101  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::2  prefixlen 64  scopeid 0x20<link>
        ether 84:16:F9:AB:CD:EF  txqueuelen 1000  (Ethernet)
        RX packets 5120  bytes 2560000 (2.5 MB)
        TX packets 4096  bytes 1024000 (1.0 MB)

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 1024  bytes 512000 (512 KB)
        TX packets 1024  bytes 512000 (512 KB)
```

### Utilité pour l'Audit
- 🎯 Identifier les interfaces Wi-Fi actives
- 🎯 Voir les adresses MAC (BSSID)
- 🎯 Vérifier les adresses IP
- 🎯 Voir les statistiques (RX/TX)

---

## 2️⃣ `ip` - Commandes IP Avancées

### Description
Outil moderne pour gérer la configuration réseau. Remplace `ifconfig`, `route`, etc.

### Permissions
- ✅ Affichage sans root
- ⚠️ Certaines modifications requièrent root

### Syntaxe
```bash
# Voir all addresses
ip addr show

# Voir routing table
ip route show

# Voir les liens (interfaces)
ip link show

# Voir détails interface spécifique
ip addr show wlan0
```

### Exemples Réels

**Commande:** `ip addr show`
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 08:00:27:26:30:c7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 3599sec preferred_lft 3599sec
    inet6 fe80::1/64 scope link
       valid_lft forever preferred_lft forever

3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 84:16:F9:AB:CD:EF brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.50/24 brd 192.168.1.255 scope global dynamic wlan0
       valid_lft 7200sec preferred_lft 7200sec
    inet6 fe80::8616:f9ff:feab:cdef/64 scope link
       valid_lft forever preferred_lft forever
```

### Utilité pour l'Audit
- 🎯 Voir configuration IP détaillée
- 🎯 Voir les routes (routing)
- 🎯 Vérifier adresses IPv4 et IPv6
- 🎯 Plus d'infos que `ifconfig`

---

## 3️⃣ `airmon-ng` - Mode Monitor Wi-Fi

### Description
Outil pour activer/désactiver le **mode monitor** sur les interfaces Wi-Fi.

### Permissions
- ⚠️ **REQUIERT ROOT** - Modification d'état système

### Syntaxe
```bash
# Voir interfaces Wi-Fi
airmon-ng

# Démarrer mode monitor
airmon-ng start wlan0

# Arrêter mode monitor
airmon-ng stop wlan0mon
```

### Modes Expliqués

**Mode Managed** (Normal)
- Interface connectée à un réseau
- Peut communiquer avec le routeur seulement
- Incapable de voir autres réseaux

**Mode Monitor** (Audit)
- Interface en lecture seule
- Capture TOUS les paquets Wi-Fi
- Necessaire pour l'audit de sécurité

### Exemple Réel

**Avant activation:**
```bash
airmon-ng

PHY     Interface    Driver        Chipset
phy0    wlan0        ath10k        Qualcomm Atheros QCA9377 802.11ac Wireless Network Adapter
```

**Activer:**
```bash
airmon-ng start wlan0

Found 2 processes: wlan0
Switched wlan0 into monitor mode (wlan0mon)
```

**Après activation:**
```bash
airmon-ng

PHY     Interface    Driver        Chipset
phy0    wlan0        ath10k        (Qualcomm Atheros QCA9377 802.11ac Wireless Network Adapter) - Monitor Mode
phy0    wlan0mon     ath10k        Qualcomm Atheros QCA9377 802.11ac Wireless Network Adapter
```

**Désactiver:**
```bash
airmon-ng stop wlan0mon

Switching wlan0mon into managed mode (wlan0)
Stopped monitor mode
```

### Utilité pour l'Audit
- 🎯 Activer mode audit/capture
- 🎯 Scanner tous les réseaux à proximité
- 🎯 Base pour utiliser `airodump-ng`

---

## 4️⃣ `airodump-ng` - Scanner Wi-Fi

### Description
Capture et affiche tous les réseaux Wi-Fi à proximité avec détails de sécurité.

### Permissions
- ⚠️ **REQUIERT** mode monitor activé (airmon-ng start)
- ⚠️ **REQUIERT ROOT**

### Syntaxe
```bash
# Scanner l'interface wlan0mon
airodump-ng wlan0mon

# Scanner spécifique channel
airodump-ng -c 6 wlan0mon

# Sauvegarder capture en fichier
airodump-ng -w capture wlan0mon
```

### Exemple Réel Output

```
 BSSID              PWR  Beacons    #Data, #/s  CH  MB  ENC CIPHER AUTH ESSID
 
 AA:11:22:33:44:55  -25   145       2400   10  6   130 WPA2 CCMP   PSK  HomeNetwork
 BB:22:33:44:55:66  -45   89        1200   5   11  108 WEP  WEP         PublicWiFi
 CC:33:44:55:66:77  -50   234       5600   20  1   130 WPA2 CCMP   PSK  CoffeeShop
 DD:44:55:66:77:88  -65   45        120    2   44  54  WPA3 CCMP   PSK  SecureOffice
 
 BSSID              STATION            PWR   Rate    Lost    Frames  Probe
 
 AA:11:22:33:44:55  11:22:33:44:55:66  -30   130e   0        450     HomeNetwork
 AA:11:22:33:44:55  22:33:44:55:66:77  -40   130e   12       280     HomeNetwork
 BB:22:33:44:55:66  33:44:55:66:77:88  -35   130e   5        320     PublicWiFi
```

### Signification des Colonnes

| Colonne | Signification |
|---------|---------------|
| BSSID | Adresse MAC du routeur |
| PWR | Force du signal (-1/-100dBm) |
| Beacons | Paquets d'identification |
| #Data | Paquets de données capturés |
| CH | Canal (1-14 pour 2.4GHz, 36-165 pour 5GHz) |
| MB | Vitesse maximale |
| ENC | Type de chiffrement (WEP/WPA/WPA2/WPA3) |
| CIPHER | Algorithme (TKIP/CCMP) |
| AUTH | Méthode d'auth |
| ESSID | Nom du réseau |

### Utilité pour l'Audit
- 🎯 Voir tous les réseaux Wi-Fi
- 🎯 Identifier les réseaux faibles/ouverts
- 🎯 Voir le type de chiffrement
- 🎯 Identifier clients connectés
- 🎯 Repérer réseaux cachés

---

## 5️⃣ `ps` - Liste des Processus

### Description
Affiche tous les processus actuellement en cours d'exécution.

### Permissions
- ✅ Peut s'exécuter sans root (affichage seulement)

### Syntaxe
```bash
# Afficher processus de l'utilisateur
ps

# Afficher TOUS les processus détail
ps aux

# Format détaillé
ps -ef

# Chercher un processus spécifique
ps aux | grep python

# Format personnalisé
ps -o pid,user,cmd
```

### Exemple Réel

**Commande:** `ps aux`
```
USER       PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
root         1  0.1  0.0  19356  1892 ?   Ss   10:00   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?   S    10:00   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?   S    10:00   0:00 [rcu_gp]
ubuntu    1234  0.5  0.2 123456 56000 ?   Sl   10:15   0:05 python3 /app/main.py
ubuntu    1235  0.3  0.1  98765 45000 ?   Sl   10:15   0:02 node /app/frontend/server.js
root      1236  0.0  0.0  12345  1000 ?   S    10:15   0:00 /usr/sbin/sshd
ubuntu    1237  0.1  0.0  54321  8000 pts/0 S  10:16   0:00 bash
```

### Signification des Colonnes

| Colonne | Signification |
|---------|---------------|
| USER | Utilisateur propriétaire du processus |
| PID | ID du processus (process ID) |
| %CPU | Utilisation CPU |
| %MEM | Utilisation mémoire |
| VSZ | Taille virtuelle (KB) |
| RSS | Mémoire résidente (KB) |
| TTY | Terminal (? = pas de terminal) |
| STAT | État (S=sleep, R=running, Ss=session leader) |
| START | Heure de démarrage |
| TIME | Temps CPU utilisé |
| COMMAND | Commande exécutée |

### Utilité pour l'Audit
- 🎯 Voir processus actifs
- 🎯 Identifier les services réseau actifs
- 🎯 Vérifier aircrack-ng/outils audit
- 🎯 Chercher processus suspects

---

## 6️⃣ `kill` - Terminer un Processus

### Description
Termine (tue) un processus spécifique par son PID.

### Permissions
- ✅ Peut tuer ses propres processus (sans root)
- ⚠️ Tue d'autres processus requiert root

### Syntaxe
```bash
# Terminer un processus
kill 1234

# Forcer la fermeture
kill -9 1234

# Signaux courants
kill -TERM 1234   # Arrêt gracieux (défaut)
kill -9 1234      # Arrêt forcé (SIGKILL)
kill -STOP 1234   # Pause le processus
kill -CONT 1234   # Reprendre le processus
```

### Exemple Réel

```bash
# Voir processus
ps aux | grep python
ubuntu    1234  0.5  0.2 123456 56000 ?  Sl  10:15  0:05 python3 /app/main.py

# Terminer le processus
kill 1234

# Forcer si non-responsif
kill -9 1234

# Vérifier qu'il a disparu
ps aux | grep 1234
# (Aucun résultat = succès)
```

### Utilité pour l'Audit
- 🎯 Arrêter un processus audit
- 🎯 Nettoyer après test
- 🎯 Terminer processus d'attaque (astuces)

---

## 📋 Résumé des Commandes

| N° | Commande | Mode | Root? | Utilité |
|----|----------|------|-------|---------|
| 1 | `ifconfig` | Managed | ✅ | Voir interfaces réseau |
| 2 | `ip` | Managed | ✅ | Config IP avancée |
| 3 | `airmon-ng` | Both | ⚠️ | Activer mode monitor |
| 4 | `airodump-ng` | Monitor | ⚠️ | Scanner Wi-Fi |
| 5 | `ps` | Managed | ✅ | Voir processus |
| 6 | `kill` | Managed | ✅ | Terminer processus |

---

## 🚀 Workflow Typique d'Audit

```
1. Vérifier interfaces
   → Commande: ifconfig
   → Identifier: wlan0
   
2. Voir config IP
   → Commande: ip addr show
   → Identifier: 192.168.1.100
   
3. Activer mode monitor
   → Commande: airmon-ng start wlan0
   → Résultat: wlan0mon activée
   
4. Scanner réseaux
   → Commande: airodump-ng wlan0mon
   → Identifier réseaux faibles
   
5. Analyser dans NetShield
   → Voir les vulnérabilités détectées
   → Générer recommandations

6. Arrêter mode monitor
   → Commande: airmon-ng stop wlan0mon
   → Résultat: retour au mode normal
```

---

## 🔐 Considérations de Sécurité

### Installation des Outils

```bash
# Sur Debian/Ubuntu
sudo apt install net-tools     # pour ifconfig
sudo apt install aircrack-ng   # pour airmon-ng, airodump-ng

# Vérifier installation
which airmon-ng
which airodump-ng
```

### Prérequis Matériel

- **Carte Wi-Fi compatible:** Atheros, Intel, Broadcom (certaines)
- **Drivers:** Voir: https://www.aircrack-ng.org/doku.php?id=install_drivers

### Non Autorisées à Proximité

❌ Ne scannez PAS les réseaux publics sans autorisation
❌ Ne cassez PAS les mots de passe Wi-Fi
❌ Respectez les lois locales

✅ Utilisez seulement sur:
- Vos propres réseaux
- Réseaux de test autorisés
- Environnements contrôlés

---

## 📞 Besoin de Détails?

Consultez:
- `LINUX_MODE.md` - Mode réel complet
- `QUICK_REAL_MODE.md` - Démarrage rapide
- `COMMANDS_GUIDE.md` - Tous les détails sécurité
- Documentations officielles:
  - https://www.aircrack-ng.org/
  - https://linux.die.net/man/8/ifconfig
  - https://man7.org/linux/man-pages/man1/ps.1.html

---

**Prêt à scaner des réseaux Wi-Fi en vrai!** 🚀
