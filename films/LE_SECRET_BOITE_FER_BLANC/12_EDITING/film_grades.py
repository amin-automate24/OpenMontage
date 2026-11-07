"""Reglages d'etalonnage (FFmpeg, video seulement) par segment. Sources en lecture seule.
Cle = nom du fichier mix du segment ; valeur = chaine de filtres appliquee a ce segment (temps du segment)."""
FLAGS = "huesaturation=colors=r:saturation=0.45:strength=1"
GRADES_V1 = {
    "MIX_S1-S2_final_v5.mp4": "",
    "MIX_S3_v4.mp4": ("colorbalance=rs=0.02:bs=-0.03:rm=0.05:gm=0.025:bm=-0.07:rh=0.06:gh=0.035:bh=-0.09,"
                      "eq=saturation=1.08:contrast=1.03," + FLAGS),
    "MIX_S4_final_v4.mp4": FLAGS,
    "MIX_S5_v9.mp4": ("colorbalance=rs=0.03:bs=-0.04:rm=0.05:gm=0.01:bm=-0.06:rh=0.04:bh=-0.06,"
                      "eq=saturation=1.12," + FLAGS),
    # S6-01 (0-9 s, fondu a 8,2-9) : salle plus claire que les autres -> assombrie et rechauffee, effet qui s'efface
    "MIX_S6_v4.mp4": ("eq=brightness='-0.07*clip((9-t)/1,0,1)':gamma='1-0.10*clip((9-t)/1,0,1)':"
                      "saturation='1-0.12*clip((9-t)/1,0,1)':eval=frame,"
                      "colorbalance=rm=0.04:bm=-0.05:rh=0.03:bh=-0.05:enable='lt(t,8.5)'," + FLAGS +
                      # S6-10 (68,7 s -> fin) : drapeau rose delave -> rouge plus franc, etoile verte plus lisible
                      ",huesaturation=colors=r:saturation=0.55:strength=1:enable='gte(t,68.7)'"
                      ",huesaturation=colors=g:saturation=0.5:intensity=0.12:strength=1:enable='gte(t,68.7)'"),
}
