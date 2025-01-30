import pandas as pd
import json
import random, string


# Constants
null = None
false = False
true = True

template = {
    "SurveyID": "SV_5vTYBmxykYQ6Ghw",
    "Element": "SQ",
    "PrimaryAttribute": "",
    "SecondaryAttribute": "",
    "TertiaryAttribute": null,
    "Payload": {
        "QuestionText": "",
        "DefaultChoices": false,
        "DataExportTag": "",
        "QuestionType": "Matrix",
        "Selector": "Likert",
        "SubSelector": "SingleAnswer",
        "DataVisibility": {"Private": false, "Hidden": false},
        "Configuration": {
            "QuestionDescriptionOption": "UseText",
            "TextPosition": "inline",
            "ChoiceColumnWidth": 25,
            "MobileFirst": true,
            "RepeatHeaders": "none",
            "WhiteSpace": "OFF"
        },
        "QuestionDescription": "",
        "Choices": {
            "1": {"Display": "Useful"},
            "2": {"Display": "Transparent"},
            "3": {"Display": "Trustworthy"}
        },
        "ChoiceOrder": ["1", "2", "3"],
        "Validation": {
            "Settings": {
                "ForceResponse": "ON",
                "ForceResponseType": "ON",
                "Type": "None"
            }
        },
        "GradingData": [],
        "Language": [],
        "NextChoiceId": 4,
        "NextAnswerId": 3,
        "Answers": {
            "1": {"Display": "Explanation A"},
            "2": {"Display": "Explanation B"}
        },
        "AnswerOrder": [1, 2],
        "ChoiceDataExportTags": false,
        "QuestionID": ""
    }
}

# Read input Excel file
df = pd.read_excel("explanations.xlsx")

# HTML strings for question formatting
start_string = "<table width=\"100%\" style=\"border: none;\" cellspacing=\"1\" cellpadding=\"1\" border=\"0\">\n\t<caption>The explanation pair to evaluate</caption>\n\t<thead>\n\t\t<tr>\n\t\t\t<th style=\"text-align: center; padding: 1em;\" scope=\"col\">Explanation A</th>\n\t\t\t<th style=\"text-align: center; padding: 1em;\" scope=\"col\">&nbsp;</th>\n\t\t\t<th style=\"text-align: center; padding: 1em;\" scope=\"col\">Explanation B</th>\n\t\t</tr>\n\t</thead>\n\t<tbody>\n\t\t<tr>\n\t\t\t<td style=\"background-color: rgba(39, 129, 245, 0.05); border-radius: 10px; text-align: left; vertical-align: top; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-right: 10px; min-width: 50%;\" class=\"explanation\">\n"
middle_string = "</td>\n\t\t\t<td style=\"background-color: rgba(0, 0, 0, 0.00);\" class=\"explanation\">&nbsp;</td>\n\t\t\t<td style=\"background-color: rgba(39, 129, 245, 0.05); border-radius: 10px; text-align: left; vertical-align: top; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-left: 10px; min-width: 50%;\" class=\"explanation\">"
end_string = "</td>\n\t\t</tr>\n\t</tbody>\n</table>\n\n<h3>&nbsp;</h3>\n\n<h3>Indicate which of the two explanations shown above feels more:<br></h3>"

result = []

blocks = []

for i, row in enumerate(df.itertuples()):
    # Copy the template to fill in data
    to_fill = json.loads(json.dumps(template))  # Deep copy

    qid = f"QID{34 + i}"

    to_fill["PrimaryAttribute"] = qid
    to_fill["Payload"]["QuestionID"] = qid

    qstring = (
        start_string
        + row[5].replace("```html", "").replace("```", "").replace("h1", "h3").replace("h2", "h3").replace("h4", "h3").replace("h5", "h3")
        + middle_string
        + row[6].replace("```html", "").replace("```", "").replace("h1", "h3").replace("h2", "h3").replace("h4", "h3").replace("h5", "h3")
        + end_string
    )

    # Escape quotes in the generated HTML
    # qstring = qstring.replace('</', '</')

    to_fill["Payload"]["QuestionText"] = qstring

    code = f"{int(row[1]):06}v{int(row[2]):06}"

    to_fill["Payload"]["DataExportTag"] = code
    to_fill["Payload"]["QuestionDescription"] = code
    to_fill["SecondaryAttribute"] = code

    blocks.append({"Type": "Standard", "Description": f"Block {2 + i}", "ID": f"BL_{''.join(random.choices(string.ascii_letters + string.digits, k=15))}", "BlockElements": [{"Type": "Question", "QuestionID": qid}]})

    # Append formatted JSON string to result
    result.append(json.dumps(to_fill, ensure_ascii=False))

