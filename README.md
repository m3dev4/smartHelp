# SmartHelp

SmartHelp est une API FastAPI conçue pour traiter un ticket de support client à partir de trois entrées :
- un fichier audio de description du problème,
- une photo du produit ou du défaut,
- un contexte textuel issu du règlement interne.

Le service transcrit l’audio, analyse l’image, puis utilise un moteur de récupération augmentée (RAG) pour retrouver la règle applicable dans le règlement.

---

## 1. Objectif du projet

L’objectif est de fournir un assistant de support capable de :
1. transcrire un message vocal,
2. détecter visuellement une anomalie sur une image,
3. rechercher la règle correspondante dans un document PDF de politique interne,
4. retourner un résultat structuré pouvant être utilisé par un front-end ou un outil métier.

---

## 2. Architecture du projet

Le projet est organisé comme suit :

- main.py : point d’entrée de l’API FastAPI.
- routes/ingestionsRoute.py : définition de l’endpoint principal d’ingestion.
- services/ : logique métier pour la transcription audio et l’analyse d’image.
- validations/ : validation des fichiers uploadés.
- utils/ : sauvegarde temporaire des fichiers uploadés.
- rag/ : chargement du PDF, découpage en chunks, stockage vectoriel et RAG.
- models/ : initialisation des modèles de transcription et d’analyse.
- config/ : configuration partagée des modèles.
- vectorstore/ : base vectorielle locale utilisée par Chroma.

---

## 3. Fonctionnement global

Quand un client envoie une requête à l’endpoint /ingestions/support-ticket :

1. l’audio est validé,
2. l’image est validée,
3. l’audio est enregistré temporairement puis transcrit,
4. l’image est analysée pour détecter une anomalie,
5. la transcription est utilisée comme requête pour le moteur RAG,
6. le système renvoie un résultat combinant transcription, classification d’image et règle de politique.

---

## 4. Prérequis

Avant de démarrer, il faut disposer de :
- Python 3.10 ou plus récent,
- un environnement virtuel Python,
- un token Hugging Face si vous utilisez des modèles hébergés via Hugging Face,
- Internet pour charger les modèles et le PDF si nécessaire.

---

## 5. Installation

### 5.1 Cloner le projet

```bash
git clone <url-du-projet>
cd smartHelp
```

### 5.2 Créer un environnement virtuel

Sous Windows :

```bash
py -m venv .venv
.venv\Scripts\activate
```

Sous Linux/macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5.3 Installer les dépendances

```bash
pip install -r requierements.txt
```

### 5.4 Configurer les variables d’environnement

Le fichier .env contient les variables essentielles :

```env
MODEL_PROVIDER="local"
OPENAI_WHISPER_MODEL_NAME="openai/whisper-small"
MODEL_PROVIDER_HF="hf"
GOOGLE_VIT_BASE_PATCHED_MODEL_NAME="google/gemma-4-31B-it:novita"
HF_TOKEN="votre_token_huggingface"
OPENROUTER_API_KEY="votre_cle_openrouter"
MODEL_NAME_OPENROUTER="inclusionai/ling-3.0-flash:free"
```

> Si vous n’avez pas de token Hugging Face, certaines fonctionnalités liées aux modèles distants peuvent ne pas fonctionner.

---

## 6. Lancer l’API

Depuis la racine du projet :

```bash
uvicorn main:app --reload
```

L’API sera ensuite disponible sur :
- http://127.0.0.1:8000

La documentation Swagger sera disponible ici :
- http://127.0.0.1:8000/docs

---

## 7. Endpoints disponibles

### 7.1 Endpoint principal

#### POST /ingestions/support-ticket

Cet endpoint accepte :
- un fichier audio (`audio`),
- un fichier image (`image`),
- une chaîne optionnelle `description`.

#### Paramètres

- `audio`: fichier audio au format MP3 ou WAV.
- `image`: fichier image au format JPEG ou PNG.
- `description`: texte libre optionnel, non utilisé directement dans le flux actuel mais conservé pour l’extension future.

#### Réponse attendue

