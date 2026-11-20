# Rapport QC r2 — MASTER FINAL CINÉMA (20/11/2026)
Verdict : CONFORME (mesures automatiques).
Fichier : `/home/user/OpenMontage/projects/le-carnet-de-la-liberte/deliverables/FINAL_CINEMA/LE_CARNET_DE_LA_LIBERTE_CINEMA_FINAL_1080p.mp4` — 209562821 octets — SHA-256 `0f72fc9ad6f82526af2a34d31fd34d52d1d48cea36c85835e5fedf38795c029d`
Source : CINÉMA v5 NON FINAL, SHA-256 `596d4a227c8753494f503e22eb12d9b1252411bdad4744abb1963f9a9ed5505e` (vérifié avant et après) ; remultiplexage `ffmpeg -c copy` sans réencodage, métadonnées nettoyées.

- OK  Nombre d'images : 7475 (attendu 7 475)
- OK  Durée : conteneur 299.000 s, vidéo 299.000 s, audio 299.000 s
- OK  Résolution 1920×1080, cadence 25/1 constante ; H.264 High ; AAC 48000 Hz, 2 canaux
- OK  Balisage couleur conservé (BT.709 / matrice 170M / plage limitée) — indispensable à la lecture
- OK  Décodage complet : 0 erreur
- OK  Flux vidéo : 7475 paquets, horodatages/tailles/drapeaux identiques à v5 ; données d19c4f36… = v5 d19c4f36…
- OK  Données des paquets vidéo identiques (MD5 sur flux copié)
- OK  Flux audio : 14017 paquets identiques à v5 (horodatages, tailles, données)
- OK  Images décodées identiques à v5 : 7475 empreintes MD5 image par image égales
- OK  Audio décodé identique à v5 : 14016 trames égales ; synchronisation inchangée (départs vidéo 0.000000 / audio 0.000000)
- OK  Métadonnées de conteneur nettoyées : restent seulement `title=LE CARNET DE LA LIBERTÉ`, marque/version MP4, langues (und / fra) et noms de gestionnaires génériques (VideoHandler / SoundHandler) ; aucune balise d'encodeur, aucun commentaire, aucune mention « NON FINAL » ; 0 occurrence de nom de personne, d'école, de BnF/Gallica/Rol dans tout le fichier (contrôle refait au 2e passage)
- INFO Identifiant technique « Lavc60.31.102 » présent **à l'intérieur des flux** (56 trames AAC, 1 unité du flux vidéo) : écrit par l'encodeur lors du rendu de v4/v5, identique dans v5 ; non personnel ; le retirer modifierait les flux, ce qui est exclu.
- INFO Le flux H.264 conserve son message SEI technique x264 (réglages d'encodage, aucune donnée personnelle) : le retirer modifierait le flux vidéo, ce qui est exclu.
- OK  SRT public `LE_CARNET_DE_LA_LIBERTE_FR.srt` = copie octet pour octet du SRT v5 ; UTF-8 sans BOM, 32 répliques, fin 269.000 s ≤ 299 s ; aucun nom de personne réelle ni d'établissement
- OK  CINÉMA v5 NON FINAL inchangé (SHA-256 vérifié après opérations)

SRT public : `LE_CARNET_DE_LA_LIBERTE_FR.srt` — SHA-256 `2d9b2afaa68d84ed1fc212cdd4b760a1fd04c7028464ab6b4d7fd1cc4f01c22d`.
Note : le 1er passage (`RAPPORT_QC_CINEMA_FINAL.md`, conservé) marquait « ÉCHEC » parce que mon critère cherchait « Lavc » dans tout le fichier, y compris dans les données des flux ; le conteneur ne contient aucune de ces balises. Fichier inchangé entre les deux passages.
