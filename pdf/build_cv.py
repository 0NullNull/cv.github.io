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

SHOW_CASE = False  # True once the showcase page is back

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

# Warm Nordic Editorial palette (matches style.css)
INK, MUTED, LINE = HexColor("#171614"), HexColor("#6A665E"), HexColor("#E2DDD4")
BRINE, AMBER, PAPER = HexColor("#171614"), HexColor("#D44724"), HexColor("#FFFFFF")
CAT = {
    "core":   (HexColor("#D44724"), HexColor("#F6F4EF")),
    "ai":     (HexColor("#1E5643"), HexColor("#E5F1EC")),
    "integr": (HexColor("#1E5643"), HexColor("#F6F4EF")),
    "infra":  (HexColor("#8C4A1C"), HexColor("#F6F4EF")),
    "tools":  (HexColor("#3D3A35"), HexColor("#EDEAE2")),
    "other":  (HexColor("#6A665E"), HexColor("#F6F4EF")),
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
        "contact": [("Email", "kasper@kuirinlahti.dev", "mailto:kasper@kuirinlahti.dev"),
                    ("GitHub", "github.com/0NullNull", "https://github.com/0NullNull"),
                    ("Sijainti", "Parkano, Pirkanmaa", None)],
        "h": {"profile": "Profiili", "exp": "Työkokemus", "side": "Omat projektit", "edu": "Koulutus",
              "trust": "Luottamustehtävät"},
        "profile": [
            "Ohjelmistokehittäjä, joka suunnittelee, rakentaa ja ylläpitää nykyisessä työssään yrityksen "
            "sisäistä toiminnanohjausalustaa pääkehittäjänä: käyttöliittymän, rajapinnat, tietokannan, "
            "palvelinympäristön, tietoturvan, teollisuuslaiteintegraation ja tekoälyominaisuudet. "
            "Pidän kokonaisuuksien rakentamisesta ja siitä, että tekniikka ratkaisee oikeita ongelmia.",
            "Olen tehnyt töitä laaja-alaisesti yksin, ja seuraavaksi haluaisin tiimiin, jossa pääsen "
            "jakamaan osaamistani, oppimaan muilta ja syventymään yhteen alueeseen.",
        ],
        "seeking": ("Haen", "ensisijaisesti etätyötä; satunnaiset toimistopäivät tai tarvittaessa lähityö onnistuvat."),
        "job": {
            "title": "Ohjelmistokehittäjä", "when": "11/2025–",
            "where": "Suomen Tekojää Oy · jäähallit, lämpöpumput ja kylmätekniikka",
            "intro": "Suunnittelen ja rakennan yrityksen sisäistä toiminnanohjausalustaa ja vastaan sen julkaisuista, "
                     "palvelimista ja tietoturvasta. Alusta on tuotantoympäristössä ensimmäisten käyttäjien "
                     "käytössä ja sitä otetaan käyttöön vaiheittain.",
            "stats": [(".NET 10", "Blazor, ASP.NET Core ja PostgreSQL"),
                      ("~2 000", "automaattista testiä CI-putkessa"),
                      ("Docker & Linux", "Nginx, julkaisut, varmuuskopiot ja valvonta")],
            "subs": [
                ("core", "Toiminnanohjausalusta", ".NET 10 · Blazor · PostgreSQL",
                 "Laitekanta, huolto ja työraportit, projektit, tiedostot, chat ja ilmoitukset. "
                 "Kaksikielinen PWA, rooli- ja kohdekohtaiset käyttöoikeudet."),
                ("integr", "PLC-datankeruu", "Python · Beckhoff ADS",
                 "Lukee teollisuusohjaimia ja lähettää datan allekirjoitettuna ja salattuna. "
                 "Hälytykset avaavat huoltotiketit automaattisesti."),
                ("ai", "Tekoälyavustaja", "Claude API · Ollama · RAG",
                 "Työkaluja kutsuva avustaja ja dokumenttihaku, aina käyttäjän käyttöoikeuksien rajoissa."),
                ("core", "Asiakasportaali", "ASP.NET Core",
                 "Erillinen sovellus asiakkaille, rajatut näkymät ilman pääsyä henkilöstön dataan."),
                ("infra", "Palvelimet ja tietoturva", "Docker · Nginx · Linux",
                 "Konttipohjainen ympäristö, julkaisut palautuksella, varmuuskopiot, valvonta."),
            ],
            "case": ("Projektiesittely", "Kenttätoimintojen alusta",
                     "", SITE + "/showcase/"),
        },
        "job2": ("Tilaustyöprojektit", "2021–2024", "Opintojen aikana",
                 "Pelejä paikallisille yrityksille tilaustyönä koulun kautta."),
        "side": None,
        "edu": ("Tieto- ja viestintätekniikan perustutkinto", "2021–2024", "Ohjelmistokehittäjä · Vuoksi"),
        "trust": [("Parkanon nuorisovaltuuston varapuheenjohtaja", "2019–2020")],
        "groups": [
            ("core", "Päivittäin", False, ["C#", ".NET / ASP.NET Core", "Blazor", "Entity Framework",
                                           "SignalR", "PostgreSQL", "JavaScript", "HTML / CSS", "Git"]),
            ("tools", "Myös tuotannossa", False, ["Python", "Bash", "Node.js", "FastAPI", "TimescaleDB",
                                                  "pgvector", "xUnit", "GitHub Actions"]),
            ("infra", "Palvelimet ja tietoturva", False, ["Docker Compose", "Linux", "Nginx", "YARP",
                                                          "TLS / oma CA", "pgAudit"]),
            ("ai", "Tekoäly", False, ["Claude API", "Tool calling", "Ollama", "RAG",
                                     "Tekoälyavusteinen kehitys"]),
            ("integr", "Integraatiot", False, ["Beckhoff TwinCAT / ADS", "Entra ID & Graph", "Teams-botti",
                                              "Pipedrive API", "Google Maps API", "Web Push",
                                              "WebAuthn / passkeys"]),
            ("other", "Työkalut", False, ["Visual Studio", "VS Code", "Claude Code", "pgAdmin", "Photoshop",
                                         "DaVinci Resolve"]),
        ],
        "rows": [("Kielet", [("Suomi", "äidinkieli"), ("Englanti", "erinomainen")]),
                 ("Muuta", [("Kyberturvallisuus", "opiskelu (TryHackMe)"), ("B-ajokortti", "oma auto")])],
        "footer": ("Verkossa", SITE, "Päivitetty 11/2026"),
        "legend": "täytetty = päivittäin · ääriviiva = kokemusta",
    },
    "en": {
        "file": "Kasper_Kuirinlahti_CV_EN.pdf",
        "title": "Software Developer",
        "tagline": "Full-stack .NET · databases · server infrastructure · AI integrations",
        "phone": "Phone",
        "contact": [("Email", "kasper@kuirinlahti.dev", "mailto:kasper@kuirinlahti.dev"),
                    ("GitHub", "github.com/0NullNull", "https://github.com/0NullNull"),
                    ("Location", "Parkano, Finland", None)],
        "h": {"profile": "Profile", "exp": "Experience", "side": "Side projects", "edu": "Education",
              "trust": "Positions of trust"},
        "profile": [
            "Software developer currently designing, building and maintaining a company's internal "
            "operations platform as its main developer: the user interface, APIs, database, server "
            "infrastructure, security, industrial device integration and AI features. I enjoy building "
            "whole systems where technology solves real problems.",
            "I have worked broadly on my own, and next I would like to join a team where I can share "
            "what I have learned, learn from others and go deeper in one area.",
        ],
        "seeking": ("Looking for", "primarily remote roles; occasional office visits or on-site possible if needed."),
        "job": {
            "title": "Software Developer", "when": "11/2025–",
            "where": "Suomen Tekojää Oy · ice rinks, heat pumps and refrigeration",
            "intro": "I design and build the company's internal operations platform and handle its releases, servers "
                     "and security. The platform is live in production with its first users and being rolled out "
                     "gradually.",
            "stats": [(".NET 10", "Blazor, ASP.NET Core and PostgreSQL"),
                      ("~2,000", "automated tests in CI"),
                      ("Docker & Linux", "Nginx, releases, backups and monitoring")],
            "subs": [
                ("core", "Operations platform", ".NET 10 · Blazor · PostgreSQL",
                 "Equipment registry, service and work reports, projects, files, chat and notifications. "
                 "Bilingual PWA with role- and site-level permissions."),
                ("integr", "PLC data collection", "Python · Beckhoff ADS",
                 "Reads industrial controllers and sends the data signed and encrypted. "
                 "Alarms open service tickets automatically."),
                ("ai", "AI assistant", "Claude API · Ollama · RAG",
                 "Tool-calling assistant and document search, always within the user's access rights."),
                ("core", "Customer portal", "ASP.NET Core",
                 "Separate app for customers, with restricted views and no access to staff data."),
                ("infra", "Servers and security", "Docker · Nginx · Linux",
                 "Container environment, scripted releases with rollback, backups, monitoring."),
            ],
            "case": ("Case study", "Field Operations Platform",
                     "", SITE + "/showcase/en.html"),
        },
        "job2": ("Commissioned projects", "2021–2024", "During studies",
                 "Games for local companies, commissioned through school."),
        "side": None,
        "edu": ("Vocational Qualification in ICT", "2021–2024", "Software Developer · Vuoksi"),
        "trust": [("Vice-chair, Parkano Youth Council", "2019–2020")],
        "groups": [
            ("core", "Daily use", False, ["C#", ".NET / ASP.NET Core", "Blazor", "Entity Framework",
                                          "SignalR", "PostgreSQL", "JavaScript", "HTML / CSS", "Git"]),
            ("tools", "Also in production", False, ["Python", "Bash", "Node.js", "FastAPI", "TimescaleDB",
                                                    "pgvector", "xUnit", "GitHub Actions"]),
            ("infra", "Infrastructure & security", False, ["Docker Compose", "Linux", "Nginx", "YARP",
                                                           "TLS / private CA", "pgAudit"]),
            ("ai", "AI", False, ["Claude API", "Tool calling", "Ollama", "RAG", "AI-assisted development"]),
            ("integr", "Integrations", False, ["Beckhoff TwinCAT / ADS", "Entra ID & Graph", "Teams bot",
                                              "Pipedrive API", "Google Maps API", "Web Push",
                                              "WebAuthn / passkeys"]),
            ("other", "Tools", False, ["Visual Studio", "VS Code", "Claude Code", "pgAdmin", "Photoshop",
                                      "DaVinci Resolve"]),
        ],
        "rows": [("Languages", [("Finnish", "native"), ("English", "excellent")]),
                 ("Other", [("Cybersecurity", "self-study (TryHackMe)"), ("Driving licence (B)", "own car")])],
        "footer": ("Online", SITE + "/en.html", "Updated 11/2026"),
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
    p.roundRect(x, y_top - d, d, d, 10)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(ImageReader(buf), x, y_top - d, d, d)
    c.restoreState()
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y_top - d, d, d, 10, stroke=1, fill=0)


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
    spaced(c, d["title"].upper(), hx, top - 41, "Mono-Md", 8.6, AMBER, 1.4)
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
        y -= para(c, t, style(9.4, leading=13.1), x, y, w) + 3
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
    y -= para(c, j["intro"], style(9.1, leading=12.7), x, y, w) + 5

    # figures
    stats = j.get("stats", [])
    if stats:
        cw = (w - 6) / 3
        heights = []
        for i, (num, label) in enumerate(stats):
            heights.append(Paragraph(label, style(7.2, color=MUTED, leading=9)).wrap(cw - 14, 100)[1])
        bh = 22 + max(heights) + 3
        for i, (num, label) in enumerate(stats):
            bx = x + i * (cw + 3)
            c.setStrokeColor(LINE)
            c.setFillColor(PAPER)
            c.setLineWidth(0.6)
            c.roundRect(bx, y - bh, cw, bh, 3, stroke=1, fill=1)
            c.setFillColor(BRINE)
            c.setFont("Cond-Bd", 14)
            c.drawString(bx + 7, y - 17, num)
            para(c, label, style(7.2, color=MUTED, leading=9), bx + 7, y - 21, cw - 14)
        y -= bh + 6

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
        y -= 5

    # case study box (off until the employer approves the showcase in writing)
    if SHOW_CASE:
      tag, title, stats, url = j["case"]
      y -= 2
      bh = 42
      c.setFillColor(CAT["core"][1])
      c.roundRect(x, y - bh, w, bh, 3, stroke=0, fill=1)
      c.setFillColor(BRINE)
      c.rect(x, y - bh, 2.6, bh, stroke=0, fill=1)
      spaced(c, tag.upper(), x + 11, y - 11, "Mono-Md", 6.4, BRINE, 1)
      c.setFillColor(INK)
      c.setFont("Cond-Bd", 12.5)
      c.drawString(x + 11, y - 23, title)
      c.setFillColor(MUTED)
      c.setFont("Sans", 7.6)
      c.drawString(x + 11, y - 33.5, stats)
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
    y -= para(c, where2 + " · " + desc2, style(8.8, color=MUTED), x, y, w) + 10

    # side project (optional)
    if d.get("side"):
        y -= main_heading(c, d["h"]["side"], x, y, w)
        st, sw, swhere, sdesc, surl = d["side"]
        c.setFillColor(BRINE)
        c.setFont("Sans-Sb", 10)
        c.drawString(x, y - 9.5, st)
        c.linkURL(surl, (x, y - 12, x + pdfmetrics.stringWidth(st, "Sans-Sb", 10), y), relative=0)
        pill(c, sw, x + w, y)
        y -= 14
        y -= para(c, swhere + " · " + sdesc, style(8.5, color=MUTED, leading=11.2), x, y, w) + 10

    # education
    y -= main_heading(c, d["h"]["edu"], x, y, w)
    et, ew, ed = d["edu"]
    c.setFillColor(BRINE)
    c.setFont("Sans-Sb", 10)
    c.drawString(x, y - 9.5, et)
    pill(c, ew, x + w, y)
    y -= 14
    y -= para(c, ed, style(8.8, color=MUTED), x, y, w) + 10

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
