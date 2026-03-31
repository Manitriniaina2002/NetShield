# 🔐 Guide: Panneau de Commandes Système Sécurisé

## Vue d'ensemble

NetShield inclut maintenant un **Panneau de Commandes Système Sécurisé** permettant d'exécuter des commandes système directement depuis l'interface web, **sans ouvrir de terminal**.

Toutes les exécutions requièrent une **authentification administrateur par mot de passe** au préalable.

---

## 🔒 Sécurité

### Mesures de Sécurité Implémentées

1. **Authentification Obligatoire**
   - Chaque exécution de commande requiert une authentification admin
   - Le mot de passe est demandé via une modale sécurisée
   - Sessions de 1 heure de durée

2. **Whitelist de Commandes**
   - Seules les commandes sûres et autorisées peuvent s'exécuter
   - Liste des commandes autorisées:
     - `ifconfig` - Affiche les interfaces réseau
     - `ip` - Commandes réseau avancées
     - `airmon-ng` - Mode monitor Wi-Fi
     - `airodump-ng` - Scan Wi-Fi
     - `ps` - Liste des processus
     - `kill` - Terminer un processus

3. **Gestion des Sessions**
   - Session ID unique par authentification
   - Durée de vie: 1 heure
   - Session invalide = re-authentification requise

4. **Pas de Stockage de Mot de Passe**
   - Le mot de passe n'est jamais stocké
   - Passé uniquement en HTTPS (en production)
   - Vidé après authentification

---

## 📖 Comment Utiliser

### Accéder au Panneau de Commandes

1. Lancez l'application NetShield
2. Cliquez sur l'onglet **⚙️ Commandes** dans le Dashboard
3. Le panneau de commandes s'affiche

### Exécuter une Commande

**Première exécution:**

1. Sélectionnez une commande dans la liste
2. (Optionnel) Entrez les arguments dans le champ texte
3. Cliquez sur **▶️ Exécuter**
4. Une modale d'authentification s'ouvre
5. Entrez votre mot de passe administrateur
6. Cliquez sur **🔓 S'authentifier**
7. La commande s'exécute et le résultat s'affiche

**Exécutions suivantes (session active):**

1. Sélectionnez une commande
2. (Optionnel) Entrez les arguments
3. Cliquez sur **▶️ Exécuter**
4. La commande s'exécute immédiatement (pas de re-authentification pendant 1 heure)

### Déconnexion

Cliquez sur le bouton **🚪 Déconnecter** pour terminer la session et forcer une re-authentification à la prochaine exécution.

---

## 📱 Interface du Panneau

### Zone de Sélection (à gauche)

- **Liste de commandes**: Sélectionnez une commande autorisée
- **Champ d'arguments**: Entrez les paramètres optionnels
- **Boutons d'action**: Exécuter ou Déconnecter

### Zone d'Information (à droite)

- **Sécurité**: Rappel des mesures de sécurité
- **Whitelist**: Confirmation des commandes autorisées
- **Statut**: État d'authentification
- **Session**: Durée de vie de la session

### Zone de Résultat (bas de page)

Affiche le résultat (output) de la commande exécutée en format texte.

---

## 🔑 Authentification Détaillée

### Modale d'Authentification

La modale affiche:

1. **Avertissement en rouge**: Type d'authentification requise
2. **Aperçu de la commande**: Exactement ce qui va s'exécuter
3. **Champ mot de passe**: Entrée sécurisée du mot de passe
4. **Bouton "Montrer"**: Révèle/cache le mot de passe
5. **Avertissement de sécurité**: Mise en garde légale
6. **Boutons**: Annuler ou S'authentifier

### Process d'Authentification

```
Utilisateur                API Backend
     |                          |
     |-- POST /api/commands/auth
     |     { password: "xxx" }
     |                          |
     |                          |-- Vérifier permissions admin/root
     |                          |
     |                          |-- Créer session ID unique
     |                          |
     |                          |-- Retourner session_id
     |<-- 200 OK
     |     { session_id: "uuid-xxxxx" }
     |
     |-- Utiliser session_id pour exécuter commandes
```

---

## 💻 Mode Simulation vs Mode Réel

### Mode Simulation (Par défaut)

- ✅ Fonctionne sur tous les systèmes
- ✅ Accepte tout mot de passe valide (min. 4 caractères)
- ✅ Retourne des résultats simulés réalistes
- ✅ Parfait pour tester et former

**Activation**: Défaut dans `.env` → `SIMULATION_MODE=True`

### Mode Réel (Linux ou Windows Admin)

- 🐧 Requiert Linux (pour les vrai commandes Wi-Fi)
- 🪟 Requiert Windows Admin (privilèges)
- Exécute **véritablement** les commandes système
- ⚠️ À utiliser avec extrême prudence

**Activation**: Modifier `.env` → `SIMULATION_MODE=False`

---