Le service renvoie un JSON contenant :
- `transcription`: texte transcrit de l’audio,
- `defect_detected`: résultat de l’analyse de l’image,
- `policy_rule_applied`: réponse du moteur RAG,
- `diagnostic_status`: statut produit par le RAG.

#### Exemple d’appel avec curl

```bash
curl -X POST "http://127.0.0.1:8000/ingestions/support-ticket" \
  -F "audio=@votre_audio.mp3" \
  -F "image=@votre_image.png" \
  -F "description=Produit endommagé"
```

---

## 8. Composants clés

### 8.1 Validation des fichiers

Le dossier validations contient :
- audioValidate.py : vérifie que l’audio est bien au format MP3 ou WAV et ne dépasse pas 10 Mo.
- imageValidate.py : vérifie que l’image est bien au format JPEG ou PNG et ne dépasse pas 10 Mo.

### 8.2 Service de transcription

Le service whisperService.py appelle le modèle Whisper configuré dans models/whisperModel.py.

### 8.3 Service d’analyse d’image

Le service vitService.py envoie l’image à un modèle de vision et tente d’obtenir une classification structurée en JSON.

### 8.4 RAG (Retrieval-Augmented Generation)

Le sous-dossier rag contient :
- un chargeur PDF,
- un découpage en chunks,
- une base vectorielle Chroma,
- une chaîne de récupération et réponse.

Le système cherche ensuite la meilleure information dans le règlement et renvoie une réponse basée sur ce contexte.

---

## 9. Flux technique détaillé

### Étape 1 : réception du fichier

Les fichiers sont envoyés via multipart/form-data à l’API FastAPI.

### Étape 2 : validation

Les validations empêchent :
- les types de fichiers non supportés,
- les fichiers trop volumineux.

### Étape 3 : sauvegarde temporaire

Les fichiers sont enregistrés localement dans un dossier temporaire pour être lus par les services de transcription et d’analyse.

### Étape 4 : transcription

Le contenu audio est transcrit à l’aide du modèle Whisper.

### Étape 5 : analyse d’image

L’image est encodée en base64 et passée à un modèle de vision.

### Étape 6 : RAG

La transcription devient la requête utilisée pour extraire la règle pertinente depuis le règlement PDF.

---

## 10. Dépannage

### Problème : l’API ne démarre pas

Vérifiez :
- que l’environnement virtuel est activé,
- que toutes les dépendances sont installées,
- que Python est bien compatible avec les versions listées dans requirements.

### Problème : erreur liée au modèle Hugging Face

Vérifiez :
- que HF_TOKEN est défini,
- que le modèle demandé est bien accessible,
- que votre clé possède les permissions nécessaires.

### Problème : endpoint rejeté avec 400 ou 413

Vérifiez :
- le type du fichier uploadé,
- la taille du fichier,
- le format du fichier.

---

## 11. Bonnes pratiques

- conserver les fichiers temporaires propres et éviter les gros uploads en production,
- protéger les clés API via un stockage sécurisé,
- utiliser un moteur de stockage vectoriel plus robuste en production,
- ajouter des tests unitaires et d’intégration,
- ne jamais exposer directement les secrets dans le code source.

---

## 12. Extension possible

Le projet peut facilement évoluer vers :
- une interface web plus ergonomique,
- une base de données pour stocker les tickets traités,
- un système d’authentification,
- une orchestration plus robuste avec un worker asynchrone.

---

## 13. Licence

Ce projet est publié sous licence MIT.

La licence MIT permet :
- l’utilisation commerciale,
- la modification,
- la redistribution,
- la distribution sous une autre forme, sous réserve de conserver l’avertissement de copyright et la licence.

### Texte de licence MIT

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, OR ILLUSTRATION
OF THE SOFTWARE IN ANY EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER SOFTWARE.
```

---

## 14. Résumé rapide

SmartHelp est un assistant IA de support client capable de :
- analyser un audio,
- analyser une image,
- chercher une règle dans un règlement,
- retourner un diagnostic utile à un humain.

C’est un bon point de départ pour construire un outil de service client plus intelligent, plus rapide et plus automatisé.
