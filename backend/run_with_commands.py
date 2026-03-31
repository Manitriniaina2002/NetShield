#!/usr/bin/env python3
"""
Script de test pour le système de commandes avec authentification admin
Lance le serveur backend et affiche les informations d'accès
"""

import subprocess
import sys
import time
import platform

def main():
    print("=" * 60)
    print("🔐 NetShield - Panneau de Commandes Sécurisé")
    print("=" * 60)
    print()
    
    # Vérifier l'environnement
    is_windows = platform.system() == "Windows"
    venv_dir = "venv" if is_windows else "venv"
    
    print("📋 Configuration:")
    print(f"  • OS: {platform.system()}")
    print(f"  • Python: {sys.version.split()[0]}")
    print()
    
    # Étape 1: Activer venv
    print("1️⃣  Activation de l'environnement virtuel...")
    if is_windows:
        activate_cmd = f"{venv_dir}\\Scripts\\activate.bat && python -m pip install -r requirements.txt"
    else:
        activate_cmd = f"source {venv_dir}/bin/activate && python -m pip install -r requirements.txt"
    
    try:
        subprocess.run(activate_cmd, shell=True, cwd="backend", check=False)
        print("   ✅ Environnement activé")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return
    
    print()
    print("2️⃣  Lancement du serveur backend...")
    print("   ⏳ Démarrage sur http://localhost:8000")
    print()
    
    # Lancer le serveur
    try:
        subprocess.run(
            "python main.py",
            shell=True,
            cwd="backend"
        )
    except KeyboardInterrupt:
        print()
        print("🛑 Serveur arrêté")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
