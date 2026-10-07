import streamlit as st
from datetime import date
import plotly.graph_objects as go

# -----------------------------
# INSTÄLLNINGAR
# -----------------------------

st.set_page_config(
    page_title="GMG - Election Bet",
    page_icon="🏆",
    layout="centered"
)


# -----------------------------
# DATA
# -----------------------------

deltagare = [
    {"namn": "Damiano", "dagar": 120, "gissat_datum": "2027-01-12"},
    {"namn": "Simon", "dagar": 100, "gissat_datum": "2026-12-23"},
    {"namn": "César", "dagar": 75, "gissat_datum": "2026-11-28"},
    {"namn": "Patrick", "dagar": 59, "gissat_datum": "2026-11-12"},
    {"namn": "Robin", "dagar": 55, "gissat_datum": "2026-11-08"},
    {"namn": "Oscar ML", "dagar": 52, "gissat_datum": "2026-11-05"},
    {"namn": "Aston", "dagar": 51, "gissat_datum": "2026-11-04"},
    {"namn": "William", "dagar": 47, "gissat_datum": "2026-10-31"},
    {"namn": "Gustaf", "dagar": 45, "gissat_datum": "2026-10-29"},
    {"namn": "Ella", "dagar": 43, "gissat_datum": "2026-10-27"},
    {"namn": "Diego", "dagar": 42, "gissat_datum": "2026-10-26"},
    {"namn": "Oscar L", "dagar": 32, "gissat_datum": "2026-10-16"},
    {"namn": "Oscar M", "dagar": 30, "gissat_datum": "2026-10-14"},
    {"namn": "Jesper", "dagar": 19, "gissat_datum": "2026-10-03"},
    {"namn": "Tobias", "dagar": 10, "gissat_datum": "2026-09-24"},
]


# -----------------------------
# BERÄKNA TABELL
# -----------------------------

def beräkna_tabell(deltagare):

    idag = date.today()

    resultat = []

    for person in deltagare:

        gissat_datum = date.fromisoformat(person["gissat_datum"])

        avvikelse = (gissat_datum - idag).days

        poäng = abs(avvikelse)

        resultat.append({
            "Person": person["namn"],
            "Days Guessed": person["dagar"],
            "Date Guessed": gissat_datum,
            "-Points": poäng
        })

    # Lägst poäng först
    resultat.sort(key=lambda x: x["-Points"])

    # Position
    for position, person in enumerate(resultat, start=1):
        person["Position"] = position

    return resultat


# -----------------------------
# RUBRIK
# -----------------------------

