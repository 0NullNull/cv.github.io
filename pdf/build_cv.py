#!/usr/bin/env python3
"""
Builds the one-page A4 PDF versions of the CV (Finnish + English).

    python3 pdf/build_cv.py

Writes Kasper_Kuirinlahti_CV.pdf and Kasper_Kuirinlahti_CV_EN.pdf to the repo root.
These public copies have no phone number.

Private copies for job applications, with the phone number (never written into the repo):

    CV_PHONE="+358 ..." python3 pdf/build_cv.py --out <folder outside the repo>

Needs: reportlab, Pillow. Fonts (IBM Plex, OFL) live in pdf/fonts/.
Content is kept in CONTENT below -- update it together with index.html / en.html.
"""
from io import BytesIO
import os
import sys
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "pdf" / "fonts"
SITE = "kuirinlahti.dev"

for name, file in {
    "Sans": "IBMPlexSans-Regular.ttf",
    "Sans-Md": "IBMPlexSans-Medium.ttf",
    "Sans-Sb": "IBMPlexSans-SemiBold.ttf",
    "Cond-Bd": "IBMPlexSansCondensed-Bold.ttf",
    "Mono": "IBMPlexMono-Regular.ttf",
    "Mono-Md": "IBMPlexMono-Medium.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONTS / file)))

# Same palette as style.css (light theme)
INK, MUTED, LINE = HexColor("#13212B"), HexColor("#55656F"), HexColor("#D3DCE0")
BRINE, AMBER, PAPER = HexColor("#24617D"), HexColor("#B67A06"), HexColor("#FFFFFF")
CAT = {
    "core":   (HexColor("#24617D"), HexColor("#E2EEF4")),
    "ai":     (HexColor("#6A4DA6"), HexColor("#EEE8F8")),
    "integr": (HexColor("#2B7A4B"), HexColor("#E1F1E7")),
    "infra":  (HexColor("#9A5A00"), HexColor("#F7EBD6")),
    "tools":  (HexColor("#4B5A78"), HexColor("#E7EAF1")),
    "other":  (HexColor("#5A676E"), HexColor("#ECEFF1")),
}

W, H = A4
M = 34                       # page margin
MAIN_X, MAIN_W = M, 336
SIDE_X = M + MAIN_W + 22
SIDE_W = W - M - SIDE_X

# ---------------------------------------------------------------- content
CONTENT = {
    "fi": {
        "file": "Kasper_Kuirinlahti_CV.pdf",
        "title": "Ohjelmistokehittäjä",
        "tagline": "Full-stack .NET · tietokannat · palvelinympäristöt · tekoälyintegraatiot",
        "phone": "Puh",
        "contact": [("Email", "kuirinlahtikasper@gmail.com", "mailto:kuirinlahtikasper@gmail.com"),
                    ("GitHub", "github.com/0NullNull", "https://github.com/0NullNull"),
                    ("Sijainti", "Parkano, Pirkanmaa", None)],
        "h": {"profile": "Profiili", "exp": "Työkokemus", "edu": "Koulutus", "trust": "Luottamustehtävät"},
        "profile": [
            "Ohjelmistokehittäjä, joka on suunnitellut ja rakentanut tuotantokäytössä olevan, laajan "
            "toiminnanohjausalustan alusta loppuun: käyttöliittymästä ja rajapinnoista tietokantaan, "
            "palvelinympäristöön ja tekoälyintegraatioihin. Teen mielelläni kokonaisuuksia, joissa "
            "tekniikka palvelee oikeaa työtä, ja opin uutta nopeasti.",
            "Olen laaja-alainen kehittäjä, ja nyt haluan syventyä yhteen alueeseen ja kasvaa sen "
            "asiantuntijaksi kokeneempien kehittäjien rinnalla.",
        ],
        "seeking": ("Haen", "ohjelmistokehittäjän tehtäviä Pirkanmaalla tai etänä."),
        "job": {
            "title": "Ohjelmistokehittäjä", "when": "11/2025–",
            "where": "Suomen Tekojää Oy · jäähallit, lämpöpumput ja kylmätekniikka",
            "intro": "Suunnittelin ja rakensin yrityksen sisäisen toiminnanohjausalustan, joka on päivittäisessä "
                     "tuotantokäytössä noin 15 käyttäjällä, ja käyttöönotto laajenee edelleen. Vastaan sen "
                     "kehityksestä ja ylläpidosta.",
            "stats": [("400+", "laitetta yli 200 kohteessa"), ("20 000+", "tiedostoa ja kuvaa"),
                      ("≈ 100 000", "muutosta muutoslokissa")],
            "subs": [
                ("core", "Toiminnanohjausalusta", ".NET 10 · Blazor · PostgreSQL",
                 "Laitekanta, huolto ja työraportit, projektinhallinta, chat ja ilmoitukset."),
                ("integr", "PLC-datankeruuohjelma", "Python · Windows-palvelu",
                 "Kerää dataa kohteiden ohjaimilta. Asennusvelho ja allekirjoitetut automaattipäivitykset."),
                ("ai", "Tekoälyavustaja", "Claude API · Ollama · RAG",
                 "Hakee ja käsittelee yrityksen omaa dataa käyttäjän käyttöoikeuksien rajoissa."),
                ("core", "Asiakasportaali", "ASP.NET Core",
                 "Erillinen internet-sovellus asiakkaille, eristetty sisäisestä datasta."),
                ("infra", "Palvelinympäristö", "Docker · Nginx · Linux",
                 "Julkaisut, varmuuskopiot, valvonta ja tietoturva omalla laitteistolla."),
            ],
            "case": ("Projektiesittely", "Kenttätoimintojen alusta",
                     "≈ 270 000 riviä koodia · 1 600+ committia · 9 osa-aluetta", SITE + "/showcase/"),
        },
        "job2": ("Tilaustyöprojektit", "2021–2024", "Opintojen aikana",
                 "Pelejä paikallisille yrityksille tilaustyönä koulun kautta."),
        "edu": ("Tieto- ja viestintätekniikan perustutkinto", "2021–2024", "Ohjelmistokehittäjä · Vuoksi"),
        "trust": [("Parkanon nuorisovaltuuston varapuheenjohtaja", "2019–2020")],
        "groups": [
            ("core", "Päivittäinen käyttö", False, ["C#", ".NET / ASP.NET Core", "Blazor", "Entity Framework",
                                                    "PostgreSQL", "JavaScript", "HTML / CSS", "Docker", "Linux", "Git"]),
            ("core", "Kokemusta", True, ["Python", "C++", "SignalR", "TimescaleDB", "REST-rajapinnat"]),
            ("ai", "Tekoäly", False, ["Claude API", "Ollama", "RAG / pgvector", "LLM-agentit",
                                     "Tekoälyavusteinen kehitys"]),
            ("tools", "Kehitystyökalut", False, ["Visual Studio", "VS Code", "Claude Code", "GitHub",
                                                "GitHub Actions", "pgAdmin", "xUnit"]),
            ("infra", "Palvelimet ja tietoturva", False, ["Docker Compose", "Nginx", "YARP",
                                                         "TLS / oma varmentaja (CA)", "pgAudit"]),
            ("integr", "Integraatiot", False, ["Beckhoff TwinCAT / ADS", "Microsoft Entra ID & Graph",
                                              "Pipedrive API", "Google Maps API", "Web Push",
                                              "WebAuthn / passkeys", "PyInstaller"]),
            ("other", "Muut ohjelmistot", False, ["Photoshop", "DaVinci Resolve", "Word & Excel"]),
        ],
        "rows": [("Kielet", [("Suomi", "äidinkieli"), ("Englanti", "erinomainen")]),
                 ("Muuta", [("B-ajokortti", "oma auto")])],
        "footer": ("Verkossa", SITE, "Päivitetty 10/2026"),
        "legend": "täytetty = päivittäin · ääriviiva = kokemusta",
    },
    "en": {
        "file": "Kasper_Kuirinlahti_CV_EN.pdf",
        "title": "Software Developer",
        "tagline": "Full-stack .NET · databases · server infrastructure · AI integrations",
        "phone": "Phone",
        "contact": [("Email", "kuirinlahtikasper@gmail.com", "mailto:kuirinlahtikasper@gmail.com"),
                    ("GitHub", "github.com/0NullNull", "https://github.com/0NullNull"),
                    ("Location", "Parkano, Finland", None)],
        "h": {"profile": "Profile", "exp": "Experience", "edu": "Education", "trust": "Positions of trust"},
        "profile": [
            "Software developer who designed and built a large operations platform that is in daily "
            "production use, end to end: from the user interface and APIs to the database, server "
            "infrastructure and AI integrations. I enjoy building systems where technology supports "
            "real work, and I learn new things quickly.",
            "I am a generalist by experience, and now I want to go deep in one area and grow into "
            "an expert in it alongside more experienced developers.",
        ],
        "seeking": ("Looking for", "software developer roles in the Pirkanmaa region or remote."),
        "job": {
            "title": "Software Developer", "when": "11/2025–",
            "where": "Suomen Tekojää Oy · ice rinks, heat pumps and refrigeration",
            "intro": "Designed and built the company's internal operations platform, which is in daily production "
                     "use by about 15 people, with rollout still expanding. I am responsible for its development "
                     "and operation.",
            "stats": [("400+", "devices across 200+ sites"), ("20,000+", "files and images"),
                      ("≈ 100,000", "changes in the audit trail")],
            "subs": [
                ("core", "Operations platform", ".NET 10 · Blazor · PostgreSQL",
                 "Equipment registry, service and work reports, project management, chat and notifications."),
                ("integr", "PLC data collector", "Python · Windows service",
                 "Collects data from controllers at customer sites. Setup wizard and signed automatic updates."),
                ("ai", "AI assistant", "Claude API · Ollama · RAG",
                 "Finds and works with company data within each user's access rights."),
                ("core", "Customer portal", "ASP.NET Core",
                 "Separate internet-facing app for customers, isolated from internal data."),
                ("infra", "Server infrastructure", "Docker · Nginx · Linux",
                 "Deployments, backups, monitoring and security on company-owned hardware."),
            ],
            "case": ("Case study", "Field Operations Platform",
                     "≈ 270,000 lines of code · 1,600+ commits · 9 feature areas", SITE + "/showcase/en.html"),
        },
        "job2": ("Commissioned projects", "2021–2024", "During studies",
                 "Games for local companies, commissioned through school."),
        "edu": ("Vocational Qualification in ICT", "2021–2024", "Software Developer · Vuoksi"),
        "trust": [("Vice-chair, Parkano Youth Council", "2019–2020")],
        "groups": [
            ("core", "Daily use", False, ["C#", ".NET / ASP.NET Core", "Blazor", "Entity Framework",
                                          "PostgreSQL", "JavaScript", "HTML / CSS", "Docker", "Linux", "Git"]),
            ("core", "Experience with", True, ["Python", "C++", "SignalR", "TimescaleDB", "REST APIs"]),
            ("ai", "AI", False, ["Claude API", "Ollama", "RAG / pgvector", "LLM agents",
                                "AI-assisted development"]),
            ("tools", "Development tools", False, ["Visual Studio", "VS Code", "Claude Code", "GitHub",
                                                  "GitHub Actions", "pgAdmin", "xUnit"]),
            ("infra", "Infrastructure & security", False, ["Docker Compose", "Nginx", "YARP",
                                                          "TLS / private CA", "pgAudit"]),
            ("integr", "Integrations", False, ["Beckhoff TwinCAT / ADS", "Microsoft Entra ID & Graph",
                                              "Pipedrive API", "Google Maps API", "Web Push",
                                              "WebAuthn / passkeys", "PyInstaller"]),
            ("other", "Other software", False, ["Photoshop", "DaVinci Resolve", "Word & Excel"]),
        ],
        "rows": [("Languages", [("Finnish", "native"), ("English", "excellent")]),
                 ("Other", [("Driving licence (B)", "own car")])],
        "footer": ("Online", SITE + "/en.html", "Updated 10/2026"),
        "legend": "filled = daily use · outlined = experience",
    },
}

# ---------------------------------------------------------------- helpers
def style(size, font="Sans", color=INK, leading=None):
    return ParagraphStyle("s", fontName=font, fontSize=size, leading=leading or size * 1.38,
                          textColor=color, alignment=TA_LEFT)


def para(c, text, st, x, y, w):
    """Draw a wrapped paragraph with its top at y; return its height."""
    text = text.replace("&", "&amp;")
    p = Paragraph(text, st)
    _, h = p.wrap(w, 2000)
    p.drawOn(c, x, y - h)
    return h


def spaced(c, text, x, y, font, size, color, space=0.9):
    """Uppercase label with letter-spacing; return its width."""
    c.saveState()
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(space)
    t.setFillColor(color)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()
    return pdfmetrics.stringWidth(text, font, size) + space * len(text)


def main_heading(c, text, x, y, w):
    c.setFillColor(AMBER)
    c.roundRect(x, y - 7.5, 6, 6, 1, stroke=0, fill=1)
    tw = spaced(c, text.upper(), x + 11, y - 7, "Mono-Md", 7.6, INK, 1.1)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(x + 11 + tw + 6, y - 4.8, x + w, y - 4.8)
    return 15


def side_heading(c, text, x, y, w, color):
    c.setFillColor(color)
    c.circle(x + 2.6, y - 4.6, 2.6, stroke=0, fill=1)
    tw = spaced(c, text.upper(), x + 9, y - 7, "Mono-Md", 7, color, 0.9)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(x + 9 + tw + 5, y - 4.8, x + w, y - 4.8)
    return 13


def pill(c, text, x_right, y):
    tw = pdfmetrics.stringWidth(text, "Mono", 7.6)
    c.setStrokeColor(LINE)
    c.setFillColor(PAPER)
    c.setLineWidth(0.6)
    c.roundRect(x_right - tw - 10, y - 12, tw + 10, 12.5, 2, stroke=1, fill=1)
    c.setFillColor(INK)
    c.setFont("Mono", 7.6)
    c.drawRightString(x_right - 5, y - 8.8, text)
    return tw + 10


def chips(c, items, x, y, w, cat, outline):
    fg, bg = CAT[cat]
    size, ph, h, gap = 7.5, 4.5, 13.5, 3.2
    cx, cy = x, y
    for item in items:
        tw = pdfmetrics.stringWidth(item, "Mono-Md", size) + ph * 2
        if cx + tw > x + w and cx > x:
            cx, cy = x, cy - h - gap
        if outline:
            c.setFillColor(PAPER)
            c.setStrokeColor(fg)
            c.setLineWidth(0.7)
            c.roundRect(cx, cy - h, tw, h, 2, stroke=1, fill=1)
        else:
            c.setFillColor(bg)
            c.roundRect(cx, cy - h, tw, h, 2, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Mono-Md", size)
        c.drawString(cx + ph, cy - h + 4.2, item)
        cx += tw + gap
    return y - cy + h


def circle_photo(c, path, x, y_top, d):
    img = Image.open(path).convert("RGB")
    s = min(img.size)
    left, top = (img.width - s) // 2, (img.height - s) // 2
    img = img.crop((left, top, left + s, top + s)).resize((600, 600))
    buf = BytesIO()
    img.save(buf, "JPEG", quality=90)
    buf.seek(0)
    c.saveState()
    p = c.beginPath()
    p.circle(x + d / 2, y_top - d / 2, d / 2)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(buf), x, y_top - d, d, d)
    c.restoreState()
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.circle(x + d / 2, y_top - d / 2, d / 2, stroke=1, fill=0)


# ---------------------------------------------------------------- page
def build(lang, out_dir, phone):
    d = CONTENT[lang]
    out = out_dir / d["file"]
    contact = ([(d["phone"], phone, None)] if phone else []) + d["contact"]
    c = canvas.Canvas(str(out), pagesize=A4)
    c.setTitle("Kasper Kuirinlahti – CV")
    c.setAuthor("Kasper Kuirinlahti")
    c.setSubject(d["title"])
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # ---- header
    top = H - M
    photo = 74
    circle_photo(c, ROOT / "images" / "kuva.png", M, top, photo)
    hx = M + photo + 20
    c.setFillColor(INK)
    c.setFont("Cond-Bd", 30)
    c.drawString(hx, top - 26, "Kasper Kuirinlahti")
    spaced(c, d["title"].upper(), hx, top - 41, "Mono-Md", 8.6, BRINE, 1.4)
    c.setFillColor(MUTED)
    c.setFont("Sans", 9)
    c.drawString(hx, top - 54, d["tagline"])
    cx, cy = hx, top - 68
    for label, value, link in contact:
        need = pdfmetrics.stringWidth(label.upper(), "Mono-Md", 6.4) + 0.7 * len(label) + 4 \
            + pdfmetrics.stringWidth(value, "Sans-Md", 8.4)
        if cx + need > W - M:
            cx, cy = hx, cy - 12
        lw = spaced(c, label.upper(), cx, cy, "Mono-Md", 6.4, MUTED, 0.7)
        c.setFillColor(INK)
        c.setFont("Sans-Md", 8.4)
        c.drawString(cx + lw + 4, cy, value)
        vw = pdfmetrics.stringWidth(value, "Sans-Md", 8.4)
        if link:
            c.linkURL(link, (cx + lw + 4, cy - 2, cx + lw + 4 + vw, cy + 8), relative=0)
        cx += lw + 4 + vw + 14
    rule_y = top - photo - 12
    c.setStrokeColor(INK)
    c.setLineWidth(1.4)
    c.line(M, rule_y, W - M, rule_y)

    # ---- main column
    y = rule_y - 16
    x, w = MAIN_X, MAIN_W
    y -= main_heading(c, d["h"]["profile"], x, y, w)
    for t in d["profile"]:
        y -= para(c, t, style(9.4, leading=13.4), x, y, w) + 4
    lab, txt = d["seeking"]
    lw = spaced(c, lab.upper(), x, y - 8, "Mono-Md", 6.6, MUTED, 0.7)
    para(c, txt, style(9), x + lw + 5, y, w - lw - 5)
    y -= 20

    y -= main_heading(c, d["h"]["exp"], x, y, w)
    j = d["job"]
    c.setFillColor(BRINE)
    c.setFont("Sans-Sb", 11.2)
    c.drawString(x, y - 10, j["title"])
    pill(c, j["when"], x + w, y)
    y -= 15
    y -= para(c, j["where"], style(8.8, color=MUTED), x, y, w) + 3
    y -= para(c, j["intro"], style(9.1, leading=12.9), x, y, w) + 6

    # figures
    cw = (w - 6) / 3
    heights = []
    for i, (num, label) in enumerate(j["stats"]):
        heights.append(Paragraph(label, style(7.2, color=MUTED, leading=9)).wrap(cw - 14, 100)[1])
    bh = 22 + max(heights) + 6
    for i, (num, label) in enumerate(j["stats"]):
        bx = x + i * (cw + 3)
        c.setStrokeColor(LINE)
        c.setFillColor(PAPER)
        c.setLineWidth(0.6)
        c.roundRect(bx, y - bh, cw, bh, 3, stroke=1, fill=1)
        c.setFillColor(BRINE)
        c.setFont("Cond-Bd", 14)
        c.drawString(bx + 7, y - 17, num)
        para(c, label, style(7.2, color=MUTED, leading=9), bx + 7, y - 21, cw - 14)
    y -= bh + 8

    # sub-projects
    for cat, name, tech, desc in j["subs"]:
        fg, _ = CAT[cat]
        start = y
        c.setFillColor(INK)
        c.setFont("Sans-Sb", 9.2)
        c.drawString(x + 9, y - 8.5, name)
        c.setFillColor(fg)
        c.setFont("Mono-Md", 6.9)
        c.drawRightString(x + w, y - 8.3, tech)
        y -= 12
        y -= para(c, desc, style(8.5, color=MUTED, leading=11.4), x + 9, y, w - 9)
        c.setFillColor(fg)
        c.rect(x, y - 1, 2.4, start - y + 1, stroke=0, fill=1)
        y -= 7

    # case study box
    tag, title, stats, url = j["case"]
    y -= 2
    bh = 46
    c.setFillColor(CAT["core"][1])
    c.roundRect(x, y - bh, w, bh, 3, stroke=0, fill=1)
    c.setFillColor(BRINE)
    c.rect(x, y - bh, 2.6, bh, stroke=0, fill=1)
    spaced(c, tag.upper(), x + 11, y - 11, "Mono-Md", 6.4, BRINE, 1)
    c.setFillColor(INK)
    c.setFont("Cond-Bd", 12.5)
    c.drawString(x + 11, y - 24.5, title)
    c.setFillColor(MUTED)
    c.setFont("Sans", 7.6)
    c.drawString(x + 11, y - 36, stats)
    c.setFillColor(BRINE)
    c.setFont("Mono-Md", 7.2)
    c.drawRightString(x + w - 9, y - 11, url)
    c.linkURL("https://" + url, (x, y - bh, x + w, y), relative=0)
    y -= bh + 12

    # second job
    t2, when2, where2, desc2 = d["job2"]
    c.setFillColor(BRINE)
    c.setFont("Sans-Sb", 10)
    c.drawString(x, y - 9.5, t2)
    pill(c, when2, x + w, y)
    y -= 14
    y -= para(c, where2 + " · " + desc2, style(8.8, color=MUTED), x, y, w) + 14

    # education
    y -= main_heading(c, d["h"]["edu"], x, y, w)
    et, ew, ed = d["edu"]
    c.setFillColor(BRINE)
    c.setFont("Sans-Sb", 10)
    c.drawString(x, y - 9.5, et)
    pill(c, ew, x + w, y)
    y -= 14
    y -= para(c, ed, style(8.8, color=MUTED), x, y, w) + 14

    # positions of trust
    y -= main_heading(c, d["h"]["trust"], x, y, w)
    for text, when in d["trust"]:
        c.setFillColor(INK)
        c.setFont("Sans", 8.6)
        c.drawString(x, y - 9, text)
        c.setFillColor(MUTED)
        c.setFont("Mono", 7.6)
        c.drawRightString(x + w, y - 9, when)
        y -= 14
    main_bottom = y

    # ---- sidebar
    x, w = SIDE_X, SIDE_W
    y = rule_y - 16
    for cat, title, outline, items in d["groups"]:
        y -= side_heading(c, title, x, y, w, CAT[cat][0])
        y -= chips(c, items, x, y, w, cat, outline) + 14
        if outline:  # explain filled vs outlined right after the "experience" group
            c.setFillColor(MUTED)
            c.setFont("Sans", 6.6)
            c.drawString(x, y + 5, d["legend"])
            y -= 6
    for title, rows in d["rows"]:
        y -= side_heading(c, title, x, y, w, CAT["other"][0])
        for i, (k, v) in enumerate(rows):
            c.setFillColor(INK)
            c.setFont("Sans", 8.4)
            c.drawString(x, y - 9, k)
            c.setFillColor(MUTED)
            c.setFont("Mono", 7.4)
            c.drawRightString(x + w, y - 9, v)
            y -= 13
            if i < len(rows) - 1:
                c.setStrokeColor(LINE)
                c.setDash(1.5, 1.5)
                c.setLineWidth(0.5)
                c.line(x, y + 1, x + w, y + 1)
                c.setDash()
        y -= 9
    side_bottom = y

    # ---- footer
    fy = M - 14
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(M, fy + 11, W - M, fy + 11)
    lab, url, updated = d["footer"]
    lw = spaced(c, lab.upper(), M, fy, "Mono-Md", 6.4, MUTED, 0.7)
    c.setFillColor(BRINE)
    c.setFont("Mono-Md", 7.4)
    c.drawString(M + lw + 5, fy, url)
    c.linkURL("https://" + url, (M + lw + 5, fy - 2, M + lw + 5 + pdfmetrics.stringWidth(url, "Mono-Md", 7.4), fy + 8), relative=0)
    c.setFillColor(MUTED)
    c.setFont("Mono", 6.8)
    c.drawRightString(W - M, fy, updated)

    c.showPage()
    c.save()
    lowest = min(main_bottom, side_bottom)
    print(f"{out.name}: main ends {main_bottom:.0f}pt, sidebar ends {side_bottom:.0f}pt, footer at {fy + 11:.0f}pt")
    if lowest < fy + 16:
        raise SystemExit(f"{out.name}: content overflows into the footer")


if __name__ == "__main__":
    phone = os.environ.get("CV_PHONE", "").strip()
    out_dir = ROOT
    if "--out" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--out") + 1]).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
    if phone and (out_dir == ROOT or ROOT in out_dir.parents):
        raise SystemExit("CV_PHONE is set: pass --out <folder outside the repo> so the phone number never lands in it")
    for lang in CONTENT:
        build(lang, out_dir, phone)
