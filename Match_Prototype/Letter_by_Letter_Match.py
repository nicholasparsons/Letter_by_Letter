{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Letter by Letter Match.ipynb",
      "provenance": [],
      "authorship_tag": "ABX9TyMRUzbxq8X7YPH1jdhAAOK/",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/nicholasparsons/Letter_by_Letter/blob/main/Match_Prototype/Letter_by_Letter_Match.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!git clone https://github.com/nicholasparsons/Letter_by_Letter/\n",
        "\n",
        "import os\n",
        "os.chdir(\"Letter_by_Letter\")"
      ],
      "metadata": {
        "id": "u-ofn_IP8hdb"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install -r /content/Letter_by_Letter/Match_Prototype/requirements.txt"
      ],
      "metadata": {
        "id": "8etlMMBur7-8"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Imports\n",
        "import pandas as pd"
      ],
      "metadata": {
        "id": "wQ8aE4B7-Phs"
      },
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "O9aZaQTcP489"
      },
      "outputs": [],
      "source": [
        "#Pull data from Google Sheets\n",
        "from google.colab import auth\n",
        "auth.authenticate_user()\n",
        "\n",
        "import gspread\n",
        "from google.auth import default\n",
        "creds, _ = default()\n",
        "\n",
        "gc = gspread.authorize(creds)\n",
        "\n",
        "worksheet = gc.open('Letter by Letter Match Sheet').sheet1\n",
        "\n",
        "# get_all_records gives a list of rows with top row frozen.\n",
        "rows = worksheet.get_all_records()\n",
        "\n",
        "# Convert to a DataFrame and render as \"df\"\n",
        "df = pd.DataFrame.from_records(rows)"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Remove blank entries.\n",
        "df = df.drop(df[df['Native_Language']=='null'].index)"
      ],
      "metadata": {
        "id": "I5H6Wo0n-JUp"
      },
      "execution_count": 46,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Use df.index[-1] to find the final index of a dataframe.\n",
        "df[\"Match_Score\"] = 0.0"
      ],
      "metadata": {
        "id": "ePwO3X8k6h71"
      },
      "execution_count": 47,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "i = 0\n",
        "for index, row in df.iterrows():\n",
        "  if row[\"Target_Language\"] != df.at[df.index[-1],\"Native_Language\"] or row[\"Native_Language\"] != df.at[df.index[-1],\"Target_Language\"]:\n",
        "    i=i+1\n",
        "    continue\n",
        "  elif row[\"Available_Matches\"] == 0:\n",
        "    i = i+1\n",
        "    continue\n",
        "  else:\n",
        "    df.at[i,\"Match_Score\"] = df.at[i,\"Match_Score\"] + 1\n",
        "    language_level_score = ((abs(df.at[df.index[-1],\"Language_Level\"] - df.at[i,\"Language_Level\"])**2)*(-1/16))+1\n",
        "    df.at[i,\"Match_Score\"] = df.at[i,\"Match_Score\"] + language_level_score\n",
        "    if df.at[df.index[-1],\"Age\"] != 0 and df.at[i,\"Age\"] != 0:\n",
        "      age_score = ((abs(df.at[df.index[-1],\"Age\"] - df.at[i,\"Age\"])**2)*(-1/64))+1\n",
        "      df.at[i,\"Match_Score\"] = df.at[i,\"Match_Score\"] + age_score\n",
        "    if df.at[df.index[-1],\"Gender\"] != \"\" and df.at[df.index[-1],\"Gender\"] == df.at[i,\"Gender\"]:\n",
        "      df.at[i,\"Match_Score\"] = df.at[i,\"Match_Score\"] + 1\n",
        "    if df.at[df.index[-1],\"Study_Method\"] != \"\" and df.at[df.index[-1],\"Study_Method\"] == df.at[i,\"Study_Method\"]:\n",
        "      df.at[i,\"Match_Score\"] = df.at[i,\"Match_Score\"] + 1\n",
        "    if df.at[df.index[-1],\"Interests\"] != \"\":\n",
        "      Respondent_Interests = df.at[df.index[-1],\"Interests\"].split(\", \")\n",
        "      Target_Interests = df.at[i,\"Interests\"].split(\", \")\n",
        "      interest_score = 0\n",
        "      for j in Respondent_Interests:\n",
        "        for k in Target_Interests:\n",
        "          if j == k:\n",
        "            interest_score = interest_score + 1\n",
        "      interest_score = ((1/len(Respondent_Interests))**2)*(interest_score**2)\n",
        "      df.at[i,\"Match_Score\"] = df.at[i,\"Match_Score\"] + interest_score\n",
        "    i=i+1"
      ],
      "metadata": {
        "id": "KGVA5dg3DQtX"
      },
      "execution_count": 48,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "df[\"Match\"] = \"No\"\n",
        "for c in range(df.at[df.index[-1],\"Available_Matches\"]):\n",
        "  max = 0\n",
        "  max_index = 0\n",
        "  for index in df[\"Match_Score\"].index:\n",
        "    if df[\"Match_Score\"][index] > max and df[\"Match\"][index] != \"Yes\":\n",
        "      max = df[\"Match_Score\"][index]\n",
        "      max_index = index\n",
        "  df.loc[max_index,\"Match\"] = \"Yes\"\n",
        "  df.loc[max_index,\"Available_Matches\"] = df.loc[max_index,\"Available_Matches\"]-1"
      ],
      "metadata": {
        "id": "B9Kh8XMebq6y"
      },
      "execution_count": 49,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "df_match = df[df.Match == \"Yes\"].copy().reset_index()\n",
        "num_matches = df_match.shape[0]\n",
        "print(f\"You received {num_matches} matches.\")\n",
        "df_match.at[0,\"First_Name\"]\n",
        "for x in range(num_matches):\n",
        "  print(f\"Match number {x+1}: \" + df_match.at[x,\"First_Name\"]+\" \" + df_match.at[x,\"Last_Name\"] + f\"\\nMatch {x+1} Address: \" + df_match.at[x,\"Mailing_Address\"])"
      ],
      "metadata": {
        "id": "C_OE3ALcZtUL"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}