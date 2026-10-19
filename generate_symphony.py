#!/usr/bin/env python3
"""
Symphonie en Ré (M. posth.) — « L'Horloge et l'Océan »
Grande Édition Symphonique Intégrale (~25 minutes 16 secondes)
Hommage symphonique dans le style de Maurice Ravel (1875–1937)

Durées des 4 mouvements :
- I.   Prélude et Allegro moderato (Forme Sonate complète, 174 mesures, 96 BPM)  : 7 min 15 s
- II.  Scherzo — Vif et nerveux : Mirages basques (232 mesures, 132 BPM)         : 5 min 16 s
- III. Lent et soutenu — Grande Passacaille : 18 Variations (144 mes., 64 BPM)   : 6 min 45 s
- IV.  Final — Animé et féerique : La Grande Horlogerie (186 mesures, 124 BPM)   : 6 min 00 s
----------------------------------------------------------------------------------------------
Durée totale : 25 min 16 s (1 516 secondes)
"""

import json
import os
import struct
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class NoteEvent:
    pitch: int
    start_beat: float
    duration: float
    velocity: int
    instrument: str
    section: str = ""


@dataclass
class Movement:
    number: int
    roman: str
    title: str
    subtitle: str
    tempo_marking: str
    bpm: float
    time_signature: Tuple[int, int]
    key_signature: str
    description: str
    total_beats: float
    notes: List[NoteEvent] = field(default_factory=list)


