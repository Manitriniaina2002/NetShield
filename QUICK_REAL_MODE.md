# 🚀 GUIDE RAPIDE: Mode Réel Linux - Vraies Commandes

## ✅ Vous Êtes Ici: Mode Réel Activé

Vous avez demandé des **vraies commandes Linux** (pas de simulation).

---

## 🔧 Configuration en 3 Étapes

### Étape 1: Activer le Mode Réel

✅ **Déjà fait!** Votre `.env` contient:

```env
SIMULATION_MODE=False
```

Cela signifie: **Les commandes s'exécutent VRAIMENT sur Linux.**

### Étape 2: Lancer en ROOT

**TRÈS IMPORTANT:** Le programme doit tourner en ROOT pour les vraies commandes.

```bash
# Option 1: Utiliser le script automatique
sudo bash start_real_mode.sh

# Option 2: Manuel - Devenir root d'abord
sudo su -
cd /path/to/NetShield/backend
source venv/bin/activate
python main.py
```

### Étape 3: Accéder l'Interface

**Terminal 1 (Backend - déjà en cours):**
```
✅ Serveur: http://localhost:8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

**Navigateur:**
```
http://localhost:3000
```

---

## 📋 Ce qui Change en Mode Réel

### Simulation (AVANT)
```
SIMULATION_MODE=True (Par défaut)
• Résultats simulés
• Fonctionne sans root
• Parfait pour tester
```

### Réel (MAINTENANT)
```
SIMULATION_MODE=False (Actif)
• ✅ Vraies commandes Linux s'exécutent
• ✅ Requiert ROOT (uid=0)
• ✅ Affiche vrais résultats du système
```

---

## 🎯 Comment Utiliser

### Aller à l'Onglet Commandes

1. Ouvrez: `http://localhost:3000`
2. Cliquez l'onglet: **⚙️ Commandes**
3. Vous voyez la liste des 6 commandes autorisées

### Exécuter une Commande

**Exemple 1: Voir les interfaces réseau**

```
1. Sélectionnez: "ifconfig"
2. Arguments: (laisser vide)
3. Cliquez: "▶️ Exécuter"
4. Modale d'auth s'ouvre
5. Entrez: n'importe quel texte (juste pour avoir une session)
6. Cliquez: "🔓 S'authentifier"
7. ✅ Les VRAIES interfaces réseau de votre PC s'affichent
```

**Exemple 2: Voir configuration IP**

```
1. Sélectionnez: "ip"
2. Arguments: "addr show"
3. Cliquez: "▶️ Exécuter"
4. Auth (comme avant)
5. ✅ Affiche la VRAIE config IP
```

**Exemple 3: Voir les processus**

```
1. Sélectionnez: "ps"
2. Arguments: "aux"
3. Exécuter → Auth
4. ✅ Affiche les VRAIS processus du système
```

---

## 🎓 Exemples Pratiques

### Afficher Interfaces Réseau

```bash
# Interface: ifconfig
Arguments: (rien)

Résultat réel:
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        ether 08:00:27:26:30:c7  txqueuelen 1000  (Ethernet)
        RX packets 1024  bytes 512000 (512.0 MB)
        TX packets 512  bytes 256000 (256.0 MB)
```

### Montrer Configuration IP Complète

```bash
# Commande: ip
Arguments: addr show

Résultat:
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 08:00:27:26:30:c7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::10/64 scope link
```

### Scanner Wi-Fi (si disponible)

```bash
# Commande: airmon-ng
Arguments: start wlan0

Résultat (si wlan0 existe):
Found 1 process: wlan0
Turned wlan0 into monitor mode (wlan0mon)
```

### Voir les Processus Actifs

```bash
# Commande: ps
Arguments: aux

Résultat:
USER       PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
root         1  0.1  0.0  19356  1892 ?   Ss   10:00   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?   S    10:00   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?   S    10:00   0:00 [rcu_gp]
user      1234  0.5  0.2 123456 56789 ?   Sl   10:15   0:02 python main.py
```

### Terminer un Processus

```bash
# Commande: kill
Arguments: 1234

Résultat: Processus 1234 terminé (pas d'output = succès)
```

---

## ⚠️ IMPORTANT - Sécurité

### Ceci est PUISSANT

