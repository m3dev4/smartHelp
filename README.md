# Support Ticket AI API

Micro-service FastAPI qui analyse automatiquement une réclamation client
(audio et/ou photo et/ou texte) et retourne un diagnostic JSON structuré.

## Architecture
mouhamed donne l'architecture

## Installation

```bash
python -m venv venv
source venv/bin/activate       # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn main:app --reload
```

Documentation interactive Swagger : http://127.0.0.1:8000/docs
Health check : http://127.0.0.1:8000/health

## Test rapide avec curl

```bash
# Avec texte seulement
curl -X POST http://127.0.0.1:8000/support-ticket \
  -F "texte=Mon produit est arrivé cassé, je veux un remboursement"

# Avec audio
curl -X POST http://127.0.0.1:8000/support-ticket \
  -F "audio=@reclamation.wav"

# Avec audio + image
curl -X POST http://127.0.0.1:8000/support-ticket \
  -F "audio=@reclamation.wav" \
  -F "image=@produit.jpg"
```

## Réponse type

```json
{
  "transcription": "Mon produit est arrivé cassé, je veux un remboursement",
  "texte_description": null,
  "diagnostic_image": {
    "label_predit": "broken glass",
    "score_confiance": 0.812,
    "defaut_detecte": true
  },
  "regle_interne": {
    "question_associee": "Le produit reçu est cassé ou endommagé à la livraison",
    "reponse": "Un produit endommagé à la réception est remboursé intégralement ou échangé sous 14 jours...",
    "categorie": "retour",
    "score_similarite": 0.734
  },
  "statut_propose": "Remboursable",
  "avertissements": []
}
```

## Points clés de conformité

- **Optimisation mémoire** : chaque modèle (Whisper, ViT, embeddings) est chargé
  une seule fois grâce à `@lru_cache(maxsize=1)`, et préchargé au démarrage
  (`@app.on_event("startup")`) plutôt qu'à la première requête.
- **Validation des fichiers** : extensions vérifiées avant tout traitement,
  taille max appliquée pendant la lecture par blocs (pas de chargement complet
  en mémoire avant rejet).
- **Nettoyage garanti** : les fichiers temporaires sont supprimés dans un bloc
  `finally`, y compris en cas d'erreur pendant le traitement.
- **Gestion des erreurs** : chaque étape (ASR, vision, RAG) est isolée dans son
  propre `try/except` ; une erreur sur un module n'empêche pas les autres de
  fonctionner et remonte comme un avertissement non bloquant plutôt qu'un crash.

## Limite connue

Le modèle de vision (`google/vit-base-patch16-224`) est un classifieur
générique ImageNet utilisé ici à des fins de démonstration. Pour une vraie
détection de "produit endommagé", il faudrait le remplacer par un modèle
fine-tuné sur des photos de produits abîmés/conformes — l'architecture du
service (`vision_service.py`) resterait identique.