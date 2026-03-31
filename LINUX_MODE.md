# 🐧 Mode Réel Linux - Exécution de Vraies Commandes

## ⚠️ ATTENTION - Mode Avancé

Cette configuration permet à NetShield d'exécuter des **vraies commandes Linux** directement sur votre système.

**Ceci est puissant et dangereux - À utiliser avec extrême prudence!**

---

## 🔧 Configuration du Mode Réel

### Étape 1: Activer le Mode Réel

Modifiez `backend/.env`:

```env
SIMULATION_MODE=False
```

**Avant:**
```env
SIMULATION_MODE=True  ← Mode simulation (sûr, partout)
```

**Après:**
```env
SIMULATION_MODE=False ← Mode réel (vraies commandes Linux)
```

### Étape 2: Lancer avec Privilèges Root

**IMPORTANT:** Le mode réel requiert les permissions **root** (sudo).

```bash
# Option 1: Lancer directement avec sudo
cd backend
sudo python main.py

# Option 2: Lancer dans un environnement root
sudo -s
source venv/bin/activate
python main.py
```

### Étape 3: Accéder l'Interface

1. Ouvrez: `http://localhost:3000`
2. Allez à l'onglet **⚙️ Commandes**
3. Entrez votre mot de passe **root/sudo**

---

## 🔓 Authentification en Mode Réel

### Sur Linux

Quand vous cliquez **🔓 S'authentifier**:

1. Le système **vérifie vos permissions root** (uid == 0)
2. Si vous êtes root → Authentification réussie
3. Si vous n'êtes pas root → Erreur "Authentification échouée"

**Comment vérifier vous êtes root:**

```bash
whoami
# Doit retourner: root

id
# Doit montrer: uid=0(root) gid=0(root) groups=0(root)
```

### Obtenir les Permissions Root

**Option 1: Sudo (recommandé)**

```bash
sudo su -
source /path/to/venv/bin/activate
python /path/to/backend/main.py
```

**Option 2: Changer utilisateur**

```bash
su root
cd backend
source venv/bin/activate
python main.py
```

---

## 📋 Commandes Autorisées (Whitelist)

Seules ces 6 commandes peuvent s'exécuter:

| Commande | Description | Exemple |
|----------|-------------|---------|
| `ifconfig` | Interfaces réseau | `ifconfig` |
| `ip` | Commandes réseau avancées | `ip addr show` |
| `airmon-ng` | Mode monitor Wi-Fi | `airmon-ng start wlan0` |
| `airodump-ng` | Scan Wi-Fi | `airodump-ng wlan0` |
| `ps` | Liste processus | `ps aux` |
| `kill` | Terminer processus | `kill 1234` |

---

## 🚀 Exemples d'Utilisation

### Exemple 1: Afficher les Interfaces Réseau

```
Commande: ifconfig
Arguments: (laisser vide)

Résultat:
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::1  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:26:30:c7  txqueuelen 1000  (Ethernet)
        RX packets 1024  bytes 512000 (512.0 MB)
        TX packets 512  bytes 256000 (256.0 MB)
```

### Exemple 2: Afficher Configuration IP

```
Commande: ip
Arguments: addr show

Résultat:
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 08:00:27:26:30:c7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::1/64 scope link
```

### Exemple 3: Scanner Les Réseaux Wi-Fi

```
Commande: airodump-ng
Arguments: wlan0

Note: L'interface doit exister et supporter le mode monitor
```

### Exemple 4: Lister les Processus

```
Commande: ps
Arguments: aux

Résultat:
USER       PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
root         1  0.1  0.0  19356  1892 ?   Ss   10:00   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?   S    10:00   0:00 [kthreadd]
...
```

---

## 🔒 Sécurité en Mode Réel

### Ce qui est Protégé

✅ **Whitelist stricte** - Seulement 6 commandes
✅ **Authentification requise** - Session admin obligatoire
✅ **Pas de pipes** - `|`, `&&`, `||` interdits dans les arguments
✅ **Pas de redirection** - `>`, `<`, `>>` interdits
✅ **Pas d'escalade** - `sudo`, `su` interdits
✅ **Logs complets** - Chaque commande loggée

### Ce qui EST dangereux

