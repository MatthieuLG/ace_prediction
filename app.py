# Import packages
import joblib
import streamlit as st
import warnings
from PIL import Image
import pandas as pd
import re

def calculer_ecart_en_pourcentage(chiffre_a, chiffre_b):
    try:
        ecart_en_pourcentage = ((chiffre_b - chiffre_a) / abs(chiffre_a)) * 100
        return ecart_en_pourcentage
    except ZeroDivisionError:
        # En cas de division par zéro (si chiffre_a est 0), gestion de l'exception.
        return float('inf')
    

st.set_page_config(
    page_title="ACE Prediction",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# setup  page Streamlit
# define styles
main_bg = "#1B4094"
banner_color = "#FFFFFF"
# style of page
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: {main_bg};
        padding-top: 0;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# style of banner
st.markdown(
    f"""
    <style>
    .css-1tq3xr3 {{
        display: flex;
        align-items: center;
        background-color: {banner_color};
        padding: 0.5rem;modele
        margin-bottom: 0.3rem;
        border-radius: 25px;
        text-align: center;
        margin-top: -5rem;  /* Réduire la marge supérieure */
    }}
    .css-1tq3xr3 img {{
        margin-right: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="css-1tq3xr3" style="display: flex; justify-content: space-between; align-items: center;">
        <img src="https://seeklogo.com/images/A/association-of-tennis-professionals-atp-logo-AD67CAB60A-seeklogo.com.png" alt="ATP" width="100" style="margin-right: auto;">
        <h1 style="color: #0d85e6; text-align: center;">Aces Predictions</h1>
        <img src="https://seeklogo.com/images/A/association-of-tennis-professionals-atp-logo-AD67CAB60A-seeklogo.com.png" alt="ATP" width="100" style="margin-left: auto;">
    </div>

    """, 
    unsafe_allow_html=True
)

# Import de fichiers
select_player = pd.read_csv("SelectionOFPlayer.csv")
playerj1 = pd.read_csv("Player1.csv")
playerj2 = pd.read_csv("Player2.csv")
select_player_f1 = select_player['Player1_name_unique'].unique()
select_player_f2 = select_player['Player1_name_unique'].unique()

# Tabs
col1, col2, col3, col4 = st.columns(4)

# creation of filter competition
with col1:
    filtre_j1 = st.selectbox("Player 1 ", select_player_f1)
    f_j1 = select_player[select_player['Player1_name_unique'] == filtre_j1]['Player1_name_unique'].unique()

with col2:
    filtre_j2 = st.selectbox("Player 2 ", select_player_f2)
    f_j2 = select_player[select_player['Player1_name_unique'] == filtre_j2]['Player1_name_unique'].unique()

l1 = playerj1[playerj1['Player1_name'] == filtre_j1]
l2 = playerj2[playerj2['Player2_name'] == filtre_j2]

l3 = playerj1[playerj1['Player1_name'] == filtre_j2]
l4 = playerj2[playerj2['Player2_name'] == filtre_j1]

data = {
    'Player1_ht': [],
    'Player1_df': [],
    'Player1_prcent1st': [],
    'Player1_prcent1stwin': [],
    'Player1_prcent2ndwin': [],
    'Player1_prcentgameserve': [],
    'Player2_ht': [],
    'Player2_prcentgamesreturn': [],
    'Player2_prcent1stwinreturn': [],
    'Player2_prcent2ndwinreturn': [],
    'Player2_breakwin': []
}
df_pred1 = pd.DataFrame(data)
df_pred2 = pd.DataFrame(data)

df_pred1.iloc[:, 0] = l1.iloc[:, 2]
df_pred1.iloc[0, 1] = l1.iloc[0, 3]
df_pred1.iloc[0, 2] = l1.iloc[0, 5]
df_pred1.iloc[0, 3] = l1.iloc[0, 6]
df_pred1.iloc[0, 4] = l1.iloc[0, 7]
df_pred1.iloc[0, 5] = l1.iloc[0, 8]
# df_pred1.iloc[0, 6] = l1.iloc[0, 9]
df_pred1.iloc[0, 6] = l2.iloc[0, 2]
df_pred1.iloc[0, 7] = l2.iloc[0, 3]
df_pred1.iloc[0, 8] = l2.iloc[0, 4]
df_pred1.iloc[0, 9] = l2.iloc[0, 5]
df_pred1.iloc[0, 10] = l2.iloc[0, 6]
# df_pred1.iloc[0, 11] = l2.iloc[0, 7]

df_pred2.iloc[:, 0] = l3.iloc[:, 2]
df_pred2.iloc[0, 1] = l3.iloc[0, 3]
df_pred2.iloc[0, 2] = l3.iloc[0, 5]
df_pred2.iloc[0, 3] = l3.iloc[0, 6]
df_pred2.iloc[0, 4] = l3.iloc[0, 7]
df_pred2.iloc[0, 5] = l3.iloc[0, 8]
# df_pred2.iloc[0, 6] = l3.iloc[0, 9]
df_pred2.iloc[0, 6] = l4.iloc[0, 2]
df_pred2.iloc[0, 7] = l4.iloc[0, 3]
df_pred2.iloc[0, 8] = l4.iloc[0, 4]
df_pred2.iloc[0, 9] = l4.iloc[0, 5]
df_pred2.iloc[0, 10] = l4.iloc[0, 6]
# df_pred2.iloc[0, 11] = l4.iloc[0, 7]



model = joblib.load('modele_foret_aleatoire.pkl')

# Tabs
col1, col2, col3, col4, col5 = st.columns(5)
st.write("<br>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

# creation of filter competition
with col1:
    ligne_1 = df_pred1.iloc[0]
    prediction1 = model.predict([ligne_1])
    st.write(f"Joueur : {filtre_j1} : {round(prediction1[0],2)} aces")

with col2:
    ligne_2 = df_pred2.iloc[0]
    prediction2 = model.predict([ligne_2])
    st.write(f"Joueur : {filtre_j2} : {round(prediction2[0],2)} aces")

with col3:
    total_aces = prediction1[0] + prediction2[0]
    st.write(f"Total match : {round(total_aces,2)} aces")
df_cote = pd.read_csv("listedescotes.csv")
df_match = pd.read_csv("listedesmatchs.csv")
sel_match = df_match['match'].unique()
def extraire_dernier_mot(chaine):
    # Utilisation d'une expression régulière pour extraire le dernier mot
    dernier_mot = re.findall(r'\b[A-Z][a-z]*\b', chaine)[-1]
    return dernier_mot

def extraire_noms(chaine):
    # Utilisation d'une expression régulière pour extraire les noms
    matches = re.findall(r'\b[A-Z][a-z]*\b', chaine)

    # Assignation des noms aux variables J1 et J2
    if len(matches) >= 2:
        J1 = matches[0]
        J2 = matches[1]
        return J1, J2
    else:
        return None, None
# Tabs
col1, col2, col3, col4 = st.columns(4)

# creation of filter competition
with col1:
    match_f = st.selectbox("Match a venir via BETCLIC", sel_match)
    match_s = df_match[df_match['match'] == match_f]['match'].unique()

    J3 = extraire_dernier_mot(match_f)
    J1, J2 = extraire_noms(match_f)
    Joueur1 = J2
    Joueur2 = J3
    valeurs_joueurs = ["Match"+Joueur1+Joueur2, Joueur1, Joueur2]
    # Remplacer "Davidovich" par "Fokina" dans les colonnes Joueur1 et Joueur2

    df_filtre_cote = df_cote[df_cote['Qui'].isin(valeurs_joueurs)]
    df_filtre_cote['Items'] = df_filtre_cote['Items'].astype(str)
    df_filtre_cote = df_filtre_cote.reset_index(drop=True)



col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.write("Côte Betclic pour", Joueur1)
    ligne_2 = df_filtre_cote.loc[2, ['Items', 'Cotes']]
    ligne_3 = df_filtre_cote.loc[3, ['Items', 'Cotes']]

    # Afficher les valeurs
    st.write(f"{ligne_2['Items']}, Cotes: {ligne_2['Cotes']}")
    st.write(f"{ligne_3['Items']}, Cotes: {ligne_3['Cotes']}")
    chiffres1 = ''.join(c for c in ligne_2['Items'] if c.isdigit() or c == '.')
    bet1 = float(chiffres1)
    ecart1 = calculer_ecart_en_pourcentage(bet1, prediction1)
    ecart1 = float(ecart1)
    ecart1 = round(ecart1,2)
    st.write("ECART % de" , ecart1)
with col2:
    st.write("Côte Betclic pour", Joueur2)
    ligne_4 = df_filtre_cote.loc[4, ['Items', 'Cotes']]
    ligne_5 = df_filtre_cote.loc[5, ['Items', 'Cotes']]

    # Afficher les valeurs
    st.write(f"{ligne_4['Items']}, Cotes: {ligne_4['Cotes']}")
    st.write(f"{ligne_5['Items']}, Cotes: {ligne_5['Cotes']}")

    chiffres2 = ''.join(c for c in ligne_4['Items'] if c.isdigit() or c == '.')
    bet2 = float(chiffres2)
    ecart2 = calculer_ecart_en_pourcentage(bet2, prediction2)
    ecart2 = float(ecart2)
    ecart2 = round(ecart2,2)
    st.write("ECART % de" , ecart2)
with col3:
    st.write("Côte Betclic dans le match")
    ligne_0 = df_filtre_cote.loc[0, ['Items', 'Cotes']]
    ligne_1 = df_filtre_cote.loc[1, ['Items', 'Cotes']]

    # Afficher les valeurs
    st.write(f"{ligne_0['Items']}, Cotes: {ligne_0['Cotes']}")
    st.write(f"{ligne_1['Items']}, Cotes: {ligne_1['Cotes']}")
    chiffres3 = ''.join(c for c in ligne_0['Items'] if c.isdigit() or c == '.')
    bet3 = float(chiffres3)
    ecart3 = calculer_ecart_en_pourcentage(bet3, (prediction2+prediction1))
    ecart3 = float(ecart3)
    ecart3 = round(ecart3,2)
    st.write("ECART % de" , ecart3)