# Write the result to a text file
with open("./result.txt", "w", encoding="utf-8") as f:
    f.write(",\n".join(result) + ",")

print(str(blocks))


# [{"Type":"Default","Description":"Default Question Block","ID":"BL_7W22qSLzXCCwupg","BlockElements":[{"Type":"Question","QuestionID":"QID1"},{"Type":"Question","QuestionID":"QID3"},{"Type":"Question","QuestionID":"QID4"},{"Type":"Question","QuestionID":"QID5"},{"Type":"Question","QuestionID":"QID7"},{"Type":"Question","QuestionID":"QID14"},{"Type":"Question","QuestionID":"QID15"},{"Type":"Question","QuestionID":"QID16"},{"Type":"Question","QuestionID":"QID17"},{"Type":"Question","QuestionID":"QID18"},{"Type":"Question","QuestionID":"QID19"},{"Type":"Question","QuestionID":"QID20"},{"Type":"Question","QuestionID":"QID21"},{"Type":"Question","QuestionID":"QID22"},{"Type":"Question","QuestionID":"QID23"},{"Type":"Question","QuestionID":"QID24"},{"Type":"Question","QuestionID":"QID25"},{"Type":"Question","QuestionID":"QID26"},{"Type":"Question","QuestionID":"QID27"},{"Type":"Question","QuestionID":"QID28"},{"Type":"Question","QuestionID":"QID29"},{"Type":"Question","QuestionID":"QID30"},{"Type":"Question","QuestionID":"QID31"},{"Type":"Question","QuestionID":"QID32"},{"Type":"Question","QuestionID":"QID33"},{"Type":"Question","QuestionID":"QID12"}]},{"Type":"Trash","Description":"Trash \/ Unused Questions","ID":"BL_bkl548Z1AIkQ2fI","BlockElements":[{"Type":"Question","QuestionID":"QID2"},{"Type":"Question","QuestionID":"QID6"}]},{"Type":"Standard","SubType":"","Description":"Block 1","ID":"BL_b2ENPTJvZIyzwUu","BlockElements":[{"Type":"Question","QuestionID":"QID8"},{"Type":"Question","QuestionID":"QID11"},{"Type":"Question","QuestionID":"QID9"},{"Type":"Question","QuestionID":"QID10"},{"Type":"Question","QuestionID":"QID13"}]},{"Type":"Standard","SubType":"","Description":"Block 2","ID":"BL_ebwmAjc1WMUtKK2","Options":{"BlockLocking":"false","RandomizeQuestions":"RandomWithOnlyX","Randomization":{"Advanced":{"TotalRandSubset":"10","QuestionsPerPage":0,"FixedOrder":["QID34"]},"EvenPresentation":true}},"BlockElements":[{"Type": "Question", "QuestionID": "QID34"}, {"Type": "Question", "QuestionID": "QID35"}, {"Type": "Question", "QuestionID": "QID36"}, {"Type": "Question", "QuestionID": "QID37"}, {"Type": "Question", "QuestionID": "QID38"}, {"Type": "Question", "QuestionID": "QID39"}, {"Type": "Question", "QuestionID": "QID40"}, {"Type": "Question", "QuestionID": "QID41"}, {"Type": "Question", "QuestionID": "QID42"}, {"Type": "Question", "QuestionID": "QID43"}, {"Type": "Question", "QuestionID": "QID44"}, {"Type": "Question", "QuestionID": "QID45"}, {"Type": "Question", "QuestionID": "QID46"}, {"Type": "Question", "QuestionID": "QID47"}, {"Type": "Question", "QuestionID": "QID48"}, {"Type": "Question", "QuestionID": "QID49"}, {"Type": "Question", "QuestionID": "QID50"}, {"Type": "Question", "QuestionID": "QID51"}, {"Type": "Question", "QuestionID": "QID52"}, {"Type": "Question", "QuestionID": "QID53"}, {"Type": "Question", "QuestionID": "QID54"}, {"Type": "Question", "QuestionID": "QID55"}, {"Type": "Question", "QuestionID": "QID56"}, {"Type": "Question", "QuestionID": "QID57"}, {"Type": "Question", "QuestionID": "QID58"}, {"Type": "Question", "QuestionID": "QID59"}, {"Type": "Question", "QuestionID": "QID60"}, {"Type": "Question", "QuestionID": "QID61"}, {"Type": "Question", "QuestionID": "QID62"}, {"Type": "Question", "QuestionID": "QID63"}, {"Type": "Question", "QuestionID": "QID64"}, {"Type": "Question", "QuestionID": "QID65"}, {"Type": "Question", "QuestionID": "QID66"}, {"Type": "Question", "QuestionID": "QID67"}, {"Type": "Question", "QuestionID": "QID68"}, {"Type": "Question", "QuestionID": "QID69"}, {"Type": "Question", "QuestionID": "QID70"}, {"Type": "Question", "QuestionID": "QID71"}, {"Type": "Question", "QuestionID": "QID72"}, {"Type": "Question", "QuestionID": "QID73"}, {"Type": "Question", "QuestionID": "QID74"}, {"Type": "Question", "QuestionID": "QID75"}, {"Type": "Question", "QuestionID": "QID76"}, {"Type": "Question", "QuestionID": "QID77"}, {"Type": "Question", "QuestionID": "QID78"}, {"Type": "Question", "QuestionID": "QID79"}, {"Type": "Question", "QuestionID": "QID80"}, {"Type": "Question", "QuestionID": "QID81"}, {"Type": "Question", "QuestionID": "QID82"}, {"Type": "Question", "QuestionID": "QID83"}, {"Type": "Question", "QuestionID": "QID84"}, {"Type": "Question", "QuestionID": "QID85"}, {"Type": "Question", "QuestionID": "QID86"}, {"Type": "Question", "QuestionID": "QID87"}, {"Type": "Question", "QuestionID": "QID88"}, {"Type": "Question", "QuestionID": "QID89"}, {"Type": "Question", "QuestionID": "QID90"}, {"Type": "Question", "QuestionID": "QID91"}, {"Type": "Question", "QuestionID": "QID92"}, {"Type": "Question", "QuestionID": "QID93"}, {"Type": "Question", "QuestionID": "QID94"}, {"Type": "Question", "QuestionID": "QID95"}, {"Type": "Question", "QuestionID": "QID96"}, {"Type": "Question", "QuestionID": "QID97"}, {"Type": "Question", "QuestionID": "QID98"}, {"Type": "Question", "QuestionID": "QID99"}, {"Type": "Question", "QuestionID": "QID100"}, {"Type": "Question", "QuestionID": "QID101"}, {"Type": "Question", "QuestionID": "QID102"}, {"Type": "Question", "QuestionID": "QID103"}, {"Type": "Question", "QuestionID": "QID104"}, {"Type": "Question", "QuestionID": "QID105"}, {"Type": "Question", "QuestionID": "QID106"}, {"Type": "Question", "QuestionID": "QID107"}, {"Type": "Question", "QuestionID": "QID108"}, {"Type": "Question", "QuestionID": "QID109"}, {"Type": "Question", "QuestionID": "QID110"}, {"Type": "Question", "QuestionID": "QID111"}, {"Type": "Question", "QuestionID": "QID112"}, {"Type": "Question", "QuestionID": "QID113"}, {"Type": "Question", "QuestionID": "QID114"}, {"Type": "Question", "QuestionID": "QID115"}, {"Type": "Question", "QuestionID": "QID116"}, {"Type": "Question", "QuestionID": "QID117"}, {"Type": "Question", "QuestionID": "QID118"}, {"Type": "Question", "QuestionID": "QID119"}, {"Type": "Question", "QuestionID": "QID120"}, {"Type": "Question", "QuestionID": "QID121"}, {"Type": "Question", "QuestionID": "QID122"}, {"Type": "Question", "QuestionID": "QID123"}, {"Type": "Question", "QuestionID": "QID124"}, {"Type": "Question", "QuestionID": "QID125"}, {"Type": "Question", "QuestionID": "QID126"}, {"Type": "Question", "QuestionID": "QID127"}, {"Type": "Question", "QuestionID": "QID128"}, {"Type": "Question", "QuestionID": "QID129"}, {"Type": "Question", "QuestionID": "QID130"}, {"Type": "Question", "QuestionID": "QID131"}, {"Type": "Question", "QuestionID": "QID132"}, {"Type": "Question", "QuestionID": "QID133"}, {"Type": "Question", "QuestionID": "QID134"}, {"Type": "Question", "QuestionID": "QID135"}, {"Type": "Question", "QuestionID": "QID136"}, {"Type": "Question", "QuestionID": "QID137"}, {"Type": "Question", "QuestionID": "QID138"}, {"Type": "Question", "QuestionID": "QID139"}, {"Type": "Question", "QuestionID": "QID140"}, {"Type": "Question", "QuestionID": "QID141"}, {"Type": "Question", "QuestionID": "QID142"}, {"Type": "Question", "QuestionID": "QID143"}, {"Type": "Question", "QuestionID": "QID144"}, {"Type": "Question", "QuestionID": "QID145"}, {"Type": "Question", "QuestionID": "QID146"}, {"Type": "Question", "QuestionID": "QID147"}, {"Type": "Question", "QuestionID": "QID148"}, {"Type": "Question", "QuestionID": "QID149"}, {"Type": "Question", "QuestionID": "QID150"}, {"Type": "Question", "QuestionID": "QID151"}, {"Type": "Question", "QuestionID": "QID152"}, {"Type": "Question", "QuestionID": "QID153"}, {"Type": "Question", "QuestionID": "QID154"}, {"Type": "Question", "QuestionID": "QID155"}, {"Type": "Question", "QuestionID": "QID156"}, {"Type": "Question", "QuestionID": "QID157"}, {"Type": "Question", "QuestionID": "QID158"}, {"Type": "Question", "QuestionID": "QID159"}, {"Type": "Question", "QuestionID": "QID160"}, {"Type": "Question", "QuestionID": "QID161"}, {"Type": "Question", "QuestionID": "QID162"}, {"Type": "Question", "QuestionID": "QID163"}, {"Type": "Question", "QuestionID": "QID164"}, {"Type": "Question", "QuestionID": "QID165"}, {"Type": "Question", "QuestionID": "QID166"}, {"Type": "Question", "QuestionID": "QID167"}, {"Type": "Question", "QuestionID": "QID168"}, {"Type": "Question", "QuestionID": "QID169"}, {"Type": "Question", "QuestionID": "QID170"}, {"Type": "Question", "QuestionID": "QID171"}, {"Type": "Question", "QuestionID": "QID172"}, {"Type": "Question", "QuestionID": "QID173"}, {"Type": "Question", "QuestionID": "QID174"}, {"Type": "Question", "QuestionID": "QID175"}, {"Type": "Question", "QuestionID": "QID176"}, {"Type": "Question", "QuestionID": "QID177"}, {"Type": "Question", "QuestionID": "QID178"}, {"Type": "Question", "QuestionID": "QID179"}, {"Type": "Question", "QuestionID": "QID180"}, {"Type": "Question", "QuestionID": "QID181"}, {"Type": "Question", "QuestionID": "QID182"}, {"Type": "Question", "QuestionID": "QID183"}, {"Type": "Question", "QuestionID": "QID184"}, {"Type": "Question", "QuestionID": "QID185"}, {"Type": "Question", "QuestionID": "QID186"}, {"Type": "Question", "QuestionID": "QID187"}, {"Type": "Question", "QuestionID": "QID188"}, {"Type": "Question", "QuestionID": "QID189"}, {"Type": "Question", "QuestionID": "QID190"}, {"Type": "Question", "QuestionID": "QID191"}, {"Type": "Question", "QuestionID": "QID192"}, {"Type": "Question", "QuestionID": "QID193"}]}]}