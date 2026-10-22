Sommelier Zero Tracas — 2.0.0-beta.1

Une cave virtuelle partagée dans Home Assistant : photo d'étiquette, fiche à valider,
stock par catégorie, envies, sorties, dégustations et régions.
Statut : version bêta, à tester avant publication stable

Cette livraison a fait l'objet de vérifications de syntaxe et de tests du stockage
isolé. Elle n'a PAS été exécutée dans Home Assistant et aucun appel Gemini réel
n'a été effectué pour la valider. Le minimum Home Assistant 2025.6.0 est un seuil
proposé pour les API utilisées, pas une version minimale certifiée par des essais.
Ne pas annoncer « plug and play testé » avant les essais sur une instance propre,
sur Android et sur iPhone. Les quotas et la disponibilité Gemini restent externes.
Fonctionnalités de cette bêta

    Panneau « Ma cave » enregistré par l'intégration, sans carte Lovelace à installer.

    Prise de photo mobile (selon le navigateur), choix galerie, réduction locale en JPEG.

    Consentement explicite avant transmission de photo et des 30 derniers avis à Google.

    Ajout manuel utilisable sans appel IA après installation.

    Scan sans modification du stock : l'utilisateur confirme l'ajout ou le retrait.

    Catégories : Rouge, Rose, Blanc sec, Blanc moelleux, Champagne/Effervescent.

    Liste « À compléter » pour les catégories indéterminées.

    Fiches modifiables, quantité, dernier prix payé et emplacement.

    Estimations IA de prix en EUR pour 75 cl, toujours non vérifiées et facultatives.

    Envies (le transfert vers la cave ne supprime pas automatiquement l'envie).

    Sorties avec motif ; avis proposé après une dégustation et possible plus tard.

    Historique, annulation de mouvements, sauvegarde JSON exportable.

    Filtrage par catégories et régions ; carte SCHÉMATIQUE française, pas carte SIG.

    Capteur de stock réel ; aucune liste de photos volumineuse dans les attributs HA.

    Modèle et clé modifiables depuis Réglages pour les administrateurs.

    Conseils IA prudents utilisant les avis enregistrés ; pas de score de goût inventé.

Installation avec HACS

Prérequis : HACS déjà installé, compte Gemini et clé API personnelle.

    Publier le CONTENU du dossier de dépôt à la racine du dépôt GitHub.
    hacs.json et custom_components/ doivent être à la racine.

    Dans HACS, ajouter ce dépôt comme dépôt personnalisé, type « Intégration ».

    Télécharger Sommelier Zero Tracas.

    Redémarrer Home Assistant.

    Paramètres > Appareils et services > Ajouter une intégration > Sommelier Zero Tracas.

    Saisir sa clé API personnelle et le modèle. La vérification initiale interroge la
    liste des modèles ; elle ne garantit pas le succès des générations.

    Ouvrir « Ma cave » dans la barre latérale.

Le dépôt doit être public pour le parcours prévu. La présence dans le catalogue
HACS par défaut n'est pas automatique. Ne pas présenter les validations GitHub
comme équivalentes à une acceptation HACS ou à un test Home Assistant.
Installation manuelle / mise à jour de la version existante

    Faire une sauvegarde complète Home Assistant AVANT remplacement.

    Copier le dossier custom_components/sommelier_zero_tracas dans
    /config/custom_components/sommelier_zero_tracas.

    Le fichier d'entrée s'appelle exactement __init__.py (deux underscores).

    Remplacer les anciens fichiers, puis redémarrer Home Assistant.

    L'entrée de configuration existante est réutilisée si elle existe.

    Ouvrir Ma cave > Réglages. Choisir le modèle et tester une requête texte.

    Si le panneau paraît ancien : fermer/réouvrir l'application puis actualiser
    complètement la page ; vérifier le cache du navigateur.

La même clé de stockage sommelier_zero_tracas_cave est conservée. La migration
ajoute categorie sans supprimer couleur. Un ancien « Blanc » reste à compléter :
il ne permet pas de déduire sec ou moelleux. Les anciens avis présents sur une fiche
sont préservés, mais ne deviennent pas artificiellement de nouvelles dégustations.

L'ancienne action sommelier_zero_tracas.scan_wine n'est pas exposée dans cette
bêta : les actions passent par le panneau et son API WebSocket authentifiée.
Les automatisations qui utilisent cette ancienne action devront être adaptées.
Modèle Gemini et coûts

Le modèle initial proposé est gemini-3.5-flash-lite. Ce nom n'est pas garanti
utilisable pour tous les comptes. Modifier le modèle depuis Réglages sans éditer
le Python. La liste des modèles ne garantit ni compatibilité image ni disponibilité.
Le bouton « Tester » lance une génération texte facturable selon les conditions
Google. Le scan lance jusqu'à 3 tentatives en cas d'erreur 500/502/503/504.
Pas de bascule automatique vers un modèle potentiellement plus coûteux.
404 : vérifier modèle/version/accès ; 429 : consulter quotas ; 503 : disponibilité.
Aucune clé partagée ni garantie de gratuité ou de disponibilité illimitée.
Prix et identification

L'IA n'effectue AUCUNE recherche de prix sur les sites marchands dans cette version.
La fourchette est une estimation incertaine pour une bouteille de 75 cl, pas une
expertise, pas un prix observé, pas une valeur de revente. Si la référence ou le
format sont insuffisants, elle doit rester vide. Vérifier toute information avant
achat. Le prix payé est saisi séparément et n'est jamais remplacé par l'estimation.
Le prix total de la cave, les prix marchands sourcés et le suivi des formats seront
des évolutions distinctes, non annoncées comme déjà disponibles.

Une nouvelle entrée ne fusionne JAMAIS automatiquement avec une ancienne.
Lors d'un ajout, sélectionner explicitement une référence existante si besoin.
Lors d'un scan pour sortie, « Chercher dans mon stock » propose une recherche par
nom ; choisir la bonne cuvée et le bon millésime. Pas de reconnaissance garantie
entre deux photos. Une sortie nécessite toujours confirmation.
Confidentialité et sécurité

    Cave et avis partagés entre les utilisateurs authentifiés de cette instance.

    Ce n'est pas un profil privé distinct par personne. Les mouvements portent l'ID utilisateur.

    La clé reste dans la configuration HA, jamais renvoyée au panneau ou publiée.

    Photos réduites et miniatures sauvegardées localement via Store.

    Lors d'une analyse : photo + synthèse des 30 derniers avis envoyés à Google.

    Aucun téléversement dans /config/www, aucune photo rendue publiquement accessible.

    Aucun appel de prix externe ni suivi publicitaire.

    Les suggestions IA restent incertaines et modifiables par l'utilisateur.

    Pas de token longue durée à coller dans le JavaScript.

    Le stockage JSON contient des miniatures : surveiller sa taille pour une grosse cave.

    L'export contient des données personnelles ; ne pas le publier sur GitHub.

    Export JSON lisible disponible ; IMPORT/restauration via ce fichier non implémenté.
    Utiliser les sauvegardes Home Assistant pour restaurer.

Tests locaux

python -m unittest discover -s tests -v

Les tests isolent le stockage avec une imitation minimale de Store. Ils ne testent
pas Home Assistant lui-même, les websockets, HACS, l'appareil photo ou Google.
node --check custom_components/sommelier_zero_tracas/frontend/panel.js
vérifie la syntaxe JavaScript si Node est installé ; Node n'est pas requis dans HA.
Recette avant publication stable

Voir TESTS_MANUELS.md. Les fonctionnalités doivent être validées en conditions
réelles, y compris restauration de sauvegarde, réseau indisponible et données
existantes. Un workflow de compilation ne constitue pas une recette fonctionnelle.