## 🔧 Exemples d'Utilisation

### Exemple 1: Afficher les Interfaces Réseau

1. Sélectionner: `ifconfig`
2. Arguments: (laisser vide)
3. Exécuter
4. Affiche toutes les interfaces réseau de l'ordinateur

### Exemple 2: Activer le Mode Monitor Wi-Fi

1. Sélectionner: `airmon-ng`
2. Arguments: `start wlan0`
3. Exécuter
4. Active le mode monitor sur wlan0 (si disponible)

### Exemple 3: Lister les Processus Actifs

1. Sélectionner: `ps`
2. Arguments: (laisser vide)
3. Exécuter
4. Affiche les processus actuels du système

---

## 🛡️ Bonnes Pratiques de Sécurité

### Pour les Administrateurs

1. **Utilisez des mots de passe forts**: Min. 4 caractères, idéalement complexes
2. **Déconnectez-vous**: Cliquez **🚪 Déconnecter** après chaque session importante
3. **Vérifiez les commandes**: Lisez l'aperçu avant de confirmer
4. **En production**: Activez HTTPS et authentification robuste
5. **Logs**: Consultez les logs du serveur pour l'audit

### Pour les Utilisateurs

1. **Ne partagez pas** votre mot de passe administrateur
2. **Vérifiez les commandes** avant d'accepter dans la modale
3. **Attendez** la confirmation visuelle avant supposant exécution
4. **Contactez l'admin** si quelque chose semble suspect

---

## ⚠️ Limitations et Restrictions

### Commandes Non Autorisées

❌ Les commandes suivantes **ne peuvent PAS** s'exécuter:
- `rm`, `dd`, `format` (destruction de données)
- `sudo`, `su` (escalade de privilèges)
- `curl`, `wget` (téléchargements arbitraires)
- N'importe quelle autre commande non dans la whitelist

### Erreurs Possibles

| Erreur | Cause | Solution |
|--------|-------|----------|
| "Authentification échouée" | Mot de passe incorrect | Vérifiez le mot de passe |
| "Commande non autorisée" | Commande non dans la whitelist | Sélectionnez une commande autorisée |
| "Session expirée" | 1 heure dépassée | Re-authentifiez-vous |
| "Erreur de connexion" | Backend indisponible | Vérifiez que le serveur tourne |

---

## 🔌 Intégration API

### Endpoints Disponibles

#### 1. Obtenir les Commandes Autorisées
```bash
GET /api/commands/allowed
# Retourne la liste des commandes autorisées
```

#### 2. S'authentifier
```bash
POST /api/commands/auth
Content-Type: application/json

{
  "password": "admin123"
}

# Retourne:
{
  "success": true,
  "session_id": "uuid-xxxxx",
  "expires_in": 3600,
  "message": "Authentification réussie"
}
```

#### 3. Exécuter une Commande
```bash
POST /api/commands/execute
Content-Type: application/json

{
  "command": "ifconfig",
  "args": [],
  "session_id": "uuid-xxxxx"
}

# Retourne:
{
  "success": true,
  "output": "wlan0: flags=4163...",
  "code": 0
}
```

#### 4. Exécuter avec Double Confirmation
```bash
POST /api/commands/execute-safe
?command=airmon-ng&args=start+wlan0&session_id=uuid-xxxxx&confirmed=true
```

---

## 🐛 Troubleshooting

### "Modale d'auth ne s'ouvre pas"
- Vérifiez que le backend tourne: `http://localhost:8000`
- Vérifiez les logs du navigateur (F12)
- Redémarrez l'application

### "Password accepted mais pas d'exécution"
- Vérifiez la session n'a pas expiré
- Cliquez Déconnecter → re-authentifiez
- Vérifiez la commande est dans la whitelist

### "Résultat vide/timeout"
- En mode simulation: résultats simulés
- En mode réel: la commande est peut-être lente
- Augmentez le timeout dans `app/services/command_execution.py`

---

## 🚀 Prochaines Étapes

### Améliorations Prévues

1. **Token JWT**: Remplacer session ID simples par JWT sécurisés
2. **2FA**: Authentification à deux facteurs
3. **Logs complets**: Audit trail de toutes les commandes
4. **Permissions granulaires**: Définir qui peut exécuter quoi
5. **Scripts**: Enregistrer et rejouer des séquences de commandes
6. **Rate limiting**: Limiter le nombre d'exécutions par minute
7. **HTTPS obligatoire**: Chiffrer les communications en production

---

## 📞 Support

Pour des questions:
1. Consultez la documentation complète: `README.md`
2. Vérifiez `RUN.md` pour le troubleshooting
3. Examinez les logs du serveur: `backend/logs/`
4. Testez l'API directement avec `curl` ou Postman

---

**Sécurité d'abord™** 🔐

NetShield - Plateforme d'Audit de Sécurité Wi-Fi Éducative
