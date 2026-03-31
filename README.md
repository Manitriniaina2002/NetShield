# NetShield - Wi-Fi Security Audit Lab

Une plateforme web professsionnelle d'audit et de simulation de sécurité Wi-Fi à des fins **éducatives et défensives**.

## ⚠️ AVERTISSEMENT LÉGAL ET ÉTHIQUE

**Cet outil est destiné UNIQUEMENT à :**
- ✅ Des fins éducatives
- ✅ Des tests de sécurité AUTORISÉS (pentest avec consentement écrit)
- ✅ Un environnement contrôlé (laboratoire, sandboxe, test interne)

**Utilisation INTERDITE:**
- ❌ Tout accès NON AUTORISÉ à des réseaux Wi-Fi
- ❌ Tests sur des réseaux tiers SANS CONSENTEMENT EXPLICITE
- ❌ Toute activité violant les lois locales/nationales

**L'utilisateur assume l'entière responsabilité légale de l'utilisation de cet outil.**

---

## 🎯 Objectifs

NetShield fournit une interface graphique professionnelle permettant de :

1. **📡 Exécuter des audits Wi-Fi** - Scanner les réseaux en mode simulation
2. **🔍 Identifier les vulnérabilités** - Détection automatique des faiblesses de sécurité
3. **💡 Générer des recommandations** - Mesures de sécurité automatiques et contextualisées
4. **📄 Produire des rapports** - Rapports PDF professionnels avec analyse complète

---

## 🚀 Démarrage Rapide

### Prérequis

- **Python 3.9+** (Backend)
- **Node.js 16+** (Frontend)
- **pip** (gestionnaire de paquets Python)
- **npm** (gestionnaire de paquets Node.js)

### 1️⃣ Installation du Backend

```bash
# Naviguez dans le répertoire backend
cd backend

# Créez un environnement virtuel
python -m venv venv

# Activez l'environnement (Windows)
venv\Scripts\activate

# ou (Linux/Mac)
source venv/bin/activate

# Installez les dépendances
pip install -r requirements.txt
```

### 2️⃣ Démarrage du Backend

```bash
# Depuis le répertoire backend/
python main.py

# ou avec uvicorn directement
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Le backend sera accessible à : **http://localhost:8000**
- API Docs (Swagger) : http://localhost:8000/api/docs
- ReDoc : http://localhost:8000/api/redoc

### 3️⃣ Installation du Frontend

```bash
# Naviguez dans le répertoire frontend
cd frontend

# Installez les dépendances
npm install
```

### 4️⃣ Démarrage du Frontend

```bash
# Depuis le répertoire frontend/
npm run dev

# L'application sera accessible à : http://localhost:3000
```

---

## 📋 Architecture

```
NetShield/
├── backend/                    # API FastAPI (Python)
│   ├── app/
│   │   ├── api/               # Routes API
│   │   ├── models/            # Modèles Pydantic
│   │   ├── services/          # Logique métier
│   │   ├── utils/             # Utilitaires
│   │   └── config.py          # Configuration
│   ├── main.py                # Point d'entrée
│   └── requirements.txt        # Dépendances
│
└── frontend/                  # Interface React + Vite
    ├── src/
    │   ├── components/        # Composants React
    │   ├── api.js             # Client API
    │   ├── App.jsx
    │   └── main.jsx
    ├── index.html
    └── package.json
