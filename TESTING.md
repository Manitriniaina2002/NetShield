# 🧪 Test Rapide - NetShield

Fichier pour tester rapidement la fonctionnalité après installation.

## ✅ Checklist de Test

### 1️⃣ Backend Santé
```bash
# Vérifier que le backend répond
curl http://localhost:8000/

# Réponse attendue:
# {"message":"Bienvenue sur NetShield...","version":"1.0.0",...}
```
**Status**: ✅ OK / ❌ ERREUR

### 2️⃣ API Documentation  
```bash
# Ouvrir dans navigateur
http://localhost:8000/api/docs

# Vérifier: Interface Swagger chargée avec endpoints listés
```
**Status**: ✅ OK / ❌ ERREUR

### 3️⃣ Santé API
```bash
# Requête test
curl http://localhost:8000/health

# Réponse attendue:
# {"status":"healthy","app_name":"NetShield...","version":"1.0.0",...}
```
**Status**: ✅ OK / ❌ ERREUR

### 4️⃣ Frontend Accessible
```bash
# Ouvrir dans navigateur
http://localhost:3000

# Vérifier: Page chargée avec header NetShield bleu visible
```
**Status**: ✅ OK / ❌ ERREUR

### 5️⃣ Scan Wi-Fi
```javascript
// Dans console navigateur (F12)
const response = await fetch('http://localhost:8000/api/scan/networks?duration=5&name=Test');
const data = await response.json();
console.log(data.networks_found, 'réseaux détectés');

// Réponse attendue:
// 6 réseaux détectés
```
**Status**: ✅ OK / ❌ ERREUR

### 6️⃣ Interface Dashboard
```
Actions dans l'interface:
1. Bouton "🔍 Démarrer un Scan" → clicker
2. Attendre ~10 secondes
3. Vérifier que tableau se remplit (6 réseaux)
4. Vérifier couleurs (red=danger, orange=warning, yellow=medium, green=safe)
```
**Status**: ✅ OK / ❌ ERREUR

### 7️⃣ Analyse Vulnérabilité
```
1. Après scan, cliquer "Analyser" sur un réseau
2. Aller à onglet "Vulnérabilités"
3. Vérifier que vulnérabilités apparaissent
4. Vérifier descriptions complètes
```
**Status**: ✅ OK / ❌ ERREUR

### 8️⃣ Recommandations
```
1. Aller à onglet "Recommandations"
2. Vérifier que recommandations apparaissent
3. Vérifier groupement par priorité (Critique/Élevée/Moyen/Faible)
4. Vérifier étapes détaillées pour chaque
```
**Status**: ✅ OK / ❌ ERREUR

### 9️⃣ Rapport PDF
```
1. Aller à onglet "Rapport"  
2. Cliquer "Générer PDF"
3. Vérifier que fichier se télécharge
4. Ouvrir PDF et vérifier contenu:
   - Page de garde
   - Tableau réseaux
   - Vulnérabilités
   - Recommandations
   - Score de risque
```
**Status**: ✅ OK / ❌ ERREUR

### 🔟 Export JSON
```
1. Onglet "Rapport" toujours visible
2. Cliquer "Exporter JSON"
3. Vérifier que fichier JSON se télécharge
4. Ouvrir et vérifier structure:
   - Root object
   - Arrays: networks, vulnerabilities, recommendations
```
**Status**: ✅ OK / ❌ ERREUR

### 1️⃣1️⃣ Mentions Légales
```
1. Cliquer bouton "⚠️ Mentions Légales" en haut droite
2. Vérifier modal s'affiche
3. Vérifier texte:
   - AVERTISSEMENT LÉGAL
   - Utilisation Autorisée
   - Utilisation Interdite
   - Clause responsabilité
4. Cliquer "J'ai compris" pour fermer
```
**Status**: ✅ OK / ❌ ERREUR

---

## 🐛 Dépannage Test

### Backend URL ne répond pas
```bash
# Vérifier que backend s'exécute
# Terminal backend doit montrer: "Uvicorn running on http://127.0.0.1:8000"

# Si absent, relancer:
cd backend
python main.py
```

