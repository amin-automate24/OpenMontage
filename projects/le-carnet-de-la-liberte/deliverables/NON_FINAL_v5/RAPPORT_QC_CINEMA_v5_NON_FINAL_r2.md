# Rapport QC r2 — CINÉMA v5 NON FINAL (20/11/2026)
Verdict technique : CONFORME (mesures automatiques ; contrôle visuel de la planche JPEG, sans visionnage continu ni écoute).
Fichier : `/home/user/OpenMontage/projects/le-carnet-de-la-liberte/deliverables/NON_FINAL_v5/LE_CARNET_DE_LA_LIBERTE_CINEMA_NON_FINAL_v5_1080p.mp4` — 209562954 octets (209.56 Mo) — SHA-256 `596d4a227c8753494f503e22eb12d9b1252411bdad4744abb1963f9a9ed5505e`
Modifications : (1) SH08 images 901–988 = plan du master QC3 (photo de famille sépia), sans photo BnF ; (2) générique v006 anonyme (carton 1 option A, carton 3 sans crédit BnF). Audio, étalonnage nuit, durée, transitions inchangés. Statut NON FINAL.

- OK  Format : 7475 images, 299.000 s, 25/1 ips constant, 1920×1080, h264 High niveau 40, yuv420p
- OK  Balisage couleur = v4 (BT.709 / matrice 170M / plage limitée) ; vidéo 299.000 s, audio 299.000 s, départs 0.000000/0.000000
- OK  Décodage intégral : 0 erreur
- OK  Audio : flux AAC identique à v4 (MD5 des paquets c419bfc0…) et PCM décodé identique ; AAC 48 kHz stéréo ; synchronisation inchangée (mêmes départs, mêmes durées)
- OK  Comparaison v5 ↔ v4 sur 7475 images
- OK  Hors SH08 et générique, film (0–6902) identique à v4 (PSNR ≥ 45 dB ; min 53.0 dB, moyenne 98.8 dB) ; plages différentes : [(901, 988), (6911, 7045), (7127, 7469)]
- OK  Étalonnage nuit SH21–SH23 inchangé (images 3001–3638 vs v4 : PSNR min 99.0 dB)
- OK  SH08 (images 901–988, 88 images, 36,04–39,56 s) = plan du master QC3 sans photo BnF : PSNR vs QC3 min 50.7 dB, moyenne 53.0 dB ; vs v4 (avec photo BnF) max 26.0 dB (différent) (contrôle refait au 2e passage)
- OK  Continuité SH07→SH08→SH09 (images 895–995 vs master QC3) : 101 images, PSNR min 50.7 dB ; coupes aux images 901 et 989 conservées (contrôle refait au 2e passage)
- OK  Carton 2 (devise, images 7065–7113) inchangé vs v4 : PSNR min 55.7 dB ; cartons 1 et 3 modifiés (plages <45 dB : [(6911, 7045), (7127, 7469)])
- OK  Chaînes interdites : 0 occurrence de « benhida / tiddas / communautaire / gallica / agence rol » dans les 209,6 Mo du fichier v5 (flux et métadonnées : TAG:major_brand=isom ; TAG:minor_version=512 ; TAG:compatible_brands=isomiso2avc1mp41 ; TAG:title=LE CARNET DE LA LIBERTÉ — NON FINAL (contrôle interne) ; TAG:encoder=Lavf60.16.100 ; TAG:comment=NON FINAL — diffusion non autorisée) ; 0 « BnF / Rol / Gallica / nom / école » dans le SRT v5 et le paquet YouTube public v3 (la recherche de « bnf », 3 octets, dans le flux binaire n'est pas significative et a été écartée) ; texte des cartons contrôlé sur la planche (contrôle refait au 2e passage)
- OK  SRT v5 = SRT v4 octet pour octet (SHA-256 2d9b2afaa68d84ed…)
- OK  CINÉMA v4, SCOLAIRE v4 et quiz FINAL inchangés (SHA-256)

Planche : `PLANCHE_CINEMA_v5_SH08_ET_GENERIQUE.jpg`. Non vérifié : lecture continue, écoute. Preuves de licence ElevenLabs et Magnific : en attente. Aucune publication ; aucune étiquette FINAL.

Note : le 1er passage affichait 3 « ÉCHEC » dus à des critères défectueux de mon script (flux découpés tués par la mémoire ; faux positifs de la recherche binaire « bnf ») ; mesures sous-jacentes inchangées ; contrôles refaits ici. Fichier et mesures du 1er passage conservés dans RAPPORT_QC_CINEMA_v5_NON_FINAL.md.