❌ **Les commandes whitelistées s'exécutent vraiment** - `kill` va vraiment terminer un processus
❌ **Les interfaces réseau s'affichent** - Toute info est accessible
❌ **Pas de limite** - Pas de rate-limiting sur le nombre de commandes/minute
❌ **État local** - Les changements affectent le système réel

---

## ⚙️ Configuration Avancée

### Ajouter des Commandes à la Whitelist

Modifiez `backend/app/services/command_execution.py`:

```python
ALLOWED_COMMANDS = {
    "ifconfig": "Affiche les interfaces réseau",
    "ip": "Commandes réseau avancées",
    "airmon-ng": "Activer/désactiver le mode monitor",
    "airodump-ng": "Scanner les réseaux Wi-Fi",
    "ps": "Lister les processus",
    "kill": "Terminer un processus",
    # Ajouter ici:
    "iwconfig": "Affiche config Wi-Fi",
    "nmcli": "Network Manager CLI",
}
```

### Changer la Durée de Session

Modifiez `backend/app/services/command_execution.py`:

```python
SESSION_LIFETIME = 3600  # En secondes (3600 = 1 heure)
# Devenir:
SESSION_LIFETIME = 7200  # 2 heures au lieu de 1
```

---

## 📊 Architecture du Mode Réel

```
┌─────────────────────────────────────────┐
│ Navigateur - Interface Web              │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ POST /api/commands/auth                 │
│ {password: "root_password"}             │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ verify_admin_auth()                     │
│ • Vérifie uid == 0 (root)               │
│ • Crée session_id                       │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ Session ID retourné au client           │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ POST /api/commands/execute              │
│ {command: "ifconfig", session_id: "xxx"}│
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ Vérifications :                         │
│ ✅ Session valide?                      │
│ ✅ Commande en whitelist?               │
│ ✅ Pas de pipe/redirection?             │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ subprocess.run(["ifconfig"])             │
│ Exécute la commande RÉELLEMENT          │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│ Output retourné au client               │
│ Affiché dans le navigateur              │
└─────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### "Authentification échouée"

**Cause:** Vous n'êtes pas root

**Solution:**

```bash
# Vérifiez:
whoami
# Doit afficher: root

# Si ce n'est pas root:
sudo su -
cd /path/to/backend
python main.py
```

### "Commande timeout"

**Cause:** La commande prend trop longtemps (> 30 secondes)

**Solution:**

- Augmentez le timeout dans `command_execution.py`
- Ou utilisez une commande plus simple

### "Pas de sortie"

**Cause:** La commande existe mais ne retourne rien

**Solution:** C'est normal pour certaines commandes (ex: `kill`)

### "Erreur: sh: 1: command not found"

**Cause:** La commande n'existe pas sur le système

**Solution:** 

```bash
# Vérifiez la commande existe:
which ifconfig
which airmon-ng
```

---

## 🚨 Avertissements Importants

### N'UTILISEZ PAS en Production

⚠️ **Cette configuration n'est pas sécurisée pour:**
- Internet public
- Environnement multi-utilisateurs
- Serveurs de production

### À Utiliser Seulement Pour:

✅ Tests locaux
✅ Environnement de laboratoire
✅ Pentest autorités sur réseau fermé
✅ Recherche en cybersécurité
✅ Formation/éducation

### Bonnes Pratiques

1. **Utilisateur dédié**: Créez un compte Linux pour NetShield
2. **Sudo sans mot de passe**: Configurez sudoers pour la commande spécifique
3. **Firewall**: Limitez accès au port 8000/3000
4. **VPN/SSH**: Tunnelez le traffic
5. **Audit logs**: Loggez toutes les commandes
6. **Backups**: Backupez avant de tester

---

## 🔄 Repasser en Mode Simulation

Si vous voulez revenir au mode simulation:

```env
# backend/.env
SIMULATION_MODE=True
```

Puis redémarrez le serveur.

---

## 📞 Support

Pour des problèmes:

1. Consultez ce fichier: `RUN.md` > Mode Réel
2. Vérifiez les logs du serveur: `backend/logs/`
3. Testez manuellement: `sudo bash -c "ifconfig"`
4. Vérifiez les permissions: `id` → doit montrer uid=0

---

**Sécurité d'abord** 🔐

NetShield Mode Réel Linux - À manier avec prudence!