### Frontend n'affiche rien
```bash
# Vérifier console développeur (F12)
# Vérifier qu'aucune erreur CORS

# Relancer frontend:
cd frontend
npm run dev
```

### Scan retourne 0 réseaux
```bash
# Vérifier que backend fonctionne
curl http://localhost:8000/api/scan/networks

# Simulé, doit toujours retourner 6 réseaux
# Si problème, vérifier backend logs
```

### PDF ne génère pas
```bash
# Vérifier que reportlab est installé
pip list | grep reportlab

# Si absent:
pip install reportlab
```

---

## 📊 Résultats Attendus

### Scan
- **Réseaux détectés**: 6
- **Noms**: FreeFi_Public, CoffeShop_WiFi, HomeNetwork, SecureOffice, ModernHome, HiddenNetwork
- **Sécurités**: Open, WEP, WPA, WPA2, WPA3, WPA2
- **Couleurs**: Rouge, Rouge, Orange, Jaune, Vert, Jaune

### Vulnérabilités  
- **Critiques**: 2 (Open, WEP)
- **Élevées**: 2-3 (WPA)
- **Moyennes**: 3-4 (WPA2, détails additionnels)
- **Total**: 15-25 vulnérabilités

### Recommandations
- **Critiques**: 2-3 (chiffrement)
- **Élevées**: 3-4 (configuration)
- **Moyennes**: 2-3 (maintenance)
- **Générales**: 4-5 (architecture)
- **Total**: 10-15 recommandations

### Score Risque
- Pour 6 réseaux mixtes: 50-70/100 (Moyen à Élevé)
- Baseline critique attendue: 70-80/100

### PDF
- **Page 1**: Couverture
- **Page 2**: Sommaire
- **Page 3**: Résumé exécutif
- **Pages suivantes**: Détails
- **Dernières**: Conclusion
- **Total**: 5-8 pages

---

## ⏱️ Temps Attendus

| Opération | Temps |
|-----------|-------|
| Backend démarrage | 2-3 sec |
| Frontend démarrage | 3-5 sec |
| Accès interface | <2 sec |
| Scan Wi-Fi | 10 sec |
| Analyse | 1 sec |
| PDF génération | 2-5 sec |
| Total audit | 15-20 sec |

---

## 🎯 Critères de Succès

✅ **Test réussi si:**
- [x] Tous les endpoints répondent
- [x] Interface charge sans erreur
- [x] Scan retourne 6 réseaux
- [x] Vulnérabilités détectées automatiquement
- [x] Recommandations générées
- [x] PDF généré et téléchargeable
- [x] Mentions légales affichées
- [x] Aucune erreur console
- [x] Performances < 20 sec par audit complet

---

## 📝 Log Test

```
Date: [Remplir]
Heure: [Remplir]
Testeur: [Remplir]

Test Backend Health: ☐ OK / ☐ KO
Test API Docs: ☐ OK / ☐ KO
Test Frontend: ☐ OK / ☐ KO
Test Scan: ☐ OK / ☐ KO
Test Vulnerabilities: ☐ OK / ☐ KO
Test Recommendations: ☐ OK / ☐ KO
Test PDF: ☐ OK / ☐ KO
Test JSON: ☐ OK / ☐ KO
Test Notices: ☐ OK / ☐ KO

Résultat global: ☐ PASS / ☐ FAIL

Remarques:
[Ajouter observations]

Performance:
Backend: ___ ms
Frontend: ___ ms  
Scan: ___ sec
PDF: ___ sec

Signature: ___________
```

---

## 🚀 Prochaines Étapes après Test

Si tous les tests passent (☑️):
1. ✅ Application prête production/éducation
2. ✅ Créer scénarios audit réalistes
3. ✅ Former utilisateurs
4. ✅ Mettre en place backups rapports
5. ✅ Monitorer performances

Si tests échouent (❌):
1. ❌ Consulter INSTALL.md
2. ❌ Vérifier logs détaillés
3. ❌ Relancer clean installation
4. ❌ Contacter support

---

**Testing complet en ~15 minutes ⏱️**