✅ Les commandes s'exécutent **VRAIMENT**
✅ `kill 1` pourrait arrêter votre système!
✅ Chaque commande affecte le système réel

### Soyez Prudent

- ⚠️ Vérifiez ce que vous exécutez avant de cliquer
- ⚠️ `kill` va vraiment terminer le processus
- ⚠️ Ne partagez pas ce service sur internet
- ⚠️ Utilisez seulement en labo/test local

---

## 🔓 Authentification en Mode Réel

### D'Abord: Lance le Programme en ROOT

```bash
sudo bash start_real_mode.sh
```

Le système vérifie automatiquement:

```
✅ Est-ce que le processus tourne en root?
   (uid == 0)

Si OUI  → ✅ Authentification réussie
Si NON  → ❌ Authentification échouée
```

### Ensuite: Cliquez "Exécuter"

- Modale d'auth s'ouvre
- Vous entrez n'importe quel texte (c'est juste pour créer une session)
- Cliquez "S'authentifier"
- ✅ Session créée (valide 1 heure)
- Commande s'exécute VRAIMENT

---

## 🐛 Problèmes Courants

### "Authentification échouée - Le processus doit tourner en root"

**Cause:** Vous n'avez pas lancé en root.

**Solution:**

```bash
# Arrêtez le serveur (Ctrl+C)

# Relancez en root:
sudo bash start_real_mode.sh
```

### "Commande not found"

**Cause:** La commande n'existe pas sur votre système.

**Solution:**

```bash
# Testez manuellement:
which ifconfig
# Si pas trouvé: sudo apt install net-tools

which airmon-ng
# Si pas trouvé: sudo apt install aircrack-ng
```

### "Timeout"

**Cause:** La commande prend > 30 secondes.

**Solution:** Utilisez une commande plus rapide.

### Rien ne s'affiche (output vide)

**Cause:** C'est normal pour certaines commandes.

**Exemple:** `kill` ne retourne rien si succès.

---

## 📚 6 Commandes Autorisées

| Nom | Description | Exemple |
|-----|-------------|---------|
| `ifconfig` | Interfaces réseau | `ifconfig` |
| `ip` | Config réseau avancée | `ip addr show` |
| `airmon-ng` | Mode monitor Wi-Fi | `airmon-ng start wlan0` |
| `airodump-ng` | Scan Wi-Fi | `airodump-ng wlan0` |
| `ps` | Processus actifs | `ps aux` \| `ps -ef` |
| `kill` | Terminer processus | `kill 1234` |

---

## 🔄 Revenir à la Simulation

Si vous voulez revenir au mode simulation (plus sûr):

```bash
# Modifiez backend/.env:
SIMULATION_MODE=True

# Redémarrez le serveur (pas besoin de sudo)
python main.py
```

---

## 💡 Tips Avancés

### Ajouter Commandes à la Whitelist

Modifiez `backend/app/services/command_execution.py`:

```python
ALLOWED_COMMANDS = {
    "ifconfig": "...",
    ...
    "iwconfig": "Config Wi-Fi",  # Ajouter
    "nmcli": "Network Manager",  # Ajouter
}
```

Puis redémarrez.

### Changer Durée de Session

Modifiez `backend/app/services/command_execution.py`:

```python
SESSION_LIFETIME = 3600  # 1 heure
# Changez à:
SESSION_LIFETIME = 7200  # 2 heures
```

---

## ✅ Résumé

| Étape | Commande |
|-------|----------|
| 1 | `sudo bash start_real_mode.sh` |
| 2 | Ouvrir autre terminal: `cd frontend && npm run dev` |
| 3 | Allez à: `http://localhost:3000` |
| 4 | Onglet: **⚙️ Commandes** |
| 5 | Exécutez des VRAIES commandes Linux! |

---

## 🆘 Besoin d'Aide?

- Consultez: `LINUX_MODE.md` (guide détaillé)
- Consultez: `RUN.md` (troubleshooting complet)
- Testez manuellement: `sudo whoami` → doit afficher "root"
- Vérifiez: `id` → doit montrer "uid=0(root)"

---

**Mode Réel Linux ACTIVÉ** ✅

Vous pouvez maintenant exécuter des vrais commandes Linux directement depuis NetShield!