st.markdown(
    """
    <h1 style="text-align: center;">🏆 GMG - Election Bet</h1>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# BANNER
# -----------------------------

election_night = date(2026, 9, 14)
today = date.today()

days_passed = (today - election_night).days

st.markdown(
    f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        padding: 12px;
        margin: 20px 0;
        border-radius: 10px;
        background-color: #f0f2f6;
        font-weight: bold;
    ">
        <span>Days passed since election night:</span>
        <span style="font-size: 24px;">{days_passed}</span>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# LEADERBOARD
# -----------------------------

st.markdown(
    """
    <h3 style="
        text-align: left;
        margin-top: 10px;
        margin-bottom: 5px;
        font-weight: 700;
    ">
        Leaderboard
    </h3>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TABELL
# -----------------------------

resultat = beräkna_tabell(deltagare)
# -----------------------------
# TABELL
# -----------------------------

resultat = beräkna_tabell(deltagare)

# Skapa HTML-tabell
html = """
<style>
.leaderboard {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-size: 14px;
}

.leaderboard th {
    font-weight: bold;
    text-align: center;
    padding: 5px 2px;
}

.leaderboard td {
    text-align: center;
    padding: 5px 2px;
}

.leaderboard th,
.leaderboard td {
    width: 20%;
}
</style>

<table class="leaderboard">
<thead>
<tr>
<th>Position</th>
<th>Person</th>
<th>Days Guessed</th>
<th>Date Guessed</th>
<th>-Points</th>
</tr>
</thead>
<tbody>
"""

for person in resultat:

    medalj = ""

    if person["Position"] == 1:
        medalj = " 🥇"
    elif person["Position"] == 2:
        medalj = " 🥈"
    elif person["Position"] == 3:
        medalj = " 🥉"

    html += f"""
<tr>
<td>{person["Position"]}</td>
<td>{person["Person"]}{medalj}</td>
<td>{person["Days Guessed"]}</td>
<td>{person["Date Guessed"].strftime("%Y-%m-%d")}</td>
<td>{person["-Points"]}</td>
</tr>
"""

html += """
</tbody>
</table>
"""

st.markdown(html, unsafe_allow_html=True)

# -----------------------------
# TIDSSERIE
# -----------------------------

st.markdown(
    """
    <h3 style="
        text-align: left;
        margin-top: 30px;
        margin-bottom: 5px;
        font-weight: 700;
    ">
        Position over time
    </h3>
    """,
    unsafe_allow_html=True
)


# Valnatten
election_night = date(2026, 9, 14)

# Dagens datum
today = date.today()

# Hur många dagar som har gått
days_passed = (today - election_night).days


# Skapa tidsserie från dag 0 till idag
tidsserie = []

for dag in range(0, days_passed + 1):

    dagens_resultat = []

    for person in deltagare:

        # Personens gissning är uttryckt i dagar efter valnatten
        gissning = person["dagar"]

        # Poäng på den aktuella dagen
        poäng = abs(gissning - dag)

        dagens_resultat.append({
            "namn": person["namn"],
            "poäng": poäng
        })

    # Sortera efter lägst poäng
    dagens_resultat.sort(key=lambda x: x["poäng"])

    # Spara positionen
    for position, person in enumerate(dagens_resultat, start=1):

        tidsserie.append({
            "dag": dag,
            "namn": person["namn"],
            "position": position
        })

# Skapa graf
fig = go.Figure()

# En linje per person
for person in deltagare:

    namn = person["namn"]

    person_data = [
        rad for rad in tidsserie
        if rad["namn"] == namn
    ]

    fig.add_trace(
        go.Scatter(
            x=[rad["dag"] for rad in person_data],
            y=[rad["position"] for rad in person_data],
            mode="lines",
            name=namn,
            hovertemplate=(
                "%{customdata}<br>"
                "Position: %{y}"
                "<extra></extra>"
            ),
            customdata=[namn] * len(person_data)
        )
    )


# ---------------------------------
# HOVER-ORDNING
# ---------------------------------

# För varje dag: skapa namnlistan i aktuell positionsordning
hover_order = {}

for dag in range(0, days_passed + 1):

    dagens = [
        rad for rad in tidsserie
        if rad["dag"] == dag
    ]

    dagens.sort(key=lambda x: x["position"])

    hover_order[dag] = "<br>".join(
        f'{rad["position"]}. {rad["namn"]}'
        for rad in dagens
    )


# Uppdatera hover för varje linje
for trace in fig.data:

    namn = trace.name

    customdata = []

    for dag in range(0, days_passed + 1):

        aktuell_rad = next(
            rad for rad in tidsserie
            if rad["dag"] == dag
            and rad["namn"] == namn
        )

        customdata.append(
            f'{aktuell_rad["position"]}. {namn}'
            f'<br><br>{hover_order[dag]}'
        )

    trace.customdata = customdata

    trace.hovertemplate = (
        "<b>Day %{x}</b><br><br>"
        "%{customdata}"
        "<extra></extra>"
    )


fig.update_layout(
    xaxis_title="Days since election night",
    yaxis_title="Position",

    xaxis=dict(
        range=[0, max(days_passed, 1)],
        dtick=5
    ),

    yaxis=dict(
        autorange="reversed",
        dtick=1,
        range=[15.5, 0.5]
    ),

    height=650,

    margin=dict(
        l=40,
        r=20,
        t=20,
        b=40
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ),

    hovermode="closest"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)