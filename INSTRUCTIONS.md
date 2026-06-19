# 🇵🇹 BLS Portugal — Alerte RDV sur Telegram
## Instructions complètes (serveur cloud GRATUIT)

---

## ÉTAPE 1 — Créer ton Bot Telegram (2 minutes)

1. Ouvre Telegram et cherche **@BotFather**
2. Envoie `/newbot`
3. Donne un nom : `BLS Portugal Alert`
4. Donne un username : `blsportugal_monnom_bot`
5. BotFather te donne un **TOKEN** qui ressemble à :
   `7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
6. **Copie ce token** — tu en auras besoin

---

## ÉTAPE 2 — Déployer sur Render.com (GRATUIT)

1. Va sur **https://render.com** et crée un compte gratuit
2. Clique **"New +"** → **"Web Service"**
3. Choisis **"Deploy from existing code"** → Upload tes fichiers
   OU connecte ton GitHub

### Via GitHub (recommandé) :
1. Crée un repo GitHub privé
2. Upload les fichiers `bls_checker.py` et `requirements.txt`
3. Sur Render : connecte le repo
4. Configure :
   - **Runtime** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `python bls_checker.py`
5. Dans **Environment Variables**, ajoute :
   - `TELEGRAM_TOKEN` = ton token BotFather

---

## ÉTAPE 3 — Modifier le script

Ouvre `bls_checker.py` et remplace ligne 8 :
```
TELEGRAM_BOT_TOKEN = "METS_TON_TOKEN_ICI"
```
par ton vrai token.

---

## ÉTAPE 4 — Démarrer le bot Telegram

Cherche ton bot sur Telegram et envoie `/start`
→ Tu recevras un message de confirmation !

---

## Alternative ENCORE PLUS SIMPLE — Railway.app

1. Va sur **https://railway.app**
2. Connecte avec GitHub
3. "Deploy from GitHub repo"
4. Ajoute la variable : `TELEGRAM_TOKEN=ton_token`
5. C'est tout !

---

## ⚠️ Notes importantes

- Ton **Telegram ID** est déjà configuré dans le script : `7809383847`
- Le bot vérifie **toutes les 30 secondes**
- Tu recevras un rapport **toutes les heures**
- Si le site change de structure, le bot te préviendra

---

## 📱 Notifications que tu recevras

- ✅ Message de démarrage
- 🎉 **ALERTE** quand un créneau est dispo (avec lien direct)
- 😔 Si le créneau est déjà pris
- 📊 Rapport horaire
