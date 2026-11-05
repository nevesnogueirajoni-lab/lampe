# Lampe : version autonome

Lampe fonctionne sans Claude ni ChatGPT. Tout ce qu'il faut est ici, et les comptes sont à ton nom.

## Les pièces

| Pièce | Où | À qui |
|---|---|---|
| L'application (fichiers du site) | Dépôt GitHub `lampe`, publié par GitHub Pages | Ton compte GitHub |
| Les comptes et les données (synchro iPhone / Mac / famille) | Projet Firebase « lampe » (Authentication + Firestore) | Ton compte Google |
| Les sauvegardes | Réglages → Sauvegarde → « Exporter mes données » (fichier .json) | Toi (iCloud Drive, par exemple) |

Aucune intelligence artificielle n'est utilisée dans la version autonome : les études, cultes et quiz sont des contenus fixes intégrés, et tout le reste ouvre JW Library.

## Installer sur l'iPhone

1. Ouvre l'adresse de Lampe dans **Safari**.
2. Touche **Partager** puis **Sur l'écran d'accueil**.
3. Ouvre Lampe depuis l'icône, puis connecte-toi (e-mail + mot de passe).

Sur le Mac, ouvre la même adresse dans Chrome ou Safari et connecte-toi avec le même compte.

## Récupérer ses données si besoin

- **Changement de téléphone** : installe Lampe et connecte-toi. Tout revient depuis Firebase.
- **Problème avec le compte** : sur l'écran de bienvenue (ou dans Réglages → Sauvegarde), touche **Restaurer** et choisis ton dernier fichier de sauvegarde.

## Inviter la famille

Réglages → Mon compte → **Inviter quelqu'un**. La personne ouvre le lien, crée son compte et rejoint la famille. Ses notes et son plan de lecture restent privés.

## Programme des réunions

Le programme détaillé (chapitres, titres) est intégré jusqu'à la date indiquée dans Réglages → Mes réunions. Après cette date, chaque préparation ouvre directement la bonne semaine dans JW Library : rien ne s'arrête.

## Mettre à jour l'application (pour un développeur)

1. Modifier `src/index.html` (le code lisible).
2. Lancer `python3 tools/build_pwa.py` : cela produit les fichiers du site.
3. Envoyer les fichiers sur le dépôt GitHub. GitHub Pages publie en une minute.

Les règles de sécurité de la base sont dans `firestore.rules` (à coller dans la console Firebase → Firestore → Règles).