```

---

## 🎨 Fonctionnalités Principales

### 1. Dashboard Moderne
- Vue d'ensemble des réseaux Wi-Fi
- Statut et indicateurs temps réel
- Résumé des vulnérabilités détectées

### 2. Scan Wi-Fi Intelligent
- Scanner les réseaux (mode simulation)
- Tableau détaillé avec :
  - **SSID** - Nom du réseau
  - **BSSID** - MAC address du routeur
  - **Canal** - Fréquence utilisée
  - **Sécurité** - Type de chiffrement (Open/WEP/WPA/WPA2/WPA3)
  - **Signal** - Force du signal en dBm et %
  - **Clients** - Nombre d'appareils connectés

### 3. Détection de Risque Automatique
- 🔴 **Critique** - Open, WEP
- 🟠 **Élevé** - WPA faible
- 🟡 **Moyen** - WPA2
- 🟢 **Sécurisé** - WPA2/WPA3 fort

### 4. Analysis de Vulnérabilités
Pour chaque réseau analysé :
- **Réseaux ouverts** - Absence de chiffrement
- **WEP** - Chiffrement obsolète et cassé
- **WPA** - Vulnérable à TKIP
- **Mots de passe faibles** - Sensibilité au cracking
- **WPS** - Protocol faible
- **Configuration** - Paramètres non optimisés

### 5. Recommandations Automatiques
Génération dynamique selon le type de vulnérabilité :

**👉 Réseau OPEN :**
- Activer WPA2 ou WPA3
- Ajouter un mot de passe fort
- Optionnel : désactiver SSID broadcast

**👉 Réseau WEP :**
- Migrer vers WPA2 ou WPA3 immédiatement
- Ne plus utiliser WEP (obsolète)

**👉 WPA/WPA2 faible :**
- Utiliser un mot de passe long (>12 caractères)
- Mélanger majuscules, minuscules, chiffres, symboles
- Activer WPA3 si possible

**👉 Recommandations générales :**
- Activer filtrage MAC
- Désactiver WPS
- Mettre à jour firmware routeur
- Segmenter le réseau (VLAN)
- Surveillance du trafic

### 6. Génération de Rapport PDF
Bouton "Générer Rapport" qui crée un PDF professionnel contenant :

📄 **Page de Garde**
- Nom du projet
- Date d'audit
- Auteur

📊 **Contenu**
1. Résumé exécutif
2. Réseaux détectés (tableau avec détails)
3. Vulnérabilités identifiées (avec sévérité)
4. Méthodologie de test utilisée
5. Recommandations détaillées
6. Évaluation du risque global
7. Conclusion et prochaines étapes

### 7. Terminal Intégré (Optional)
- Affichage des commandes exécutées
- Logs en temps réel
- Historique des actions

### 8. Sécurité de l'Application
- ✅ Mode simulation (safe mode)
- ✅ Confirmation avant commandes sensibles
- ✅ Journalisation complète
- ✅ Sandbox pour exécution des commandes
- ✅ Message légal obligatoire

---

## 📊 API Endpoints

### Scan Wi-Fi
```
POST /api/scan/networks
  - Paramètres: duration (5-60s), name
  - Retour: Liste des réseaux détectés

GET /api/scan/networks/{bssid}
  - Retour: Détails d'un réseau spécifique
```

### Vulnérabilités
```
POST /api/vulnerabilities/analyze/{bssid}
  - Paramètres: Données du réseau
  - Retour: Vulnérabilités identifiées

POST /api/vulnerabilities/analyze-batch
  - Paramètres: Liste de réseaux
  - Retour: Synthèse des vulnérabilités
```

### Recommandations
```
POST /api/recommendations/generate
  - Paramètres: Vulnérabilités, Réseaux
  - Retour: Recommandations générées

GET /api/recommendations/by-priority/{priority}
GET /api/recommendations/by-category/{category}
```

### Rapports
```
POST /api/reports/pdf
  - Paramètres: Données du rapport
  - Retour: PDF généré

POST /api/reports/json
  - Retour: Données JSON du rapport

POST /api/reports/save
  - Retour: Chemin du fichier sauvegardé
```

### Commandes
```
GET /api/commands/allowed
  - Retour: Commandes autorisées

POST /api/commands/execute
  - Paramètres: Command, args
  - Retour: Résultat d'exécution
