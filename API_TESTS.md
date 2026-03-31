# API Tests

Collection de reqêtes pour tester l'API NetShield.

## Base URL
```
http://localhost:8000
```

## 1. Info Application
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/api/info
```

## 2. Scan Wi-Fi
```bash
# Lancer un scan
curl -X POST "http://localhost:8000/api/scan/networks?duration=10&name=TestScan"

# Récupérer détails d'un réseau
curl "http://localhost:8000/api/scan/networks/AA:11:22:33:44:55?channel=6"
```

## 3. Analyse Vulnérabilités
```bash
# Analyser un réseau
curl -X POST "http://localhost:8000/api/vulnerabilities/analyze/AA:11:22:33:44:55" \
  -H "Content-Type: application/json" \
  -d '{"ssid":"TestNet","bssid":"AA:11:22:33:44:55","channel":6,"frequency":"2.4GHz","security":"Open","signal_strength":-50,"clients":5}'

# Analyser par batch
curl -X POST "http://localhost:8000/api/vulnerabilities/analyze-batch" \
  -H "Content-Type: application/json" \
  -d '[...]'
```

## 4. Recommandations
```bash
# Générer recommandations
curl -X POST "http://localhost:8000/api/recommendations/generate" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## 5. Rapports
```bash
# Générer PDF
curl -X POST "http://localhost:8000/api/reports/pdf" \
  -H "Content-Type: application/json" \
  -d '{...}' \
  > report.pdf

# Exporter JSON
curl -X POST "http://localhost:8000/api/reports/json" \
  -H "Content-Type: application/json" \
  -d '{...}' \
  > report.json
```

## 6. Commandes
```bash
# Lister commandes autorisées
curl "http://localhost:8000/api/commands/allowed"

# Exécuter commande
curl -X POST "http://localhost:8000/api/commands/execute?command=ifconfig"
```

## Utiliser Postman/Insomnia

- Importer la collection des endpoints
- Configurer l'environnement (localhost:8000)
- Exécuter les tests

---

**Pour plus de détails, consulter /api/docs**
