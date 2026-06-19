import asyncio
import aiohttp
import time
from datetime import datetime

# ========================================
# CONFIGURATION
# ========================================
TELEGRAM_BOT_TOKEN = "8943017115:AAH55y5TXpdiNAutjJTdmiVyvCcB7g_fOdU"  # Tu obtiendras ce token après (voir instructions)
TELEGRAM_CHAT_ID = "7809383847"             # Ton ID Telegram
CHECK_INTERVAL = 30                          # Vérification toutes les 30 secondes
BLS_URL = "https://morocco.blsportugal.com/MAR/appointmentdata/myappointments"

# ========================================
# TELEGRAM
# ========================================
async def send_telegram(session, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        async with session.post(url, json=payload) as resp:
            result = await resp.json()
            if result.get("ok"):
                print(f"[Telegram] Message envoyé ✓")
            else:
                print(f"[Telegram] Erreur: {result}")
    except Exception as e:
        print(f"[Telegram] Exception: {e}")

# ========================================
# VÉRIFICATION BLS
# ========================================
async def check_bls(session):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Xiaomi) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,*/*",
        "Accept-Language": "fr-MA,fr;q=0.9,ar;q=0.8",
        "Referer": "https://morocco.blsportugal.com/",
    }
    try:
        async with session.get(BLS_URL, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            html = await resp.text()
            return html, resp.status
    except Exception as e:
        print(f"[BLS] Erreur requête: {e}")
        return None, 0

def detect_slots(html):
    if not html:
        return False, "erreur"

    lower = html.lower()

    # Pas de créneau
    no_slot_keywords = [
        "no appointment", "no slot", "aucun créneau",
        "not available", "unavailable", "complet", "full",
        "no appointments available", "there are no"
    ]

    # Créneaux disponibles
    slot_keywords = [
        "select date", "select time", "choose date",
        "available slot", "book now", "réserver",
        "appointment available", "pick a date",
        "datepicker", "timeslot", "time-slot"
    ]

    has_negative = any(k in lower for k in no_slot_keywords)
    has_positive = any(k in lower for k in slot_keywords)

    if has_positive and not has_negative:
        return True, "créneaux détectés"
    elif has_negative:
        return False, "complet"
    else:
        return False, "inconnu"

# ========================================
# BOUCLE PRINCIPALE
# ========================================
async def main():
    print("=" * 50)
    print("🇵🇹 BLS Portugal — Surveillant de RDV")
      
    print(f"📱 Notifications → Telegram {TELEGRAM_CHAT_ID}")
    print(f"⏱️  Intervalle: {CHECK_INTERVAL} secondes")
    print(f"🔗 URL: {BLS_URL}")
    print("=" * 50)

    check_count = 0
    slot_found = False

    async with aiohttp.ClientSession() as session:
        # Message de démarrage
        await send_telegram(session, 
            "🚀 <b>Surveillance BLS Portugal démarrée !</b>\n"
            f"📍 Casablanca\n"
            f"⏱️ Vérification toutes les {CHECK_INTERVAL}s\n"
            "Je t'enverrai un message dès qu'un créneau est disponible !"
        )

        while True:
            check_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] Vérification #{check_count}...")

            html, status = await check_bls(session)

            if status == 200:
                has_slots, reason = detect_slots(html)
                print(f"  → Statut HTTP: {status} | Créneaux: {'OUI ✓' if has_slots else f'Non ({reason})'}")

                if has_slots and not slot_found:
                    slot_found = True
                    await send_telegram(session,
                        "🎉🎉🎉 <b>CRÉNEAU DISPONIBLE !</b> 🎉🎉🎉\n\n"
                        "📅 Un rendez-vous BLS Portugal est disponible !\n\n"
                        f"👉 <a href='{BLS_URL}'>RÉSERVER MAINTENANT</a>\n\n"
                        "⚡ Fais vite avant que ça parte !"
                    )
                    print("  🚨 ALERTE ENVOYÉE SUR TELEGRAM !")

                elif not has_slots and slot_found:
                    slot_found = False
                    await send_telegram(session,
                        "😔 Le créneau a été pris.\n"
                        "Je continue à surveiller..."
                    )

            elif status == 403 or status == 401:
                print(f"  ⚠️ Non connecté (HTTP {status}) — reconnecte-toi sur le site")
                if check_count % 20 == 0:  # Rappel toutes les 10 minutes
                    await send_telegram(session,
                        "⚠️ <b>Attention !</b>\n"
                        "Le bot ne peut pas accéder au site.\n"
                        "Peut-être que ta session a expiré.\n"
                        f"Reconnecte-toi sur BLS Portugal."
                    )
            else:
                print(f"  ⚠️ HTTP {status}")

            # Rapport toutes les heures
            if check_count % 120 == 0:
                await send_telegram(session,
                    f"📊 <b>Rapport de surveillance</b>\n"
                    f"✅ {check_count} vérifications effectuées\n"
                    f"🕐 Heure: {now}\n"
                    f"🔄 Je continue à surveiller..."
                )

            await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