def compose_movement_1() -> Movement:
    """
    I. Prélude et Allegro moderato (Forme Sonate complète • 174 mesures à 4/4 • 696 temps @ 96 BPM = 7m15s)
    """
    mvt = Movement(
        number=1,
        roman="I",
        title="Prélude et Allegro moderato",
        subtitle="Brumes matinales et mécanique céleste (Forme Sonate)",
        tempo_marking="Très modéré, fluide et lumineux — Allegro moderato",
        bpm=96.0,
        time_signature=(4, 4),
        key_signature="Ré dorien / Ré majeur Lydien",
        description=(
            "Grande forme sonate ravélienne précédée d'un Lever du jour (mes. 1–24), suivie de "
            "l'Exposition du Thème I horloger (mes. 25–56), d'un Pont polytonal en planing (mes. 57–72), "
            "du Thème II lyrique au hautbois en La mixolydien (mes. 73–96), d'un vaste Développement "
            "océanique (mes. 97–136), de la Réexposition solaire (mes. 137–160) et de la Coda (mes. 161–174)."
        ),
        total_beats=696.0,
    )
    n1 = mvt.notes
    add = lambda p, s, d, v, i, sec: n1.append(NoteEvent(p, s, d, v, i, sec))

    progressions = [
        (38, [50, 57, 60, 64, 69], [62, 64, 65, 69, 72, 76, 79, 81]),  # Dm9
        (38, [50, 59, 62, 65, 71], [62, 65, 67, 71, 74, 77, 79, 83]),  # G13/D
        (38, [52, 59, 62, 66, 69], [64, 66, 67, 71, 74, 78, 79, 83]),  # Em11/D
        (38, [52, 57, 61, 64, 69], [61, 64, 67, 69, 73, 76, 79, 81]),  # A13/D
        (41, [53, 60, 64, 67, 71], [60, 64, 67, 71, 72, 76, 79, 84]),  # Fmaj9#11
        (35, [47, 54, 57, 62, 66], [59, 62, 66, 69, 71, 74, 78, 81]),  # Bm11
        (43, [55, 59, 62, 66, 69], [59, 62, 66, 69, 71, 74, 78, 83]),  # Gmaj9
        (45, [52, 57, 60, 64, 67], [60, 64, 67, 71, 72, 76, 79, 81]),  # Am11
    ]
    theme_cells = [
        [(0.0, 1.5, 0), (1.5, 0.5, 1), (2.0, 1.0, 2), (3.0, 1.0, 4)],
        [(0.0, 1.5, 3), (1.5, 0.5, 2), (2.0, 1.0, 1), (3.0, 1.0, 0)],
        [(0.5, 1.0, 2), (1.5, 0.5, 4), (2.0, 0.5, 5), (2.5, 1.5, 6)],
        [(0.0, 2.0, 5), (2.0, 1.0, 3), (3.0, 1.0, 2)],
        [(0.0, 1.0, 4), (1.0, 0.5, 5), (1.5, 0.5, 6), (2.0, 1.5, 7), (3.5, 0.5, 5)],
        [(0.0, 1.5, 6), (1.5, 0.5, 4), (2.0, 1.0, 2), (3.0, 1.0, 1)],
    ]

    for bar in range(174):
        b0 = bar * 4.0
        trans = 0
        if bar < 24:
            sec = "Introduction — Lever du jour (Harpe, Célesta & Flûte en Ré dorien)"
            mode, dyn = "prelude", 58 + bar // 2
        elif bar < 56:
            sec = "Exposition (Thème I) — Allegro moderato : L'Horlogerie céleste"
            mode, dyn = "theme1", 74
        elif bar < 72:
            sec = "Pont modulant — Miroitements polytonaux & Planing d'accords de 9e"
            mode, trans, dyn = "bridge", 3, 78
        elif bar < 96:
            sec = "Exposition (Thème II) — Chant lyrique du Hautbois en La mixolydien"
            mode, trans, dyn = "theme2", 7, 68
        elif bar < 136:
            sec = "Grand Développement — Tourmente océanique & Contrepoint orchestral"
            mode, trans, dyn = "dev", ((bar - 96) % 5) * 2 - 3, 82 + (bar - 96) // 3
        elif bar < 160:
            sec = "Réexposition solaire — Thèmes I & II transfigurés en Ré majeur Lydien"
            mode, trans, dyn = "recap", 0, 88
        else:
            sec = "Coda — Scintillement final de l'Horloge en Ré majeur 9e"
            mode, trans, dyn = "coda", 0, max(54, 92 - (bar - 160) * 3)

        bass0, pad0, arp0 = progressions[bar % len(progressions)]
        bass = bass0 + (trans - 12 if trans > 4 else trans)
        pad = [p + trans for p in pad0]
        arp = [p + trans for p in arp0]

        if mode in ("theme1", "bridge", "dev"):
            for beat in range(4):
                add(bass if beat % 2 == 0 else bass + 7, b0 + beat, 0.42, dyn + 6, "pizz", sec)
                add(pad[beat % len(pad)], b0 + beat + 0.5, 0.35, dyn - 2, "pizz", sec)
        else:
            add(bass, b0, 3.9, dyn, "bass", sec)

        for p in pad:
            add(p, b0, 3.85, dyn - 8, "strings", sec)
        if mode in ("dev", "recap"):
            add(pad[1], b0, 3.7, dyn - 4, "horn", sec)
        if mode == "dev" and bar % 2 == 0:
            add(bass, b0, 0.6, dyn + 10, "timpani", sec)
            add(pad[2] + 12, b0 + 2.0, 1.8, dyn, "brass", sec)

        arp_sub = 16 if mode in ("prelude", "recap", "coda") else 8
        step = 4.0 / arp_sub
        for i in range(arp_sub):
            idx = i if i < arp_sub // 2 else (arp_sub - 1 - i)
            add(arp[idx % len(arp)], b0 + i * step, step * 1.4, dyn - 10 + (i % 4) * 2, "harp", sec)
        if bar % 2 == 0 or mode in ("prelude", "coda"):
            add(arp[-1] + 12, b0 + 1.0, 1.2, dyn - 14, "celesta", sec)
            add(arp[-2] + 12, b0 + 3.0, 1.0, dyn - 16, "celesta", sec)

        cell = theme_cells[(bar + bar // 8) % len(theme_cells)]
        lead_inst = (
            "flute" if mode == "prelude"
            else ("oboe" if bar % 8 < 4 else "flute") if mode == "theme1"
            else "clarinet" if mode == "bridge"
            else ("oboe" if bar % 8 < 4 else "clarinet") if mode == "theme2"
            else ("flute" if bar % 4 < 2 else "brass") if mode == "dev"
            else "flute"
        )
        for st, dur, deg in cell:
            pitch = arp[deg % len(arp)] + (12 if deg >= len(arp) else 0)
            add(pitch, b0 + st, dur, min(108, dyn + 14), lead_inst, sec)
            if mode in ("theme1", "theme2", "recap"):
                harm_inst = "oboe" if lead_inst == "flute" else "clarinet"
                add(pitch - 3, b0 + st, dur, min(100, dyn + 6), harm_inst, sec)
            if mode == "recap":
                add(pitch - 12, b0 + st, dur, dyn + 8, "strings", sec)

    return mvt


def compose_movement_2() -> Movement:
    """
    II. Scherzo — Vif et nerveux : Mirages basques (232 mesures à 3/4 • 696 temps @ 132 BPM = 5m16s)
    """
    mvt = Movement(
        number=2,
        roman="II",
        title="Scherzo — Vif et nerveux",
        subtitle="Mirages basques (Alborada, Nocturne & Zortziko)",
        tempo_marking="Vif, incisif et rythmique",
        bpm=132.0,
        time_signature=(3, 4),
        key_signature="Mi phrygien / Sol mineur",
        description=(
            "Architecture en cinq volets (A–B–A'–C–A'') : Scherzo I en Mi phrygien (mes. 1–56), "
            "Trio I nocturne au cor voilé (mes. 57–104), Reprise variée en hémiole (mes. 105–152), "
            "Trio II pastoral basque (mes. 153–192), puis Strette et Coda foudroyante (mes. 193–232)."
        ),
        total_beats=696.0,
    )
    n2 = mvt.notes
    add = lambda p, s, d, v, i, sec: n2.append(NoteEvent(p, s, d, v, i, sec))

    phryg_prog = [
        (40, [52, 56, 59, 62, 65]), (41, [53, 57, 60, 64, 69]),
        (43, [55, 59, 62, 65, 69]), (41, [53, 57, 60, 64, 67]),
        (40, [52, 56, 59, 64, 68]), (45, [57, 60, 64, 67, 71]),
        (41, [53, 56, 59, 62, 65]), (40, [52, 56, 59, 64, 69]),
    ]
    trio_prog = [
        (43, [55, 58, 62, 66, 69]), (39, [51, 55, 58, 62, 65]),
        (36, [48, 55, 58, 63, 67]), (38, [50, 54, 57, 60, 66]),
        (43, [55, 58, 62, 65, 69]), (41, [53, 56, 60, 63, 68]),
        (39, [51, 55, 58, 62, 67]), (40, [52, 56, 59, 62, 65]),
    ]
    scherzo_cells = [
        [(0.0, 0.5, 4), (0.5, 0.25, 5), (0.75, 0.25, 4), (1.0, 0.5, 3), (1.5, 1.0, 4), (2.5, 0.5, 1)],
        [(0.0, 0.5, 2), (0.5, 0.5, 4), (1.0, 0.5, 5), (1.5, 1.0, 7), (2.5, 0.5, 6)],
        [(0.0, 0.75, 6), (0.75, 0.75, 5), (1.5, 0.75, 4), (2.25, 0.75, 2)],
        [(0.0, 0.5, 3), (0.5, 0.5, 2), (1.0, 0.5, 1), (1.5, 1.5, 0)],
    ]

    for bar in range(232):
        b0 = bar * 3.0
        trans = 0
        if bar < 56:
            sec, is_trio, dyn = "Scherzo I (A) — Alborada basque : Pizzicati en guitare & Mi phrygien", False, 86
        elif bar < 104:
            sec, is_trio, dyn = "Trio I Nocturne (B) — Solo de Cor voilé & Célesta en Sol mineur", True, 64
        elif bar < 152:
            sec, is_trio, trans, dyn = "Scherzo II (A') — Reprise variée en hémiole (3/4 ↔ 6/8)", False, 2, 90
        elif bar < 192:
            sec, is_trio, trans, dyn = "Trio II Pastoral (C) — Zortziko basque aux Hautbois & Harpe", True, 5, 68
        else:
            sec, is_trio, trans, dyn = "Strette & Coda — Tourbillon ibérique et fusée finale", False, 0, 94 + min(14, (bar - 192) // 3)

        prog = trio_prog if is_trio else phryg_prog
        bass0, ch0 = prog[bar % len(prog)]
        bass = bass0 + (trans - 12 if trans > 3 else trans)
        ch = [p + trans for p in ch0]

        if not is_trio:
            add(bass, b0, 0.45, dyn + 4, "timpani", sec)
            add(bass, b0, 0.8, dyn, "bass", sec)
            add(bass + 7, b0 + 1.5, 0.8, dyn - 4, "bass", sec)
            for sub in (0.0, 0.75, 1.5, 2.25):
                for i, p in enumerate(ch):
                    add(p + 12, b0 + sub + i * 0.03, 0.3, dyn - 4, "pizz", sec)
            cell = scherzo_cells[(bar + bar // 4) % len(scherzo_cells)]
            for st, dur, deg in cell:
                p = ch[deg % len(ch)] + 12 + (12 if deg >= len(ch) else 0)
                add(p, b0 + st, dur, min(110, dyn + 8), "oboe" if bar % 2 == 0 else "clarinet", sec)
                add(p + 12, b0 + st, dur * 0.8, min(106, dyn + 2), "flute", sec)
                if bar >= 192:
                    add(p, b0 + st, dur, dyn + 4, "brass", sec)
        else:
            add(bass, b0, 2.9, dyn, "bass", sec)
            for p in ch:
                add(p, b0, 2.85, dyn - 10, "strings", sec)
            for i in range(6):
                add(ch[i % len(ch)] + 12, b0 + i * 0.5, 0.7, dyn - 10, "celesta", sec)
                add(ch[(i + 2) % len(ch)] + 12, b0 + i * 0.5, 0.8, dyn - 8, "harp", sec)
            solo_inst = "horn" if bar < 104 else "oboe"
            p1 = ch[(bar * 2) % len(ch)] + 12
            p2 = ch[(bar * 2 + 2) % len(ch)] + 12
            add(p1, b0, 1.9, dyn + 18, solo_inst, sec)
            add(p2, b0 + 2.0, 0.95, dyn + 14, solo_inst, sec)

    return mvt


def compose_movement_3() -> Movement:
    """
    III. Lent et soutenu — Grande Passacaille : 18 Variations (144 mesures à 3/4 • 432 temps @ 64 BPM = 6m45s)
    """
    mvt = Movement(
        number=3,
        roman="III",
        title="Lent et soutenu — Grande Passacaille",
        subtitle="Tombeau d'un monde disparu (18 Variations sur une basse de Sarabande)",
        tempo_marking="Lent, très expressif et sans rigueur",
        bpm=64.0,
        time_signature=(3, 4),
        key_signature="Fa♯ mineur / La majeur",
        description=(
            "Dix-huit variations symphoniques sur un cycle de sarabande de 8 mesures en Fa♯ mineur 9e, "
            "progressant du solo dépouillé des violoncelles et du cor anglais jusqu'au grand climax "
            "orchestral (Variations XII–XIV) avant de s'éteindre sur une tierce picarde lumineuse."
        ),
        total_beats=432.0,
    )
    n3 = mvt.notes
    add = lambda p, s, d, v, i, sec: n3.append(NoteEvent(p, s, d, v, i, sec))

    pass_cycle = [
        (42, [54, 57, 61, 64, 68]), (40, [52, 56, 59, 61, 66]),
        (38, [50, 54, 57, 61, 64]), (37, [49, 53, 56, 59, 62]),
        (35, [47, 50, 54, 57, 61]), (32, [44, 50, 54, 57, 62]),
        (37, [49, 53, 57, 61, 64]), (42, [54, 57, 61, 64, 68]),
    ]
    cycle_names = [
        "Var. I — Basse de Sarabande nue aux Violoncelles & Contrebasses",
        "Var. II — Entrée de la grande cantilène du Cor anglais solo",
        "Var. III — Dialogue du Cor anglais et de la Flûte sur tapis de Cordes",
        "Var. IV — Arabesques de Clarinette en dixièmes",
        "Var. V — Miroitements de Harpe en triolets (Hommage à la Pavane)",
        "Var. VI — Chant des Violons divisés dans le registre aigu",
        "Var. VII — Clair-obscur nocturne : Célesta, Harpe & Cor voilé",
        "Var. VIII — Contrepoint chromatique des Bois",
        "Var. IX — Éclaircie modale en La majeur (Planing d'accords de 11e)",
        "Var. X — Frémissement intérieur (Pizzicati & Arpèges croisés)",
        "Var. XI — Montée dramatique des Cordes et des Cors",
        "Var. XII — Grand Appel des Cuivres sur la basse obstinée",
        "Var. XIII — Apogée lyrique (Tutti symphonique passionné)",
        "Var. XIV — Illumination ravélienne (Glissandi de Harpe & Chœur des Bois)",
        "Var. XV — Décroissance et souvenir lointain",
        "Var. XVI — Retour solitaire du Cor anglais et du Violon solo",
        "Var. XVII — Murmure cristallin de Célesta et Cordes en sourdine",
        "Var. XVIII — Extinction sur la Tierce picarde (Fa# majeur 9e)",
    ]

    for c in range(18):
        sec = cycle_names[c]
        dyn = round(52 + c * 3.8 if c <= 12 else max(48, 98 - (c - 12) * 9))
        for b_in in range(8):
            bar = c * 8 + b_in
            b0 = bar * 3.0
            bass, ch_orig = pass_cycle[b_in]
            ch = [54, 58, 61, 65, 68] if (c >= 16 and b_in == 7) else ch_orig

            add(bass, b0, 1.9, dyn + 4, "bass", sec)
            add(bass + 12, b0 + 2.0, 0.95, dyn, "bass", sec)
            for p in ch:
                add(p, b0, 2.9, dyn - 8, "strings", sec)
            if c >= 2:
                for i, p in enumerate(ch):
                    add(p + 12, b0 + 0.5 + i * 0.25, 1.4, dyn - 10, "harp", sec)
            if c in (6, 8, 13) or c >= 16:
                add(ch[-1] + 24, b0 + 1.0, 1.5, dyn - 12, "celesta", sec)
            if c >= 1:
                lead = "oboe" if c % 4 == 1 else "flute" if c % 4 == 2 else "clarinet" if c % 4 == 3 else "horn"
                m1 = ch[(b_in + c) % len(ch)] + 12
                m2 = ch[(b_in + c + 2) % len(ch)] + 12
                m3 = ch[(b_in + c + 4) % len(ch)] + 12
                add(m1, b0, 1.5, min(106, dyn + 14), lead, sec)
                add(m2, b0 + 1.5, 0.5, min(104, dyn + 10), lead, sec)
                add(m3, b0 + 2.0, 1.0, min(106, dyn + 12), lead, sec)
                if 10 <= c <= 14:
                    add(m1 + 12, b0, 1.5, dyn + 8, "flute", sec)
                    add(m1, b0, 2.8, dyn + 6, "brass", sec)

    return mvt


def compose_movement_4() -> Movement:
    """
    IV. Final : Animé et féerique — La Grande Horlogerie et l'Océan (186 mesures à 4/4 • 744 temps @ 124 BPM = 6m00s)
    """
    mvt = Movement(
        number=4,
        roman="IV",
        title="Final — Animé et féerique",
        subtitle="La Grande Horlogerie et l'Océan (12 Paliers d'accumulation cyclique)",
        tempo_marking="Animé, éblouissant et implacable",
        bpm=124.0,
        time_signature=(4, 4),
        key_signature="Ré majeur Lydien",
        description=(
            "Douze grands paliers d'accumulation orchestrale (alliant l'implacable crescendo de Boléro "
            "à la Danse générale de Daphnis et Chloé) avec récapitulation cyclique des thèmes des "
            "quatre mouvements jusqu'à l'apothéose en Ré majeur 13e (#11)."
        ),
        total_beats=744.0,
    )
    n4 = mvt.notes
    add = lambda p, s, d, v, i, sec: n4.append(NoteEvent(p, s, d, v, i, sec))

    fin_cycle = [
        (38, [50, 57, 61, 66, 69]), (40, [52, 59, 62, 66, 71]),
        (42, [54, 61, 64, 69, 73]), (43, [55, 62, 66, 69, 74]),
        (38, [50, 57, 62, 66, 71]), (36, [48, 55, 60, 64, 69]),
        (43, [55, 59, 62, 67, 71]), (45, [57, 62, 64, 69, 74]),
    ]
    palier_names = [
        "Palier I — Murmure mécanique initial (Ostinato de Pizzicati & Harpe seule)",
        "Palier II — Entrée de la Flûte solitaire sur le mouvement d'horlogerie",
        "Palier III — Dialogue de la Clarinette et du Hautbois en mode de Ré Lydien",
        "Palier IV — Éclat cristallin du Célesta et des Cordes divisées",
        "Palier V — Appel lointain des Cors et doublement en tierces parallèles",
        "Palier VI — Polytonalité ravélienne (Superposition Ré majeur / Do majeur 9e)",
        "Palier VII — Rappel cyclique de la Passacaille (Mouvement III) aux Bois",
        "Palier VIII — Rappel cyclique du Scherzo basque (Mouvement II) aux Pizzicati",
        "Palier IX — Grande Vague océanique : Arpèges de Harpe & Cordes passionnées",
        "Palier X — Rappel cyclique solennel du Thème initial (Mouvement I) aux Cuivres",
        "Palier XI — Danse générale incandescente (Tutti symphonique & Timbales)",
        "Palier XII — Apothéose finale : La Grande Horlogerie en Ré majeur 13e (#11)",
    ]
    inst_list = ["flute", "clarinet", "oboe", "flute", "horn", "oboe", "oboe", "clarinet", "flute", "brass", "brass", "brass"]

    for bar in range(186):
        b0 = bar * 4.0
        stage = min(11, bar // 15)
        sec = palier_names[stage]
        dyn = round(54 + stage * 4.5)
        bass, ch = fin_cycle[bar % len(fin_cycle)]

        add(bass, b0, 1.9, dyn + 6, "bass", sec)
        add(bass + 7, b0 + 2.0, 1.9, dyn + 4, "bass", sec)
        if stage >= 6:
            add(bass, b0, 0.5, dyn + 10, "timpani", sec)
            add(bass + 7, b0 + 2.0, 0.5, dyn + 6, "timpani", sec)
            if stage >= 10:
                add(bass, b0 + 3.5, 0.4, dyn + 8, "timpani", sec)

        for s in range(8):
            po = ch[s % len(ch)] + 12
            add(po, b0 + s * 0.5, 0.4, dyn - 4, "harp", sec)
            if stage <= 4 or stage == 7:
                add(ch[(s + 1) % len(ch)], b0 + s * 0.5, 0.3, dyn, "pizz", sec)
            if stage >= 3:
                add(po + 12, b0 + s * 0.5 + 0.25, 0.35, dyn - 8, "celesta", sec)

        if stage >= 1:
            for p in ch:
                add(p, b0, 3.9, dyn - 4, "strings", sec)
        if stage >= 4:
            add(ch[1], b0, 3.8, dyn, "horn", sec)
            add(ch[3], b0, 3.8, dyn, "horn", sec)
        if stage >= 9:
            for p in ch:
                add(p + 12, b0, 3.8, dyn + 4, "brass", sec)

        lead = inst_list[stage]
        mp1 = ch[(bar * 2) % len(ch)] + 12
        mp2 = ch[(bar * 2 + 1) % len(ch)] + 12
        mp3 = ch[(bar * 2 + 3) % len(ch)] + 12
        add(mp1, b0, 1.5, min(110, dyn + 12), lead, sec)
        add(mp2, b0 + 1.5, 0.5, min(108, dyn + 8), lead, sec)
        add(mp3, b0 + 2.0, 2.0, min(112, dyn + 14), lead, sec)
        if stage >= 4:
            add(mp1 - 3, b0, 1.5, dyn + 6, "clarinet", sec)
            add(mp3 - 3, b0 + 2.0, 2.0, dyn + 8, "clarinet", sec)
        if stage >= 8:
            add(mp1 + 12, b0, 1.5, dyn + 8, "flute", sec)
            add(mp3 + 12, b0 + 2.0, 2.0, dyn + 10, "flute", sec)

    return mvt


# ============================================================================
# EXPORT MIDI STANDARD (FORMAT 1 MULTI-PISTES)
# ============================================================================

GM_PROGRAM_MAP = {
    "flute": (0, 73),
    "oboe": (1, 68),
    "clarinet": (2, 71),
    "horn": (3, 60),
    "brass": (4, 56),
    "harp": (5, 46),
    "celesta": (6, 8),
    "strings": (7, 48),
    "pizz": (8, 45),
    "bass": (10, 43),
    "timpani": (11, 47),
}


def encode_varlen(value: int) -> bytes:
    buf = [value & 0x7F]
    value >>= 7
    while value > 0:
        buf.append((value & 0x7F) | 0x80)
        value >>= 7
    buf.reverse()
    return bytes(buf)


def write_midi_file(movements: List[Movement], filepath: str) -> None:
    ticks_per_beat = 480
    tracks_data: List[bytes] = []

    t0_events: List[Tuple[int, bytes]] = []
    current_tick = 0
    for mvt in movements:
        us_per_beat = int(60_000_000 / mvt.bpm)
        tempo_meta = b"\xFF\x51\x03" + struct.pack(">I", us_per_beat)[1:]
        t0_events.append((current_tick, tempo_meta))
        title_bytes = f"{mvt.roman}. {mvt.title}".encode("utf-8")
        marker_meta = b"\xFF\x06" + encode_varlen(len(title_bytes)) + title_bytes
        t0_events.append((current_tick, marker_meta))
        current_tick += int((mvt.total_beats + 4.0) * ticks_per_beat)

    t0_bytes = bytearray()
    last_tick = 0
    for tick, data in sorted(t0_events, key=lambda x: x[0]):
        t0_bytes.extend(encode_varlen(tick - last_tick))
        t0_bytes.extend(data)
        last_tick = tick
    t0_bytes.extend(b"\x00\xFF\x2F\x00")
    tracks_data.append(bytes(t0_bytes))

    for inst_name, (channel, program) in GM_PROGRAM_MAP.items():
        inst_events: List[Tuple[int, int, bytes]] = []
        name_bytes = inst_name.capitalize().encode("ascii")
        inst_events.append((0, 0, b"\xFF\x03" + encode_varlen(len(name_bytes)) + name_bytes))
        inst_events.append((0, 1, bytes([0xC0 | channel, program])))

        base_tick = 0
        for mvt in movements:
            for n in mvt.notes:
                if n.instrument == inst_name:
                    st_tick = base_tick + int(round(n.start_beat * ticks_per_beat))
                    end_tick = base_tick + int(round((n.start_beat + n.duration) * ticks_per_beat))
                    pitch = max(0, min(127, n.pitch))
                    vel = max(1, min(127, n.velocity))
                    inst_events.append((st_tick, 2, bytes([0x90 | channel, pitch, vel])))
                    inst_events.append((end_tick, 1, bytes([0x80 | channel, pitch, 0])))
            base_tick += int((mvt.total_beats + 4.0) * ticks_per_beat)

        inst_events.sort(key=lambda x: (x[0], x[1]))
        tr_bytes = bytearray()
        last_t = 0
        for tick, _, ev_bytes in inst_events:
            tr_bytes.extend(encode_varlen(max(0, tick - last_t)))
            tr_bytes.extend(ev_bytes)
            last_t = tick
        tr_bytes.extend(b"\x00\xFF\x2F\x00")
        tracks_data.append(bytes(tr_bytes))

    with open(filepath, "wb") as f:
        f.write(b"MThd" + struct.pack(">IHHH", 6, 1, len(tracks_data), ticks_per_beat))
        for tr in tracks_data:
            f.write(b"MTrk" + struct.pack(">I", len(tr)) + tr)


def export_score_json(movements: List[Movement], json_path: str) -> None:
    total_sec = sum(m.total_beats * 60.0 / m.bpm for m in movements)
    data = {
        "title": "Symphonie en Ré (M. posth.) — « L'Horloge et l'Océan »",
        "composer": "Dans le style de Maurice Ravel (1875–1937)",
        "total_duration_seconds": round(total_sec, 1),
        "total_duration_formatted": f"{int(total_sec // 60)}m {int(total_sec % 60):02d}s",
        "movements": [
            {
                "number": m.number,
                "roman": m.roman,
                "title": m.title,
                "subtitle": m.subtitle,
                "tempo_marking": m.tempo_marking,
                "bpm": m.bpm,
                "time_signature": list(m.time_signature),
                "key_signature": m.key_signature,
                "description": m.description,
                "total_beats": m.total_beats,
                "duration_seconds": round(m.total_beats * 60.0 / m.bpm, 1),
                "note_count": len(m.notes),
            }
            for m in movements
        ],
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    midi_dir = os.path.join(base_dir, "midi")
    os.makedirs(midi_dir, exist_ok=True)

    movements = [
        compose_movement_1(),
        compose_movement_2(),
        compose_movement_3(),
        compose_movement_4(),
    ]

    total_notes = sum(len(m.notes) for m in movements)
    total_sec = sum(m.total_beats * 60.0 / m.bpm for m in movements)

    for mvt in movements:
        m_sec = mvt.total_beats * 60.0 / mvt.bpm
        m_path = os.path.join(midi_dir, f"Ravel_Symphonie_Mvt_{mvt.number}_{mvt.roman}.mid")
        write_midi_file([mvt], m_path)
        print(f"[OK] MIDI Mouvement {mvt.roman} ({int(m_sec // 60)}m{int(m_sec % 60):02d}s, {len(mvt.notes)} notes) : {m_path}")

    full_midi_path = os.path.join(midi_dir, "Ravel_Symphonie_en_Re_Integrale.mid")
    write_midi_file(movements, full_midi_path)
    print(f"[OK] MIDI Symphonie integrale ({int(total_sec // 60)}m{int(total_sec % 60):02d}s, {total_notes} notes) : {full_midi_path}")

    json_path = os.path.join(base_dir, "symphony_score.json")
    export_score_json(movements, json_path)
    print(f"[OK] Metadonnees de partition exportees : {json_path}")


if __name__ == "__main__":
    main()