```

---

## 🔐 Mode Simulation

Par défaut, l'application s'exécute en **mode simulation sécurisé**:

- ✅ Aucune exécution réelle de commandes Wi-Fi
- ✅ Données synthétiques réalistes
- ✅ Pas de risque pour les réseaux
- ✅ Idéal pour l'apprentissage et les tests

Pour activer le mode réel (Linux uniquement):
1. Modifier `SIMULATION_MODE=False` dans `.env`
2. S'assurer que `airmon-ng` et `airodump-ng` sont installés
3. Exécuter avec privilèges root

---

## 📚 Exemples d'Utilisation

### Audit complet d'un environnement
```
1. Cliquer "Démarrer un Scan"
2. Attendre les résultats
3. Vérifier les vulnérabilités détectées
4. Consulter les recommandations
5. Générer un rapport PDF
6. Envoyer le rapport au responsable IT
```

### Tester une configuration spécifique
```
1. Analyser un réseau spécifique
2. Voir les vulnérabilités potentielles
3. Suivre les étapes de correction
4. Valider les changements
```

---

## 🛠️ Dépannage

### Le backend ne s'exécute pas
```bash
# Vérifier que Python 3.9+ est installé
python --version

# Vérifier les erreurs dans requirements.txt
pip install -r requirements.txt --force-reinstall
```

### Le frontend ne se connecte pas au backend
```bash
# Vérifier que le backend s'exécute
curl http://localhost:8000/health

# Vérifier la configuration CORS dans app/config.py
# Vérifier les origins autorisés
```

### Les rapports PDF ne génèrent pas
```bash
# Vérifier que reportlab est installé
pip install reportlab --force-reinstall
```

---

## 📝 Configuration

### Backend (.env)
```env
DEBUG=False                    # Mode debug (développement)
CORS_ORIGINS=[...]            # Origines autorisées
BACKEND_HOST=127.0.0.1        # Hôte du serveur
BACKEND_PORT=8000             # Port du serveur
SIMULATION_MODE=True          # Mode simulation (recommandé)
REQUIRE_CONFIRMATION=True     # Confirmation avant actions
```

### Frontend (vite.config.js)
```javascript
// Configurer le proxy API
proxy: {
  '/api': {
    target: 'http://localhost:8000'
  }
}
```

---

## 🎓 Cas d'Utilisation Éducatifs

1. **Formation en cybersécurité** - Comprendre les vulnérabilités Wi-Fi
2. **Audit interne** - Vérifier la conformité de sa propre infrastructure
3. **Pentest autorisé** - Tests de sécurité avec consentement
4. **Démonstration** - Présenter les risques de sécurité Wi-Fi
5. **Laboratoire** - Environnement d'apprentissage sécurisé

---

## 📦 Technologies Utilisées

### Backend
- **FastAPI** - Framework web asynchrone
- **Pydantic** - Validation de données
- **ReportLab** - Génération PDF
- **Python 3.9+**

### Frontend
- **React 18** - Bibliothèque UI
- **Vite** - Bundler ultra-rapide
- **TailwindCSS** - Styling moderne
- **Axios** - Client HTTP
- **Chart.js** - Graphiques (optionnel)

---

## 📄 Licence

Cet outil est fourni à titre éducatif uniquement. Les utilisateurs sont responsables de son utilisation légale et éthique.

---

## 🤝 Support et Contribution

Pour les questions ou problèmes :
1. Consulter la documentation API : http://localhost:8000/api/docs
2. Vérifier les logs du backend et frontend
3. Valider la configuration

---

## 🎯 Feuille de Route

- [ ] Mode pentest réel (Linux)
- [ ] Historique des audits
- [ ] Système de rôles utilisateurs
- [ ] Base de données persistante
- [ ] Export CVSS/CVE
- [ ] Intégration Slack/Email
- [ ] Dark mode avancé
- [ ] Tests de sécurité additionnels

---

**Développé avec ❤️ pour la cybersécurité défensive**

*Dernière mise à jour : 2024*
