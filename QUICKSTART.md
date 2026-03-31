# NetShield - Quick Start Guide

## ⚡ Démarrage rapide (< 5 minutes)

### Windows
```batch
start.bat
```

### Linux / Mac
```bash
chmod +x start.sh
./start.sh
```

---

## 🎯 Première utilisation

1. **Accédez à l'application**
   - Ouvrez http://localhost:3000 dans votre navigateur

2. **Consultez les mentions légales**
   - Cliquez sur "⚠️ Mentions Légales" en haut à droite
   - Confirmez que vous acceptez les conditions

3. **Lancez votre premier scan**
   - Cliquez sur "🔍 Démarrer un Scan"
   - Attendez ~10 secondes pour les résultats

4. **Explorez les résultats**
   - **Onglet Vue d'ensemble**: Tableau des réseaux détectés
   - **Onglet Vulnérabilités**: Faiblesses identifiées
   - **Onglet Recommandations**: Actions correctives
   - **Onglet Rapport**: Génération de documentations

5. **Générez un rapport**
   - Allez à "Rapport"
   - Cliquez "Générer PDF"
   - Téléchargez le fichier

---

## 📊 Compréhension des Résultats

### Niveaux de Sécurité
- 🔓 **Open** = Pas de chiffrement (CRITIQUE)
- 🔴 **WEP** = Chiffrement obsolète (CRITIQUE)
- 🟠 **WPA** = Chiffrement plus faible (ÉLEVÉ)
- 🟡 **WPA2** = Chiffrement moderne (MOYEN)
- 🟢 **WPA3** = Meilleur chiffrement (SÉCURISÉ)

### Score de Risque
- **0-20**: Très faible risque ✓
- **20-40**: Risque faible
- **40-60**: Risque modéré ⚖️
- **60-80**: Risque élevé ⚠️
- **80-100**: Risque critique 🔴

---

## 📚 Cas d'Utilisation Courants

### Audit maison
1. Scanner votre réseau Wi-Fi personnel
2. Vérifier la sécurité
3. Appliquer les recommandations
4. Rescan après changements

### Formation
1. Analyser plusieurs réseaux fictifs
2. Comprendre les vulnérabilités
3. Apprendre les mesures correctives
4. Générer des rapports d'étude

### Pentest autorisé
1. Scanner l'infrastructure client
2. Documenter les résultats
3. Générer un rapport professionnel
4. Présenter les recommandations

---

## 🔗 Ressources Utiles

- **API Documentation**: http://localhost:8000/api/docs
- **Backend Logs**: Vérifier la console du backend
- **Frontend Logs**: Ouvrir Dev Tools (F12)
- **GitHub Issues**: Signaler les problèmes

---

## ⚠️ Points Importants

✅ **Autorisé:**
- Auditer votre propre réseau
- Tests dans un environnement de lab
- Usage éducatif
- Pentest avec consentement écrit

❌ **Interdit:**
- Tester sans authorization
- Réseaux d'autrui
- Usages malveillants
- Violation de lois

---

## 🆘 Dépannage Rapide

**Le backend démarre pas?**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python main.py
```

**Le frontend ne charge pas?**
```bash
cd frontend
rm -rf node_modules  # ou rmdir /s node_modules sur Windows
npm install
npm run dev
```

**Connexion API refusée?**
- Vérifier que le backend s'exécute: http://localhost:8000/health
- Vérifier les CORS dans backend/app/config.py
- Essayer d'accéder à http://localhost:8000/api/docs

---

**🎉 Profitez bien de NetShield!**
